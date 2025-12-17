import json
from pathlib import Path

import pandas as pd

from util.text import safe_text



def extract_fragging(parsed_folder: Path) -> tuple[str, str, pd.DataFrame]:
    """
    Reads AWPY output in parsed_folder and returns:
      match_id, map_name, df(player,kills,deaths,assists)
    """
    header_path = parsed_folder / "header.json"
    kills_path = parsed_folder / "kills.parquet"

    if not header_path.exists():
        raise FileNotFoundError(f"Missing header.json in {parsed_folder}")
    if not kills_path.exists():
        raise FileNotFoundError(f"Missing kills.parquet in {parsed_folder}")

    header = json.loads(header_path.read_text(encoding="utf-8"))
    map_name = safe_text(header.get("map_name", "unknown_map"))

    # Use demo_file_stamp if available. Fallback to folder name.
    match_id = safe_text(header.get("demo_file_stamp") or parsed_folder.name)

    kills = pd.read_parquet(kills_path)

    kills_count = kills.groupby("attacker_name").size().rename("kills")
    deaths_count = kills.groupby("victim_name").size().rename("deaths")

    assists_series = kills["assister_name"].dropna()
    assists_series = assists_series[assists_series.astype(str).str.len() > 0]
    assists_count = assists_series.value_counts().rename("assists")

    df = pd.concat([kills_count, deaths_count, assists_count], axis=1).fillna(0).astype(int)
    df.index.name = "player"
    df = df.reset_index()

    # sanitize text columns
    df["player"] = df["player"].map(safe_text)

    # sort like your current v1
    df = df.sort_values(["kills", "assists", "deaths"], ascending=[False, False, True])

    return match_id, map_name, df
