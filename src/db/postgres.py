from datetime import datetime

import pandas as pd

from util.text import safe_text


try:
    import psycopg2
except Exception:
    psycopg2 = None


DB = {
    "host": "localhost",
    "port": 5433,
    "dbname": "cs2_demo_analyzer",
    "user": "postgres",
    # password comes from env var PGPASSWORD if set
}


def _log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def try_insert_match_player_stats_v1(match_id: str, map_name: str, df: pd.DataFrame, source_demo: str) -> None:
    """
    Best-effort insert. Never raises to caller (GUI shouldn't break).
    Inserts into: match_player_stats_v1
    """
    if psycopg2 is None:
        _log("DB insert skipped: psycopg2 not installed.")
        return

    try:
        rows = df.copy()
        rows["match_id"] = safe_text(match_id)
        rows["map_name"] = safe_text(map_name)
        rows["source_demo"] = safe_text(source_demo)

        # enforce column order
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
