infernos.parquet

| Field             | Type   | Description       |
| ----------------- | ------ | ----------------- |
| `entity_id`       | int64  | Inferno entity ID |
| `start_tick`      | int64  | Fire start        |
| `end_tick`        | int64  | Fire end          |
| `round_num`       | uint32 | Round number      |
| `thrower_steamid` | int64  | Thrower SteamID   |
| `thrower_name`    | string | Thrower name      |
| `thrower_side`    | string | Thrower side      |
| `thrower_health`  | int64  | Thrower HP        |
| `thrower_place`   | string | Map location      |
| `thrower_X`       | double | Thrower X         |
| `thrower_Y`       | double | Thrower Y         |
| `thrower_Z`       | double | Thrower Z         |
| `X`               | double | Fire centroid X   |
| `Y`               | double | Fire centroid Y   |
| `Z`               | double | Fire centroid Z   |

**Molotov / Incendiary fire zones**

### Notes

#### Entity lifecycle
- Each inferno entity has a defined lifetime from `start_tick` to `end_tick`.
- Infernos represent area denial zones, not guaranteed damage.
- Fire presence does not imply player contact or damage.

#### Timing interpretation
- Fire duration must be calculated using:
- Fire may persist after combat has ended.
- Start and end ticks represent server-side entity state changes.

#### Spatial interpretation
- `X`, `Y`, `Z` represent the fire centroid, not the full burn area.
- Fire coverage is irregular and map-dependent.
- Do not treat infernos as circular or uniform zones.

#### Thrower context
- Thrower fields represent the player at throw time, not during burn duration.
- Thrower may be dead while the inferno is still active.

#### Analyst pitfalls
- Treating infernos as guaranteed space denial.
- Using centroid position for precise area control modeling.
- Assuming fire duration implies tactical effectiveness.

