# CS2 Demo Analyzer (V1)

## Purpose
Internal analyst tool for Counter-Strike 2 that parses a real HLTV .dem file
and produces basic per-player match statistics for team analysis.

This tool is built for correctness, structure, and future extensibility —
not for completeness or polish in v1.

## Input
- One HLTV `.dem` file
- Single match
- Exactly 10 players (5v5)

## Output
- A basic GUI that allows the user to select a `.dem` file and run analysis
- A JSON file (`match_v1.json`) containing parsed match data
- Parsed data displayed in a simple table inside the GUI

## Database
- PostgreSQL
- Stores:
  - Match metadata
  - Teams
  - Player match statistics
- Data is inserted only after successful parsing of a real `.dem`

## V1 Fields (Locked)
- match_id
- map_name
- team_name (real team names)
- player_name
- kills
- deaths
- assists

## Done Definition (V1)
V1 is complete when:
- The user selects a real `.dem` file in the GUI
- The application parses the demo successfully
- `match_v1.json` is created with correct data
- Match data is inserted into Postgres without duplication
- Player stats are displayed in the GUI

## Constraints (Non-Negotiable)
- Real `.dem` files only (no dummy data)
- No advanced metrics (ADR, KAST, ratings, etc.)
- No large-scale data extraction
- No complex SQL joins
- No fancy UI or dashboards
- No redesign until v1 works end-to-end
