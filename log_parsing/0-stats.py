#!/usr/bin/python3
import sys


def print_stats(total_size, status_codes):
    """Print accumulated metrics."""
    print("File size: {}".format(total_size))

    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print("{}: {}".format(code, status_codes[code]))


def main():
    total_size = 0
    line_count = 0

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
        for line in sys.stdin:
            line_count += 1

            try:
                parts = line.split()
                status = int(parts[-2])
                file_size = int(parts[-1])

                total_size += file_size

                if status in status_codes:
                    status_codes[status] += 1

            except (ValueError, IndexError):
                continue

            if line_count % 10 == 0:
                print_stats(total_size, status_codes)

    except KeyboardInterrupt:
        print_stats(total_size, status_codes)


if __name__ == "__main__":
    main()
