README

contact randorandy (ironrusty) or strotlog with questions

simple readme for now

1.download this repository
2.place a copy of the Subversion 1.2 rom in the roms folder - it must be named Subversion12.sfc
3.run Main.py in console
4. optionally, command line arguments are available:
 -h   : Help
 -c   : Casual Logic (Default)
 -e   : Expert logic
 -s   : Speedrun fill (Default)
 -m   : Medium fill
 -d   : Assumed fill
 -a   : Area Rando

This should create a randomized rom with the given name in the roms folder and a spoiler log (.txt) in the spoilers folder.

Casual logic notes: -c
For now, casual logic is the only one published. More are possible and coming eventually. You could update the logicCasual file if you want a different experience. Casual logic is meant to mimic the "intended" experience of Subversion, with its few moments of suitless underwater movement, no hellruns, and no "gate glitches" in logic. Logic regarding the shutdown, space port, and Suzi is overly cautious so I would be surprised to find any progress there besides Torpedo Bay. In casual, Torpedo Bay (the vanilla missile) will always have morph or missile as your intended escape from the space port, then the very next pack of items that will be placed are Missile, Morph, and GravityBoots. If you are looking into the code, see the earlyItemList.

Expert logic notes: -e
Notable tricks in expert logic include p-shooter-only gate glitches, single springball jumps, and hellruns. Once you have 5 E-tanks, most hellruns are in logic. Items and areas in lava require Metroid Suit.

Speedrun fill notes: -s
This mostly works like the speedrun fill of varia.run, as I understand it. After the initial placement of Missile, Morph, and Gravity Boots, all progression items are put into a progression pool and placed into any available location. This often puts powerful items "on the way" to your goal and makes for a speedy experience. Fun!

Medium fill notes: -m
To make for a more layered logical experience, the progression items are placed into a low-power and high-power pool. Most often, this gives you a few progression items early that open up other areas which may have more high-power items to beat the game. This leads to a slower, more calculated experience.

Major/Minor fill notes: -mm
Compatible with casual/expert/etc logic and places Unique+Energy items at the Unique+Energy locations. 23 unique and 16 energy locations in all. While this puts the hard-to-reach unique locations into the major pool, energy tanks seem to be sprinkled around, making this option a nice balance of hard-to-reach items and available energy locations. Note that Refuel tanks, damage amps, accel charge, and space jump boosts are all in the minor pool.

Area Rando notes: -a
Logically shuffles the major areas of the game and places items in logical places according to the door placement. Also creates a "logical" escape due to some map changes that happen during the final escape. (Warning: the elevator out of Sky Temple is bugged during the escape, so do NOT use it!) For now, this logic does not account for turning the power on/off to collect items. Now compatible with casual or expert logic, and speedrun or medium fill. Not currently compatible with major-minor.
