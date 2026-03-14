import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np
import sys
import os
import glob

# =============================================================================
#  USER-TUNABLE SETTINGS
#  All visual parameters are defined here.  No need to touch the code below.
# =============================================================================

# -----------------------------------------------------------------------------
#  Output resolution
# -----------------------------------------------------------------------------
INDIVIDUAL_FIGURE_WIDTH_PIXELS  = 1280
INDIVIDUAL_FIGURE_HEIGHT_PIXELS = 720
FIGURE_DPI                      = 100   # pixels-per-inch used when saving

# Dashboard is scaled relative to individual figures
DASHBOARD_WIDTH_SCALE  = 1.6   # e.g. 1.6 × individual width
DASHBOARD_HEIGHT_SCALE = 2.1   # e.g. 2.1 × individual height

# -----------------------------------------------------------------------------
#  X-axis padding
#  A small coloured zone is added to the right of the last data point so the
#  line end is visible.  Expressed as a fraction of the total x range.
# -----------------------------------------------------------------------------
X_AXIS_RIGHT_PADDING_FRACTION = 0.04   # 0.04 = 4 % of total duration

# -----------------------------------------------------------------------------
#  Individual figure – text sizes (points)
# -----------------------------------------------------------------------------
INDIVIDUAL_AXIS_LABEL_FONT_SIZE   = 15   # "Time (seconds)", "CWND (Packets)", …
INDIVIDUAL_TICK_LABEL_FONT_SIZE   = 13   # numbers on x and y axes
INDIVIDUAL_CC_LABEL_FONT_SIZE     = 13   # scheme names above the plot area

# -----------------------------------------------------------------------------
#  Individual figure – line style
# -----------------------------------------------------------------------------
INDIVIDUAL_LINE_COLOR     = '#0d3b6e'   # dark navy blue for all metric lines
INDIVIDUAL_LINE_WIDTH     = 1.3         # thickness in points
INDIVIDUAL_LINE_ALPHA     = 0.95        # opacity  (0 = invisible, 1 = solid)

# -----------------------------------------------------------------------------
#  Individual figure – loss scatter markers
# -----------------------------------------------------------------------------
LOSS_MARKER_STYLE  = 'o'   # matplotlib marker code: 'o', 's', '^', 'D', …
LOSS_MARKER_SIZE   = 5     # diameter in points

# -----------------------------------------------------------------------------
#  Individual figure – grid
# -----------------------------------------------------------------------------
INDIVIDUAL_GRID_LINE_STYLE = '--'   # '-', '--', ':', '-.'
INDIVIDUAL_GRID_ALPHA      = 0.45   # opacity of grid lines

# -----------------------------------------------------------------------------
#  Individual figure – CC interval background shading
# -----------------------------------------------------------------------------
INDIVIDUAL_CC_BAND_ALPHA = 0.32   # opacity of the coloured background bands

# -----------------------------------------------------------------------------
#  60-second milestone markers on the x-axis spine
# -----------------------------------------------------------------------------
MILESTONE_INTERVAL_SECONDS  = 60       # draw a marker every N seconds
MILESTONE_MARKER_COLOR      = 'red'    # fill colour of the bullet
MILESTONE_MARKER_EDGE_COLOR = 'darkred'
MILESTONE_MARKER_SIZE       = 7        # diameter in points
MILESTONE_MARKER_EDGE_WIDTH = 0.8

# -----------------------------------------------------------------------------
#  CC interval background colours (cycled when there are more schemes)
#  Add or replace hex values to suit your palette.
# -----------------------------------------------------------------------------
CC_INTERVAL_COLORS = [
    '#93B8E0',   # soft blue
    '#95CB95',   # soft green
    '#F0A878',   # soft orange
    '#C4A0D8',   # soft purple
    '#F0D870',   # soft yellow
    '#EE9090',   # soft red
]

# -----------------------------------------------------------------------------
#  Dashboard – text sizes (points)
# -----------------------------------------------------------------------------
DASHBOARD_AXIS_LABEL_FONT_SIZE  = 12
DASHBOARD_TICK_LABEL_FONT_SIZE  = 10
DASHBOARD_CC_LABEL_FONT_SIZE    = 9
DASHBOARD_TITLE_FONT_SIZE       = 17
DASHBOARD_SUBTITLE_FONT_SIZE    = 11
DASHBOARD_TABLE_FONT_SIZE       = 11
DASHBOARD_TABLE_TITLE_FONT_SIZE = 13   # "CC Scheme Transitions" heading

# -----------------------------------------------------------------------------
#  Dashboard – CC interval background shading
# -----------------------------------------------------------------------------
DASHBOARD_CC_BAND_ALPHA = 0.30

# -----------------------------------------------------------------------------
#  Dashboard – line style (panels inside dashboard)
# -----------------------------------------------------------------------------
DASHBOARD_LINE_COLOR  = '#0d3b6e'
DASHBOARD_LINE_WIDTH  = 1.3
DASHBOARD_LINE_ALPHA  = 0.95
DASHBOARD_LOSS_MARKER_SIZE = 4   # markers in the loss panel inside dashboard

# -----------------------------------------------------------------------------
#  Dashboard – colours (light theme)
# -----------------------------------------------------------------------------
DASHBOARD_BACKGROUND_COLOR       = '#f4f6fb'   # outer figure background
DASHBOARD_PANEL_COLOR            = '#ffffff'   # individual plot card background
DASHBOARD_GRID_COLOR             = '#e0e4ee'   # grid line colour inside panels
DASHBOARD_PANEL_BORDER_COLOR     = '#c8cedf'   # border around each panel card
DASHBOARD_FOREGROUND_COLOR       = '#1a2035'   # primary text (labels, ticks)
DASHBOARD_SUBTITLE_COLOR         = '#5a6480'   # secondary text (subtitle)
DASHBOARD_ACCENT_COLOR           = '#2a5fbd'   # divider line under header
DASHBOARD_TABLE_HEADER_BG_COLOR  = '#dce6f7'   # background of table header row
DASHBOARD_TABLE_HEADER_TEXT_COLOR= '#1a2035'
DASHBOARD_TABLE_ROW_TEXT_COLOR   = '#111133'
DASHBOARD_TABLE_BORDER_COLOR     = '#b0bcd8'
DASHBOARD_TABLE_ROW_BORDER_COLOR = '#c8cedf'
DASHBOARD_TABLE_ROW_TINT_OPACITY = '66'        # 2-char hex suffix for row tint (~40%)
DASHBOARD_CC_LABEL_COLOR         = '#333355'   # CC scheme labels above panels
DASHBOARD_LEGEND_FONT_SIZE       = 10

# -----------------------------------------------------------------------------
#  Dashboard – layout proportions  (fractions of figure, 0–1)
# -----------------------------------------------------------------------------
DASHBOARD_MARGIN_LEFT   = 0.07
DASHBOARD_MARGIN_RIGHT  = 0.97
DASHBOARD_MARGIN_TOP    = 0.915
DASHBOARD_MARGIN_BOTTOM = 0.06
DASHBOARD_HSPACE        = 0.62   # vertical gap between rows
DASHBOARD_WSPACE        = 0.30   # horizontal gap between columns
DASHBOARD_TABLE_HEIGHT_RATIO = 0.60   # height of table row relative to plot rows

# =============================================================================
#  END OF USER-TUNABLE SETTINGS
# =============================================================================


# ── Derived geometry (computed from pixel settings above) ────────────────────
_FIGURE_WIDTH_INCHES  = INDIVIDUAL_FIGURE_WIDTH_PIXELS  / FIGURE_DPI
_FIGURE_HEIGHT_INCHES = INDIVIDUAL_FIGURE_HEIGHT_PIXELS / FIGURE_DPI


# ── Parsers ───────────────────────────────────────────────────────────────────

def parse_cc_periods(path):
    """Read cc_periods file → list of (start, end, label), raw x_min, raw x_max."""
    periods = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t') if '\t' in line else line.split()
            periods.append((float(parts[0]), float(parts[1]), parts[2].strip()))
    if not periods:
        raise ValueError("cc_periods is empty or malformed.")
    return periods, periods[0][0], periods[-1][1]


def parse_loss_stats(path):
    """Read loss_stats file → (time_array, loss_ratio_array).
    Time = slot_number × 10 seconds."""
    slots, ratios = [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t') if '\t' in line else line.split()
            slots.append(int(parts[0]))
            ratios.append(float(parts[-1]))
    return np.array(slots, dtype=float) * 10, np.array(ratios, dtype=float)


def assign_cc_colors(periods):
    """Map each unique CC scheme label to a colour from CC_INTERVAL_COLORS."""
    seen, color_map = [], {}
    for _, _, label in periods:
        if label not in seen:
            color_map[label] = CC_INTERVAL_COLORS[len(seen) % len(CC_INTERVAL_COLORS)]
            seen.append(label)
    return color_map


# ── Low-level drawing helpers ─────────────────────────────────────────────────

def _apply_axis_style(ax, tick_font_size, tick_color='#222222'):
    """Apply consistent tick and spine styling to an axes object."""
    ax.tick_params(axis='both', labelsize=tick_font_size, colors=tick_color)
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color('#aaaaaa')


def _get_last_cc_color(periods, color_map, x_max_raw):
    """Return the background colour of the last active CC interval."""
    for start, end, label in reversed(periods):
        if start <= x_max_raw:
            return color_map[label]
    return color_map[periods[-1][2]]


def _draw_cc_bands_and_labels(ax, periods, color_map,
                               x_min, x_max, x_max_raw,
                               cc_font_size, label_color, band_alpha):
    """Shade each CC interval and write its name above the plot area.
    The right-side padding zone [x_max_raw, x_max] is filled with the
    colour of the last active interval."""
    x_range = x_max - x_min

    for start, end, label in periods:
        ax.axvspan(start, end, alpha=band_alpha, color=color_map[label], zorder=0)
        label_x_fraction = ((start + end) / 2 - x_min) / x_range
        ax.text(label_x_fraction, 1.015, label,
                transform=ax.transAxes,
                ha='center', va='bottom',
                fontsize=cc_font_size, color=label_color, clip_on=False)

    if x_max > x_max_raw:
        last_color = _get_last_cc_color(periods, color_map, x_max_raw)
        ax.axvspan(x_max_raw, x_max, alpha=band_alpha, color=last_color, zorder=0)


def _draw_milestone_markers(ax, x_min, x_max):
    """Draw a coloured bullet on the x-axis spine at every milestone interval."""
    marks = np.arange(MILESTONE_INTERVAL_SECONDS, x_max + 1e-9, MILESTONE_INTERVAL_SECONDS)
    marks = marks[marks <= x_max]
    y_bottom, _ = ax.get_ylim()
    for x_mark in marks:
        ax.plot(x_mark, y_bottom,
                marker='o',
                color=MILESTONE_MARKER_COLOR,
                markersize=MILESTONE_MARKER_SIZE,
                markeredgecolor=MILESTONE_MARKER_EDGE_COLOR,
                markeredgewidth=MILESTONE_MARKER_EDGE_WIDTH,
                zorder=5, clip_on=False)


def _finalize_axes(ax, x_label_text, y_label_text,
                   x_min, x_max, x_max_raw, periods, color_map,
                   axis_label_font_size,
                   tick_font_size,
                   cc_label_font_size,
                   axis_label_color,
                   cc_label_color,
                   grid_line_color,
                   grid_alpha,
                   cc_band_alpha):
    """Set limits, labels, grid, CC bands, and milestone markers on an axes."""
    ax.set_xlim(x_min, x_max)
    ax.set_xlabel(x_label_text, fontsize=axis_label_font_size, color=axis_label_color)
    ax.set_ylabel(y_label_text, fontsize=axis_label_font_size, color=axis_label_color)

    grid_kwargs = dict(linestyle=INDIVIDUAL_GRID_LINE_STYLE, alpha=grid_alpha, zorder=1)
    if grid_line_color:
        grid_kwargs['color'] = grid_line_color
    ax.grid(True, **grid_kwargs)

    ax.autoscale(enable=False)
    _apply_axis_style(ax, tick_font_size=tick_font_size)
    _draw_cc_bands_and_labels(ax, periods, color_map,
                               x_min, x_max, x_max_raw,
                               cc_font_size=cc_label_font_size,
                               label_color=cc_label_color,
                               band_alpha=cc_band_alpha)
    _draw_milestone_markers(ax, x_min, x_max)


# ── Individual plot ───────────────────────────────────────────────────────────

def plot_metric(x_data, y_data, y_axis_label,
                output_dir, output_filename,
                x_min, x_max, x_max_raw, periods, color_map,
                point_marker=None, point_marker_size=LOSS_MARKER_SIZE,
                line_style='-'):
    """Render and save a single metric figure."""
    fig, ax = plt.subplots(figsize=(_FIGURE_WIDTH_INCHES, _FIGURE_HEIGHT_INCHES))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    ax.plot(x_data, y_data,
            color=INDIVIDUAL_LINE_COLOR,
            linewidth=INDIVIDUAL_LINE_WIDTH,
            linestyle=line_style,
            marker=point_marker,
            markersize=point_marker_size,
            alpha=INDIVIDUAL_LINE_ALPHA,
            zorder=2)

    _finalize_axes(
        ax,
        x_label_text='Time (seconds)',
        y_label_text=y_axis_label,
        x_min=x_min, x_max=x_max, x_max_raw=x_max_raw,
        periods=periods, color_map=color_map,
        axis_label_font_size=INDIVIDUAL_AXIS_LABEL_FONT_SIZE,
        tick_font_size=INDIVIDUAL_TICK_LABEL_FONT_SIZE,
        cc_label_font_size=INDIVIDUAL_CC_LABEL_FONT_SIZE,
        axis_label_color='#222222',
        cc_label_color='#222222',
        grid_line_color=None,
        grid_alpha=INDIVIDUAL_GRID_ALPHA,
        cc_band_alpha=INDIVIDUAL_CC_BAND_ALPHA,
    )

    fig.tight_layout(pad=0.4)
    plt.subplots_adjust(top=0.88)   # headroom for CC labels above the plot area

    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print(f"    -> Saved: {output_path}")


# ── Dashboard ─────────────────────────────────────────────────────────────────

def build_dashboard(df, loss_x, loss_y, periods, color_map,
                    x_min, x_max, x_max_raw, output_dir, run_id):
    """Build and save the multi-panel professional dashboard."""

    dashboard_width  = _FIGURE_WIDTH_INCHES  * DASHBOARD_WIDTH_SCALE
    dashboard_height = _FIGURE_HEIGHT_INCHES * DASHBOARD_HEIGHT_SCALE
    fig = plt.figure(figsize=(dashboard_width, dashboard_height),
                     facecolor=DASHBOARD_BACKGROUND_COLOR)

    gs = gridspec.GridSpec(
        3, 2,
        figure=fig,
        left=DASHBOARD_MARGIN_LEFT,
        right=DASHBOARD_MARGIN_RIGHT,
        top=DASHBOARD_MARGIN_TOP,
        bottom=DASHBOARD_MARGIN_BOTTOM,
        hspace=DASHBOARD_HSPACE,
        wspace=DASHBOARD_WSPACE,
        height_ratios=[1, 1, DASHBOARD_TABLE_HEIGHT_RATIO],
    )

    # ── Header ────────────────────────────────────────────────────────────────
    fig.text(0.5, 0.965,
             f'Network Performance Dashboard  ·  {run_id}',
             ha='center', va='top',
             fontsize=DASHBOARD_TITLE_FONT_SIZE,
             fontweight='bold',
             color=DASHBOARD_FOREGROUND_COLOR,
             family='monospace')
    fig.text(0.5, 0.942,
             f'{len(periods)} CC transitions  ·  '
             f'duration {x_max - x_min:.1f} s  ·  '
             f'{len(df)} samples',
             ha='center', va='top',
             fontsize=DASHBOARD_SUBTITLE_FONT_SIZE,
             color=DASHBOARD_SUBTITLE_COLOR)
    fig.add_artist(plt.Line2D(
        [0.06, 0.94], [0.928, 0.928],
        transform=fig.transFigure,
        color=DASHBOARD_ACCENT_COLOR, linewidth=1.2, alpha=0.7))

    # ── Four metric panels ────────────────────────────────────────────────────
    panel_definitions = [
        (gs[0, 0], df['TIME'],  df['CWND'],      'CWND (Packets)', None),
        (gs[0, 1], df['TIME'],  df['RATE_MBPS'], 'Rate (Mbps)',    None),
        (gs[1, 0], df['TIME'],  df['RTT_MS'],    'RTT (ms)',       None),
        (gs[1, 1], loss_x,      loss_y,          'Loss Ratio (%)', LOSS_MARKER_STYLE),
    ]

    for panel_index, (grid_spec, x_data, y_data, y_label, marker) in enumerate(panel_definitions):
        ax = fig.add_subplot(grid_spec, facecolor=DASHBOARD_PANEL_COLOR)
        ax.patch.set_linewidth(0.6)
        ax.patch.set_edgecolor(DASHBOARD_PANEL_BORDER_COLOR)

        marker_size = DASHBOARD_LOSS_MARKER_SIZE if marker else 4
        ax.plot(x_data, y_data,
                color=DASHBOARD_LINE_COLOR,
                linewidth=DASHBOARD_LINE_WIDTH,
                linestyle='-',
                marker=marker,
                markersize=marker_size,
                alpha=DASHBOARD_LINE_ALPHA,
                zorder=2)

        x_label_text = 'Time (seconds)' if panel_index >= 2 else ''
        _finalize_axes(
            ax,
            x_label_text=x_label_text,
            y_label_text=y_label,
            x_min=x_min, x_max=x_max, x_max_raw=x_max_raw,
            periods=periods, color_map=color_map,
            axis_label_font_size=DASHBOARD_AXIS_LABEL_FONT_SIZE,
            tick_font_size=DASHBOARD_TICK_LABEL_FONT_SIZE,
            cc_label_font_size=DASHBOARD_CC_LABEL_FONT_SIZE,
            axis_label_color=DASHBOARD_FOREGROUND_COLOR,
            cc_label_color=DASHBOARD_CC_LABEL_COLOR,
            grid_line_color=DASHBOARD_GRID_COLOR,
            grid_alpha=0.5,
            cc_band_alpha=DASHBOARD_CC_BAND_ALPHA,
        )

        for spine in ax.spines.values():
            spine.set_color(DASHBOARD_PANEL_BORDER_COLOR)
            spine.set_linewidth(0.7)
        ax.tick_params(colors=DASHBOARD_FOREGROUND_COLOR,
                       labelsize=DASHBOARD_TICK_LABEL_FONT_SIZE)

    # ── CC transition table ───────────────────────────────────────────────────
    ax_table = fig.add_subplot(gs[2, :], facecolor=DASHBOARD_BACKGROUND_COLOR)
    ax_table.axis('off')
    ax_table.set_title('CC Scheme Transitions',
                       fontsize=DASHBOARD_TABLE_TITLE_FONT_SIZE,
                       color=DASHBOARD_FOREGROUND_COLOR,
                       pad=8, loc='left', fontweight='bold')

    column_headers = ['#', 'CC Scheme', 'Start (s)', 'End (s)', 'Duration (s)']
    table_rows = [
        [str(index), label, f'{start:.2f}', f'{end:.2f}', f'{end - start:.2f}']
        for index, (start, end, label) in enumerate(periods, 1)
    ]

    table = ax_table.table(
        cellText=table_rows,
        colLabels=column_headers,
        loc='center',
        cellLoc='center',
    )
    table.auto_set_font_size(False)
    table.set_fontsize(DASHBOARD_TABLE_FONT_SIZE)
    table.scale(1, 1.7)

    for col_index in range(len(column_headers)):
        header_cell = table[0, col_index]
        header_cell.set_facecolor(DASHBOARD_TABLE_HEADER_BG_COLOR)
        header_cell.set_text_props(color=DASHBOARD_TABLE_HEADER_TEXT_COLOR,
                                   fontweight='bold')
        header_cell.set_edgecolor(DASHBOARD_TABLE_BORDER_COLOR)

    for row_index, (start, end, label) in enumerate(periods, 1):
        tint_color = color_map[label] + DASHBOARD_TABLE_ROW_TINT_OPACITY
        for col_index in range(len(column_headers)):
            data_cell = table[row_index, col_index]
            data_cell.set_facecolor(tint_color)
            data_cell.set_text_props(color=DASHBOARD_TABLE_ROW_TEXT_COLOR)
            data_cell.set_edgecolor(DASHBOARD_TABLE_ROW_BORDER_COLOR)

    # ── Bottom legend ─────────────────────────────────────────────────────────
    legend_patches = [
        mpatches.Patch(facecolor=color_map[label], alpha=0.80,
                       label=label, edgecolor='#888')
        for label in dict.fromkeys(lbl for _, _, lbl in periods)
    ]
    fig.legend(handles=legend_patches,
               loc='lower center',
               ncol=len(legend_patches),
               fontsize=DASHBOARD_LEGEND_FONT_SIZE,
               labelcolor=DASHBOARD_FOREGROUND_COLOR,
               facecolor=DASHBOARD_PANEL_COLOR,
               edgecolor=DASHBOARD_PANEL_BORDER_COLOR,
               framealpha=0.9,
               bbox_to_anchor=(0.5, 0.002))

    output_path = os.path.join(output_dir, 'dashboard.png')
    plt.savefig(output_path, dpi=FIGURE_DPI,
                facecolor=DASHBOARD_BACKGROUND_COLOR,
                bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"    -> Saved: {output_path}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analysis/plot_results.py <run_directory>")
        sys.exit(1)

    run_dir = sys.argv[1]
    if not os.path.isdir(run_dir):
        print(f"[!] Error: '{run_dir}' is not a valid directory.")
        sys.exit(1)

    # Locate required files inside the run directory
    csv_files = glob.glob(os.path.join(run_dir, "*.csv"))
    if not csv_files:
        print(f"[!] Error: No CSV file found in '{run_dir}'."); sys.exit(1)
    if len(csv_files) > 1:
        print(f"[!] Warning: multiple CSV files found, using '{csv_files[0]}'.")
    csv_file = csv_files[0]

    cc_periods_file = os.path.join(run_dir, "cc_periods")
    loss_stats_file = os.path.join(run_dir, "loss_stats")
    for required_file in (cc_periods_file, loss_stats_file):
        if not os.path.exists(required_file):
            print(f"[!] Error: required file '{required_file}' not found."); sys.exit(1)

    # Create output directory
    run_id     = os.path.basename(os.path.normpath(run_dir))
    output_dir = os.path.join("analysis", "images", run_id)
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Output directory: {output_dir}")

    # Parse cc_periods and compute x-axis limits
    periods, x_min_raw, x_max_raw = parse_cc_periods(cc_periods_file)
    color_map = assign_cc_colors(periods)
    x_min = x_min_raw
    x_max = x_max_raw + (x_max_raw - x_min_raw) * X_AXIS_RIGHT_PADDING_FRACTION
    print(f"[*] X range: [{x_min:.2f}, {x_max:.2f}]  "
          f"(data ends at {x_max_raw:.2f}, +{X_AXIS_RIGHT_PADDING_FRACTION*100:.0f}% padding)")
    for start, end, label in periods:
        print(f"    [{start:.3f} – {end:.3f}]  {label}")

    # Parse and filter loss stats
    loss_x_all, loss_y_all = parse_loss_stats(loss_stats_file)
    within_range = loss_x_all <= x_max_raw
    loss_x  = loss_x_all[within_range]
    loss_y  = loss_y_all[within_range]
    dropped = (~within_range).sum()
    if dropped:
        print(f"[*] Dropped {dropped} loss point(s) beyond data end ({x_max_raw:.2f} s).")

    # Read main metrics CSV
    try:
        df = pd.read_csv(csv_file)
    except Exception as error:
        print(f"[!] CSV read error: {error}"); sys.exit(1)

    shared_kwargs = dict(
        x_min=x_min, x_max=x_max, x_max_raw=x_max_raw,
        periods=periods, color_map=color_map,
    )

    # Individual figures
    print("[*] Generating individual figures ...")
    plot_metric(df['TIME'], df['CWND'],
                y_axis_label='CWND (Packets)',
                output_dir=output_dir, output_filename='cwnd.png',
                **shared_kwargs)

    plot_metric(df['TIME'], df['RATE_MBPS'],
                y_axis_label='Rate (Mbps)',
                output_dir=output_dir, output_filename='rate.png',
                **shared_kwargs)

    plot_metric(df['TIME'], df['RTT_MS'],
                y_axis_label='RTT (ms)',
                output_dir=output_dir, output_filename='rtt.png',
                **shared_kwargs)

    plot_metric(loss_x, loss_y,
                y_axis_label='Loss Ratio (%)',
                output_dir=output_dir, output_filename='loss.png',
                point_marker=LOSS_MARKER_STYLE,
                point_marker_size=LOSS_MARKER_SIZE,
                **shared_kwargs)

    # Dashboard
    print("[*] Generating dashboard ...")
    build_dashboard(df, loss_x, loss_y, periods, color_map,
                    x_min, x_max, x_max_raw, output_dir, run_id)

    print("[*] Done.")


if __name__ == "__main__":
    main()