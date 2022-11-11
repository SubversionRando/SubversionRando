from item_data import Item, items_unpackable
from location_data import Location

CraterR = ('1c678', '5BBB00056E06060000800000', 'Early', 'CraterR', 0)
SunkenNestL = ('1c7a4', '2CBA00040106000000800000', 'Early', 'SunkenNestL', 0)
RuinedConcourseBL = ('1caf8', 'C2970004115601050080CCA9', 'Early', 'RuinedConcourseBL', 1)
RuinedConcourseTR = ('1cbc4', 'C29700051E0601000080B6A9', 'Early', 'RuinedConcourseTR', 1)
CausewayR = ('1a1e4', '2FA300013E06030000800000', 'Early', 'CausewayR', 1)
SporeFieldTR = ('1c8c4', '578800052E06020000800000', 'Early', 'SporeFieldTR', 1)
SporeFieldBR = ('1a2ec', '578800053E4603040080E4A6', 'Early', 'SporeFieldBR', 1)
OceanShoreR = ('1ca74', '0F8500057E26070200800000', 'SandLand', 'OceanShoreR', 0)
EleToTurbidPassageR = ('1c15c', '73CC00050E26000200800000', 'SandLand', 'EleToTurbidPassageR', 2)
PileAnchorL = ('1c66c', '879F00040116000100800000', 'Sandland', 'PileAnchorL', 0)
ExcavationSiteL = ('1a130', '19EC00000206000000800000', 'PirateLab', 'ExcavationSiteL', 1)
WestCorridorR = ('1bed4', 'B7E100050E16000100800000', 'PirateLab', 'WestCorridorR', 3)
FoyerR = ('197c4', 'CD8A00051E06010000800000', 'PirateLab', 'FoyerR', 3)
ConstructionSiteL = ('1c900', 'EB9E00040136000300800000', 'PirateLab', 'ConstructionSiteL', 1)
AlluringCenoteR = ('194b8', '3CBF00056E06060000800000', 'PirateLab', 'AlluringCenoteR', 3)
FieldAccessL = ('1a454', '71A000040106000000800000', 'ServiceSector', 'FieldAccessL', 1)
TransferStationR = ('1a0f4', 'B89B00051E06010000800000', 'ServiceSector', 'TransferStationR', 1)
CellarR = ('1c8f4', '3A8100052E06020000800000', 'ServiceSector', 'CellarR', 1)
SubbasementFissureL = ('1c864', 'CC9300040126000200800000', 'ServiceSector', 'SubbasementFissureL', 1)
WestTerminalAccessL = ('1c6e4', 'C78100040126000200800000', 'SkyWorld', 'WestTerminalAccessL', 0)
MezzanineConcourseL = ('1a4f0', '93A200040146000400800000', 'SkyWorld', 'MezzanineConcourseL', 1)
VulnarCanyonL = ('19788', '598B00044166040600800000', 'SkyWorld', 'VulnarCanyonL', 3)
CanyonPassageR = ('195d8', '9F8B00012E06020000800000', 'SkyWorld', 'CanyonPassageR', 3)
ElevatorToCondenserL = ('1c2f4', 'BAED00040136000300800000', 'SkyWorld', 'ElevatorToCondenserL', 2)
LoadingDockSecurityAreaL = ('1bf4c', '8B9000040216000120010000', 'SpacePort', 'LoadingDockSecurityAreaL', 3)
ElevatorToWellspringL = ('1cb7c', '36CD00040126000200800000', 'LifeTemple', 'ElevatorToWellspringL', 2)
NorakBrookL = ('1965c', 'E58B00000126000200800000', 'LifeTemple', 'NorakBrookL', 3)
NorakPerimeterTR = ('1a0b8', '6F8900051E06010000800000', 'LifeTemple', 'NorakPerimeterTR', 3)
NorakPerimeterBL = ('1bad8', '6F890004012600020080ACA7', 'LifeTemple', 'NorakPerimeterBL', 3)
VulnarDepthsElevatorEL = ('1c87c', 'A9A100040106000000800000', 'FireHive', 'VulnarDepthsElevatorEL', 1)
VulnarDepthsElevatorER = ('1c888', 'A9A100050E06000000800000', 'FireHive', 'VulnarDepthsElevatorER', 1)
HiveBurrowL = ('1bd84', 'E5D500040146000400800000', 'FireHive', 'HiveBurrowL', 2)
SequesteredInfernoL = ('1c4b0', '84F300040116000100800000', 'FireHive', 'SequesteredInfernoL', 2)
CollapsedPassageR = ('1cb04', '89CB00051E06010000800000', 'FireHive', 'CollapsedPassageR', 2)
MagmaPumpL = ('1c2e8', 'A0BE00040106000000800000', 'Geothermal', 'MagmaPumpL', 2)
ReservoirMaintenanceTunnelR = ('1c414', 'B0F100051E160101008020A6', 'Geothermal', 'ReservoirMaintenanceTunnelR', 2)
IntakePumpR = ('1c4c8', '0FF300052E06020000800000', 'Geothermal', 'IntakePumpR', 2)
ThermalReservoir1R = ('1cbac', 'F09C00055E06050000800000', 'Geothermal', 'ThermalReservoir1R', 2)
GeneratorAccessTunnelL = ('1c1b0', 'F4CF00043106030000800000', 'Geothermal', 'GeneratorAccessTunnelL', 2)
ElevatorToMagmaLakeR = ('1c0fc', '67EF00050E06000000800000', 'DrayLand', 'ElevatorToMagmaLakeR', 2)
MagmaPumpAccessR = ('1c2b8', 'E99700050E06000000800000', 'DrayLand', 'MagmaPumpAccessR', 2)
FieryGalleryL = ('1c174', 'D7CB00040116000100800000', 'Verdite', 'FieryGalleryL', 2)
RagingPitL = ('1c12c', '2FEE00040116000100800000', 'Verdite', 'RagingPitL', 2)
HollowChamberR = ('1c108', '1BD000051E06010000800000', 'Verdite', 'HollowChamberR', 2)
PlacidPoolR = ('1c8a0', 'CBA300051E06010000800000', 'Verdite', 'PlacidPoolR', 1)
SporousNookL = ('1a340', 'A59300040106000000800000', 'Verdite', 'SporousNookL', 1)
RockyRidgeTrailL = ('1bac0', 'E38800040116000100800000', 'Daphne', 'RockyRidgeTrailL', 3)
TramToSuziIslandR = ('1c7ec', '23A000050E06000000800000', 'Suzi', 'TramToSuziIslandR', 0)

# Casual logic updater
# updates unusedLocations

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable

def otherDoor(door,Connections) :
    for pair in Connections :
        if (door in pair) :
            other = pair[0]
            if door == other :
                other = pair[1]
    return other

def updateAreaLogic(availableLocations, locArray, loadout, Connections) :
    exitSpacePort = True
    jumpAble = exitSpacePort and (GravityBoots in loadout)
    underwater = jumpAble and ((HiJump in loadout) or (GravitySuit in loadout))
    pinkDoor = (Missile in loadout) or (Super in loadout)
    vulnar = jumpAble and pinkDoor
    canUseBombs = (Morph in loadout) and ((Bombs in loadout) or (PowerBomb in loadout))
    canUsePB = (Morph in loadout) and (PowerBomb in loadout)
    canFly = canUseBombs or (SpaceJump in loadout)
    wave = (Wave in loadout) or ((Charge in loadout) and (Hypercharge in loadout))
    breakIce = (Plasma in loadout) or ((Charge in loadout) and (Hypercharge in loadout))
    icePod = ((Ice in loadout) and pinkDoor) or ((Charge in loadout) and (Hypercharge in loadout))
    energyCount=0
    for item in loadout :
        if item == Energy :
            energyCount += 1
    movement = False #check if loadout keeps increasing
    while movement == False :
        tempLoadout = []
        tempLoadout.extend(loadout)
        if (SunkenNestL not in loadout) :
            other=otherDoor(SunkenNestL,Connections)
            loadout.append(SunkenNestL)
            loadout.append(other)
        if (CraterR not in loadout) :
            other=otherDoor(CraterR,Connections)
            if canFly and canUsePB :
                loadout.append(CraterR)
                loadout.append(other)
        if (RuinedConcourseBL not in loadout) :
            other=otherDoor(RuinedConcourseBL,Connections)
            if (other in loadout) :
                loadout.append(RuinedConcourseBL)
            elif (
                jumpAble and
                (Missile in loadout) and
                canUseBombs
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (RuinedConcourseTR in loadout) and (
                jumpAble and
                (Morph in loadout) and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (CausewayR in loadout) and (
                jumpAble and
                canUseBombs and
                ((SpeedBooster in loadout) or
                 (Speedball in loadout) or
                 ((GravitySuit in loadout) and
                  wave))
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (SporeFieldTR in loadout) and (
                jumpAble and
                canUseBombs
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (SporeFieldBR in loadout) and (
                jumpAble and
                wave and
                canUseBombs
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
        if (RuinedConcourseTR not in loadout) :
            other=otherDoor(RuinedConcourseTR,Connections)
            if (other in loadout) :
                loadout.append(RuinedConcourseTR)
            elif (vulnar and
                  canUseBombs and
                  (SpeedBooster in loadout)
                  ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (RuinedConcourseBL in loadout) and (
                jumpAble and
                (Morph in loadout) and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (CausewayR in loadout) and (
                jumpAble and
                canUseBombs and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (SporeFieldTR in loadout) and (
                jumpAble and
                canUseBombs and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (SporeFieldBR in loadout) and (
                jumpAble and
                canUseBombs and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
        if (CausewayR not in loadout) :
            other=otherDoor(CausewayR,Connections)
            if (other in loadout) :
                loadout.append(CausewayR)
            elif (vulnar and
                  canUseBombs and
                  ((SpeedBooster in loadout) or
                   (Speedball in loadout) or
                   ((GravitySuit in loadout) and
                    wave))
                  ):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (RuinedConcourseBL in loadout) and (
                jumpAble and
                canUseBombs and
                ((SpeedBooster in loadout) or
                 (Speedball in loadout) or
                 ((GravitySuit in loadout) and
                  wave))
                ):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (RuinedConcourseTR in loadout) and (
                jumpAble and
                canUseBombs and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (SporeFieldTR in loadout) and (
                vulnar and
                ((SpeedBooster in loadout) or
                 (Speedball in loadout) or
                 ((GravitySuit in loadout) and
                  wave)) and
                canUseBombs
                ):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (SporeFieldBR in loadout) and (
                vulnar and
                ((SpeedBooster in loadout) or
                 (Speedball in loadout) or
                 ((GravitySuit in loadout) and
                  wave)) and
                canUseBombs and
                wave
                ):
                loadout.append(CausewayR)
                loadout.append(other)
        if (OceanShoreR not in loadout) :
            other=otherDoor(OceanShoreR,Connections)
            if (other in loadout) :
                loadout.append(OceanShoreR)
            elif (EleToTurbidPassageR in loadout) and (
                jumpAble and
                (Morph in loadout) and
                underwater and
                (Speedball in loadout) and
                (DarkVisor in loadout) and
                pinkDoor and
                (wave or
                 (Speedbooster in loadout) or
                 (Screw in loadout) or
                 ((Super in loadout) and
                  ((Speedball in loadout) or
                   canUsePB)))
                ):
                loadout.append(OceanShoreR)
                loadout.append(other)
            elif (PileAnchorL in loadout) and (
                jumpAble and
                (GravitySuit in loadout) and
                canUsePB and
                (Super in loadout) and
                (SpeedBooster in loadout) and
                (Grapple in loadout) and
                (DarkVisor in loadout)
                ):
                loadout.append(OceanShoreR)
                loadout.append(other)
        if (EleToTurbidPassageR not in loadout) :
            other=otherDoor(EleToTurbidPassageR,Connections)
            if (other in loadout) :
                loadout.append(EleToTurbidPassageR)
            elif (OceanShoreR in loadout) and (
                jumpAble and
                (Morph in loadout) and
                underwater and
                (Speedball in loadout) and
                (DarkVisor in loadout) and
                (Super in loadout)
                ):
                loadout.append(EleToTurbidPassageR)
                loadout.append(other)
            elif (PileAnchorL in loadout) and (
                jumpAble and
                (GravitySuit in loadout) and
                canUsePB and
                (Super in loadout) and
                (Grapple in loadout) and
                (DarkVisor in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout)
                ):
                loadout.append(EleToTurbidPassageR)
                loadout.append(other)
        if (PileAnchorL not in loadout) :
            other=otherDoor(EleToTurbidPassageR,Connections)
            if (other in loadout) :
                loadout.append(PileAnchorL)
            elif (OceanShoreR in loadout) and (
                jumpAble and
                (GravitySuit in loadout) and
                canUsePB and
                (Super in loadout) and
                (SpeedBooster in loadout) and
                (Grapple in loadout) and
                (DarkVisor in loadout)
                ):
                loadout.append(PileAnchorL)
                loadout.append(other)
            elif (EleToTurbidPassageR in loadout) and (
                jumpAble and
                (GravitySuit in loadout) and
                canUsePB and
                (Super in loadout) and
                (Grapple in loadout) and
                (DarkVisor in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout)
                ):
                loadout.append(PileAnchorL)
                loadout.append(other)
        if (ExcavationSiteL not in loadout) :
            other=otherDoor(ExcavationSiteL,Connections)
            if (other in loadout) :
                loadout.append(ExcavationSiteL)
            elif (WestCorridorR in loadout) and (
                jumpAble and
                (pinkDoor or
                 (Charge in loadout) or
                 (Ice in loadout) or
                 wave or
                 breakIce or
                 canUsePB or
                 (Spazer in loadout))
                ):
                loadout.append(ExcavationSiteL)
                loadout.append(other)
            elif (FoyerR in loadout) and (
                jumpAble and
                underwater and
                ((canUsePB and
                  wave and
                  (Bombs in loadout)) or
                 ((pinkDoor or
                   (Charge in loadout) or
                   (Ice in loadout) or
                   wave or
                   breakIce or
                   canUsePB or
                   (Spazer in loadout)) and
                  (Morph in loadout) and
                  (Screw in loadout)))
                ):
                loadout.append(ExcavationSiteL)
                loadout.append(other)
            elif (ConstructionSiteL in loadout) and (
                jumpAble and
                (canUsePB or
                 (underwater and
                  pinkDoor and
                  (Morph in loadout) and
                  (Screw in loadout) and
                  wave and
                  (Bombs in loadout)))
                ):
                loadout.append(ExcavationSiteL)
                loadout.append(other)
            elif (AlluringCenoteR in loadout) and (
                jumpAble and
                canUsePB and
                (Grapple in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout) and
                ((Screw in loadout) or
                 (MetroidSuit in loadout)) and
                ((wave and
                  (Bombs in loadout)) or
                 ((Screw in loadout) and
                  underwater))
                ):
                loadout.append(ExcavationSiteL)
                loadout.append(other)
        if (WestCorridorR not in loadout) :
            other=otherDoor(WestCorridorR,Connections)
            if (other in loadout) :
                loadout.append(WestCorridorR)
            elif (ExcavationSiteL in loadout) and (
                jumpAble and
                (pinkDoor or
                 (Charge in loadout) or
                 (Ice in loadout) or
                 wave or
                 breakIce or
                 canUsePB or
                 (Spazer in loadout))
                ):
                loadout.append(WestCorridorR)
                loadout.append(other)
            elif (FoyerR in loadout) and (
                jumpAble and
                ((canUsePB and
                  pinkDoor and
                  underwater and
                  wave and
                  (Bombs in loadout)) or
                 (underwater and
                  (Morph in loadout) and
                  (Screw in loadout)))
                ):
                loadout.append(WestCorridorR)
                loadout.append(other)
            elif (ConstructionSiteL in loadout) and (
                pinkDoor and
                jumpAble and
                (canUsePB or
                 (underwater and
                  (Morph in loadout) and
                  (Screw in loadout) and
                  wave and
                  (Bombs in loadout)))
                ):
                loadout.append(WestCorridorR)
                loadout.append(other)
            elif (AlluringCenoteR in loadout) and (
                jumpAble and
                canUsePB and
                (Grapple in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout) and
                ((Screw in loadout) or
                 (MetroidSuit in loadout)) and
                ((wave and
                  (Bombs in loadout)) or
                 ((Screw in loadout) and
                  underwater and
                  pinkDoor))
                ):
                loadout.append(WestCorridorR)
                loadout.append(other)
        if (FoyerR not in loadout) :
            other=otherDoor(FoyerR,Connections)
            if (other in loadout) :
                loadout.append(FoyerR)
            elif (ExcavationSiteL in loadout) and (
                jumpAble and
                underwater and
                ((canUsePB and
                  wave and
                  (Bombs in loadout)) or
                 ((pinkDoor or
                   (Charge in loadout) or
                   (Ice in loadout) or
                   wave or
                   breakIce or
                   canUsePB or
                   (Spazer in loadout)) and
                  (Morph in loadout) and
                  (Screw in loadout)))
                ):
                loadout.append(FoyerR)
                loadout.append(other)
            elif (WestCorridorR in loadout) and (
                jumpAble and
                ((canUsePB and
                  pinkDoor and
                  underwater and
                  wave and
                  (Bombs in loadout)) or
                 (underwater and
                  (Morph in loadout) and
                  (Screw in loadout)))
                ):
                loadout.append(FoyerR)
                loadout.append(other)
            elif (ConstructionSiteL in loadout) and (
                jumpAble and
                underwater and
                ((canUsePB and
                  (Screw in loadout) and
                  pinkDoor) or
                 ((Morph in loadout) and
                  wave and
                  (Bombs in loadout)))
                ):
                loadout.append(FoyerR)
                loadout.append(other)
            elif (AlluringCenoteR in loadout) and (
                jumpAble and
                canUsePB and
                (Grapple in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout) and
                ((Screw in loadout) or
                 (MetroidSuit in loadout))
                ):
                loadout.append(FoyerR)
                loadout.append(other)
        if (ConstructionSiteL not in loadout) :
            other=otherDoor(ConstructionSiteL,Connections)
            if (other in loadout) :
                loadout.append(ConstructionSiteL)
            elif (ExcavationSiteL in loadout) and (
                jumpAble and
                (canUsePB or
                 (underwater and
                  pinkDoor and
                  (Morph in loadout) and
                  (Screw in loadout) and
                  wave and
                  (Bombs in loadout)))
                ):
                loadout.append(ConstructionSiteL)
                loadout.append(other)
            elif (WestCorridorR in loadout) and (
                pinkDoor and
                jumpAble and
                (canUsePB or
                 (underwater and
                  (Morph in loadout) and
                  (Screw in loadout) and
                  wave and
                  (Bombs in loadout)))
                ):
                loadout.append(ConstructionSiteL)
                loadout.append(other)
            elif (FoyerR in loadout) and (
                jumpAble and
                underwater and
                ((canUsePB and
                  (Screw in loadout) and
                  pinkDoor) or
                 ((Morph in loadout) and
                  wave and
                  (Bombs in loadout)))
                ):
                loadout.append(ConstructionSiteL)
                loadout.append(other)
            elif (AlluringCenoteR in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                (Grapple in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout) and
                ((Screw in loadout) or
                 (MetroidSuit in loadout)) and
                ((wave and
                  (Bombs in loadout)) or
                 ((Screw in loadout) and
                  pinkDoor))
                ):
                loadout.append(ConstructionSiteL)
                loadout.append(other)
        if (AlluringCenoteR not in loadout) :
            other=otherDoor(AlluringCenoteR,Connections)
            if (other in loadout) :
                loadout.append(AlluringCenoteR)
            elif (ExcavationSiteL in loadout) and (
                jumpAble and
                canUsePB and
                (Grapple in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout) and
                ((Screw in loadout) or
                 (MetroidSuit in loadout)) and
                ((wave and
                  (Bombs in loadout)) or
                 ((Screw in loadout) and
                  underwater))
                ):
                loadout.append(AlluringCenoteR)
                loadout.append(other)
            elif (WestCorridorR in loadout) and (
                jumpAble and
                canUsePB and
                (Grapple in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout) and
                ((Screw in loadout) or
                 (MetroidSuit in loadout)) and
                ((wave and
                  (Bombs in loadout)) or
                 ((Screw in loadout) and
                  underwater and
                  pinkDoor))
                ):
                loadout.append(AlluringCenoteR)
                loadout.append(other)
            elif (FoyerR in loadout) and (
                jumpAble and
                canUsePB and
                (Grapple in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout) and
                ((Screw in loadout) or
                 (MetroidSuit in loadout))
                ):
                loadout.append(AlluringCenoteR)
                loadout.append(other)
            elif (ConstructionSiteL in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                (Grapple in loadout) and
                (SpeedBooster in loadout) and
                (Speedball in loadout) and
                ((Screw in loadout) or
                 (MetroidSuit in loadout)) and
                ((wave and
                  (Bombs in loadout)) or
                 ((Screw in loadout) and
                  pinkDoor))
                ):
                loadout.append(AlluringCenoteR)
                loadout.append(other)
        if (FieldAccessL not in loadout) :
            other=otherDoor(FieldAccessL,Connections)
            if (other in loadout) :
                loadout.append(FieldAccessL)
            elif (TransferStationR in loadout) and (
                jumpAble and
                pinkDoor and
                (DarkVisor in loadout) and
                wave and
                canUseBombs
                ):
                loadout.append(FieldAccessL)
                loadout.append(other)
            elif (CellarR in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUsePB and
                (DarkVisor in loadout) and
                wave
                ):
                loadout.append(FieldAccessL)
                loadout.append(other)
            elif (SubbasementFissureL in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUsePB and
                wave and
                (DarkVisor in loadout)
                ):
                loadout.append(FieldAccessL)
                loadout.append(other) 
        if (TransferStationR not in loadout) :
            other=otherDoor(TransferStationR,Connections)
            if (other in loadout) :
                loadout.append(TransferStationR)
            elif (FieldAccessL in loadout) and (
                jumpAble and
                pinkDoor and
                (DarkVisor in loadout) and
                wave and
                canUseBombs
                ):
                loadout.append(TransferStationR)
                loadout.append(other)
            elif (CellarR in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUsePB and
                (DarkVisor in loadout) and
                wave
                ):
                loadout.append(TransferStationR)
                loadout.append(other)
            elif (SubbasementFissureL in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUsePB and
                wave and
                (DarkVisor in loadout)
                ):
                loadout.append(TransferStationR)
                loadout.append(other)
        if (CellarR not in loadout) :
            other=otherDoor(CellarR,Connections)
            if (other in loadout) :
                loadout.append(CellarR)
            elif (FieldAccessL in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUseBombs and
                (DarkVisor in loadout) and
                wave and
                underwater
                ):
                loadout.append(CellarR)
                loadout.append(other)
            elif (TransferStationR in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUseBombs and
                (DarkVisor in loadout) and
                wave and
                underwater
                ):
                loadout.append(CellarR)
                loadout.append(other)
            elif (SubbasementFissureL in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUsePB and
                (DarkVisor in loadout) and
                underwater
                ):
                loadout.append(CellarR)
                loadout.append(other)
        if (SubbasementFissureL not in loadout) :
            other=otherDoor(SubbasementFissureL,Connections)
            if (other in loadout) :
                loadout.append(SubbasementFissureL)
            elif (FieldAccessL in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUseBombs and
                (DarkVisor in loadout) and
                wave and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (SpeedBooster in loadout))
                ):
                loadout.append(SubbasementFissureL)
                loadout.append(other)
            elif (TransferStationR in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUseBombs and
                (DarkVisor in loadout) and
                wave and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (SpeedBooster in loadout))
                ):
                loadout.append(SubbasementFissureL)
                loadout.append(other)
            elif (CellarR in loadout) and (
                jumpAble and
                (Super in loadout) and
                canUseBombs and
                (DarkVisor in loadout) and
                underwater and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (SpeedBooster in loadout))
                ):
                loadout.append(SubbasementFissureL)
                loadout.append(other)
        if (WestTerminalAccessL not in loadout) :
            other=otherDoor(WestTerminalAccessL,Connections)
            if (other in loadout) :
                loadout.append(WestTerminalAccessL)
            elif (MezzanineConcourseL in loadout) and (
                jumpAble and
                (canFly or
                 (SpeedBooster in loadout) or
                 (Ice in loadout))
                ):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and (
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and (
                jumpAble and
                (SpeedBooster in loadout) and
                (canUseBombs or
                 (Screw in loadout))
                ):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and (
                jumpAble and
                canUseBombs and
                breakIce and
                underwater and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Bombs in loadout) or
                 (Grapple in loadout))
                 ):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
        if (MezzanineConcourseL not in loadout) :
            other=otherDoor(MezzanineConcourseL,Connections)
            if (other in loadout) :
                loadout.append(MezzanineConcourseL)
            elif (WestTerminalAccessL in loadout) and (
                jumpAble and
                (canFly or
                 (SpeedBooster in loadout) or
                 (Ice in loadout))
                ):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and (
                (VulnarCanyonL in loadout)):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and (
                jumpAble and
                canUseBombs and
                breakIce and
                underwater and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Bombs in loadout) or
                 (Grapple in loadout))
                 ):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
        if (VulnarCanyonL not in loadout) :
            other=otherDoor(VulnarCanyonL,Connections)
            if (other in loadout) :
                loadout.append(VulnarCanyonL)
            elif (WestTerminalAccessL in loadout) and (
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (MezzanineConcourseL in loadout) and (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and (
                jumpAble
                ):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
        if (CanyonPassageR not in loadout) :
            other=otherDoor(CanyonPassageR,Connections)
            if (other in loadout) :
                loadout.append(CanyonPassageR)
            elif (WestTerminalAccessL in loadout) and (
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (MezzanineConcourseL in loadout) and (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and jumpAble:
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(CanyonPassageR)
                loadout.append(other)
        if (ElevatorToCondenserL not in loadout) :
            other=otherDoor(ElevatorToCondenserL,Connections)
            if (other in loadout) :
                loadout.append(ElevatorToCondenserL)
            elif (WestTerminalAccessL in loadout) and (
                jumpAble and
                canUseBombs and
                breakIce and
                underwater and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Bombs in loadout) or
                 (Grapple in loadout))
                ):
                loadout.append(ElevatorToCondenserL)
                loadout.append(other)
            elif (MezzanineConcourseL in loadout) and (
                jumpAble and
                canUseBombs and
                breakIce and
                underwater and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Bombs in loadout) or
                 (Grapple in loadout))
                 ):
                loadout.append(ElevatorToCondenserL)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (SpeedBooster in loadout)
                ):
                loadout.append(ElevatorToCondenserL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and (
                (VulnarCanyonL in loadout)
                ):
                loadout.append(ElevatorToCondenserL)
                loadout.append(other)
        if (LoadingDockSecurityAreaL not in loadout):
            other=otherDoor(ElevatorToCondenserL,Connections)
            if (other in loadout) :
                loadout.append(LoadingDockSecurityAreaL)
        if (ElevatorToWellspringL not in loadout):
            other=otherDoor(ElevatorToWellspringL,Connections)
            if (other in loadout) :
                loadout.append(ElevatorToWellspringL)
            elif (NorakBrookL in loadout) and (
                jumpAble and
                canUseBombs and
                ((HiJump in loadout) or
                 (SpaceJump in loadout)) and
                (GravitySuit in loadout)
                ):
                loadout.append(ElevatorToWellspringL)
                loadout.append(other)
            elif (NorakPerimeterTR in loadout) and (
                jumpAble and
                canUseBombs and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Morph in loadout)) and
                (GravitySuit in loadout) and
                (MetroidSuit in loadout)
                ):
                loadout.append(ElevatorToWellspringL)
                loadout.append(other)
            elif (NorakPerimeterBL in loadout) and (
                jumpAble and
                canUseBombs and
                ((HiJump in loadout) or
                 (SpaceJump in loadout)) and
                (GravitySuit in loadout)
                ):
                loadout.append(ElevatorToWellspringL)
                loadout.append(other)
        if (NorakBrookL not in loadout):
            other=otherDoor(NorakBrookL,Connections)
            if (other in loadout) :
                loadout.append(NorakBrookL)
            elif (ElevatorToWellspringL in loadout) and (
                jumpAble and
                canUseBombs and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Morph in loadout)) and
                (GravitySuit in loadout)
                ):
                loadout.append(NorakBrookL)
                loadout.append(other)
            elif (NorakPerimeterTR in loadout) and (
                jumpAble and
                (MetroidSuit in loadout)
                ):
                loadout.append(NorakBrookL)
                loadout.append(other)
            elif (NorakPerimeterBL in loadout) and (
                jumpAble and
                (canUseBombs or
                 (Screw in loadout))
                ):
                loadout.append(NorakBrookL)
                loadout.append(other)
        if (NorakPerimeterTR not in loadout):
            other=otherDoor(NorakPerimeterTR,Connections)
            if (other in loadout) :
                loadout.append(NorakPerimeterTR)
            elif (ElevatorToWellspringL in loadout) and (
                jumpAble and
                underwater and
                canUseBombs and
                ((HiJump in loadout) or
                 (SpaceJump in loadout)) and
                (MetroidSuit in loadout)
                ):
                loadout.append(NorakPerimeterTR)
                loadout.append(other)
            elif (NorakBrookL in loadout) and (
                jumpAble and
                (MetroidSuit in loadout)
                ):
                loadout.append(NorakPerimeterTR)
                loadout.append(other)
            elif (NorakPerimeterBL in loadout) and (
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (MetroidSuit in loadout)
                ):
                loadout.append(NorakPerimeterTR)
                loadout.append(other)
        if (NorakPerimeterBL not in loadout):
            other=otherDoor(NorakPerimeterBL,Connections)
            if (other in loadout) :
                loadout.append(NorakPerimeterBL)
            elif (ElevatorToWellspringL in loadout) and (
                jumpAble and
                underwater and
                canUseBombs and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Morph in loadout))
                ):
                loadout.append(NorakPerimeterBL)
                loadout.append(other)
            elif (NorakBrookL in loadout) and (
                jumpAble and
                (canUseBombs or
                 (Screw in loadout))
                ):
                loadout.append(NorakPerimeterBL)
                loadout.append(other)
            elif (NorakPerimeterTR in loadout) and (
                jumpAble and
                (canUseBombs or
                 (Screw in loadout)) and
                (MetroidSuit in loadout)
                ):
                loadout.append(NorakPerimeterBL)
                loadout.append(other)
        if (VulnarDepthsElevatorEL not in loadout):
            other=otherDoor(VulnarDepthsElevatorEL,Connections)
            if (other in loadout) :
                loadout.append(VulnarDepthsElevatorEL)
            elif (VulnarDepthsElevatorER in loadout) :
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
            elif (SequesteredInfernoL in loadout) and (
                jumpAble and
                pinkDoor and
                canUseBombs and
                (Varia in loadout) and
                ((MetroidSuit in loadout) or
                 ((Charge in loadout) and
                  (Hypercharge in loadout)))
                ):
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
            elif (CollapsedPassageR in loadout) and (
                jumpAble and
                wave and
                canUseBombs and
                (Super in loadout) and
                (Varia in loadout)
                ):
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
        if (VulnarDepthsElevatorER not in loadout):
            other=otherDoor(VulnarDepthsElevatorER,Connections)
            if (other in loadout) :
                loadout.append(VulnarDepthsElevatorER)
            elif (VulnarDepthsElevatorEL in loadout) :
                loadout.append(VulnarDepthsElevatorER)
                loadout.append(other)
        if (SequesteredInfernoL not in loadout):
            other=otherDoor(SequesteredInfernoL,Connections)
            if (other in loadout) :
                loadout.append(SequesteredInfernoL)
            elif (VulnarDepthsElevatorEL in loadout) and (
                jumpAble and
                pinkDoor and
                canUseBombs and
                (Varia in loadout) and
                ((MetroidSuit in loadout) or
                 ((Charge in loadout) and
                  (Hypercharge in loadout)))
                ):
                loadout.append(SequesteredInfernoL)
                loadout.append(other)
            elif (CollapsedPassageR in loadout) and (
                jumpAble and
                canUseBombs and
                (Super in loadout) and
                (Varia in loadout) and
                ((MetroidSuit in loadout) or
                 ((Charge in loadout) and
                  (Hypercharge in loadout)))
                ):
                loadout.append(SequesteredInfernoL)
                loadout.append(other)
        if (CollapsedPassageR not in loadout):
            other=otherDoor(CollapsedPassageR,Connections)
            if (other in loadout) :
                loadout.append(CollapsedPassageR)
            elif (VulnarDepthsElevatorEL in loadout) and (
                jumpAble and
                wave and
                canUseBombs and
                (Super in loadout) and
                (Varia in loadout)
                ):
                loadout.append(CollapsedPassageR)
                loadout.append(other)
            elif (SequesteredInfernoL in loadout) and (
                jumpAble and
                canUseBombs and
                (Super in loadout) and
                (Varia in loadout) and
                ((MetroidSuit in loadout) or
                 ((Charge in loadout) and
                  (Hypercharge in loadout)))
                ):
                loadout.append(CollapsedPassageR)
                loadout.append(other)
        if (MagmaPumpL not in loadout):
            other=otherDoor(MagmaPumpL,Connections)
            if (other in loadout) :
                loadout.append(MagmaPumpL)
            elif (ReservoirMaintenanceTunnelR in loadout) and (
                jumpAble and
                (((Plasma in loadout) and
                  wave) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout))) and
                (Varia in loadout) and
                canUseBombs
                ):
                loadout.append(MagmaPumpL)
                loadout.append(other)
            elif (IntakePumpR in loadout) and (
                jumpAble and
                underwater and
                (((Plasma in loadout) and
                  wave) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout))) and
                (Varia in loadout) and
                canUsePB and
                ((MetroidSuit in loadout) or
                 (Screw in loadout))
                ):
                loadout.append(MagmaPumpL)
                loadout.append(other)
            elif (ThermalReservoir1R in loadout) and (
                jumpAble and
                underwater and
                (((Plasma in loadout) and
                  wave) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout))) and
                (Varia in loadout) and
                (MetroidSuit in loadout) and
                (Screw in loadout)
                ):
                loadout.append(MagmaPumpL)
                loadout.append(other)
            elif (GeneratorAccessTunnelL in loadout) and (
                jumpAble and
                underwater and
                (((Plasma in loadout) and
                  wave) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout))) and
                (Varia in loadout) and
                canUsePB and
                (MetroidSuit in loadout) and
                (Screw in loadout)
                ):
                loadout.append(MagmaPumpL)
                loadout.append(other)
        if (ReservoirMaintenanceTunnelR not in loadout):
            other=otherDoor(ReservoirMaintenanceTunnelR,Connections)
            if (other in loadout) :
                loadout.append(ReservoirMaintenanceTunnelR)
            elif (MagmaPumpL in loadout) and (
                jumpAble and
                (((Plasma in loadout) and
                  wave) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout))) and
                (Varia in loadout) and
                canUseBombs
                ):
                loadout.append(ReservoirMaintenanceTunnelR)
                loadout.append(other)
            elif (IntakePumpR in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                ((MetroidSuit in loadout) or
                 (breakIce and
                  (Screw in loadout)))
                ):
                loadout.append(ReservoirMaintenanceTunnelR)
                loadout.append(other)
            elif (ThermalReservoir1R in loadout) and (
                jumpAble and
                canUseBombs and
                underwater and
                (Screw in loadout) and
                (MetroidSuit in loadout) and
                (Varia in loadout)
                ): 
                loadout.append(ReservoirMaintenanceTunnelR)
                loadout.append(other)
            elif (GeneratorAccessTunnelL in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                (Screw in loadout) and
                (MetroidSuit in loadout)
                ): 
                loadout.append(ReservoirMaintenanceTunnelR)
                loadout.append(other)
        if (IntakePumpR not in loadout):
            other=otherDoor(IntakePumpR,Connections)
            if (other in loadout) :
                loadout.append(IntakePumpR)
            elif (MagmaPumpL in loadout) and (
                jumpAble and
                underwater and
                (((Plasma in loadout) and
                  wave) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout))) and
                (Varia in loadout) and
                canUsePB and
                ((MetroidSuit in loadout) or
                 (Screw in loadout))
                ):
                loadout.append(IntakePumpR)
                loadout.append(other)
            elif (ReservoirMaintenanceTunnelR in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                ((MetroidSuit in loadout) or
                 (breakIce and
                  (Screw in loadout)))
                ):
                loadout.append(IntakePumpR)
                loadout.append(other)
            elif (ThermalReservoir1R in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                (Screw in loadout) and
                (MetroidSuit in loadout) and
                (Varia in loadout)
                ): 
                loadout.append(IntakePumpR)
                loadout.append(other)
            elif (GeneratorAccessTunnelL in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                (Screw in loadout) and
                (MetroidSuit in loadout)
                ): 
                loadout.append(IntakePumpR)
                loadout.append(other)
        if (ThermalReservoir1R not in loadout):
            other=otherDoor(ThermalReservoir1R,Connections)
            if (other in loadout) :
                loadout.append(ThermalReservoir1R)
            elif (MagmaPumpL in loadout) and (
                jumpAble and
                underwater and
                (((Plasma in loadout) and
                  wave) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout))) and
                (Varia in loadout) and
                (MetroidSuit in loadout) and
                (Screw in loadout)
                ):
                loadout.append(ThermalReservoir1R)
                loadout.append(other)
            elif (ReservoirMaintenanceTunnelR in loadout) and (
                jumpAble and
                canUseBombs and
                underwater and
                (Screw in loadout) and
                (MetroidSuit in loadout) and
                (Varia in loadout)
                ): 
                loadout.append(ThermalReservoir1R)
                loadout.append(other)
            elif (IntakePumpR in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                (Screw in loadout) and
                (MetroidSuit in loadout) and
                (energyCount > 3)
                ): 
                loadout.append(ThermalReservoir1R)
                loadout.append(other)
            elif (GeneratorAccessTunnelL in loadout) and (
                jumpAble and
                canUsePB and
                (MetroidSuit in loadout) and
                (Varia in loadout)
                ): 
                loadout.append(ThermalReservoir1R)
                loadout.append(other)
        if (GeneratorAccessTunnelL not in loadout):
            other=otherDoor(GeneratorAccessTunnelL,Connections)
            if (other in loadout) :
                loadout.append(GeneratorAccessTunnelL)
            elif (MagmaPumpL in loadout) and (
                jumpAble and
                underwater and
                (((Plasma in loadout) and
                  wave) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout))) and
                (Varia in loadout) and
                canUsePB and
                (MetroidSuit in loadout) and
                (Screw in loadout)
                ):
                loadout.append(GeneratorAccessTunnelL)
                loadout.append(other)
            elif (ReservoirMaintenanceTunnelR in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                (Screw in loadout) and
                (MetroidSuit in loadout)
                ):
                loadout.append(GeneratorAccessTunnelL)
                loadout.append(other)
            elif (IntakePumpR in loadout) and (
                jumpAble and
                canUsePB and
                underwater and
                (Screw in loadout) and
                (MetroidSuit in loadout)
                ): 
                loadout.append(GeneratorAccessTunnelL)
                loadout.append(other)
            elif (ThermalReservoir1R in loadout) and (
                jumpAble and
                canUsePB and
                (MetroidSuit in loadout) and
                (Varia in loadout)
                ): 
                loadout.append(GeneratorAccessTunnelL)
                loadout.append(other)
        if (ElevatorToMagmaLakeR not in loadout):
            other=otherDoor(ElevatorToMagmaLakeR,Connections)
            if (other in loadout) :
                loadout.append(ElevatorToMagmaLakeR)
            elif (MagmaPumpAccessR in loadout) and (
                jumpAble and
                underwater and
                (MetroidSuit in loadout) and
                (Varia in loadout) and
                canUsePB and
                ((Screw in loadout) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout)))
                ):
                loadout.append(ElevatorToMagmaLakeR)
                loadout.append(other)
        if (MagmaPumpAccessR not in loadout):
            other=otherDoor(MagmaPumpAccessR,Connections)
            if (other in loadout) :
                loadout.append(MagmaPumpAccessR)
            elif (ElevatorToMagmaLakeR in loadout) and (
                jumpAble and
                underwater and
                (MetroidSuit in loadout) and
                (Varia in loadout) and
                canUsePB and
                ((Screw in loadout) or
                 ((Hypercharge in loadout) and
                  (Charge in loadout)))
                ):
                loadout.append(MagmaPumpAccessR)
                loadout.append(other)
        if (FieryGalleryL not in loadout):
            other=otherDoor(FieryGalleryL,Connections)
            if (other in loadout) :
                loadout.append(FieryGalleryL)
            elif (RagingPitL in loadout) and (
                jumpAble and
                (Varia in loadout) and
                canUsePB
                ):
                loadout.append(FieryGalleryL)
                loadout.append(other)
            elif (HollowChamberR in loadout) and (
                jumpAble and
                (Morph in loadout) and
                (Varia in loadout) and
                pinkDoor and
                icePod and
                (canUseBombs or
                 (Screw in loadout) or
                 (SpeedBooster in loadout))
                ):
                loadout.append(FieryGalleryL)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and (
                jumpAble and
                (Varia in loadout) and
                pinkDoor and
                (canUseBombs or
                 (Screw in loadout) or
                 (SpeedBooster in loadout)) and
                (icePod or
                 canUsePB)
                ):
                loadout.append(FieryGalleryL)
                loadout.append(other)
            elif (SporousNookL in loadout) and (
                jumpAble and
                (Varia in loadout) and
                underwater and
                (canUseBombs or
                 (Screw in loadout) or
                 (Super in loadout) or
                 breakIce)
                ):
                loadout.append(FieryGalleryL)
                loadout.append(other)
        if (RagingPitL not in loadout):
            other=otherDoor(RagingPitL,Connections)
            if (other in loadout) :
                loadout.append(RagingPitL)
            elif (FieryGalleryL in loadout) and (
                jumpAble and
                (Varia in loadout) and
                canUseBombs and
                (Super in loadout)
                ):
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (HollowChamberR in loadout) and (
                jumpAble and
                canUseBombs and
                (Varia in loadout) and
                (Super in loadout) and
                icePod
                ):
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and (
                jumpAble and
                canUseBombs and
                (Varia in loadout) and
                (Super in loadout) and
                (icePod or
                 canUsePB)
                ):
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (SporousNookL in loadout) and (
                jumpAble and
                canUseBombs and
                (Varia in loadout) and
                underwater and
                (Super in loadout)
                ):
                loadout.append(RagingPitL)
                loadout.append(other)
        if (HollowChamberR not in loadout):
            other=otherDoor(HollowChamberR,Connections)
            if (other in loadout) :
                loadout.append(HollowChamberR)
            elif (FieryGalleryL in loadout) and (
                jumpAble and
                (Morph in loadout) and
                (Varia in loadout) and
                (Super in loadout) and
                icePod and
                (canUseBombs or
                 (Screw in loadout) or
                 (SpeedBooster in loadout))
                ):
                loadout.append(HollowChamberR)
                loadout.append(other)
            elif (RagingPitL in loadout) and (
                jumpAble and
                canUsePB and
                (Super in loadout) and
                (Varia in loadout) and
                icePod
                ):
                loadout.append(HollowChamberR)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and (
                jumpAble and
                (Varia in loadout) and
                icePod
                ):
                loadout.append(HollowChamberR)
                loadout.append(other)
            elif (SporousNookL in loadout) and (
                jumpAble and
                (Varia in loadout) and
                icePod and
                (Super in loadout) and
                underwater
                ):
                loadout.append(HollowChamberR)
                loadout.append(other)
        if (PlacidPoolR not in loadout):
            other=otherDoor(PlacidPoolR,Connections)
            if (other in loadout) :
                loadout.append(PlacidPoolR)
            elif (FieryGalleryL in loadout) and (
                jumpAble and
                (Varia in loadout) and
                (Super in loadout) and
                (canUseBombs or
                 (Screw in loadout) or
                 (SpeedBooster in loadout)) and
                (icePod or
                 canUsePB)
                ):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (RagingPitL in loadout) and (
                jumpAble and
                canUseBombs and
                (Varia in loadout) and
                canUsePB
                ):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (HollowChamberR in loadout) and (
                jumpAble and
                (Varia in loadout) and
                icePod
                ):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (SporousNookL in loadout) and (
                jumpAble and
                (Varia in loadout) and
                (icePod or
                 canUsePB) and
                (Super in loadout) and
                underwater
                ):
                loadout.append(PlacidPoolR)
                loadout.append(other)
        if (SporousNookL not in loadout):
            other=otherDoor(SporousNookL,Connections)
            if (other in loadout) :
                loadout.append(SporousNookL)
            elif (FieryGalleryL in loadout) and (
                jumpAble and
                (Varia in loadout) and
                underwater and
                (canUseBombs or
                 (Screw in loadout) or
                 (Super in loadout) or
                 breakIce)
                ):
                loadout.append(SporousNookL)
                loadout.append(other)
            elif (RagingPitL in loadout) and (
                jumpAble and
                canUsePB and
                (Varia in loadout) and
                underwater
                ):
                loadout.append(SporousNookL)
                loadout.append(other)
            elif (HollowChamberR in loadout) and (
                jumpAble and
                (Varia in loadout) and
                icePod and
                underwater and
                (canUseBombs or
                 (Screw in loadout) or
                 (Super in loadout) or
                 breakIce)
                ):
                loadout.append(SporousNookL)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and (
                jumpAble and
                (Varia in loadout) and
                (icePod or
                 canUsePB) and
                pinkDoor and
                underwater and
                (canUseBombs or
                 (Screw in loadout) or
                 (Super in loadout) or
                 breakIce)
                ):
                loadout.append(SporousNookL)
                loadout.append(other)
        if (TramToSuziIslandR not in loadout):
            other=otherDoor(TramToSuziIslandR,Connections)
            if (other in loadout) :
                loadout.append(TramToSuziIslandR)
        if loadout == tempLoadout :
            movement = True
    return loadout

def updateLogic(unusedLocations: list[Location],
                locArray: list[Location],
                loadout: list[Item]) -> list[Location]:
    energyCount = 0
    for item in loadout:
        if item == Energy:
            energyCount += 1
    exitSpacePort = (Morph in loadout) or (Missile in loadout) or (Super in loadout) or (Wave in loadout)
    jumpAble = exitSpacePort and (GravityBoots in loadout)
    underwater = jumpAble and (GravitySuit in loadout)
    pinkDoor = (Missile in loadout) or (Super in loadout)
    canUseBombs = (Morph in loadout) and ((Bombs in loadout) or (PowerBomb in loadout))
    canUsePB = (Morph in loadout) and (PowerBomb in loadout)
    breakIce = (Plasma in loadout) or ((Hypercharge in loadout) and (Charge in loadout))
    wave = (Wave in loadout) or ((Hypercharge in loadout) and (Charge in loadout))

    vulnar = jumpAble and pinkDoor

    canFly = (Bombs in loadout) or (SpaceJump in loadout)

    icePod = ((Ice in loadout) and pinkDoor) or ((Hypercharge in loadout) and (Charge in loadout))
    suzi = underwater and (SpeedBooster in loadout) and (Grapple in loadout) and \
        (Super in loadout) and canUsePB and (Wave in loadout)
    # onAndOff = ON varia ice PB grapple OFF Hyper charge

    logic = {
        "Impact Crater: AccelCharge":
            (
                exitSpacePort and
                jumpAble and
                (Morph in loadout) and
                (Spazer in loadout) and
                ((HiJump in loadout) or
                 (SpeedBooster in loadout)
                 or canFly)
                ),
        "Subterranean Burrow":
            (
                exitSpacePort and
                ((Morph in loadout) or
                 (GravityBoots in loadout))
                ),
        "Sandy Cache":
            (
                (OceanShoreR in loadout) and
                jumpAble and
                (Missile in loadout) and
                ((Morph in loadout) or
                 (GravitySuit in loadout))
                ),
        "Submarine Nest":
            (
                (OceanShoreR in loadout) and
                pinkDoor and
                underwater
                ),
        "Shrine Of The Penumbra":
            (
                (OceanShoreR in loadout) and
                jumpAble and
                pinkDoor and
                (GravitySuit in loadout) and
                (canUsePB or
                 (canUseBombs and
                  (DarkVisor in loadout)))
                ),
        "Benthic Cache Access":
            (
                ((OceanShoreR in loadout) or
                 (EleToTurbidPassageR in loadout)) and
                underwater and canUsePB and
                (Super in loadout)
                ),
        "Benthic Cache":
            (
                ((OceanShoreR in loadout) or
                 (EleToTurbidPassageR in loadout)) and
                underwater and
                canUseBombs and
                (Super in loadout) and
                (DarkVisor in loadout)
                ),
        "Ocean Vent Supply Depot":
            (
                ((OceanShoreR in loadout) or
                 (EleToTurbidPassageR in loadout)) and
                pinkDoor and
                underwater and
                (Morph in loadout) and
                (DarkVisor in loadout) and 
                ((Super in loadout) or
                 ((GravitySuit in loadout) and
                  (Screw in loadout)))
                ),
        "Sediment Flow":
            (
                (OceanShoreR in loadout) and
                jumpAble and
                underwater and
                (Super in loadout)
                ),
        "Harmonic Growth Enhancer":
            (
                (FieldAccessL in loadout) and
                wave and
                jumpAble and
                pinkDoor and
                canUseBombs and
                (DarkVisor in loadout)
                ),
        "Upper Vulnar Power Node":
            (
                vulnar and
                canUsePB and
                (Screw in loadout) and
                (MetroidSuit in loadout)
                ),
        "Grand Vault":
            (
                vulnar and
                (Grapple in loadout)
                ),
        "Cistern":
            (
                (RuinedConcourseBL in loadout) and
                jumpAble and canUseBombs
                ),
        "Warrior Shrine: ETank":
            (
                (RuinedConcourseBL in loadout) and
                jumpAble and
                pinkDoor and
                canUsePB
                ),
        "Vulnar Caves Entrance":
            vulnar,
        "Crypt":
            (
                (RuinedConcourseBL in loadout) and
                jumpAble and
                canUseBombs and
                (pinkDoor or
                 ((GravitySuit in loadout) and
                  ((HiJump in loadout) or
                   (SpaceJump in loadout) or
                   (Bombs in loadout) or
                   (Speedball in loadout))) or
                 ((HiJump in loadout) and
                  (Speedball in loadout) or
                  (Ice in loadout))) and
                ((Wave in loadout) or
                 (Bombs in loadout))
                ),
        "Archives: SpringBall":  # yes it's actually Speed Ball, uses Spring data
            (
                vulnar and
                (Morph in loadout) and
                (Speedball in loadout)
                ),
        "Archives: SJBoost":
            (
                vulnar and
                (Morph in loadout) and
                (Speedball in loadout) and
                (SpeedBooster in loadout)
                ),
        "Sensor Maintenance: ETank":  # front
            (
                vulnar and
                canUseBombs
                ),
        "Eribium Apparatus Room":
            (
                (FieldAccessL in loadout) and
                jumpAble and
                wave and
                pinkDoor and
                canUseBombs and
                (DarkVisor in loadout)
                ),
        "Hot Spring":
            (
                ((SporousNookL in loadout) or
                 ((EleToTurbidPassageR in loadout) and
                  (Varia in loadout))) and
                jumpAble and
                canUseBombs and
                (GravitySuit in loadout)
                ),
        "Epiphreatic Crag":
            (
                (ConstructionSiteL in loadout) and
                jumpAble and
                (Morph in loadout) and
                (GravitySuit in loadout)
                ),
        "Mezzanine Concourse":
            (
                (MezzanineConcourseL in loadout) and
                jumpAble and
                (WestTerminalAccessL in loadout)
                ),
        "Greater Inferno":
            (
                (MagmaPumpAccessR in loadout) and
                jumpAble and
                canUsePB and
                (Super in loadout) and
                (GravitySuit in loadout) and
                (Varia in loadout) and
                (MetroidSuit in loadout)
                ),
        "Burning Depths Cache":
            (
                (MagmaPumpAccessR in loadout) and
                jumpAble and
                canUsePB and
                (GravitySuit in loadout) and
                (Varia in loadout) and
                (MetroidSuit in loadout) and
                (Spazer in loadout)
                ),
        "Mining Cache":
            (
                (((EleToTurbidPassageR in loadout) and
                  (Varia in loadout)) or
                 ((SporousNookL in loadout) and
                  (GravitySuit in loadout))) and
                jumpAble and
                (Super in loadout) and
                canUseBombs
                ),
        "Infested Passage":
            (
                jumpAble and
                (Varia in loadout) and
                ((VulnarDepthsElevatorEL in loadout) and
                 canUseBombs) or
                ((SequesteredInfernoL in loadout) and
                 ((MetroidSuit in loadout) or
                  ((Hypercharge in loadout) and
                   (Charge in loadout))) and
                 (Morph in loadout) and
                 icePod)
                ),
        "Fire's Boon Shrine":
            (
                ((VulnarDepthsElevatorEL in loadout) and
                 jumpAble and
                 canUseBombs and
                 pinkDoor and
                 (Varia in loadout) and
                 icePod) or
                ((SequesteredInfernoL in loadout) and
                 ((MetroidSuit in loadout) or
                  ((Charge in loadout) and
                   (Hypercharge in loadout))) and
                 pinkDoor and
                 (Varia in loadout)) or
                ((CollapsedPassageR in loadout) and
                 (Super in loadout) and
                 (Varia in loadout) and
                 canUseBombs and
                 wave)
                ),
        "Fire's Bane Shrine":
            (
                icePod and
                jumpAble and
                (Morph in loadout) and
                (((VulnarDepthsElevatorEL in loadout) and
                  canUseBombs and
                  pinkDoor and
                  (Varia in loadout)) or
                 ((SequesteredInfernoL in loadout) and
                  ((MetroidSuit in loadout) or
                   ((Charge in loadout) and
                    (Hypercharge in loadout))) and
                  pinkDoor and
                  (Varia in loadout)))
                ),
        "Ancient Shaft":
            (
                jumpAble and
                (Varia in loadout) and
                (MetroidSuit in loadout) and
                canUseBombs and
                ((VulnarDepthsElevatorEL in loadout) and
                 canUseBombs and
                 icePod) or
                ((SequesteredInfernoL in loadout) and
                 ((MetroidSuit in loadout) or
                  ((Hypercharge in loadout) and
                   (Charge in loadout))))
                ),
        "Gymnasium":
            (
                jumpAble and
                ((Varia in loadout) and
                (Grapple in loadout) and
                ((VulnarDepthsElevatorEL in loadout) and
                 canUseBombs and
                 icePod) or
                ((SequesteredInfernoL in loadout) and
                 ((MetroidSuit in loadout) or
                  ((Hypercharge in loadout) and
                   (Charge in loadout))) and
                 (Morph in loadout)))
                ),
        "Electromechanical Engine":
            (
                jumpAble and
                (Grapple in loadout) and
                (Varia in loadout) and
                (Morph in loadout) and
                (((ReservoirMaintenanceTunnelR in loadout) and
                  canUseBombs and
                  (GravitySuit in loadout) and
                  (Screw in loadout)) or
                 ((ThermalReservoir1R in loadout) and
                     (MetroidSuit in loadout)) or
                 ((GeneratorAccessTunnelL in loadout) and
                  canUsePB and
                  (MetroidSuit in loadout)))
                ),
        "Depressurization Valve":
            (
                jumpAble and
                (Morph in loadout) and
                (((ReservoirMaintenanceTunnelR in loadout) and
                  canUseBombs and
                  (GravitySuit in loadout) and
                  (Screw in loadout)) or
                 ((ThermalReservoir1R in loadout) and
                  (Varia in loadout) and
                  (MetroidSuit in loadout)) or
                 ((GeneratorAccessTunnelL in loadout) and
                  canUsePB and
                  (MetroidSuit in loadout)))
                ),
        "Loading Dock Storage Area":
            (LoadingDockSecurityAreaL in loadout),
        "Containment Area":
            (
                jumpAble and
                ((FoyerR in loadout) and
                 ((MetroidSuit in loadout) or
                  (Screw in loadout))) or
                ((AlluringCenoteR in loadout) and
                 (Grapple in loadout) and
                 (SpeedBooster in loadout) and
                 (Speedball in loadout) and
                 canUsePB)
                ),
        "Briar: SJBoost":  # top
            (
                (NorakBrookL in loadout) and
                jumpAble and
                canUsePB
                ),
        "Shrine Of Fervor":
            (
                (NorakBrookL in loadout) and
                jumpAble and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Morph in loadout))
                ),
        "Chamber Of Wind":
            (
                (NorakBrookL in loadout) and
                jumpAble and
                pinkDoor and
                canFly and
                (canUseBombs or
                 ((Screw in loadout) and
                  (Speedball in loadout) and
                  (Morph in loadout)) and
                 (SpeedBooster in loadout))
                ),
        "Water Garden":
            (
                (NorakBrookL in loadout) and
                jumpAble and
                (SpeedBooster in loadout) and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Morph in loadout))
                ),
        "Crocomire's Energy Station":
            (
                (NorakBrookL in loadout) and
                jumpAble and
                (Super in loadout) and
                (SpeedBooster in loadout) and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Morph in loadout))
                ),
        "Wellspring Cache":
            (
                (ElevatorToWellspringL in loadout) and
                jumpAble and
                (GravitySuit in loadout) and
                (Super in loadout) and
                (Morph in loadout)
                ),
        "Frozen Lake Wall: DamageAmp":
            (
                (ElevatorToCondenserL in loadout) and
                jumpAble and
                canUsePB
                ),
        "Grand Promenade":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble
                ),
        "Summit Landing":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                canUseBombs
                ),
        "Snow Cache":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                canUseBombs
                ),
        "Reliquary Access":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (Super in loadout) and
                (DarkVisor in loadout)
                ),
        "Syzygy Observatorium":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                ((Screw in loadout) or
                 (((Super in loadout) and
                   (MetroidSuit in loadout) and
                   (energyCount > 6)) or
                  ((Hypercharge in loadout) and
                   (Charge in loadout))))
                ),
        "Armory Cache 2":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                ((Screw in loadout) or
                 ((Super in loadout) and
                  canUseBombs and
                  (DarkVisor in loadout)))
                ),
        "Armory Cache 3":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                ((Screw in loadout) or
                 ((Super in loadout) and
                  canUseBombs and
                  (DarkVisor in loadout)))
                ),
        "Drawing Room":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (Super in loadout)
                ),
        "Impact Crater Overlook":
            (
                canFly and
                canUseBombs and
                (canUsePB or
                 (Super in loadout))
                ),
        "Magma Lake Cache":
            (
                (ElevatorToMagmaLakeR in loadout) and
                jumpAble and
                icePod and
                (Morph in loadout)
                ),
        "Shrine Of The Animate Spark":
            (
                (TramToSuziIslandR in loadout) and
                suzi and
                canFly and
                (Hypercharge in loadout) and
                (Charge in loadout)
                ),
        "Docking Port 4":  # (4 = letter Omega)
            (
                ((spaceDrop not in loadout) and
                 (Grapple in loadout)) or
                ((spaceDrop in loadout) and
                 (LoadingDockSecurityAreaL in loadout) and
                 jumpAble and
                 (MetroidSuit in loadout))
                ),
        "Ready Room":
            (
                ((spaceDrop not in loadout) and
                 (Super in loadout)) or
                ((spaceDrop in loadout) and
                 (LoadingDockSecurityAreaL in loadout) and
                 jumpAble and
                 (MetroidSuit in loadout) and
                 (Grapple in loadout) and
                 (Super in loadout))
                ),
        "Torpedo Bay":
            True,
        "Extract Storage":
            (
                (canUsePB and
                 (spaceDrop in loadout) == False) or
                ((spaceDrop in loadout) and
                 (LoadingDockSecurityAreaL in loadout) and
                 jumpAble and
                 (Grapple in loadout) and
                 (MetroidSuit in loadout))
                ),
        "Impact Crater Alcove":
            (
                jumpAble and
                canFly and
                canUseBombs
                ),
        "Ocean Shore: bottom":
            (
                OceanShoreR in loadout
                ),
        "Ocean Shore: top":
            (
                (OceanShoreR in loadout) and
                jumpAble and
                (canFly or
                 (HiJump in loadout) or
                 ((SpeedBooster in loadout) and
                  (GravitySuit in loadout)))
                ),
        "Sandy Burrow: ETank":  # top
            (
                (OceanShoreR in loadout) and
                underwater and
                (GravitySuit in loadout) and
                ((Screw in loadout) or
                   canUseBombs) and
                ((HiJump in loadout) or
                 (SpaceJump in loadout))
                ),
        "Submarine Alcove":
            (
                ((OceanShoreR in loadout) and
                 underwater and
                 (Morph in loadout) and
                 (((DarkVisor in loadout) and
                   pinkDoor) or
                  (Super in loadout))) or
                ((EleToTurbidPassageR in loadout) and
                 (Super in loadout) and
                 underwater and
                 (Morph in loadout) and
                 (Speedball in loadout))
                ),
        "Sediment Floor":
            (
                ((OceanShoreR in loadout) and
                 underwater and
                 (Morph in loadout) and
                 (((DarkVisor in loadout) and
                   pinkDoor) or
                  (Super in loadout))) or
                ((EleToTurbidPassageR in loadout) and
                 pinkDoor and
                 underwater and
                 (Morph in loadout) and
                 (Speedball in loadout))
                ),
        "Sandy Gully":  
            (
                (OceanShoreR in loadout) and
                underwater and
                (Super in loadout)
                ),
        "Hall Of The Elders":
            (
                (RuinedConcourseBL in loadout) and
                (((GravitySuit in loadout) and
                  ((HiJump in loadout) or
                  canFly)) or
                 pinkDoor)
                ),
        "Warrior Shrine: AmmoTank bottom":
            (
                (RuinedConcourseBL in loadout) and
                jumpAble and
                (Morph in loadout) and
                pinkDoor
                ),
        "Warrior Shrine: AmmoTank top":
            (
                (RuinedConcourseBL in loadout) and
                jumpAble and
                canUseBombs and
                pinkDoor
                ),
        "Path Of Swords":
            (
                vulnar and
                (canUseBombs or
                 ((Morph in loadout) and
                  (Screw in loadout)))
                ),
        "Auxiliary Pump Room":
            (
                vulnar and
                canUseBombs
                ),
        "Monitoring Station":
            (
                vulnar and
                (Morph in loadout) and
                (Speedball in loadout or
                 canUseBombs)
                 ),
        "Sensor Maintenance: AmmoTank":  # back
            (
                vulnar and
                canUseBombs and
                (Speedball in loadout)
                ),
        "Causeway Overlook":
            (
                (CausewayR in loadout) and
                jumpAble and
                canUseBombs
                ),
        "Placid Pool":
            (
                (PlacidPoolR in loadout) and
                jumpAble and
                canUsePB and
                icePod
                ),
        "Blazing Chasm":
            (
                (ElevatorToMagmaLakeR in loadout) and
                jumpAble and
                canUsePB and
                (GravitySuit in loadout) and
                (Varia in loadout) and
                (MetroidSuit in loadout)                  
                ),
        "Generator Manifold":
            (
                jumpAble and
                (Super in loadout) and
                canUseBombs and
                (((ReservoirMaintenanceTunnelR in loadout) and
                  (GravitySuit in loadout)) or
                 ((GeneratorAccessTunnelL in loadout) and
                  canUsePB and
                  (MetroidSuit in loadout) and
                  (Screw in loadout)) or
                 ((ThermalReservoir1R in loadout) and
                  (Varia in loadout) and
                  (MetroidSuit in loadout)
                  and (Screw in loadout)))
                ),
        "Fiery Crossing Cache":
            (
                (RagingPitL in loadout) and
                jumpAble and
                (Varia in loadout) and
                canUsePB
                ),
        "Dark Crevice Cache":
            (
                (ElevatorToMagmaLakeR in loadout) and
                jumpAble and
                canUseBombs and
                (canFly or
                 (SpeedBooster in loadout) or
                 (HiJump in loadout)) and
                (DarkVisor in loadout)
                ),
        "Ancient Basin":
            (
                (Varia in loadout) and
                (((VulnarDepthsElevatorEL in loadout) and
                  jumpAble and
                  canUseBombs and
                  pinkDoor and
                  icePod) or
                 ((SequesteredInfernoL in loadout) and
                  ((MetroidSuit in loadout) or
                   ((Charge in loadout) and
                    (Hypercharge in loadout))) and
                  pinkDoor and
                  (Morph in loadout)) or
                 ((CollapsedPassageR in loadout) and
                  (Super in loadout) and
                  canUsePB and
                  wave))
                ),
        "Central Corridor: right":
            (
                (FoyerR in loadout) and
                jumpAble and
                (GravitySuit in loadout) and
                canUseBombs
                ),
        "Briar: AmmoTank":  # bottom
            (
                (NorakBrookL in loadout) and
                jumpAble and
                (Morph in loadout)
                ),
        "Icy Flow":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (SpeedBooster in loadout) and
                breakIce
                ),
        "Ice Cave":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                breakIce
                ),
        "Antechamber":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                canUsePB
                ),
        "Eddy Channels":
            (
                (EleToTurbidPassageR in loadout) and
                underwater and
                (DarkVisor in loadout) and 
                (Morph in loadout) and
                (Speedball in loadout) and
                (Super in loadout)
                ),
        "Tram To Suzi Island":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                (Spazer in loadout) and
                (Morph in loadout)
                ),
        "Portico":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                (Super in loadout) and
                (energyCount >6)
                ),
        "Tower Rock Lookout":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                pinkDoor and
                (energyCount >6) and
                (GravitySuit in loadout) and
                (SpaceJump in loadout) and
                (HiJump in loadout)
                ),
        "Reef Nook":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                pinkDoor and
                (energyCount >6) and
                (GravitySuit in loadout) and
                (SpaceJump in loadout) and
                (HiJump in loadout)
                ),
        "Saline Cache":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                (Super in loadout) and
                (energyCount >6) and
                (GravitySuit in loadout) and
                canFly
                ),
        "Enervation Chamber":
            (
                (TramToSuziIslandR in loadout) and
                suzi and
                canFly and
                (Hypercharge in loadout) and
                (Charge in loadout)
                ),
        "Weapon Locker":
            (
                ((spaceDrop not in loadout) and
                 pinkDoor) or
                ((spaceDrop in loadout) and
                 (LoadingDockSecurityAreaL in loadout) and
                 jumpAble and
                 (MetroidSuit in loadout) and
                 (Grapple in loadout) and
                 pinkDoor)
                ),
        "Aft Battery":  
            (
                ((spaceDrop not in loadout) and
                 (Morph in loadout)) or
                ((spaceDrop in loadout) and
                 (LoadingDockSecurityAreaL in loadout) and
                 jumpAble and
                 (MetroidSuit in loadout) and
                 (Grapple in loadout) and
                 (Morph in loadout))
                ),
        "Forward Battery":
            (
                ((spaceDrop not in loadout) and
                 pinkDoor and
                 (Morph in loadout)) or
                ((spaceDrop in loadout) and
                 (LoadingDockSecurityAreaL in loadout) and
                 jumpAble and
                 (Grapple in loadout) and
                 (MetroidSuit in loadout) and
                 pinkDoor)
                ),
        "Gantry":
            (
                ((spaceDrop not in loadout) and
                 pinkDoor) or
                ((spaceDrop in loadout) and
                 (LoadingDockSecurityAreaL in
                  loadout) and
                 jumpAble and
                 (MetroidSuit in loadout) and
                 (Grapple in loadout) and
                 pinkDoor)
                ),
        "Garden Canal": 
            (
                (NorakBrookL in loadout) and
                jumpAble and
                canUsePB and
                (Spazer in loadout) and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Morph in loadout))
                ),
        "Sandy Burrow: AmmoTank":  # bottom
            (
                (OceanShoreR in loadout) and
                (GravitySuit in loadout) and
                (Morph in loadout) and
                ((HiJump in loadout) or
                 (SpaceJump in loadout))
                ),
        "Trophobiotic Chamber":
            (
                vulnar and
                (Morph in loadout) and
                (Speedball in loadout)
                ),
        "Waste Processing":
            (
                (SpeedBooster in loadout) and
                jumpAble and
                (((SubbasementFissureL in loadout) and
                  canUsePB) or
                 ((CellarR in loadout) and
                  pinkDoor and
                  canUseBombs and
                  underwater and
                  (DarkVisor in loadout)) or
                 ((TransferStationR in loadout) and
                  (DarkVisor in loadout) and
                  wave and
                  canUseBombs))
                ),
        "Grand Chasm":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                canUseBombs and
                (Screw in loadout)
                ),
        "Mining Site 1":  # (1 = letter Alpha)
            (
                canUseBombs and
                jumpAble and
                pinkDoor and
                ((EleToTurbidPassageR in loadout) and
                 (Varia in loadout) or
                 ((SporousNookL in loadout) and
                  (GravitySuit in loadout)))
                ),
        "Colosseum":  # GT
            (
                (ElevatorToMagmaLakeR in loadout) and
                jumpAble and
                (Varia in loadout) and
                (Charge in loadout)
                ),
        "Lava Pool":
            (
                (EleToTurbidPassageR in loadout) and
                jumpAble and
                (Varia in loadout) and
                (MetroidSuit in loadout) and
                canUseBombs
                ),
        "Hive Main Chamber":
            (
                (VulnarDepthsElevatorEL in loadout) and
                jumpAble and
                (Varia in loadout) and
                canUseBombs
                ),
        "Crossway Cache":
            (
                (Varia in loadout) and
                (((VulnarDepthsElevatorEL in loadout) and
                  jumpAble and
                  canUseBombs and
                  icePod) or
                 ((SequesteredInfernoL in loadout) and
                  (((Hypercharge in loadout) and
                    (Charge in loadout)) or
                   (MetroidSuit in loadout))) or
                 ((CollapsedPassageR in loadout) and
                  (Super in loadout) and
                  canUsePB and
                  wave))                                 
                ),
                
        "Slag Heap":
            (
                canUseBombs and
                jumpAble and
                (Varia in loadout) and
                (MetroidSuit in loadout) and
                (SequesteredInfernoL in loadout)                       
                ),
        "Hydrodynamic Chamber": #one of the only intended water rooms
            (
                (WestCorridorR in loadout) and
                ((GravitySuit in loadout) or
                 (HiJump in loadout)) and
                (Morph in loadout) and
                pinkDoor and
                (Spazer in loadout)
                ),
        "Central Corridor: left":
            (
                (FoyerR in loadout) and
                jumpAble and
                (GravitySuit in loadout) and
                (Speedball in loadout) and
                (SpeedBooster in loadout) and
                (Morph in loadout)
                ),
        "Restricted Area":
            (
                (FoyerR in loadout) and
                jumpAble and
                (MetroidSuit in loadout)
                ),
        "Foundry":
            (
                (FoyerR in loadout) and
                jumpAble
                ),
        "Norak Escarpment":
            (
                (NorakBrookL in loadout) and
                jumpAble and
                (canFly or
                 (SpeedBooster in loadout))
                ),
        "Glacier's Reach":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                (energyCount > 6)
                ),
        "Sitting Room":
            (
                (WestTerminalAccessL in loadout) and
                jumpAble and
                canUsePB and
                (Speedball in loadout)
                ),
        "Suzi Ruins Map Station Access":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                (energyCount > 6) and
                canUsePB and
                (Super in loadout)
                ),
        "Obscured Vestibule":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                (energyCount > 6) and
                canUseBombs
                ),
        "Docking Port 3":  # (3 = letter Gamma)
            (
                ((spaceDrop not in loadout) and
                 (Grapple in loadout)) or
                ((spaceDrop in loadout) and
                 (LoadingDockSecurityAreaL in loadout) and
                 jumpAble and
                 (MetroidSuit in loadout))
                ),
        "Arena":
            (
                (RuinedConcourseBL in loadout) and
                jumpAble and
                pinkDoor
                ),
        "West Spore Field":
            (
                vulnar and
                (canUseBombs or
                 ((Morph in loadout) and
                  (Screw in loadout))) and
                (Super in loadout) and
                (Speedball in loadout) and
                (GravitySuit in loadout)
                ),
        "Magma Chamber":
            (
                (ElevatorToMagmaLakeR in loadout) and
                jumpAble and
                pinkDoor and
                canUsePB and
                (Varia in loadout) and
                ((Charge in loadout) or
                 (MetroidSuit in loadout))
                ),
        "Equipment Locker":
            (
                (WestCorridorR in loadout) and
                jumpAble and
                pinkDoor and
                ((GravitySuit in loadout) or
                 (HiJump in loadout) or
                 canUseBombs) and
                ((MetroidSuit in loadout) or
                 (Morph in loadout))
                ),
        "Antelier":  # spelled "Antilier" in subversion 1.1
            (
                ((WestCorridorR in loadout) and
                 ((GravitySuit in loadout) or
                  (HiJump in loadout)) and
                 ((pinkDoor and
                   (Morph in loadout)) or
                  (Super in loadout))) or
                ((FoyerR in loadout) and
                 (GravitySuit in loadout) and
                 (Screw in loadout))
                ),
        "Weapon Research":
            (
                (FoyerR in loadout) and
                jumpAble and
                (wave or
                 (MetroidSuit in loadout)) and
                (canUseBombs or
                 (Spazer in loadout))
                ),
        "Crocomire's Lair":
            (
                (NorakBrookL in loadout) and
                jumpAble and
                (Super in loadout) and
                (SpeedBooster in loadout) and
                ((HiJump in loadout) or
                 (SpaceJump in loadout) or
                 (Morph in loadout))
                ),
    }

    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = logic[thisLoc['fullitemname']]

    return unusedLocations
