rounds.parquet

| Field          | Type   | Description       |
| -------------- | ------ | ----------------- |
| `round_num`    | uint32 | Round number      |
| `start`        | int32  | Round start tick  |
| `freeze_end`   | int32  | Freeze time end   |
| `end`          | int32  | Round end tick    |
| `official_end` | int32  | Official end tick |
| `winner`       | string | Round winner      |
| `reason`       | string | Win condition     |
| `bomb_plant`   | int64  | Bomb planted tick |
| `bomb_site`    | string | Bombsite          |

**Round-level structural metadata**

### Notes

#### Round phases
- Rounds contain freeze time, live round, and post-round phases.
- Analysts must explicitly define which phases are included in metrics.

#### Winner and reason
- `winner` indicates the winning side, not necessarily the last alive side.
- `reason` encodes the round-ending condition.

#### Bomb context
- `bomb_plant` indicates whether a plant occurred, not when it occurred.
- Join with `bomb.parquet` for timing and spatial details.

#### Aggregation rules
- `round_num` is the primary isolation boundary.
- Never aggregate player metrics across rounds unintentionally.

#### Analyst pitfalls
- Treating all rounds as equal duration.
- Mixing freeze-time and live-round data.
