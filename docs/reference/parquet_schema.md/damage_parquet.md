damage.parquet

| Field              | Type   | Description           |
| ------------------ | ------ | --------------------- |
| `tick`             | int32  | Game tick             |
| `round_num`        | uint32 | Round number          |
| `attacker_steamid` | uint64 | Attacker SteamID      |
| `attacker_name`    | string | Attacker name         |
| `attacker_side`    | string | Attacker side         |
| `attacker_health`  | double | Attacker HP           |
| `attacker_place`   | string | Attacker map location |
| `attacker_X`       | float  | Attacker X            |
| `attacker_Y`       | float  | Attacker Y            |
| `attacker_Z`       | float  | Attacker Z            |
| `victim_steamid`   | uint64 | Victim SteamID        |
| `victim_name`      | string | Victim name           |
| `victim_side`      | string | Victim side           |
| `victim_health`    | int32  | Victim HP             |
| `victim_place`     | string | Victim map location   |
| `victim_X`         | float  | Victim X              |
| `victim_Y`         | float  | Victim Y              |
| `victim_Z`         | float  | Victim Z              |
| `weapon`           | string | Weapon used           |
| `hitgroup`         | string | Hitgroup              |
| `armor`            | int32  | Victim armor          |
| `health`           | int32  | Health after damage   |
| `dmg_health`       | int32  | HP damage             |
| `dmg_health_real`  | int32  | Actual HP damage      |
| `dmg_armor`        | int32  | Armor damage          |
| `ct_side`          | string | CT team name          |
| `t_side`           | string | T team name           |

**All damage instances (lethal and non-lethal)**

### Notes

#### Damage semantics
- Each row represents a single damage instance, not an engagement or duel.
- Multiple damage events may occur within the same tick or between the same players.

#### Health interpretation
- `health` represents post-damage health.
- `dmg_health_real` reflects effective HP loss after armor.
- Damage may occur without a corresponding kill.

#### Temporal ordering
- Ordering of damage events within the same tick is not guaranteed.
- Always rely on `tick`, not row order, for sequencing.

#### Spatial context
- Attacker and victim positions are snapshots at damage time.
- No information is provided about projectile travel or line-of-sight.

#### Analyst pitfalls
- Using damage count as engagement count.
- Calculating ADR without round isolation.
- Assuming damage implies visibility or intent.
