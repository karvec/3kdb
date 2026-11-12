# Again (juggernaut, hardcore)

Read this only when working on Again. Re-rolled as a juggernaut 2026-10-24 after dying as a fremen.
State 2026-10-27: Gnome, botting Aegis with `botstack 6`. Earlier, 2026-10-26 evening: Clan Wolf, Gnome glvl 2 (Elemental parked at 20), player level 23. Gnome: BA 1, IS 0, 33 credits.

## Files (chars/again/guilds/, untracked, live run pending)

- `juggernaut.tin`: read by config.tin after the guild scripts; reads the two below and adds the strategies.
- `juggernaut_advance.tin`, strategy `autoadvance`: after a kill's "You have X to spend." line, chains
  `advance <stat>` + `rcost` while affordable, picking the lowest cost x weight from `jugg_adv_stats`
  (con 1, dex 1, str 2). Marks a stat capped on "Sorry sir, but you must gain another level". Stats only since
  2026-11-02 (it used to level only once every listed stat was capped: ~5-6 raises, 25-30M xp, per ~12M level).
- Same file, strategy `autolevel` (2026-11-02, karvec: levelling before stats): after a kill, `advance` + `y` as soon as
  "You need N experience" is <= 0. It runs before autoadvance on the same line, and after a level-up's `rcost` table,
  so with both on the level always goes first and stats get what's left until the next level is affordable. With
  autolevel only, no stats are raised. A level-up costs its xp (pool ~0 after), stat raises don't change the level cost.
  `advance` and `y` go out together, and the `y` is sent WITHOUT the `!` prefix: at a game prompt a line starting
  with `!` runs as a normal command ("There is no reason to 'y' here." and the prompt again). Fixed 2026-10-26.
- `juggernaut_glevel.tin`, strategy `autoglevel`: at gxp >= 100% after a kill, out of combat: `go jugg_upgrade`
  (room 1028), `upgrade` (re-probed every 3 s on "There is no reason to 'upgrade' here.", gives up after ~3 min),
  upgrades again while gxp stays >= 100, walks back, resumes the bot after 10 s.
  After the last upgrade it goes to the tech bay (`go jugg_tech`, room 1067), reads `purchase` (rows "Name  cur:cost",
  "You currently have N credits available."), and buys the first entry of `jugg_tech_plan[<suit>]` ("tech level@min glvl")
  that is below its level and due, re-reading after each "purchased for"; stops and saves at the first unaffordable one.
  Suit and suit glvl come from the "<name> has just been upgraded to a level N <Suit>!!!" line or the gs row marked
  `<=-*-=>`. A purchase with no answer in 20 s is skipped for the session. Plans for elemental and gnome are in the file.
  From player level `jugg_stash_level` (30, the house access level) it first does `go home` (Lil Hideaway, room
  54622) and `put all component in box` (the huge glowing box in that entry room, not gsort's Office box), then
  `go jugg_upgrade`. Hardcore can't craft, so fragments/essences/hearts go to the house. Player level comes from
  `gs`, `score` or a level-up line (`my[jugg][plevel]`); unknown after a reload until one of those shows.
- `juggernaut_train.tin`, strategy `autotrain`: after a kill (at most every `jugg_train_every` = 300 s) sends `gs2`
  (hidden), trains the lowest cost x weight skill from `jugg_train_skills` it can afford, re-reads `gs2`, repeats until
  the best pick is unaffordable (it saves for it). Weights: DFA 1, jump jet 1, punch 2, kick 2, heat management 3.
  Add later: `#var {jugg_train_skills[transpose]} 1` at glvl ~50, `#var {jugg_train_skills[critical hit]} 1` at Gnome ~55.
  Hides gs2 with a temporary `#action {%*}` (priority 9) between the header and the `'---'` footer.
- `chars/again/aliases.tin`: goal is a high combat % (karvec). A 10 s ticker (`again_ld`, always on) runs `ld` once
  Again has been out of combat `again_ld_after` = 300 s in a row AND nothing has been typed for `again_ld_idle` = 300 s
  (`$idle`). Combat and a running guild trip reset the count. Deadman stays high (~4 h); it is not involved.
- Deadman: autoadvance, autotrain and autoglevel never start while idle ($idle_flag). A running stat/skill chain stops
  at its next step. A guild trip that is under way finishes its upgrades and purchases, then stays at the guild with
  the bot paused (no walk back, no resume); the out-of-combat `ld` then drops it there after 5 min.
- Run state lives in `jugg[...]` (not `my[jugg]`): `my` is saved by `ld` and restored at login, which brought back a
  half-finished trip (`state walking`) and blocked autoglevel for good (2026-10-26, 1000%+ gxp). juggernaut.tin
  unvars any old `my[jugg]`. Nothing in `jugg` survives a relog; `gs` refills player level, suit and suit glvl.
- Trip routes skip rooms named in `jugg_trip_avoid` (`%*Revelwood%*`: the route from Central Plains 3711 climbed into
  Revelwood and its guards attacked). Avoid flags go on just before each `go`/`#map run` and off right after, so they
  never reach the shared map file.
- `juggernaut_info.tin`: `jinfo` crawls every guild info file into the session log; `jinfo more {a;b;c}` reads a list.

Live checks still open: the dropship walk, a second upgrade in a row, whether levelling past 19 is wanted,
the "not enough gxp" message for `upgrade` (unknown).
At level 30+: that `put all component in box` works on the huge box (else try `put all component in huge box`).

## Game facts

- Cost table: `rcost` (karvec's mud alias `cost`). Stat raise prints "Your <Stat> is now N, the next point will cost X XP."
  Stat spending raises the xp needed for the next level (shared pool). Stats capped per level.
- Level-up lines: "Well done! You are now Again, level N.", "Welcome to your new level Again, level N.",
  "Very well done Again, level N."
- Glevel: `upgrade` in room 1028 (Sub-1, via the dropship `board` exits). Success: "You are awarded N credits for
  honoring your clan." Credits per upgrade = 77 + 8 x new glvl (seen 2-7); cumulative to glvl N ~ 4N^2 + 81N - 85.
- gxp % is `$gxp` from the MIP gline (can exceed 100). Gxp comes from firing mounts.
- Credits are per suit; trainable skills (gs2) are shared across suits and earned every combat round.
  Skill rank cost is per skill and steep (rank 1 = 74, rank 6 = 1884).
- Weapon damage capped by glvl: +1 weapon level per 10 glvls (level 7 full at 60).
- Clan at glvl 20 in Elemental; required before switching suits. Clans get all powers (own at 20, then 50, 75).
- Elemental: reinforce slots at glvl 1, 50; mount points at 1, 50, 100. Tech caps: IS 15, BA 5, heat cap 7,
  heat sinks 6, PD 3, salvage 3, stim eff 4, stim regen 3, truck 5, weapons 7, TC/MG 6, ammo 4, plasma 7.
- Tech costs (`info tech costs`): IS 50 then 80/level step (160, 240, ...); BA 50/200/300/400/500;
  heat cap and heat sinks 50/200/300/...; PD 50/150/225; salvage 80/600/900; stim eff 80/600/900/1200;
  stim regen 60/1000/1500; truck 100/800/1200/1600/2000; weapons 0/500/750/1000/1250/1500/1750;
  TC/MG 70/600/900/1200/1500/1800; plasma 75/170/340/400/530/660/800; ammo 200/500/900/1350.
- Info files: full text in logs/karvec/sessions/again_2026-10-26.log, `jinfo` runs at ~146694-149132 and ~149146-150685.
- Rules: 5 min idle in combat stops gxp; 20 min idle shuts the heartbeat off. Rule 11: botting illegal.

## Long-term plan (2026-10-26): Elemental to glvl 20, then Gnome

karvec: going Gnome as soon as Elemental hits glvl 20 ("longevity/gnome").

### Elemental, glvl 7 to 20 (only job: reach 20 fast and alive)
- Credits stay with Elemental after the switch, so spend them all on things that help now.
- Get a mount first: `purchase energy weapons` (level 1 free) at the tech bay, `buy energy 1 l` in the weapons room
  (station level 1), check `gs3`. Gxp comes from firing it. The "Click. out of ammunition" spam is the wielded plasma rifle.
- Then: BA 1-2, TC 1, heat sinks 1, energy 2 at glvl 10, IS 4-6, stim eff 1. Skip plasma, salvage 2+, truck, ammo.

### Clan at 20 (needed before the suit switch)
- Clan trial (info 2.3): sponsor from the clan, `enter arena` from the visitors platform shuttle, hunt mech infantry
  squads, 90 min limit. "The combat involved in all the trials is real, and CAN KILL YOU." Hardcore: go in full,
  kennel any dog, be ready to leave.
- Wolf gets support (mech) at 20, Bear/Falcon only at 75 (Ludacris). Frenzy (Bear) adds physical damage and damage
  reduction; airdrop (Falcon) heals. All clans get all three powers by 75; powers run at your highest suit's glvl.

### Gnome (own credits from its glvl 2; mount only at 60)
- Suit: 4 reinforce slots (glvl 1, 25, 50, 75), mount at 60, overmax enhance, EB conversion (non-physical damage turns
  into edged/blunt), hard to solo for lack of damage. Gnome gxp comes from being hit (rule 13 mentions it).
- Tech order (guild notes + Ludacris): BA 1-2 (edged/blunt, which EB conversion turns most damage into), stim eff,
  IS (key), stim regen, salvage efficiency (4 reinforce slots). Point defense 1-3 (small laser + flamethrower) is cheap
  damage. Truck 4 stores/transfers stim, truck 5 does damage. Weapon techs, TC and plasma wait until ~55-60;
  Ludacris says the Gnome mount grows with glvl instead of weapon tech, so check `gview gnome` / `rtech` then.
- Gnome caps in gs2 are still unknown (Elemental's: IS 15, BA 5); check `gs2` after the switch.

### Gnome tuning in the scripts (2026-10-26)
- Gnome caps (gs2): IS 22, BA 8, stim eff 8, stim regen 5, salvage 5, truck 5, heat cap 2, heat sinks 2,
  point defense 1, plasma 1, ammo 3, all weapon techs and TC/MG 0 (MAX). Gnome glvl 2 paid 83 credits (Elemental 93).
- `jugg_tech_plan[gnome]` follows those caps: BA 2, IS 3, stim eff 1, IS 5, stim regen 1, salvage 1, PD 1, IS 8, ...
  truck 4 (stim store/transfer) mid-way, truck 5 (damage) and plasma 1 (truck pfocus) last.
  2026-11-04 (karvec: prioritize internal structure): after BA 4 the plan is `internal structure 22` first (one rank per
  purchase until 22, saving credits for it), then stim eff 4, stim regen 3, BA 5, ... as before minus the IS 15/18 steps.
  At the time: IS 12/22 (next 1040), BA 4/8, stim eff 3/8, stim regen 2/5, salvage 3/5, 636 credits.
- autotrain: DFA 1, punch 2, kick 2, jump jet 3 (Gnome wants damage; dodging also costs heat with 2/2 heat techs),
  heat management 3, transpose 1 from suit glvl 50, critical hit 1 from 55 (`jugg_train_from`).
- autoadvance: con 1, dex 2, str 2, int 5 (karvec 2026-10-29; 10 on 10-26, was 2 before that and soaked xp) with `jugg_adv_max` int 100 (int adds reinforce AC; 100 is enough).
- `overmax` and `eb` are Gnome toggles (each command flips them). Both ON since 2026-10-26: "Gnome overmax healing
  enabled.", "Gnome damage focusing enabled." (eb = EB conversion). Not automated.

### Skill points (shared by all suits, so they carry into Gnome)
- Damage: DFA, kick, punch. Ludacris went DFA 50, punch 25, kick 25; costs flatten around rank 65.
- Survival: jump jet until ~glvl 50, then transpose (usable at 60, "especially for defensive suits").
- Later: heat management (dissipate). Critical hit only matters with a mount (Gnome glvl 60). Defend last.
- Weights for cheapest-next-rank: DFA 1, jump jet 1, punch 2, kick 2, heat management 3, transpose from glvl 50,
  critical hit from Gnome glvl 55, defend never.

### Stats
- Gnome notes: focus con; str/wis raise damage; dex helps tanking a little; int adds AC when reinforcing (until capped);
  Ludacris: int 100 is enough. Current autoadvance weights con 1, dex 2, str 2, int 5.

## Stacking mobs for Gnome gxp (2026-10-27)

- Gnome gxp comes from being hit, so more attackers = more gxp. `botstack 6` then `+aegis` (shared code in
  common/bot/generic.tin + bots.tin, uncommitted; details and live-check list in notes/outstanding.md). Walks past
  targets, fights after 6 passed or before an elevator `d`/`u`, waits for hunters at each hold. `botstack off` after.
- Aegis facts from the 10-27 runs: zombies and sentries attack on sight ("X attacking you!") and hunt ("You are now
  hunted by ...", "X arrives hunting Again."). On level 4 they caught up within seconds of a hold; on level 3 three
  passed mobs never caught up over ~10 rooms. Paths go into dead ends and back, so the count is per map room.
- The old bots/old/aegis-stack.tin rotated `kill zombie 1/2/3` on tickers to keep several alive: that's what rule 13
  bans. Pull a crowd, then kill normally.
- Other stacking areas Cable suggested in clan (10-27): dark priests, land2.

## Reflect gear and Knight Training (from the wmt mirror, 2026-10-26)
- ROLM Orrery rune: ~9 rounds of reflecting all damage dealt to you back at the attacker, 1 charge, rod must be
  wielded. The shared rod has orrery unlocked (vars/boot.tin, 178 charges); gsort has it on ser (fated, lvl 62).
  Whether a level-62 item and a shared fated item work for a hardcore character: unknown.
- Celestial Zodiacs ring (Desecrator of Ptah, psychic): 1% per hit received to reflect part of the damage as energy.
  The FIRST ring worn is attuned and no second ring can be worn, so don't wear a low one. Known adjectives by scaler:
  vicious 85, horrific 125, apocalyptic 140, malevolent 150 (scaler range is 75% of level to level+5).
  Stones (swappable, one at a time; drop on Zodiac dungeon levels): amethyst (Asura of Ganesha, L2) stun/slow;
  tiger's eye (Rotseer of Willow, L3) +4 attack speed; malachite (Deceiver of Al-Nasr, L4) poison cloud on ALL mobs;
  opal (Heretic of the Elephant, L5) electric dmg; jade (Bloodseer of Ixchel, L6) +75 all resists @70, +250 @150;
  obsidian (Skinwalker of the Salmon, L7) energy dmg; rose quartz (Warlord of the Monkey, L8) twist regen 2%/4% HP,
  tap heal ~15%/30% HP (tap only with twist off); turquoise (Blackguard of Scorpio, L9) frost damage barrier.
  Pick for a hardcore Gnome: rose quartz main, jade for heavy magic. Malachite pulls every mob in the room: more
  attackers = more Gnome gxp and it's legal (rule 13 only bans retargeting to keep a mob alive and hitting you),
  but only where Again can tank the whole room.
- Easter invasion Eggshell set (9 pieces, event drop): shield reflects all damage only with the full set worn.
- Knight Training Arena (Order of the Lost Knights, by Revelation): NOT scaling, 2 h dungeon timer, rep-based, one
  `challenge` per knight at each Challenge Board (`abandon` costs rep), knights identify as 'elf'. Classes:
  stage 1 137k-1M (5-10 reps), stage 2 724k-5.4M, stage 3 4.1M-24.6M, stage 4 12.5M-58.6M, stage 5 15.8M-60.4M,
  stage 6 25M-112.8M, stage 7 102.6M (250 reps). Grand Master (5,000+ rep, once per boot) teaches sword, punch,
  shield, evasion for the MK gear specials. From Fantasy: portal, 12n, leave, 4n, 8w, enter, 3s, (search grass),
  squeeze through, s, sw, se, 2s, 3e, se. No 3kdb bot or speedrun for it.
  Update 2026-10-31: `+knights` runs it from Larry (28795, speedrun `erah_knight`) and turns in Lifelong
  Training missions itself. For Again set `#var knights_maxstage N` first: the bot stops before stage N+1, walks back
  through the cleared rooms and stops at Larry. Entering a room whose board has challengers commits Again to all of
  them (leaving = `abandon challenge`, -100 rep), so N = the last stage Again can tank every knight of.
