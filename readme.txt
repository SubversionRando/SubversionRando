README

contact randorandy (ironrusty) or strotlog with questions

simple readme for now

1.download this repository
2.place a copy of the Subversion 1.2 rom in the roms folder - it must be named Subversion12.sfc
3.run Main.py in console
4. optionally, command line arguments are available:
 -h Help
 -c Casual Logic (Default)
 -e Expert logic
 -s Speedrun fill (Default)
 -m Medium fill

This should create a randomized rom with the given name in the roms folder and a spoiler log (.txt) in the spoilers folder.

Note: keep the outer folder named SubversionRando for everything to work as intended

Casual logic notes:
For now, casual logic is the only one published. More are possible and coming eventually. You could update the logicCasual file if you want a different experience. Casual logic is meant to mimic the "intended" experience of Subversion, with its few moments of suitless underwater movement, no hellruns, and no "gate glitches" in logic. Logic regarding the shutdown, space port, and Suzi is overly cautious so I would be surprised to find any progress there besides Torpedo Bay. In casual, Torpedo Bay (the vanilla missile) will always have morph or missile as your intended escape from the space port, then the very next pack of items that will be placed are Missile, Morph, and GravityBoots. If you are looking into the code, see the earlyItemList.

Expert logic notes:
Notable tricks in expert logic include p-shooter-only gate glitches, single springball jumps, and hellruns. Once you have 5 E-tanks, most hellruns are in logic. Items and areas in lava require Metroid Suit.

Speedrun fill notes:
This mostly works like the speedrun fill of varia.run, as I understand it. After the initial placement of Missile, Morph, and Gravity Boots, all progression items are put into a progression pool and placed into any available location. This often puts powerful items "on the way" to your goal and makes for a speedy experience. Fun!

Medium fill notes:
To make for a more layered logical experience, the progression items are placed into a low-power and high-power pool. Most often, this gives you a few progression items early that open up other areas which may have more high-power items to beat the game. This leads to a slower, more calculated experience.