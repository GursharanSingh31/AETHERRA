from pathlib import Path
import pandas as pd

folder = Path("data/raw/power")

print("Checking NASA POWER files...")
print("Current folder:", Path.cwd())

if not folder.exists():
    print("ERROR: data/raw/power folder does not exist.")
    raise SystemExit

files = list(folder.glob("*.csv"))

print("CSV files found:", len(files))

if not files:
    print("ERROR: No CSV files found!")
    print("Run: python src/download_power.py")
    raise SystemExit

for file in files:
    print("\nReading:", file.name)

    with open(file, encoding="utf-8-sig") as f:
        lines = f.readlines()

    header = next(
        (i for i, line in enumerate(lines)
         if line.startswith("YEAR,MO,DY")),
        None
    )

    if header is None:
        print("ERROR: NASA POWER header not found.")
        continue

    df = pd.read_csv(file, skiprows=header)

    print("Total rows:", len(df))
    print("Columns:", df.columns.tolist())
    print(df.head(3).to_string(index=False))

print("\nVerification completed!")