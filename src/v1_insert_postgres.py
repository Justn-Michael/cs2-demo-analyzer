import json
from pathlib import Path

import pandas as pd
import psycopg2

# ---- Paths (this demo's extracted awpy folder) ----
BASE = Path(r"C:\Users\justn\Documents\cs2-demo-analyzer\outputs\awpy\furia-vs-natus-vincere-m2-inferno")
header_path = BASE / "header.json"
kills_path = BASE / "kills.parquet"

# ---- DB connection (project DB) ----
DB = {
    "host": "localhost",
    "port": 5433,
    "dbname": "cs2_demo_analyzer",
    "user": "postgres",
    # password is read from $env:PGPASSWORD
}

# ---- Load header (map only) ----
header = json.loads(header_path.read_text(encoding="utf-8"))
map_name = header.get("map_name", "unknown_map")

# ---- Create a stable match_id ----
match_id = str(header.get("demo_file_stamp") or BASE.name)
source_demo = BASE.name + ".dem"

# ---- Load kills and compute K/D/A ----
kills = pd.read_parquet(kills_path)

kills_count = kills.groupby("attacker_name").size().rename("kills")
deaths_count = kills.groupby("victim_name").size().rename("deaths")

assists_series = kills["assister_name"].dropna()
assists_series = assists_series[assists_series.astype(str).str.len() > 0]
assists_count = assists_series.value_counts().rename("assists")

df = pd.concat(
    [kills_count, deaths_count, assists_count],
    axis=1
).fillna(0).astype(int)

df.index.name = "player"
df = df.reset_index()

df["match_id"] = match_id
df["map_name"] = map_name
df["source_demo"] = source_demo

df = df[
    ["match_id", "map_name", "player", "kills", "deaths", "assists", "source_demo"]
]

# --- Remove NUL bytes from text columns (Postgres cannot store \x00 in text) ---
for c in ["match_id", "map_name", "player", "source_demo"]:
    df[c] = df[c].astype(str).str.replace("\x00", "", regex=False).str.strip()

# Optional: show any rows that still look suspicious
bad = df[df["player"].str.contains(r"[\x00]", regex=True)]
if len(bad):
    print("WARNING: players still contain NUL bytes:")
    print(bad[["player"]])


# ---- Insert into Postgres (idempotent) ----
sql = """
INSERT INTO match_player_stats_v1
(match_id, map_name, player, kills, deaths, assists, source_demo)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (match_id, player) DO NOTHING;
"""

with psycopg2.connect(**DB) as conn:
    with conn.cursor() as cur:
        for row in df.itertuples(index=False, name=None):
            cur.execute(sql, row)

print(f"Inserted (or skipped duplicates): {len(df)} rows")
print(f"match_id: {match_id}")
print(f"map_name: {map_name}")
