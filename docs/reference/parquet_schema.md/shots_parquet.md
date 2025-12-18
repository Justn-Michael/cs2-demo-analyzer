shots.parquet

| Field            | Type   | Description        |
| ---------------- | ------ | ------------------ |
| `tick`           | int32  | Game tick          |
| `round_num`      | uint32 | Round number       |
| `player_steamid` | uint64 | Shooter SteamID    |
| `player_name`    | string | Shooter name       |
| `player_side`    | string | Shooter side       |
| `player_health`  | int32  | Shooter HP         |
| `player_place`   | string | Map location       |
| `player_X`       | float  | Shooter X position |
| `player_Y`       | float  | Shooter Y position |
| `player_Z`       | float  | Shooter Z position |
| `weapon`         | string | Weapon fired       |
| `silenced`       | bool   | Silencer flag      |
| `ct_side`        | string | CT team name       |
| `t_side`         | string | T team name        |

**Weapon fire events**

### Notes

#### Shot semantics
- Each row represents a weapon fire event, not a hit or kill.
- Shots may miss, hit walls, or penetrate targets.

#### Temporal context
- Multiple shots may occur in the same tick.
- Burst and spray patterns must be derived.

#### Spatial interpretation
- Coordinates represent firing position, not bullet trajectory.
- Spread, recoil, and penetration paths are not stored.

#### Weapon context
- `weapon` reflects the weapon at time of fire.
- `silenced` applies only to supported weapons and may be null.

#### Analyst pitfalls
- Using shots fired as aim quality.
- Assuming shot volume equals pressure.
