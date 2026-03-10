import json
import subprocess
import os
import sys
from jinja2 import Environment, FileSystemLoader

# tools/ directory
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

# agent/ directory
AGENT_DIR = os.path.dirname(TOOLS_DIR)

# template location
TEMPLATE_DIR = AGENT_DIR
TEMPLATE_FILE = "IFA_Report_Template.j2"

# output report
OUTPUT_FILE = os.path.join(AGENT_DIR, "traces", "IFA_Report_Filled.txt")

# metrics script
METRICS_SCRIPT = os.path.join(TOOLS_DIR, "get_metrics_summary.py")


def get_metrics():
    """Run metrics script and return JSON"""

    result = subprocess.run(
        [sys.executable, METRICS_SCRIPT],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return json.loads(result.stdout)


def detect_trend(std, avg):
    """Basic trend heuristic"""

    if std > avg * 0.3:
        return "⬈"
    elif std < avg * 0.05:
        return "⬌"
    else:
        return "⬊"


def build_context(metrics):
    """Convert metrics JSON to template variables"""

    m = metrics["metrics"]

    cwnd = m["cwnd"]
    rate = m["rate_mbps"]
    rtt = m["rtt_ms"]

    return {
        "cwnd": {**cwnd, "trend": detect_trend(cwnd["std"], cwnd["avg"])},
        "rate": {**rate, "trend": detect_trend(rate["std"], rate["avg"])},
        "rtt": {**rtt, "trend": detect_trend(rtt["std"], rtt["avg"])}
    }


def render_report(context):

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template(TEMPLATE_FILE)

    return template.render(context)


def main():

    metrics = get_metrics()

    if metrics["status"] != "success":
        print("Metrics not ready yet.")
        return

    context = build_context(metrics)

    report = render_report(context)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        f.write(report)

    print(f"Report generated → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()