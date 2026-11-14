from pathlib import Path
import pandas as pd

# -----------------------------------
# 1. LOAD MODIS DATA
# -----------------------------------

modis_path = Path("data/processed/clean_modis.csv")

modis = pd.read_csv(modis_path)

modis["date"] = pd.to_datetime(modis["date"])
modis["district"] = (
    modis["district"].astype(str).str.strip().str.lower()
)

print("MODIS records loaded:", len(modis))

# -----------------------------------
# 2. LOAD NASA POWER DATA
# -----------------------------------

power_folder = Path("data/raw/power")
power_files = sorted(power_folder.glob("*.csv"))

all_power = []

for file in power_files:

    print("Reading:", file.name)

    with open(file, encoding="utf-8-sig") as f:
        lines = f.readlines()

    # Locate the actual weather data header
    header_index = next(
        (
            i for i, line in enumerate(lines)
            if line.strip().startswith("YEAR,DOY")
        ),
        None
    )

    if header_index is None:
        print("Skipping invalid file:", file.name)
        continue

    df = pd.read_csv(file, skiprows=header_index)
    df.columns = df.columns.str.strip()

    # Convert day of year into calendar date
    df["date"] = pd.to_datetime(
        df["YEAR"].astype(str) + df["DOY"].astype(str).str.zfill(3),
        format="%Y%j",
        errors="coerce"
    )

    # Clean missing values
    weather_cols = [
        "T2M",
        "T2M_MAX",
        "PRECTOTCORR",
        "RH2M",
        "ALLSKY_SFC_SW_DWN"
    ]

    for col in weather_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].replace(-999, float("nan"))

    df["district"] = file.stem.strip().lower().replace("_power", "")

    all_power.append(df)

if not all_power:
    raise ValueError("No valid NASA POWER datasets found.")

power = pd.concat(all_power, ignore_index=True)

power = power.dropna(subset=["date"])
power = power.sort_values(["district", "date"])

print("POWER records loaded:", len(power))

# -----------------------------------
# 3. MERGE MODIS + POWER
# -----------------------------------

records = []

for row in modis.itertuples(index=False):

    start_date = row.date
    end_date = start_date + pd.Timedelta(days=15)

    weather = power[
        (power["district"] == row.district) &
        (power["date"] >= start_date) &
        (power["date"] <= end_date)
    ]

    # Require 16 daily weather records
    if weather["date"].nunique() != 16:
        continue

    weather_cols = [
        "T2M", "T2M_MAX", "PRECTOTCORR",
        "RH2M", "ALLSKY_SFC_SW_DWN"
    ]

    if weather[weather_cols].isna().any().any():
        continue

    records.append({
        "date": start_date,
        "district": row.district,
        "ndvi": row.ndvi,
        "temperature": weather["T2M"].mean(),
        "max_temperature": weather["T2M_MAX"].max(),
        "rainfall": weather["PRECTOTCORR"].sum(),
        "humidity": weather["RH2M"].mean(),
        "solar_radiation": weather["ALLSKY_SFC_SW_DWN"].mean()
    })

# -----------------------------------
# 4. SAVE RESULTS
# -----------------------------------

merged = pd.DataFrame(records)

if merged.empty:
    print("No matching records found.")
    print("MODIS districts:", modis["district"].unique())
    print("POWER districts:", power["district"].unique())
    raise SystemExit(1)

merged = merged.sort_values(["district", "date"])

output_path = Path("data/processed/merged_dataset.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

merged.to_csv(output_path, index=False)

print("\nMERGING SUCCESSFUL!")
print("Total records:", len(merged))
print("Districts:", merged["district"].unique())
print(merged.head())
print("Saved to:", output_path)