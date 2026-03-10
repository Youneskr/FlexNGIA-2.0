import sys
import re

def main():
    # CSV Header: Changed TIMESTAMP to TIME
    print("TIME,SOURCE,DESTINATION,RATE_MBPS,RTT_MS,JITTER_MS,CWND,RTX_OUT,LOST_OUT,RTX_TOT")

    # Regex to find the timestamp and the payload
    # Matches: "   2290.257620: tcp_monitor_log: "
    base_pattern = re.compile(r"\s+(\d+\.\d+): tcp_monitor_log: (.*)")

    # Regex to capture fields (min_rtt is matched but not captured/used)
    payload_pattern = re.compile(
        r"id=(?P<src>[\d\.:]+)->(?P<dst>[\d\.:]+).*?"
        r"srate=(?P<srate>\d+).*?"
        r"rtt=(?P<rtt>\d+).*?"
        r"min_rtt=\d+.*?"             # Match min_rtt to skip it
        r"jitter=(?P<jitter>\d+).*?"
        r"cwnd=(?P<cwnd>\d+).*?"
        r"rtx_out=(?P<rtx_out>\d+).*?"
        r"lost_out=(?P<lost_out>\d+).*?"
        r"total_rtx=(?P<total_rtx>\d+)"
    )

    first_timestamp = None

    try:
        for line in sys.stdin:
            # 1. Extract Timestamp and Payload
            base_match = base_pattern.search(line)
            if not base_match:
                continue
            
            raw_timestamp_str = base_match.group(1)
            payload = base_match.group(2)
            
            try:
                current_timestamp = float(raw_timestamp_str)
            except ValueError:
                continue

            # 2. Logic for Relative Time
            # If this is the first valid line, set it as the baseline (0.0)
            if first_timestamp is None:
                first_timestamp = current_timestamp
            
            # Calculate time difference
            relative_time = current_timestamp - first_timestamp

            # 3. Extract Metrics
            metrics = payload_pattern.search(payload)
            if metrics:
                data = metrics.groupdict()
                
                # Convert Jitter from microseconds to milliseconds
                jitter_us = int(data['jitter'])
                jitter_ms = jitter_us / 1000.0
                
                # 4. Print CSV Row
                # Format relative_time to 6 decimal places
                print(f"{relative_time:.6f},{data['src']},{data['dst']},"
                      f"{data['srate']},{data['rtt']},{jitter_ms:.3f},"
                      f"{data['cwnd']},{data['rtx_out']},"
                      f"{data['lost_out']},{data['total_rtx']}")
                
                # Flush to ensure real-time writing
                sys.stdout.flush()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()