grenades.parquet

| Field             | Type   | Description       |
| ----------------- | ------ | ----------------- |
| `tick`            | int32  | Game tick         |
| `round_num`       | uint32 | Round number      |
| `entity_id`       | int32  | Grenade entity ID |
| `thrower_steamid` | uint64 | Thrower SteamID   |
| `thrower`         | string | Thrower name      |
| `grenade_type`    | string | Grenade type      |
| `X`               | float  | Grenade X         |
| `Y`               | float  | Grenade Y         |
| `Z`               | float  | Grenade Z         |

**Grenade throw events**

### Notes

#### Event semantics
- Each row represents a grenade being thrown, not its effect.
- Grenade effects (damage, smoke, fire) are represented in other tables.
- The same grenade entity may later appear in `smokes.parquet` or `infernos.parquet`.

#### Timing and tick interpretation
- `tick` represents the throw moment, not detonation or effect start.
- Grenade travel time is not encoded and must be inferred if needed.
- Time-to-effect metrics must join with effect tables and normalize by tickrate.

#### Spatial meaning
- `X`, `Y`, `Z` represent the grenade position at throw time.
- These coordinates do not represent the final detonation location.
- Vertical position (`Z`) is important for throw trajectory analysis.

#### Entity identity
- `entity_id` identifies the grenade entity for its lifetime.
- Entity IDs may be reused across rounds; always scope by `round_num`.

#### Analyst pitfalls
- Treating grenade throws as guaranteed utility impact.
- Assuming throw position equals detonation position.
- Aggregating grenade counts without round isolation.
