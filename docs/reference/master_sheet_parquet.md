# CS2 Demo Analyzer — Master Table Guide

This document is a **high-level reference** explaining the purpose, typical use cases,
and important caveats for each `.parquet` table.

Detailed schemas and field-level documentation live in their respective files.
This file exists to answer:
- “Which table should I use?”
- “What is this table good for?”
- “What should I be careful about?”

## Global Notes
- CS2 matchmaking demos typically run at **64 tick**
- Third-party demos (FACEIT / LAN) may run at **128 tick**
- All timing is **tick-based**
- Normalize time when needed:
- Always scope analysis by `round_num` unless explicitly intended otherwise

# parquet.md Notes

## cs2-demo-analyzer\docs\reference\parquet_schema.md\ticks_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Authoritative per-tick snapshot of player state.

**Use this for:**
- Movement analysis
- Positioning and spacing
- Time-on-site or time-in-area metrics
- Cross-table alignment (anchor table)

**Key notes:**
- Each row is a snapshot, not movement
- High-frequency table — joins can explode row counts
- `place` is map-specific and non-standardized

**Common pitfalls:**
- Treating ticks as continuous time
- Joining blindly with other high-frequency tables
- Aggregating across rounds unintentionally

--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\kills_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Final combat outcomes (who killed whom, where, and how).

**Use this for:**
- K/D and trade analysis
- Entry success
- Weapon effectiveness
- Round impact summaries

**Key notes:**
- Represents outcomes, not full engagements
- Multiple kills can occur in the same tick
- Flags are engine-derived and imperfect

**Common pitfalls:**
- Ignoring prior damage context
- Treating kills as pure mechanical skill indicators
- Using kill counts without round normalization

--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\damage_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Granular combat interactions before kills.

**Use this for:**
- ADR
- Chip damage analysis
- Assist logic
- Pressure and poke analysis

**Key notes:**
- One row = one damage instance
- Damage does not imply intent or visibility
- Multiple damage events can occur in one tick

**Common pitfalls:**
- Equating damage with engagements
- Calculating ADR without round isolation
- Using damage alone to explain kills

--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\shots_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Weapon usage and firing behavior.

**Use this for:**
- Shot volume
- Weapon usage patterns
- Spray/burst inference (derived)
- Pressure metrics (with context)

**Key notes:**
- Shots are not hits
- Bullet trajectory is not stored
- Multiple shots may occur in one tick

**Common pitfalls:**
- Using shots fired as aim quality
- Ignoring opponent proximity
- Assuming shots imply danger without context


--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\grenades_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Utility intent (throws), not outcomes.

**Use this for:**
- Utility usage frequency
- Timing of utility deployment
- Setup vs reactive utility

**Key notes:**
- Represents throw moment only
- Effects appear in other tables
- Entity IDs are round-scoped

**Common pitfalls:**
- Treating throws as effective utility
- Assuming throw position equals impact
- Counting grenades without round context

--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\smokes_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Vision denial and space shaping.

**Use this for:**
- Smoke timing
- Area denial analysis
- Execute structure analysis

**Key notes:**
- Smoke position is a centroid, not full volume
- Smoke presence ≠ safety
- Vertical placement matters

**Common pitfalls:**
- Treating smokes as binary blockers
- Ignoring elevation and terrain
- Assuming smoke presence implies control

--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\infernos_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Area denial via fire.

**Use this for:**
- Space denial timing
- Zone control analysis
- Delay metrics

**Key notes:**
- Fire presence does not imply damage
- Centroid ≠ full burn area
- Thrower may be dead while fire persists

**Common pitfalls:**
- Treating infernos as uniform zones
- Using duration as effectiveness proxy
- Overinterpreting centroid position

--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\footsteps_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Potential information leakage via sound.

**Use this for:**
- Noise discipline analysis
- Timing of audible movement
- Risk assessment (with context)

**Key notes:**
- Footsteps indicate sound emission, not detection
- Absence of footsteps ≠ silence
- Geometry and elevation matter heavily

**Common pitfalls:**
- Treating footsteps as “enemy heard”
- Ignoring verticality
- Binary audible/not-audible logic

--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\bomb_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Objective progression and win conditions.

**Use this for:**
- Plant timing
- Retake vs post-plant structure
- Objective pressure analysis

**Key notes:**
- Events are discrete state changes
- Bomb position is bomb entity, not player
- Events may occur after combat ends

**Common pitfalls:**
- Assuming one plant per round
- Treating bomb presence as site control
- Inferring defuse success from defuse start

--------------------------------------------------------------------------
## cs2-demo-analyzer\docs\reference\parquet_schema.md\rounds_parquet.md
--------------------------------------------------------------------------
**Purpose:**  
Structural backbone of the match.

**Use this for:**
- Round segmentation
- Phase definition
- Win condition analysis

**Key notes:**
- Rounds contain multiple phases
- `winner` ≠ last alive side
- Bomb timing lives elsewhere

**Common pitfalls:**
- Treating rounds as equal-duration units
- Mixing freeze-time with live-round data
- Using round winner to explain individual performance

--------------------------------------------------------------------------
## Final Reminder
This file explains **what each table is for**.  
Field-level truth lives in schema files.  
Metric logic lives in analysis code.

## random
bomb.parquet
['tick', 'event', 'X', 'Y', 'Z', 'steamid', 'name', 'bombsite', 'round_num']

damages.parquet
['armor', 'attacker_X', 'attacker_Y', 'attacker_Z', 'attacker_health', 'attacker_place', 'attacker_name', 'attacker_steamid', 'attacker_side', 'ct_side', 'dmg_armor', 'dmg_health', 'health', 'hitgroup', 't_side', 'tick', 'victim_X', 'victim_Y', 'victim_Z', 'victim_health', 'victim_place', 'victim_name', 'victim_steamid', 'victim_side', 'weapon', 'dmg_health_real', 'round_num']

footsteps.parquet
['ct_side', 'duration', 'radius', 'step', 't_side', 'tick', 'player_X', 'player_Y', 'player_Z', 'player_health', 'player_place', 'player_name', 'player_steamid', 'player_side', 'round_num']

grenades.parquet
['thrower_steamid', 'thrower', 'grenade_type', 'tick', 'X', 'Y', 'Z', 'entity_id', 'round_num']

infernos.parquet
['entity_id', 'start_tick', 'end_tick', 'thrower_X', 'thrower_Y', 'thrower_Z', 'thrower_health', 'thrower_place', 'thrower_name', 'thrower_steamid', 'thrower_side', 'X', 'Y', 'Z', 'round_num']

kills.parquet
['assistedflash', 'assister_X', 'assister_Y', 'assister_Z', 'assister_health', 'assister_place', 'assister_name', 'assister_steamid', 'assister_side', 'attacker_X', 'attacker_Y', 'attacker_Z', 'attacker_health', 'attacker_place', 'attacker_name', 'attacker_steamid', 'attacker_side', 'attackerblind', 'attackerinair', 'ct_side', 'distance', 'dmg_armor', 'dmg_health', 'dominated', 'headshot', 'hitgroup', 'noreplay', 'noscope', 'penetrated', 'revenge', 't_side', 'thrusmoke', 'tick', 'victim_X', 'victim_Y', 'victim_Z', 'victim_health', 'victim_place', 'victim_name', 'victim_steamid', 'victim_side', 'weapon', 'weapon_fauxitemid', 'weapon_itemid', 'weapon_originalowner_xuid', 'wipe', 'round_num']

rounds.parquet
['round_num', 'start', 'freeze_end', 'end', 'official_end', 'winner', 'reason', 'bomb_plant', 'bomb_site']

shots.parquet
['ct_side', 'silenced', 't_side', 'tick', 'player_X', 'player_Y', 'player_Z', 'player_health', 'player_place', 'player_name', 'player_steamid', 'player_side', 'weapon', 'round_num']

smokes.parquet
['entity_id', 'start_tick', 'end_tick', 'thrower_X', 'thrower_Y', 'thrower_Z', 'thrower_health', 'thrower_place', 'thrower_name', 'thrower_steamid', 'thrower_side', 'X', 'Y', 'Z', 'round_num']

ticks.parquet
['health', 'place', 'side', 'X', 'Y', 'Z', 'tick', 'steamid', 'name', 'round_num']



ticks.parquet
smokes.parquet
shots.parquet
rounds.parquet
kills.parquet
infernos.parquet
grenades.parquet
footsteps.parquet
damages.parquet
bomb.parquet

