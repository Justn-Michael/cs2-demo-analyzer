# v1_spec.md — Data Contract (V1)

This document defines the exact data structures for CS2 Demo Analyzer v1.
No fields may be added or removed during v1 development.

--------------------------------------------------
INPUT
--------------------------------------------------
- demo_path: TEXT
  - Full file path to one HLTV `.dem` file
  - Represents a single CS2 match

--------------------------------------------------
OUTPUT FILE
--------------------------------------------------
File name:
- outputs/match_v1.json

JSON Structure (Option A — Nested):

{
  "match": {
    "match_id": "string",
    "map_name": "string",
    "demo_path": "string"
  },
  "teams": [
    {
      "team_name": "string",
      "players": [
        {
          "player_name": "string",
          "kills": integer,
          "deaths": integer,
          "assists": integer
        }
      ]
    }
  ]
}

--------------------------------------------------
MATCH ID RULE
--------------------------------------------------
- match_id is deterministic
- Generated as a hash of:
  - demo_path
  - file size
  - file modified time
- Re-parsing the same demo must produce the same match_id

--------------------------------------------------
DATABASE (POSTGRES)
--------------------------------------------------

Table: matches
- match_id TEXT PRIMARY KEY
- demo_path TEXT
- parsed_at TIMESTAMP
- map_name TEXT

Table: teams
- team_id TEXT PRIMARY KEY
- match_id TEXT REFERENCES matches(match_id)
- team_name TEXT

Table: players
- player_id TEXT PRIMARY KEY
- player_name TEXT

Table: player_match_stats
- match_id TEXT REFERENCES matches(match_id)
- team_id TEXT REFERENCES teams(team_id)
- player_id TEXT REFERENCES players(player_id)
- kills INT
- deaths INT
- assists INT
- PRIMARY KEY (match_id, player_id)

--------------------------------------------------
DONE DEFINITION (TESTABLE)
--------------------------------------------------
Given one real `.dem` file:
- `match_v1.json` is generated
- Exactly 10 players are present
- Player stats match the actual match
- Rows are inserted into Postgres without duplication
