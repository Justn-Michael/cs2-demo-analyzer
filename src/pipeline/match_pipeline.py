from pathlib import Path

from parsers.awpy_cli import parse_demo_to_folder
from metrics.fragging import extract_fragging
from db.postgres import try_insert_match_player_stats_v1


def run_match(demo_path: str) -> dict:
    """
    Full pipeline:
      - awpy parse demo -> outputs/awpy/<demo_stem>/
      - extract K/D/A dataframe
      - best-effort insert into Postgres
      - return payload for GUI
    """
    parsed_folder = parse_demo_to_folder(demo_path)
    match_id, map_name, df = extract_fragging(parsed_folder)


    source_demo = Path(demo_path).name
    try_insert_match_player_stats_v1(match_id, map_name, df, source_demo)

    rows = df.to_dict(orient="records")
    return {
        "match_id": match_id,
        "map_name": map_name,
        "rows": rows,
        "parsed_folder": str(parsed_folder),
    }
