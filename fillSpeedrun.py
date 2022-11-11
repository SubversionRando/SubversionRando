from typing import Optional
import random

from fillInterface import ItemLists
from item_data import Item, items_unpackable
from location_data import Location

# this will not update any of the parameters it is given
# but it will return an item to place at a location


(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable

# itemLists should contain
# [0] earlyItemList
# [1] progressionItemList
# [2] extraItemList


def initItemLists() -> ItemLists:
    earlyItemList = [Missile,
                     Morph,
                     GravityBoots]
    progressionItemList = [Super,
                           Grapple,
                           PowerBomb,
                           Speedball,
                           Bombs,
                           HiJump,
                           GravitySuit,
                           DarkVisor,
                           Wave,
                           SpeedBooster,
                           Spazer,
                           Varia,
                           Ice,
                           MetroidSuit,
                           Plasma,
                           Screw,
                           SpaceJump,
                           Charge,
                           Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy]
    extraItemList = [Hypercharge,
                     Xray,
                     DamageAmp, DamageAmp, DamageAmp, DamageAmp, DamageAmp, DamageAmp,
                     ChargeAmp, ChargeAmp, ChargeAmp, ChargeAmp, ChargeAmp, ChargeAmp,
                     Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy, Energy,
                     Refuel, Refuel, Refuel, Refuel, Refuel, Refuel, Refuel,
                     SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
                     SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo,
                     LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
                     LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
                     LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
                     LargeAmmo, LargeAmmo, LargeAmmo]
    unused: list[Item] = []
    return earlyItemList, progressionItemList, extraItemList, unused


def placementAlg(availableLocations: list[Location],
                 locArray: list[Location],
                 loadout: list[Item],
                 itemLists: ItemLists) -> Optional[tuple[Location, Item]]:
    assert len(availableLocations), "placement algorithm received 0 available locations"

    earlyItemList, progressionItemList, extraItemList, _ = itemLists

    if availableLocations[0]['fullitemname'] == "TORPEDO BAY":
        return availableLocations[0], random.choice([Missile, Morph])

    from_items = (
        earlyItemList if len(earlyItemList) else (
            progressionItemList if len(progressionItemList) else (
                extraItemList
            )
        )
    )

    assert len(from_items), "placement algorithm received 0 items"

    return random.choice(availableLocations), random.choice(from_items)
