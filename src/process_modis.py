
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. Locate the downloaded NASA CSV
data_folder = Path("data/raw/modis")
files = list(data_folder.rglob("*results.csv"))

if not files:
    raise FileNotFoundError(
        "No MODIS results CSV found in data/raw/modis/"
    )

# 2. Load the original dataset
df = pd.read_csv(files[0])
print("Original records:", len(df))

# 3. Identify the exact NASA columns
ndvi_col = "MOD13Q1_061__250m_16_days_NDVI"
quality_col = "MOD13Q1_061__250m_16_days_pixel_reliability"

# 4. Convert dates and numbers
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df[ndvi_col] = pd.to_numeric(df[ndvi_col], errors="coerce")
df[quality_col] = pd.to_numeric(df[quality_col], errors="coerce")

# 5. Keep only our project period
df = df[
    (df["Date"] >= "2010-01-01") &
    (df["Date"] <= "2025-12-31")
].copy()

# 6. Accept only good-quality pixels
# 0 = good, 1 = marginal, 2 = snow/ice, 3 = cloudy
df = df[df[quality_col] == 0].copy()

# AppEEARS has already scaled the NDVI values
df = df[
    df[ndvi_col].between(-1, 1)
].copy()

# 7. Keep only the columns needed
clean = df[[
    "Date",
    "ID",
    "Latitude",
    "Longitude",
    ndvi_col
]].copy()

clean.columns = [
    "date", "district", "latitude", "longitude", "ndvi"
]

clean = clean.dropna()
clean = clean.sort_values(["district", "date"])

# 8. Save clean dataset
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "clean_modis.csv"
clean.to_csv(output_file, index=False)

print("Clean records:", len(clean))
print("Districts:", clean["district"].unique())
print("Saved:", output_file)

# 9. Generate the first real NASA graph
plt.figure(figsize=(12, 6))

for district, group in clean.groupby("district"):
    plt.plot(
        group["date"],
        group["ndvi"],
        label=district,
        linewidth=1,
        alpha=0.8
    )

plt.title("Punjab Vegetation Health — NASA MODIS NDVI")
plt.xlabel("Year")
plt.ylabel("NDVI")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

chart_file = output_folder / "punjab_ndvi_graph.png"
plt.savefig(chart_file, dpi=200)
plt.show()

print("Graph saved:", chart_file)
