import json
from pathlib import Path
import pandas as pd

BASE = Path(r"C:\Users\justn\Documents\cs2-demo-analyzer\outputs\awpy\furia-vs-natus-vincere-m2-inferno")

header_path = BASE / "header.json"
kills_path = BASE / "kills.parquet"

# --- Load header (map only) ---
header = {}
if header_path.exists():
    header = json.loads(header_path.read_text(encoding="utf-8"))

map_name = header.get("map_name", "unknown_map")

# --- Load kills ---
kills = pd.read_parquet(kills_path)
cols = list(kills.columns)

def pick(*names):
    for n in names:
        if n in cols:
            return n
    return None

killer_col = pick("attacker_name", "killer_name")
victim_col = pick("victim_name")
assister_col = pick("assister_name")

# --- Sanity check ---
missing = [("killer", killer_col), ("victim", victim_col)]
missing = [k for k, v in missing if v is None]
if missing:
    raise SystemExit(f"Missing columns: {missing}\nAvailable: {cols}")

# --- Compute stats ---
kills_count = kills.groupby(killer_col).size().rename("kills")
deaths_count = kills.groupby(victim_col).size().rename("deaths")

assists_count = None
if assister_col is not None:
    assists_series = kills[assister_col].dropna()
    assists_series = assists_series[assists_series.astype(str).str.len() > 0]
    assists_count = assists_series.value_counts().rename("assists")

df = pd.concat([kills_count, deaths_count, assists_count], axis=1).fillna(0).astype(int)
df.index.name = "player"
df = df.reset_index()

# --- Sort ---
df = df.sort_values(["kills", "assists", "deaths"], ascending=[False, False, True])

print(f"map_name: {map_name}")
print()
print(df.to_string(index=False))
