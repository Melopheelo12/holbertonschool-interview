#!/usr/bin/python3
"""
Log Parser - Reads and processes HTTP request log data from stdin.
Accumulates file sizes and HTTP status code counts.
Prints statistics every 10 lines and on keyboard interrupt.
"""
import sys


def print_stats(total_size, status_codes):
    """
    Print accumulated metrics.

    Args:
        total_size (int): Total accumulated file size
        status_codes (dict): Dictionary with status codes
        as keys and counts as values
    """
    print("File size: {}".format(total_size))

    # Print status codes in sorted order
    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print("{}: {}".format(code, status_codes[code]))


def main():
    """
    Main function that processes HTTP log lines from stdin.
    Accumulates total file size and counts HTTP status codes.
    Outputs statistics every 10 lines and on keyboard interrupt.
    """
    total_size = 0
    line_count = 0

    # Initialize dictionary with all expected HTTP status codes
    status_codes = {
        200: 0,
        301: 0,
        400: 0,
        401: 0,
        403: 0,
        404: 0,
        405: 0,
        500: 0
    }

    try:
        # Process each line from stdin
        for line in sys.stdin:
            line_count += 1

            try:
                # Split the line and extract status code and file size
                # Status code is second-to-last element
                parts = line.split()
                status = int(parts[-2])
                file_size = int(parts[-1])

                # Accumulate the file size
                total_size += file_size

                # Count the status code if it's in our tracked codes
                if status in status_codes:
                    status_codes[status] += 1

            except (ValueError, IndexError):
                # Skip lines that can't be parsed
                continue

            # Print statistics every 10 lines
            if line_count % 10 == 0:
                print_stats(total_size, status_codes)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully by printing final stats
        print_stats(total_size, status_codes)


# Entry point of the script
if __name__ == "__main__":
    main()
