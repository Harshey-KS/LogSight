import argparse
import re
import pandas as pd

def parse_log_line(line):
    # Example Apache log format regex
    pattern = r'(\d{1,3}(?:\.\d{1,3}){3}) - - \[(.*?)\] "(GET|POST) (.*?) HTTP/[\d.]+" (\d{3})'
    match = re.search(pattern, line)
    if match:
        return {
            'IP': match.group(1),
            'Timestamp': match.group(2),
            'Method': match.group(3),
            'URL': match.group(4),
            'Status': match.group(5)
        }
    return None

def main():
    parser = argparse.ArgumentParser(description='Parse log file and export to CSV')
    parser.add_argument('input_file', help='Path to the log file')
    parser.add_argument('output_file', help='Output CSV path')
    args = parser.parse_args()

    parsed_logs = []
    with open(args.input_file, 'r') as file:
        for line in file:
            parsed = parse_log_line(line)
            if parsed:
                parsed_logs.append(parsed)

    if parsed_logs:
        df = pd.DataFrame(parsed_logs)
        df.to_csv(args.output_file, index=False)
        print(f"✅ Parsed {len(parsed_logs)} entries. Saved to {args.output_file}")
    else:
        print("⚠️ No valid log entries found.")

if __name__ == "__main__":
    main()
