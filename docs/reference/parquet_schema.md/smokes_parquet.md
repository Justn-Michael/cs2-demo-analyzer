smokes.parquet

| Field             | Type   | Description          |
| ----------------- | ------ | -------------------- |
| `entity_id`       | int64  | Smoke entity ID      |
| `start_tick`      | int64  | Smoke start tick     |
| `end_tick`        | int64  | Smoke end tick       |
| `round_num`       | uint32 | Round number         |
| `thrower_steamid` | int64  | Thrower SteamID      |
| `thrower_name`    | string | Thrower name         |
| `thrower_side`    | string | Thrower side         |
| `thrower_health`  | int64  | Thrower HP           |
| `thrower_place`   | string | Thrower map location |
| `thrower_X`       | double | Thrower X position   |
| `thrower_Y`       | double | Thrower Y position   |
| `thrower_Z`       | double | Thrower Z position   |
| `X`               | double | Smoke centroid X     |
| `Y`               | double | Smoke centroid Y     |
| `Z`               | double | Smoke centroid Z     |

**Smoke grenade zones**

### Notes

#### Entity lifecycle
- Smoke entities persist from `start_tick` to `end_tick`.
- Smoke presence represents visual obstruction, not physical blockage.
- Smokes do not guarantee vision denial in all directions.

#### Timing interpretation
- Smoke duration must be normalized using tickrate:
- Smokes may bloom gradually; instant full opacity should not be assumed.

#### Spatial interpretation
- `X`, `Y`, `Z` represent the smoke centroid.
- Smoke volume is three-dimensional and map-dependent.
- Vertical positioning is critical for elevated or dropped smokes.

#### Tactical interpretation
- Smoke presence does not imply effective control or safety.
- Smokes must be interpreted relative to player positions and sightlines.

#### Analyst pitfalls
- Treating smokes as binary vision blockers.
- Ignoring elevation and terrain.
- Assuming smoke presence implies coordinated team play.
