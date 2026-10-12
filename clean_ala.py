import csv

path = "raw/ALA_dataset1/ALA_dataset1.csv"

with open(path, "r", encoding="utf-8-sig", errors="replace", newline="") as f:

    reader = csv.reader(f)

    headers = next(reader)

    print("\nTOTAL COLUMNS:", len(headers))
    print("\nALL COLUMN NAMES:\n")

    for i, column in enumerate(headers):
        print(i, ":", column)

    row = next(reader)

    print("\n\nFIRST ROW VALUES:\n")

    for i, value in enumerate(row):
        print(i, ":", value[:100])