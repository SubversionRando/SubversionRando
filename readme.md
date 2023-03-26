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

For example, Speed Booster cannot be at the vanilla Speed Booster location, because it requires Speed Booster to get out.

If you can't get out of a location, you shouldn't go in, because you might be soft-locked.

Common pitfalls:
  - Open the pink door left of Sediment Floor before falling into Eddy Channel. (Otherwise, it might require Supers.)
     - Also think about how to get out of Eddy Channel. (Do you need Speed Ball? Aqua Suit?)
  - Fire's Bane Shrine requires Ice Beam, or Charge and HyperCharge.
  - The bottom of Magma Chamber requires Power Bombs.
  - Shrine Of The Penumbra (behind Kraid) requires Dark Visor or Power Bombs.
  - Going through Magma Pump (in either direction) is not in logic unless you can open the plasma + wave gate.
  - Hot Spring requires a morph jump underwater in a 2-tile space (Speed Ball, or Aqua Suit and bombing).
  - Archives requires Speed Ball or advanced tricks.

Also, the logic assumes you pick up everything you can from the space port before falling from the space port.
So if you don't pick up everything you can before you free fall, you might be stuck.

Turning the power off is never in logic, unless you can turn it back on before you leave the Geothermal Energy Plant.

---

## Casual logic requirements

In casual logic (with no logic tricks), you might be required to:
  - wall-jump
  - mid-air morph in a space that is 5 tiles high
  - 1-tap short charge
     - This just means press the d-pad to start moving before pressing the dash button.
  <!-- there isn't a trick for this, but it will never be required in casual, because it's always combined with some other trick
  - underwater wall jump in a space 1-tile wide
     - If you just hold the d-pad left or right and repeatedly press jump, you'll get to the top of a space that is 1 tile wide. -->

---

## notes on options

Casual logic notes: -c
Casual logic is meant to mimic the "intended" experience of Subversion, with its few moments of suitless underwater movement, no hellruns, and no glitches in logic.

Medium logic notes: -u
A logic level between Casual and Expert, including a few common tricks.

Expert logic notes: -e
Notable tricks in expert logic include p-shooter-only gate glitches, single springball jumps, hellruns, and super-sink. Once you have 5 E-tanks, most hellruns are in logic.


Major/Minor Bias fill notes: -b
Unique item locations are more likely to have unique items, but it's not 100%. This is only unique items, and not energy tanks.
The hint system is modified in this mode to try to hint a minor location.

Major/Minor fill notes: -mm
Places Unique+Energy items at the Unique+Energy locations. 23 unique and 16 energy locations in all. While this puts the hard-to-reach unique locations into the major pool, energy tanks seem to be sprinkled around, making this option a nice balance of hard-to-reach items and available energy locations. Note that Refuel tanks, damage amps, accel charge, and space jump boosts are all in the minor pool.


Area Rando notes: -a
Logically shuffles the major areas of the game and places items in logical places according to the door placement.
This is unlikely to work when combined with casual logic and major/minor fill.

---

## hints

Somewhere in the bestiary of the log book, there's a hint for the location of an important item.
(In order to see the bestiary text, you have to kill the boss.)

The 10 bestiary entries are: Torizo, Spore Spawn, Kraid, Crocomire, Phantoon, Botwoon, Draygon, Ridley, Metroids, Aurora Unit

note: The Metroids entry is triggered by picking up the item in extract storage, and it only works if the space port is not crashed yet.
