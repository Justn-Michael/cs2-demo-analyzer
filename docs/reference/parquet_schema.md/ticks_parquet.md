ticks.parquet

| Field       | Type   | Description       |
| ----------- | ------ | ----------------- |
| `tick`      | int32  | Game tick         |
| `round_num` | uint32 | Round number      |
| `steamid`   | uint64 | Player SteamID    |
| `name`      | string | Player name       |
| `side`      | string | Player side       |
| `health`    | int32  | Player HP         |
| `place`     | string | Map location      |
| `X`         | float  | Player X position |
| `Y`         | float  | Player Y position |
| `Z`         | float  | Player Z position |

**Per-tick player state snapshots**

### Notes

#### Tickrate and time semantics
- CS2 matchmaking typically runs at 64 tick.
- Third-party demos may run at 128 tick.
- Time-based metrics must normalize ticks:
- Tickrate should not be assumed without verification.

#### Snapshot semantics
- Each row represents a snapshot at a single server tick.
- Movement between ticks is implicit and must be derived.
- Player velocity and acceleration are not directly encoded.

#### Spatial interpretation
- Positions are server-authoritative.
- Float precision may differ across tables.
- Position changes between ticks are not guaranteed to be linear.

#### Player state interpretation
- `health` reflects the state at that tick, not pre-event health.
- Multiple state changes may occur within the same tick.

#### Analyst pitfalls
- Treating tick data as continuous time.
- Aggregating ticks across rounds without isolation.
- Assuming equal tick spacing across demos.
