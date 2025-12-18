# Metrics Ownership Map — CS2 Demo Analyzer

This document defines **metric domains**, their owning modules, and the
responsibility boundaries for each file in `src/metrics/`.

Rule:
Each metric belongs to exactly ONE domain file.
Metric files never call each other.
All metric merging happens in the pipeline layer.

--------------------------------------------------
FRAGGING (fragging.py)
--------------------------------------------------
Primary responsibility:
Direct kill-based combat outcomes.

Source files:
- kills.parquet

Owned metrics:
- kills
- deaths
- assists
- K/D
- K/D/A ratio
- multi-kills (2k / 3k / 4k / ace)
- headshot kills (count, not %)
- trade kills (as killer or victim)

Explicitly NOT owned:
- damage
- ADR
- KAST
- utility impact
- opening duels

--------------------------------------------------
DAMAGE (damage.py)
--------------------------------------------------
Primary responsibility:
All health and armor damage dealt by players.

Source files:
- damages.parquet

Owned metrics:
- total_damage
- damage_per_round
- ADR (average damage per round)
- damage_to_armor
- damage_to_health
- damage_by_weapon_type (rifle, AWP, pistol, SMG)

Explicitly NOT owned:
- kills
- headshots (kill-level)
- grenade logic (belongs to utility)

--------------------------------------------------
UTILITY (utility.py)
--------------------------------------------------
Primary responsibility:
Impact from grenades and non-gun utility.

Source files:
- grenades.parquet
- infernos.parquet
- smokes.parquet

Owned metrics:
- utility_damage
- grenade_damage (HE / molotov)
- enemies_flashed
- flash_assists
- flash_duration
- smokes_thrown
- incendiaries_thrown

Explicitly NOT owned:
- kills
- total damage (gun damage lives in damage.py)
- round survival logic

--------------------------------------------------
OPENINGS (openings.py)
--------------------------------------------------
Primary responsibility:
Early-round engagements and first-contact outcomes.

Source files:
- kills.parquet
- rounds.parquet

Owned metrics:
- opening_kills
- opening_deaths
- opening_duels_attempted
- opening_duel_win_rate
- first_kill_rounds
- first_death_rounds

Explicitly NOT owned:
- clutch logic
- overall K/D

--------------------------------------------------
CLUTCHES (clutches.py)
--------------------------------------------------
Primary responsibility:
Disadvantage situations (1vX, 2vX).

Source files:
- kills.parquet
- ticks.parquet
- rounds.parquet

Owned metrics:
- 1v1 / 1v2 / 1v3 / 1v4 / 1v5 attempts
- clutch_wins
- clutch_win_rate
- survived_clutch_rounds

Explicitly NOT owned:
- opening duels
- KAST

--------------------------------------------------
ROUND IMPACT (round_impact.py)
--------------------------------------------------
Primary responsibility:
Round-level contribution and survivability.

Source files:
- rounds.parquet
- ticks.parquet
- kills.parquet

Owned metrics:
- rounds_played
- survived_rounds
- KAST
- KAST_percent
- rounds_with_kill
- rounds_with_assist
- rounds_traded

Explicitly NOT owned:
- damage totals
- clutch-specific logic

--------------------------------------------------
OBJECTIVES (objectives.py)
--------------------------------------------------
Primary responsibility:
Objective-based actions (bomb-related).

Source files:
- bomb.parquet
- rounds.parquet

Owned metrics:
- bomb_plants
- bomb_defuses
- successful_defuses
- plants_in_winning_rounds
- defuses_in_winning_rounds

Explicitly NOT owned:
- utility damage
- fragging

--------------------------------------------------
WEAPONS (weapons.py)
--------------------------------------------------
Primary responsibility:
Weapon usage and effectiveness.

Source files:
- kills.parquet
- shots.parquet

Owned metrics:
- kills_by_weapon
- deaths_by_weapon
- accuracy
- shots_fired
- hits_landed
- headshot_percent (weapon-scoped)
- AWP impact metrics

Explicitly NOT owned:
- total damage
- grenade usage

--------------------------------------------------
IDENTITY (identity.py)
--------------------------------------------------
Primary responsibility:
Player identity resolution and normalization.

Source files:
- ticks.parquet
- header.json
- Steam Web API

Owned data:
- steamid64
- player_name normalization
- avatar_url
- team association
- side (CT / T) mapping

Explicitly NOT owned:
- performance metrics of any kind

--------------------------------------------------
PIPELINE RULE
--------------------------------------------------
Metric files:
- Read raw parquet files
- Return player-keyed DataFrames only

Pipeline layer:
- Calls metric extractors
- Merges DataFrames
- Handles DB insertion
- Supplies final dataset to GUI

This separation is mandatory for maintainability and scalability.
