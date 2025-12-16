CS2 Demo Analyzer — RUNBOOK (Step 0 → V1 Complete)

Rule: Step N does not start until Step N–1 is 100% DONE. No exceptions.

Goal (V1):
A minimal desktop GUI that asks the user for a .dem file, parses it, computes basic per-player stats (K/D/A), shows them in a table, and attempts to store them in Postgres without duplicating rows on rerun.

Core constraints:

REAL .dem data only (no dummy data)

Minimal SQL complexity (avoid big joins)

Minimal extraction (only V1 fields)

Simple GUI only (no dashboards / charts)

If DB insert fails, the GUI still shows results (best UX)

============================================================
STEP 0 — PROJECT BOUNDARIES (LOCK)

Decisions to lock:

Input: one HLTV .dem file (single match)

Output V1 stats (LOCKED):

REQUIRED: match_id, map_name, player_name, kills, deaths, assists

NOT IN V1: team_name (deferred)

App type V1: desktop GUI (select file → run → show results)

Database: Postgres (local)

No advanced metrics (ADR/KAST/rating/utility/etc.) in V1

No multi-match analysis in V1 (store match rows + player rows only)

Artifacts to create:

README.md (6 bullets: input, output, db, v1 fields, done definition, constraints)

v1_spec.md (exact fields + types)

RUNBOOK.md (this file)

DONE WHEN:

V1 fields are locked

“What is V1?” can be said in one sentence without debate

============================================================
STEP 1 — FOLDER STRUCTURE (NO CODE)

Create folders:

dem_files/ (where you put .dem files)

src/ (Python source)

sql/ (schema + queries)

outputs/ (parsed artifacts; optional CSV later)

docs/ (notes, decisions)

DONE WHEN:

Folder tree exists and is clean

No work is happening in C:\Windows\System32

============================================================
STEP 2 — PARSER DECISION (LOCK ONE PATH)

Rule: We do NOT build a raw binary .dem parser from scratch in V1.
We WILL use a parsing library/engine. You still “own” the project because you control:
pipeline, schema, metrics, output, and application.

Chosen parser (V1):

awpy (uses demoparser2) on Python 3.12

Parser checklist:

Reads: map_name, kill events, assists if available

Runs locally and produces outputs reliably

Write docs/parser_choice.md:

chosen parser + version

install steps

1-line reason

DONE WHEN:

A single parser approach is chosen and written down

No more switching parsers until V1 is finished

============================================================
STEP 3 — REAL PARSE PROOF (OUTPUT ARTIFACT)

Goal: prove you can parse ONE real .dem and generate parse artifacts.

Input:

One real demo file path (single match)

Output artifact (V1):

awpy parse output extracted into:

outputs/awpy/<demo_name>/

header.json

kills.parquet

(other parquet files are allowed)

Required proof:

map_name is readable from header.json

kills.parquet exists and has attacker/victim/assister columns

STRICT RULES:

No DB requirements for Step 3 completion

Only prove the parser path works end-to-end

DONE WHEN:

The output folder exists

header.json + kills.parquet exist

You can compute K/D/A for exactly 10 players from kills.parquet

============================================================
STEP 4 — DATABASE SCHEMA (POSTGRES) FOR V1

Goal: store V1 rows with minimal schema and guaranteed no-dup reruns.

Create sql/schema_v1.sql.

V1 schema (LOCKED minimal table):

match_player_stats_v1(
match_id TEXT NOT NULL,
map_name TEXT NOT NULL,
player TEXT NOT NULL,
kills INT NOT NULL,
deaths INT NOT NULL,
assists INT NOT NULL,
source_demo TEXT NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
PRIMARY KEY (match_id, player)
)

Notes:

No players/matches tables in V1 (deferred to V2)

No team_name in V1 (deferred)

Primary key guarantees idempotency on rerun

DONE WHEN:

schema_v1.sql exists

Table can be created successfully in Postgres

============================================================
STEP 5 — REAL IMPORT (PARSED OUTPUT -> POSTGRES)

Goal: take the real parsed output and insert player rows into Postgres.

Write src/v1_insert_postgres.py (or equivalent pipeline insert):

reads outputs/awpy/<demo_name>/header.json + kills.parquet

computes K/D/A per player

inserts 10 rows into match_player_stats_v1

ON CONFLICT DO NOTHING for (match_id, player)

sanitize text to remove NUL bytes (\x00) before insert

STRICT RULES:

No complex transformations

No advanced queries

DONE WHEN:

DB contains 10 rows for the match_id

Rerunning the same demo does NOT increase row count

============================================================
STEP 6 — BASIC GUI WRAPPER (V1 APP)

Goal: a minimal GUI that runs the whole pipeline on a real demo.

GUI requirements (V1):

Window title: "CS2 Demo Analyzer (V1)" (text can be customized)

Button: "Select .dem"

Button: "Run"

Status label: shows progress + success/fail

Results table: player_name, kills, deaths, assists

(Optional) CSV export button is NOT required in V1

Behavior:

User selects .dem

Click Run:

parse demo → outputs/awpy/<demo_name>/

compute K/D/A

attempt Postgres insert (non-blocking: GUI still shows results if DB fails)

render results in table

STRICT RULES:

No fancy styling

No charts

Single window

DONE WHEN:

Selecting a real demo + clicking Run shows results in the GUI

DB insert is attempted and does not crash the GUI

Success/failure is visible to the user

============================================================
STEP 7 — V1 COMPLETE CHECKLIST (STOP HERE)

V1 is complete ONLY if all are true:

 App asks for a .dem path (file picker)

 App parses real .dem data into V1 fields

 App shows a readable summary (table)

 App attempts to store results in Postgres

 Rerunning the same demo does not duplicate rows (PRIMARY KEY (match_id, player))

 No step relies on dummy data

 README.md and v1_spec.md accurately describe what exists (update if needed)