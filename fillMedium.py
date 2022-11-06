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


def initItemLists() -> ItemLists:
    earlyItemList = [Missile,
                     Morph,
                     GravityBoots]
    lowPowerList = [Super,
                    Speedball,
                    Bombs,
                    HiJump,
                    GravitySuit,
                    DarkVisor,
                    Wave,
                    SpeedBooster,
                    SpaceJump,
                    Charge,
                    Energy, Energy, Energy, Energy, Energy]
    highPowerList = [Grapple,
                     PowerBomb,
                     Varia,
                     Ice,
                     MetroidSuit,
                     Screw,
                     Spazer,
                     Plasma,
                     Hypercharge]
    extraItemList = [Xray,
                     DamageAmp, DamageAmp, DamageAmp,
                     DamageAmp, DamageAmp, DamageAmp,
                     ChargeAmp, ChargeAmp, ChargeAmp,
                     ChargeAmp, ChargeAmp, ChargeAmp,
                     Refuel, Refuel, Refuel, Refuel, Refuel, Refuel, Refuel,
                     Energy, Energy, Energy, Energy,
                     Energy, Energy, Energy, Energy, Energy,
                     Energy, Energy, Energy, Energy,
                     SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
                     SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost, SpaceJumpBoost,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
                     SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo, SmallAmmo,
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
                     LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo, LargeAmmo,
                     LargeAmmo, LargeAmmo, LargeAmmo]
    return earlyItemList, lowPowerList, highPowerList, extraItemList


def placementAlg(availableLocations: list[Location],
                 locArray: list[Location],
                 loadout: list[Item],
                 itemLists: ItemLists) -> Optional[tuple[Location, Item]]:
    earlyItemList, lowPowerList, highPowerList, extraItemList = itemLists

    assert len(availableLocations), "placement algorithm received 0 available locations"

    from_items = (
        earlyItemList if len(earlyItemList) else (
            lowPowerList if len(lowPowerList) else (
                highPowerList if len(highPowerList) else (
                    extraItemList
                )
            )
        )
    )

    assert len(from_items), "placement algorithm received 0 items"

    return random.choice(availableLocations), random.choice(from_items)
