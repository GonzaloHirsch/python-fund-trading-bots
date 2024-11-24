import os
from logger.setup import logging

DATA_PATH = "data/pricing"


def main():
    # Get all the files we have.
    files = [
        os.path.join(DATA_PATH, f)
        for f in os.listdir(DATA_PATH)
        if os.path.isfile(os.path.join(DATA_PATH, f)) and ".csv" in f
    ]

    # Count the number of records.
    records, max_records, max_file = 0, 0, None
    for file in files:
        with open(file, "rb") as f:
            tmp = sum(1 for _ in f) - 1
            records += tmp
            if tmp > max_records:
                max_records = tmp
                max_file = file

    # Logging all the output.
    logging.info(f"Number of Records: {records}")
    logging.info(f"Maximum File: {max_file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main()
