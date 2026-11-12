# Ser notes

## infoscroll: psicorps info compendium (2026-10-31, local, uncommitted)

- chars/ser/guilds/psicorps_info.tin, read by chars/ser/guilds/psicorps.tin (config.tin reads that at login and gswap).
- `infoscroll` (not `pinfo`: that is a game command, the same as `info`) sends `info`, then `info <topic>` for every topic it finds, writes each page to notes/psicorps_info.txt
  and ends the file with a contents list and the topics that had no info file. `infoscroll more {a;b}` adds pages to the
  end of the file. `infoscroll stop` quits.
- Topics come from `topic : description` rows (not on power pages, which start with "Power Level :"), "See also:"
  lines and `powers ...`/`skills ...` info pages, then it sends the game command `powers ALL` (capital ALL: lowercase
  `powers all` filters to names containing "all"), writes that table into the file and reads `info <power>` for every row.
- Each page ends with a `pinfomark` (reply "There is no reason to 'pinfomark' here."), 15 s timeout per page, waits
  while `$incombat` is 1.
- Game facts (Ser's log 2026-10-31): pages start `--===--` / `-- PsiCorps Info: <Title>` / `--===--` with no end line;
  a missing topic answers "No guild help exists on that topic." `info power list` is a miss, `info powers list` works.
- `powers ALL` format: "All guild abilities:", a header, rows `[*]name<spaces>T Psi Sta M Area` (`*` = installed),
  footer "T - Tier, Psi - Psi Cost, Sta - Stamina cost, M - Maintainable".
- Headless test passed (fake server with the real coloured pages and the real `powers ALL` table). Check live: the
  marker line, whether power info topics with numbers (`astral construct 1`) exist, the `skills list` layout.

## Loadout check (2026-10-31, from logs 10-28..10-31, 680 kills, mostly Knights Training)

- Per round (4,351 rounds): 17,301 total = Soul Crush 8,219 (48%, ~1.04 crushes/round at ~7,900, "You grasp X's
  mental energies; and crush them like matchsticks." + "(N)" on the next line) + everything else 9,082 (~19 hits of
  ~470: psiwield/melee, construct). Soul Crush is Telepathy (Cha, Ser's lowest at 277) + Psychokinetic Power.
  karvec: more stamina means more crushes, so stamina powers (steel jaw, conductive grasp) cost crushes.
- Soul Crush comes from mud-side reflexes (karvec 2026-10-31): `gp2 >80% soul crush` and `gp2 >60% soul crush`
  (GP1 = PE, GP2 = stamina, as in the 2024 listing that also had `gp1 <33% body fuel 1800`). Soul Crush costs 320 PE,
  0 stamina: stamina only gates it. 600 rounds of 4,351 had two crushes. Heartbeat casts don't take crush rounds
  (1.15 crushes/round with a cast vs 1.00 without). No `apump` use in the logs: `apump 80` may keep stamina over 80%.
- Per fight (6.4 rounds): Astral Construct 6 ~1 cast (320 PE) for ~3,000. Flaming Shroud ~7,800 per cast (49 dmg/PE).
  Greater Biocurrent 1.2 casts (~190 PE) for 12 damage: needs SP (6 SP/mob/round) and `convert` empties SP. karvec is
  testing with convert off (2026-10-31). Bolt: median 0 damage.
- Stats: natural max 275 (karvec). Ser is 275 except Int and Cha 273 ("unable to advance any stats at your current
  level"). Cha extras: Salsa +4, mark of Aeonos +10, Fluctuating Field of the Elements +10 (5 min), and -20 for ~1 h
  from "The guilt for killing the Beatles" (Simpsons 2.0). Animal affinity bull gives Str +11, so eagle likely Cha +11.
- Ideas to test: `animal affinity eagle` vs bull for crush size, recall pain/torment right after a crush.
- karvec: psychic vampire was replaced by conductive grasp (powers ALL on 10-31 still lists psychic vampire at T6).
- Free slots at tour 100: T1 1, T2 1, T7 1. Untrained cheap skills: Autohypnosis (7,500/level), Energy Charge (2,500),
  Overchannel (5,000), Total Defense (10,000). Expertise 100/150 and Resistance 160/161 cost 3.2M / 11.6M per level.
- Recall pain/agony/torment are mutually exclusive: does one replay the last hit (a crush?) or the whole round?
  Answered 2026-11-10 (torment, 4 casts): it doubles the whole round it lands in (the next round after the cast), not
  the round before. Cooldown 10 rounds (~20 s), 320 PE. `strategy rtorment` casts it as soon as ready, except in a
  mob's last ~2 rounds. Details in notes/outstanding.md.
