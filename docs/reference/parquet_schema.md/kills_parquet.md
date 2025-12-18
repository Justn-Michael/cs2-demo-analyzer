kills.parquet

| Field              | Type   | Description         |
| ------------------ | ------ | ------------------- |
| `tick`             | int32  | Game tick           |
| `round_num`        | uint32 | Round number        |
| `attacker_steamid` | uint64 | Killer SteamID      |
| `attacker_name`    | string | Killer name         |
| `attacker_side`    | string | Killer side         |
| `attacker_health`  | int32  | Killer HP           |
| `attacker_place`   | string | Killer map location |
| `attacker_X`       | float  | Killer X            |
| `attacker_Y`       | float  | Killer Y            |
| `attacker_Z`       | float  | Killer Z            |
| `victim_steamid`   | uint64 | Victim SteamID      |
| `victim_name`      | string | Victim name         |
| `victim_side`      | string | Victim side         |
| `victim_health`    | int32  | Victim HP           |
| `victim_place`     | string | Victim map location |
| `victim_X`         | float  | Victim X            |
| `victim_Y`         | float  | Victim Y            |
| `victim_Z`         | float  | Victim Z            |
| `assister_steamid` | uint64 | Assister SteamID    |
| `assister_name`    | string | Assister name       |
| `weapon`           | string | Weapon used         |
| `distance`         | float  | Kill distance       |
| `headshot`         | bool   | Headshot            |
| `hitgroup`         | string | Hitgroup            |
| `penetrated`       | int32  | Wallbang            |
| `thrusmoke`        | bool   | Through smoke       |
| `noscope`          | bool   | No-scope            |
| `attackerblind`    | bool   | Attacker blind      |
| `attackerinair`    | bool   | Attacker airborne   |
| `assistedflash`    | bool   | Flash assist        |
| `dominated`        | int32  | Domination          |
| `revenge`          | int32  | Revenge kill        |
| `wipe`             | int32  | Team wipe           |
| `ct_side`          | string | CT team name        |
| `t_side`           | string | T team name         |

**All kill events**

### Notes

#### Event semantics
- Each row represents a completed kill event.
- Kills are discrete outcomes, not full engagements.
- Multiple kills may occur in the same tick.

#### Temporal interpretation
- Kill timing is server-tick based.
- Tick order does not represent animation or perception order.
- Always sequence by `round_num` then `tick`.

#### Spatial interpretation
- Attacker and victim coordinates are snapshots at kill time.
- Positions do not account for projectile travel or interpolation.
- Distance is calculated at the moment of the kill.

#### Flag interpretation
- Flags such as `headshot`, `noscope`, and `thrusmoke` are engine-derived.
- Flags may contain false negatives due to demo limitations.
- Flags should not be treated as perfect truth.

#### Analyst pitfalls
- Treating kills as isolated skill events.
- Ignoring prior damage history.
- Using kill count without round or context normalization.
