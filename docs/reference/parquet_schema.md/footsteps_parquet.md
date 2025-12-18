footsteps.parquet

| Field            | Type   | Description    |
| ---------------- | ------ | -------------- |
| `tick`           | int32  | Game tick      |
| `round_num`      | uint32 | Round number   |
| `player_steamid` | uint64 | Player SteamID |
| `player_name`    | string | Player name    |
| `player_side`    | string | Player side    |
| `player_health`  | int32  | Player HP      |
| `player_place`   | string | Map location   |
| `player_X`       | float  | Player X       |
| `player_Y`       | float  | Player Y       |
| `player_Z`       | float  | Player Z       |
| `duration`       | float  | Sound duration |
| `radius`         | int32  | Sound radius   |
| `step`           | bool   | Step index     |
| `ct_side`        | string | CT team name   |
| `t_side`         | string | T team name    |

**Footstep sound emission events**

### Notes

#### Sound semantics
- Each row represents a sound emission, not movement distance.
- A single movement action may generate multiple footsteps.
- Absence of footsteps does not imply silence.

#### Radius and duration
- `radius` indicates maximum audible range, not guaranteed detection.
- `duration` reflects sound emission time, not exposure duration.

#### Tactical interpretation
- Footsteps indicate potential information leakage, not confirmed detection.
- Detection depends on distance, elevation, geometry, and enemy orientation.

#### Spatial interpretation
- Coordinates represent sound origin, not final player position.
- Vertical positioning (`Z`) is critical for multi-level areas.

#### Analyst pitfalls
- Treating footsteps as confirmed detection.
- Ignoring verticality and map geometry.
