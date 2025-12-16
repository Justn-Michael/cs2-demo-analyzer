import json
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime

import pandas as pd

try:
    import psycopg2
except Exception:
    psycopg2 = None


PROJECT_ROOT = Path(r"C:\Users\justn\Documents\cs2-demo-analyzer")
OUTPUTS_DIR = PROJECT_ROOT / "outputs" / "awpy"

DB = {
    "host": "localhost",
    "port": 5433,
    "dbname": "cs2_demo_analyzer",
    "user": "postgres",
    # password comes from env var PGPASSWORD (recommended)
}


def _log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def _safe_text(s: str) -> str:
    # Postgres cannot store NUL bytes in TEXT
    return str(s).replace("\x00", "").strip()


def parse_demo_to_folder(demo_path: str) -> Path:
    """
    Runs `awpy parse <demo>` in PROJECT_ROOT so the .zip is created there.
    Then extracts the zip into outputs/awpy/<demo_stem>/ and returns that folder path.
    """
    demo = Path(demo_path)
    if not demo.exists():
        raise FileNotFoundError(f"Demo not found: {demo}")

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    zip_name = f"{demo.stem}.zip"
    zip_path = PROJECT_ROOT / zip_name

    # Remove old zip to avoid confusion
    if zip_path.exists():
        zip_path.unlink()

    _log(f"Parsing demo with awpy: {demo}")
    # Run in project root so awpy writes zip where we can access it
    result = subprocess.run(
        ["awpy", "parse", str(demo)],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        _log("awpy parse failed.")
        if result.stdout:
            _log("STDOUT:\n" + result.stdout)
        if result.stderr:
            _log("STDERR:\n" + result.stderr)
        raise RuntimeError("awpy parse failed (see logs above).")

    if not zip_path.exists():
        # Some awpy versions may write elsewhere; if this happens, we’ll handle later.
        raise RuntimeError(f"Expected zip not found at: {zip_path}")

    out_folder = OUTPUTS_DIR / demo.stem
    out_folder.mkdir(parents=True, exist_ok=True)

    _log(f"Extracting: {zip_path.name} -> {out_folder}")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_folder)

    # Optional: keep the zip as an artifact in outputs/awpy too
    zip_copy = OUTPUTS_DIR / zip_name
    if zip_copy.exists():
        zip_copy.unlink()
    zip_path.replace(zip_copy)

    return out_folder


def extract_kda(parsed_folder: Path) -> tuple[str, str, pd.DataFrame]:
    """
    Reads awpy output in parsed_folder and returns:
      match_id, map_name, df(player,kills,deaths,assists)
    """
    header_path = parsed_folder / "header.json"
    kills_path = parsed_folder / "kills.parquet"

    if not header_path.exists():
        raise FileNotFoundError(f"Missing header.json in {parsed_folder}")
    if not kills_path.exists():
        raise FileNotFoundError(f"Missing kills.parquet in {parsed_folder}")

    header = json.loads(header_path.read_text(encoding="utf-8"))
    map_name = _safe_text(header.get("map_name", "unknown_map"))

    # Use demo_file_stamp if available (yours has it). Fallback to folder name.
    match_id = _safe_text(header.get("demo_file_stamp") or parsed_folder.name)

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
    df["player"] = df["player"].map(_safe_text)

    # sort like you’ve been using
    df = df.sort_values(["kills", "assists", "deaths"], ascending=[False, False, True])

    return match_id, map_name, df


def try_insert_postgres(match_id: str, map_name: str, df: pd.DataFrame, source_demo: str) -> None:
    """
    Best-effort insert. Never raises to caller (GUI shouldn't break).
    """
    if psycopg2 is None:
        _log("DB insert skipped: psycopg2 not installed.")
        return

    try:
        rows = df.copy()
        rows["match_id"] = _safe_text(match_id)
        rows["map_name"] = _safe_text(map_name)
        rows["source_demo"] = _safe_text(source_demo)

        rows = rows[["match_id", "map_name", "player", "kills", "deaths", "assists", "source_demo"]]

        sql = """
        INSERT INTO match_player_stats_v1
        (match_id, map_name, player, kills, deaths, assists, source_demo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (match_id, player) DO NOTHING;
        """

        with psycopg2.connect(**DB) as conn:
            with conn.cursor() as cur:
                for row in rows.itertuples(index=False, name=None):
                    cur.execute(sql, row)

        _log(f"DB insert ok (attempted {len(rows)} rows, duplicates auto-skipped).")

    except Exception as e:
        _log(f"DB insert FAILED (continuing anyway): {e}")


def run_v1(demo_path: str) -> dict:
    """
    Full pipeline:
      - awpy parse demo -> outputs/awpy/<demo_stem>/
      - extract K/D/A dataframe
      - best-effort insert into Postgres
      - return payload for GUI
    """
    parsed_folder = parse_demo_to_folder(demo_path)
    match_id, map_name, df = extract_kda(parsed_folder)

    source_demo = Path(demo_path).name
    try_insert_postgres(match_id, map_name, df, source_demo)

    # return rows for GUI table
    rows = df.to_dict(orient="records")
    return {
        "match_id": match_id,
        "map_name": map_name,
        "rows": rows,
        "parsed_folder": str(parsed_folder),
    }
