# SubversionRando

contact randorandy (ironrusty) or strotlog or beauxq (buxnq) with questions

---

## setup / install

1. install Python from [https://www.python.org/](https://www.python.org/)
   - requires Python 3.9 or higher

2. download the code from this page
   1. green "Code" button in the top right portion of this page
   2. "Download ZIP"
   3. unzip it to a folder on your hard drive

3. put your Subversion 1.2 rom in the `roms` directory with this filename: `Subversion12.sfc`

---

## generate from gui

run `gui.py`

---

## generate from command line

run `Main.py` in console

optionally, command line arguments are available:
```
 -h   : Help

 -c   : Casual logic (Default)
 -i   : Medium logic
 -e   : Expert logic

 -d   : Assumed fill (Default)
 -s   : Speedrun fill
 -m   : Medium fill
 -mm  : Major/Minor fill (not compatible with area rando)

 -a   : Area Rando

 -o   : Smaller Spaceport
```

This should create a randomized rom with the given name in the roms folder and a spoiler log (.txt) in the spoilers folder.

---

## logic notes

All the logic is symmetrical. This means getting out is required to go in.

For example, Speed Ball cannot be at the vanilla Speed Ball location in the Archives, because it requires Speed Ball to get out.

If you can't get out of a location, you shouldn't go in, because you might be soft-locked.

Common pitfalls:
  - Open the pink door left of Sediment Floor before falling into Eddy Channel. (Otherwise, it might require Supers.)
     - Also think about how to get out of Eddy Channel. (Do you need Speed Ball? Aqua Suit?)
  - Fire's Bane Shrine requires Ice Beam, or Charge and HyperCharge.
  - The bottom of Magma Chamber requires Power Bombs.
  - Shrine Of The Penumbra (behind Kraid) requires Dark Visor or Power Bombs.
  - Going through Magma Pump (in either direction) is not in logic unless you can open the plasma + wave gate.
  - Hot Spring requires a morph jump underwater in a 2-tile space (Speed Ball, or Aqua Suit and bombing).
  - Archives requires Speed Ball.

Also, the logic assumes you pick up everything you can from the space port before falling from the space port.
So if you don't pick up everything you can before you free fall, you might be stuck.

Turning the power off is never in logic, unless you can turn it back on before you leave the Geothermal Energy Plant.

---

## notes on options

Casual logic notes: -c
Casual logic is meant to mimic the "intended" experience of Subversion, with its few moments of suitless underwater movement, no hellruns, and no "gate glitches" in logic. Logic regarding the shutdown, and Suzi is overly cautious so I would be surprised to find any progress there.

Medium logic notes: -u
A logic level between Casual and Expert, including a few common tricks.

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

---

## hints

Somewhere in the bestiary of the log book, there's a hint for the location of an important item.
(In order to see the bestiary text, you have to kill the boss.)

The 10 bestiary entries are: Torizo, Spore Spawn, Kraid, Crocomire, Phantoon, Botwoon, Draygon, Ridley, Metroids, Aurora Unit

note: The Metroids entry is triggered by picking up the item in extract storage, and it only works if the space port is not crashed yet.
