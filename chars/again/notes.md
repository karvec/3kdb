# Again: fremen training and advancing

These are Again's own files in `chars/again/guilds/`. Nothing in `common/` was changed. They load at
login (and on gswap into fremen) through `chars/again/guilds/fremen.tin`.

## Commands

| Command | What it does |
|---|---|
| `fskills` | Shows `skills` plus a summary: ranks, guild level, ranks to the next guild level, the rank goal, gxp |
| `fskill-train` | Lists the skills in the order `ftrain` will train them (from the last `skills`) |
| `ftrain` | Walks to the trainers and trains everything the gxp covers, then walks back |
| `ftrain stop` | Stops a training walk |
| `strategy autoadvance` | Turns auto-advance on or off (saved per guild) |

## ftrain
- **Order:** it trains one rank per skill per round. Assault and Weirding come first until they reach the next
  rank's requirement (Caid needs 30). After that it picks the cheapest skill. It stops at the first skill it
  can't afford.
- **Walk:** it visits Jessica, Otheym, Akkar and Shimoom (only the ones it needs). Each time it sends a bare
  `train`: "Train what ?" means it has arrived. It retries every 3 seconds while you travel and gives up
  after 2 minutes.
- **Rounds:** after each round it reads `skills` again and does another round if gxp is left. When nothing
  more is affordable, it walks back to where you started.
- **Bot:** `go` pauses the bot and ftrain doesn't restart it. Resume with `..`.
- **Combat:** it won't start during a fight.

## autoadvance
- **When:** after each kill it reads the "You need ... to achieve your next level" and "You have ... to
  spend" lines and does at most one thing.
- **Stats first:** while the level still has stat raises left, it raises the cheaper of con and dex (con on
  a tie). If neither is affordable yet, it waits.
- **Leveling:** with no stat raises left and the level ready, it sends `advance` and answers `y`.
- **Cost table:** it re-reads `check cost` after each raise or level.
- **Changing the order:** add a line like `#var fremen_adv_stats {con;dex;str}` to
  `chars/again/guilds/fremen.tin`, below the `#read` lines.
- **Max HP +4:** not included. Add it once the buy command is known (and whether it uses a stat raise).

## Fremen facts used
- **Guild level:** total skill ranks / 6.
- **Skill cost:** the Normal cost at that rank times the difficulty: Very Easy 0.6, Easy 0.8, Normal 1,
  Hard 1.2, Very Hard 1.4. Normal costs: rank 24 1.5M, 25 1.75M, 26 2.0M, 27 2.5M, 28 3.0M.
- **Fedaykin ranks:**

  | Rank | Guild level | Assault and Weirding |
  |---|---|---|
  | Naib | 70 | 25 |
  | Bashar | 80 | 28 |
  | Caid | 90 | 30 |
  | Burseg | 100 | 33 |
  | Mahdi | 110 | 35 (any career) |

- **fhelp mode:** keep assault, pain, litany and weirding fairly even, and prana and bindu fairly even.

## Not run live yet
Everything was tested against a fake server only. If the first live run misbehaves, run `cc_trace 30`, then
the command, so Claude can read `logs/cc_debug/<user>.log`.
