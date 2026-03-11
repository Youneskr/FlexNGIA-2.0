import sys

def generate_cc_periods(input_file, output_file):
    # Read timestamps
    with open(input_file, "r") as f:
        times = [float(line.strip()) for line in f if line.strip()]

    if len(times) < 2:
        print("Error: need at least two timestamps.")
        return

    with open(output_file, "w") as out:
        for i in range(len(times) - 1):
            start = times[i]
            end = times[i + 1]

            if i == 0:
                cc = "Reno"
            else:
                cc = f"LLM_CC_V{i}"

            out.write(f"{start}\t{end}\t{cc}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_cc_periods.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    generate_cc_periods(input_file, output_file)