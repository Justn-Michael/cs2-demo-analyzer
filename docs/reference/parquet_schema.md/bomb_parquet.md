bomb.parquet

| Field       | Type   | Description     |
| ----------- | ------ | --------------- |
| `tick`      | int32  | Game tick       |
| `round_num` | uint32 | Round number    |
| `steamid`   | uint64 | Player SteamID  |
| `name`      | string | Player name     |
| `event`     | string | Bomb event type |
| `bombsite`  | string | Bombsite        |
| `X`         | float  | World X         |
| `Y`         | float  | World Y         |
| `Z`         | float  | World Z         |

### Notes

#### Event semantics
- Each row represents a discrete bomb state transition, not continuous interaction.
- Common events include plant, defuse start, defuse end, and explosion.
- Events must always be ordered by `round_num` and then `tick`.

#### Timing and tick interpretation
- Bomb timing is tick-based, not wall-clock time.
- Time-based metrics must normalize ticks:
- Bomb timers must never be hardcoded; always infer from demo data.

#### Spatial meaning
- `X`, `Y`, and `Z` represent the bomb entity location, not the planter’s final position.
- Bomb position is usually static after plant, but should not be assumed identical across all events.

#### Round context
- Always join bomb events with `rounds.parquet` using `round_num`.
- Bomb events may occur after all players are eliminated.
- `bombsite` is authoritative and preferred over coordinate inference.

#### Analyst pitfalls
- Assuming one plant per round.
- Treating bomb presence as site control.
- Inferring defuse success from defuse start alone.
