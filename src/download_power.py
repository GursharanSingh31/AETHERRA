from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

districts = {
    "amritsar": (31.6340, 74.8723),
    "jalandhar": (31.3260, 75.5762),
    "ludhiana": (30.9010, 75.8573),
    "patiala": (30.3398, 76.3869),
}

folder = Path("data/raw/power")
folder.mkdir(parents=True, exist_ok=True)

base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"

for name, (lat, lon) in districts.items():
    params = {
        "parameters": (
            "T2M,T2M_MAX,T2M_MIN,"
            "PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN"
        ),
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": "20100101",
        "end": "20251231",
        "format": "CSV",
    }

    url = base_url + "?" + urlencode(params)
    print(f"Downloading {name}...")

    try:
        with urlopen(url, timeout=120) as response:
            content = response.read()

        # Check the response looks like NASA POWER CSV
        if b"YEAR,MO,DY" not in content:
            raise ValueError("Unexpected response from NASA POWER")

        (folder / f"{name}_power.csv").write_bytes(content)
        print(f"Saved {name}_power.csv")

    except Exception as error:
        print(f"Failed to download {name}: {error}")

print("Download process finished.")