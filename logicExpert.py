from typing import Union
from connection_data import AreaDoor, area_doors_unpackable
from item_data import Item, items_unpackable
from location_data import Location

# Expert logic updater
# updates unusedLocations

# TODO: look at logic for BrookL transitions, which needs nothing to climb up


(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

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

def updateAreaLogic(availableLocations: list[Location],
                    locArray: list[Location],
                    loadout: list[Union[Item, AreaDoor]],
                    Connections: list[tuple[AreaDoor, AreaDoor]]) -> list[Union[Item, AreaDoor]]:
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
                (Morph in loadout)
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (
                (RuinedConcourseTR in loadout) and
                jumpAble and
                (Morph in loadout) and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (
                (CausewayR in loadout) and
                jumpAble and
                canUseBombs and
                ((SpeedBooster in loadout) or
                 (Speedball in loadout))
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (
                (SporeFieldTR in loadout) and
                jumpAble and
                (Morph in loadout)
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (
                (SporeFieldBR in loadout) and
                jumpAble and
                (Morph in loadout)
                ):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
        if (RuinedConcourseTR not in loadout) : #CONSIDER WAVE LOGIC
            other=otherDoor(RuinedConcourseTR,Connections)
            if (other in loadout) :
                loadout.append(RuinedConcourseTR)
            elif (
                jumpAble and
                (Missile in loadout) and
                (Morph in loadout) and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                 ) :
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (
                (RuinedConcourseBL in loadout) and
                jumpAble and
                (Morph in loadout) and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (
                (CausewayR in loadout) and
                jumpAble and
                canUseBombs and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (
                (SporeFieldTR in loadout) and
                jumpAble and
                (Morph in loadout) and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (
                (SporeFieldBR in loadout) and
                jumpAble and
                (Morph in loadout) and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
        if (CausewayR not in loadout) :
            other=otherDoor(CausewayR,Connections)
            if (other in loadout) :
                loadout.append(CausewayR)
            elif (
                jumpAble and
                (Missile in loadout) and
                (Morph in loadout) and
                ((SpeedBooster in loadout) or
                 (Speedball in loadout))
                ):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (
                (RuinedConcourseBL in loadout) and
                jumpAble and
                (Morph in loadout) and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (
                (RuinedConcourseTR in loadout) and
                jumpAble and
                canUseBombs and
                (SpeedBooster in loadout) and
                (Energy in loadout)
                ):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (
                (SporeFieldTR in loadout) and
                jumpAble and
                (Morph in loadout) and
                ((SpeedBooster in loadout) or
                 (Speedball in loadout)) and
                canUseBombs
                ):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (
                (SporeFieldBR in loadout) and
                jumpAble and
                (Morph in loadout) and
                ((SpeedBooster in loadout) or
                 (Speedball in loadout)) and
                canUseBombs
                ):
                loadout.append(CausewayR)
                loadout.append(other)
        if (OceanShoreR not in loadout) :
            other=otherDoor(OceanShoreR,Connections)
            if (other in loadout) :
                loadout.append(OceanShoreR)
            elif (
                (EleToTurbidPassageR in loadout) and
                jumpAble and
                (Morph in loadout) and
                (Super in loadout) and 
                ((GravitySuit in loadout) or
                 (Speedball in loadout))
                ):
                loadout.append(OceanShoreR)
                loadout.append(other)
            elif (
                (PileAnchorL in loadout) and
                jumpAble and
                (GravitySuit in loadout) and
                canUsePB and
                (Super in loadout) and
                (SpeedBooster in loadout) and
                (Grapple in loadout)
                ):
                loadout.append(OceanShoreR)
                loadout.append(other)
        if (EleToTurbidPassageR not in loadout) :
            other=otherDoor(EleToTurbidPassageR,Connections)
            if (other in loadout) :
                loadout.append(EleToTurbidPassageR)
            elif (
                (OceanShoreR in loadout) and
                jumpAble and
                (Morph in loadout) and
                (Super in loadout) and 
                ((GravitySuit in loadout) or
                 (Speedball in loadout))
                ):
                loadout.append(EleToTurbidPassageR)
                loadout.append(other)
            elif (
                (PileAnchorL in loadout) and
                jumpAble and
                (GravitySuit in loadout) and
                canUsePB and
                (Super in loadout) and
                (SpeedBooster in loadout) and
                (Grapple in loadout)
                ):
                loadout.append(EleToTurbidPassageR)
                loadout.append(other)
        if (PileAnchorL not in loadout) :
            other=otherDoor(EleToTurbidPassageR,Connections)
            if (other in loadout) :
                loadout.append(PileAnchorL)
            elif (
                (OceanShoreR in loadout) and
                jumpAble and
                (GravitySuit in loadout) and
                canUsePB and
                (Super in loadout) and
                (SpeedBooster in loadout) and
                (Grapple in loadout)
                ):
                loadout.append(PileAnchorL)
                loadout.append(other)
            elif (
                (EleToTurbidPassageR in loadout) and
                jumpAble and
                (GravitySuit in loadout) and
                canUsePB and
                (Super in loadout) and
                (SpeedBooster in loadout) and
                (Grapple in loadout)
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
        if (WestCorridorR in loadout) == False :
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
        if (FoyerR in loadout) == False :
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
        if (ConstructionSiteL in loadout) == False :
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
        if (AlluringCenoteR in loadout) == False :
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
            elif (TransferStationR in loadout) and jumpAble and pinkDoor and (DarkVisor in loadout) and wave and canUseBombs:
                loadout.append(FieldAccessL)
                loadout.append(other)
            elif (CellarR in loadout) and jumpAble and (Super in loadout) and canUsePB and (DarkVisor in loadout) and wave:
                loadout.append(FieldAccessL)
                loadout.append(other)
            elif (SubbasementFissureL in loadout) and jumpAble and (Super in loadout) and canUsePB and wave :
                loadout.append(FieldAccessL)
                loadout.append(other) 
        if (TransferStationR not in loadout) :
            other=otherDoor(TransferStationR,Connections)
            if (other in loadout) :
                loadout.append(TransferStationR)
            elif (FieldAccessL in loadout) and jumpAble and pinkDoor and (DarkVisor in loadout) and wave and canUseBombs:
                loadout.append(TransferStationR)
                loadout.append(other)
            elif (CellarR in loadout) and jumpAble and (Super in loadout) and canUsePB and (DarkVisor in loadout) and wave:
                loadout.append(TransferStationR)
                loadout.append(other)
            elif (SubbasementFissureL in loadout) and jumpAble and (Super in loadout) and canUsePB and wave:
                loadout.append(TransferStationR)
                loadout.append(other)
        if (CellarR not in loadout) :
            other=otherDoor(CellarR,Connections)
            if (other in loadout) :
                loadout.append(CellarR)
            elif (FieldAccessL in loadout) and jumpAble and (Super in loadout) and canUsePB and (DarkVisor in loadout) and wave:
                loadout.append(CellarR)
                loadout.append(other)
            elif (TransferStationR in loadout) and jumpAble and (Super in loadout) and canUsePB and (DarkVisor in loadout) and wave:
                loadout.append(CellarR)
                loadout.append(other)
            elif (SubbasementFissureL in loadout) and jumpAble and (Super in loadout) and canUseBombs and (DarkVisor in loadout):
                loadout.append(CellarR)
                loadout.append(other)
        if (SubbasementFissureL not in loadout) :
            other=otherDoor(SubbasementFissureL,Connections)
            if (other in loadout) :
                loadout.append(SubbasementFissureL)
            elif (FieldAccessL in loadout) and jumpAble and (Super in loadout) and canUsePB and (DarkVisor in loadout) and wave:
                loadout.append(SubbasementFissureL)
                loadout.append(other)
            elif (TransferStationR in loadout) and jumpAble and (Super in loadout) and canUsePB and (DarkVisor in loadout) and wave:
                loadout.append(SubbasementFissureL)
                loadout.append(other)
            elif (CellarR in loadout) and jumpAble and (Super in loadout) and canUseBombs and (DarkVisor in loadout):
                loadout.append(SubbasementFissureL)
                loadout.append(other)
        if (WestTerminalAccessL not in loadout) :
            other=otherDoor(WestTerminalAccessL,Connections)
            if (other in loadout) :
                loadout.append(WestTerminalAccessL)
            elif (MezzanineConcourseL in loadout) and jumpAble and (canFly or (SpeedBooster in loadout) or (HiJump in loadout) or (Ice in loadout)):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and jumpAble and (SpeedBooster in loadout) :
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and jumpAble and (SpeedBooster in loadout) :
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
        if (MezzanineConcourseL not in loadout) :
            other=otherDoor(MezzanineConcourseL,Connections)
            if (other in loadout) :
                loadout.append(MezzanineConcourseL)
            elif (WestTerminalAccessL in loadout) and jumpAble and (canFly or (SpeedBooster in loadout) or (HiJump in loadout) or (Ice in loadout)):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and jumpAble and (SpeedBooster in loadout) :
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and jumpAble and (SpeedBooster in loadout) :
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
        if (VulnarCanyonL not in loadout) :
            other=otherDoor(VulnarCanyonL,Connections)
            if (other in loadout) :
                loadout.append(VulnarCanyonL)
            elif (WestTerminalAccessL in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (MezzanineConcourseL in loadout) and jumpAble and (SpeedBooster in loadout) :
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and jumpAble:
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
        if (CanyonPassageR not in loadout) :
            other=otherDoor(CanyonPassageR,Connections)
            if (other in loadout) :
                loadout.append(CanyonPassageR)
            elif (WestTerminalAccessL in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (MezzanineConcourseL in loadout) and jumpAble and (SpeedBooster in loadout) :
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and jumpAble:
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(CanyonPassageR)
                loadout.append(other)
        if (ElevatorToCondenserL not in loadout) :
            other=otherDoor(ElevatorToCondenserL,Connections)
            if (other in loadout) :
                loadout.append(ElevatorToCondenserL)
            elif (WestTerminalAccessL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(ElevatorToCondenserL)
                loadout.append(other)
            elif (MezzanineConcourseL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(ElevatorToCondenserL)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)) and (SpeedBooster in loadout):
                loadout.append(ElevatorToCondenserL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)) and (SpeedBooster in loadout):
                loadout.append(ElevatorToCondenserL)
                loadout.append(other)
        if (LoadingDockSecurityAreaL not in loadout) :
            other=otherDoor(ElevatorToCondenserL,Connections)
            if (other in loadout) :
                loadout.append(LoadingDockSecurityAreaL)
        if (ElevatorToWellspringL not in loadout) :
            other=otherDoor(ElevatorToWellspringL,Connections)
            if (other in loadout) :
                loadout.append(ElevatorToWellspringL)
            elif (NorakBrookL in loadout) and jumpAble and canUseBombs and (canFly or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)):
                loadout.append(ElevatorToWellspringL)
                loadout.append(other)
            elif (NorakPerimeterTR in loadout) and jumpAble and canUseBombs and (canFly or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)) and (MetroidSuit in loadout):
                loadout.append(ElevatorToWellspringL)
                loadout.append(other)
            elif (NorakPerimeterBL in loadout) and jumpAble and canUseBombs and (canFly or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)):
                loadout.append(ElevatorToWellspringL)
                loadout.append(other)
        if (NorakBrookL not in loadout) :
            other=otherDoor(NorakBrookL,Connections)
            if (other in loadout) :
                loadout.append(NorakBrookL)
            elif (ElevatorToWellspringL in loadout) and jumpAble and canUseBombs and (canFly or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)):
                loadout.append(NorakBrookL)
                loadout.append(other)
            elif (NorakPerimeterTR in loadout) and jumpAble and (MetroidSuit in loadout):
                loadout.append(NorakBrookL)
                loadout.append(other)
            elif (NorakPerimeterBL in loadout) and jumpAble and (canUseBombs or (Screw in loadout)):
                loadout.append(NorakBrookL)
                loadout.append(other)
        if (NorakPerimeterTR not in loadout) :
            other=otherDoor(NorakPerimeterTR,Connections)
            if (other in loadout) :
                loadout.append(NorakPerimeterTR)
            elif (ElevatorToWellspringL in loadout) and jumpAble and canUseBombs and (canFly or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)) and (MetroidSuit in loadout):
                loadout.append(NorakPerimeterTR)
                loadout.append(other)
            elif (NorakBrookL in loadout) and jumpAble and (MetroidSuit in loadout):
                loadout.append(NorakPerimeterTR)
                loadout.append(other)
            elif (NorakPerimeterBL in loadout) and jumpAble and (canUseBombs or (Screw in loadout)) and (MetroidSuit in loadout):
                loadout.append(NorakPerimeterTR)
                loadout.append(other)
        if (NorakPerimeterBL not in loadout) :
            other=otherDoor(NorakPerimeterBL,Connections)
            if (other in loadout) :
                loadout.append(NorakPerimeterBL)
            elif (ElevatorToWellspringL in loadout) and jumpAble and canUseBombs and (canFly or (Ice in loadout) or (HiJump in loadout) or (SpeedBooster in loadout)):
                loadout.append(NorakPerimeterBL)
                loadout.append(other)
            elif (NorakBrookL in loadout) and jumpAble and (canUseBombs or (Screw in loadout)):
                loadout.append(NorakPerimeterBL)
                loadout.append(other)
            elif (NorakPerimeterTR in loadout) and jumpAble and (canUseBombs or (Screw in loadout)) and (MetroidSuit in loadout):
                loadout.append(NorakPerimeterBL)
                loadout.append(other)
        if (VulnarDepthsElevatorEL not in loadout) :
            other=otherDoor(VulnarDepthsElevatorEL,Connections)
            if (other in loadout) :
                loadout.append(VulnarDepthsElevatorEL)
            elif (VulnarDepthsElevatorER in loadout) :
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
            elif (SequesteredInfernoL in loadout) and jumpAble and pinkDoor and canUseBombs and (energyCount > 4) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
            elif (CollapsedPassageR in loadout) and jumpAble and canUsePB and (Super in loadout) and (energyCount > 7):
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
        if (VulnarDepthsElevatorER not in loadout) :
            other=otherDoor(VulnarDepthsElevatorER,Connections)
            if (other in loadout) :
                loadout.append(VulnarDepthsElevatorER)
            elif (VulnarDepthsElevatorEL in loadout) :
                loadout.append(VulnarDepthsElevatorER)
                loadout.append(other)
            elif (SequesteredInfernoL in loadout) and jumpAble and pinkDoor and canUseBombs and (energyCount > 4) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(VulnarDepthsElevatorER)
                loadout.append(other)
            elif (CollapsedPassageR in loadout) and jumpAble and canUsePB and (Super in loadout) and (energyCount > 7):
                loadout.append(VulnarDepthsElevatorER)
                loadout.append(other)
        if (SequesteredInfernoL not in loadout) :
            other=otherDoor(SequesteredInfernoL,Connections)
            if (other in loadout) :
                loadout.append(SequesteredInfernoL)
            elif (VulnarDepthsElevatorEL in loadout) and jumpAble and pinkDoor and canUseBombs and (energyCount > 4) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(SequesteredInfernoL)
                loadout.append(other)
            elif (VulnarDepthsElevatorER in loadout) and jumpAble and pinkDoor and canUseBombs and (energyCount > 4) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(SequesteredInfernoL)
                loadout.append(other)
            elif (CollapsedPassageR in loadout) and jumpAble and pinkDoor and canUsePB and (Super in loadout) and (energyCount > 7) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(SequesteredInfernoL)
                loadout.append(other)
        if (CollapsedPassageR not in loadout) :
            other=otherDoor(CollapsedPassageR,Connections)
            if (other in loadout) :
                loadout.append(CollapsedPassageR)
            elif (VulnarDepthsElevatorEL in loadout) and pinkDoor and canUsePB and (Super in loadout) and (energyCount > 7) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(CollapsedPassageR)
                loadout.append(other)
            elif (VulnarDepthsElevatorER in loadout) and pinkDoor and canUsePB and (Super in loadout) and (energyCount > 7) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(CollapsedPassageR)
                loadout.append(other)
            elif (SequesteredInfernoL in loadout) and jumpAble and pinkDoor and canUsePB and (Super in loadout) and (energyCount > 7) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(CollapsedPassageR)
                loadout.append(other)
        if (MagmaPumpL not in loadout) :
            other=otherDoor(MagmaPumpL,Connections)
            if (other in loadout) :
                loadout.append(MagmaPumpL)
            elif (ReservoirMaintenanceTunnelR in loadout) and jumpAble and (((Plasma in loadout) and wave) or ((Hypercharge in loadout) and (Charge in loadout))) and (energyCount > 3) and canUseBombs:
                loadout.append(MagmaPumpL)
                loadout.append(other)
            elif (IntakePumpR in loadout) and jumpAble and underwater and (((Plasma in loadout) and wave) or ((Hypercharge in loadout) and (Charge in loadout))) and (energyCount > 3) and canUsePB and ((MetroidSuit in loadout) or (Screw in loadout)):
                loadout.append(MagmaPumpL)
                loadout.append(other)
            elif (ThermalReservoir1R in loadout) and jumpAble and underwater and (((Plasma in loadout) and wave) or ((Hypercharge in loadout) and (Charge in loadout))) and (energyCount > 3) and (MetroidSuit in loadout) and (Screw in loadout):
                loadout.append(MagmaPumpL)
                loadout.append(other)
            elif (GeneratorAccessTunnelL in loadout) and jumpAble and underwater and (((Plasma in loadout) and wave) or ((Hypercharge in loadout) and (Charge in loadout))) and (energyCount > 3) and canUsePB and (MetroidSuit in loadout) and (Screw in loadout):
                loadout.append(MagmaPumpL)
                loadout.append(other)
        if (ReservoirMaintenanceTunnelR not in loadout) :
            other=otherDoor(ReservoirMaintenanceTunnelR,Connections)
            if (other in loadout) :
                loadout.append(ReservoirMaintenanceTunnelR)
            elif (MagmaPumpL in loadout) and jumpAble and (((Plasma in loadout) and wave) or ((Hypercharge in loadout) and (Charge in loadout))) and (energyCount > 3) and canUseBombs:
                loadout.append(ReservoirMaintenanceTunnelR)
                loadout.append(other)
            elif (IntakePumpR in loadout) and jumpAble and canUsePB and underwater and ((MetroidSuit in loadout) or (breakIce and (Screw in loadout))):
                loadout.append(ReservoirMaintenanceTunnelR)
                loadout.append(other)
            elif (ThermalReservoir1R in loadout) and jumpAble and canUseBombs and underwater and (Screw in loadout) and (MetroidSuit in loadout) and (energyCount > 3): 
                loadout.append(ReservoirMaintenanceTunnelR)
                loadout.append(other)
            elif (GeneratorAccessTunnelL in loadout) and jumpAble and canUsePB and underwater and (Screw in loadout) and (MetroidSuit in loadout): 
                loadout.append(ReservoirMaintenanceTunnelR)
                loadout.append(other)
        if (IntakePumpR not in loadout) :
            other=otherDoor(IntakePumpR,Connections)
            if (other in loadout) :
                loadout.append(IntakePumpR)
            elif (MagmaPumpL in loadout) and jumpAble and underwater and (((Plasma in loadout) and wave) or ((Hypercharge in loadout) and (Charge in loadout))) and (energyCount > 3) and canUsePB and ((MetroidSuit in loadout) or (Screw in loadout)):
                loadout.append(IntakePumpR)
                loadout.append(other)
            elif (ReservoirMaintenanceTunnelR in loadout) and jumpAble and canUsePB and underwater and ((MetroidSuit in loadout) or (breakIce and (Screw in loadout))):
                loadout.append(IntakePumpR)
                loadout.append(other)
            elif (ThermalReservoir1R in loadout) and jumpAble and canUsePB and underwater and (Screw in loadout) and (MetroidSuit in loadout) and (energyCount > 3): 
                loadout.append(IntakePumpR)
                loadout.append(other)
            elif (GeneratorAccessTunnelL in loadout) and jumpAble and canUsePB and underwater and (Screw in loadout) and (MetroidSuit in loadout): 
                loadout.append(IntakePumpR)
                loadout.append(other)
        if (ThermalReservoir1R not in loadout) :
            other=otherDoor(ThermalReservoir1R,Connections)
            if (other in loadout) :
                loadout.append(ThermalReservoir1R)
            elif (MagmaPumpL in loadout) and jumpAble and underwater and (((Plasma in loadout) and wave) or ((Hypercharge in loadout) and (Charge in loadout))) and (energyCount > 3) and (MetroidSuit in loadout) and (Screw in loadout):
                loadout.append(ThermalReservoir1R)
                loadout.append(other)
            elif (ReservoirMaintenanceTunnelR in loadout) and jumpAble and canUseBombs and underwater and (Screw in loadout) and (MetroidSuit in loadout) and (energyCount > 3): 
                loadout.append(ThermalReservoir1R)
                loadout.append(other)
            elif (IntakePumpR in loadout) and jumpAble and canUsePB and underwater and (Screw in loadout) and (MetroidSuit in loadout) and (energyCount > 3): 
                loadout.append(ThermalReservoir1R)
                loadout.append(other)
            elif (GeneratorAccessTunnelL in loadout) and jumpAble and canUsePB and (MetroidSuit in loadout) and (energyCount > 3): 
                loadout.append(ThermalReservoir1R)
                loadout.append(other)
        if (GeneratorAccessTunnelL not in loadout) :
            other=otherDoor(GeneratorAccessTunnelL,Connections)
            if (other in loadout) :
                loadout.append(GeneratorAccessTunnelL)
            elif (MagmaPumpL in loadout) and jumpAble and underwater and (((Plasma in loadout) and wave) or ((Hypercharge in loadout) and (Charge in loadout))) and (energyCount > 3) and canUsePB and (MetroidSuit in loadout) and (Screw in loadout):
                loadout.append(GeneratorAccessTunnelL)
                loadout.append(other)
            elif (ReservoirMaintenanceTunnelR in loadout) and jumpAble and canUsePB and underwater and (Screw in loadout) and (MetroidSuit in loadout): 
                loadout.append(GeneratorAccessTunnelL)
                loadout.append(other)
            elif (IntakePumpR in loadout) and jumpAble and canUsePB and underwater and (Screw in loadout) and (MetroidSuit in loadout): 
                loadout.append(GeneratorAccessTunnelL)
                loadout.append(other)
            elif (ThermalReservoir1R in loadout) and jumpAble and canUsePB and (MetroidSuit in loadout) and (energyCount > 3): 
                loadout.append(GeneratorAccessTunnelL)
                loadout.append(other)
        if (ElevatorToMagmaLakeR not in loadout) :
            other=otherDoor(ElevatorToMagmaLakeR,Connections)
            if (other in loadout) :
                loadout.append(ElevatorToMagmaLakeR)
            elif (MagmaPumpAccessR in loadout) and jumpAble and underwater and (MetroidSuit in loadout) and canUsePB:
                loadout.append(ElevatorToMagmaLakeR)
                loadout.append(other)
        if (MagmaPumpAccessR not in loadout) :
            other=otherDoor(MagmaPumpAccessR,Connections)
            if (other in loadout) :
                loadout.append(MagmaPumpAccessR)
            elif (ElevatorToMagmaLakeR in loadout) and jumpAble and underwater and (MetroidSuit in loadout) and canUsePB:
                loadout.append(MagmaPumpAccessR)
                loadout.append(other)
        if (FieryGalleryL not in loadout) :
            other=otherDoor(FieryGalleryL,Connections)
            if (other in loadout) :
                loadout.append(FieryGalleryL)
            elif (RagingPitL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and canUseBombs and (Super in loadout) :
                loadout.append(FieryGalleryL)
                loadout.append(other)
            elif (HollowChamberR in loadout) and jumpAble and (Morph in loadout) and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and (canUseBombs or (Screw in loadout) or (SpeedBooster in loadout)):
                loadout.append(FieryGalleryL)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and (canUseBombs or (Screw in loadout) or (SpeedBooster in loadout)) and ((Ice in loadout) or canUsePB):
                loadout.append(FieryGalleryL)
                loadout.append(other)
            elif (SporousNookL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and underwater and (canUseBombs or (Screw in loadout) or (Super in loadout) or breakIce):
                loadout.append(FieryGalleryL)
                loadout.append(other)
        if (RagingPitL not in loadout) :
            other=otherDoor(RagingPitL,Connections)
            if (other in loadout) :
                loadout.append(RagingPitL)
            elif (FieryGalleryL in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) :
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (HollowChamberR in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and (Ice in loadout):
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and jumpAble and canUseBombs and  ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and ((Ice in loadout) or canUsePB):
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (SporousNookL in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and underwater:
                loadout.append(RagingPitL)
                loadout.append(other)
        if (HollowChamberR not in loadout) :
            other=otherDoor(HollowChamberR,Connections)
            if (other in loadout) :
                loadout.append(HollowChamberR)
            elif (FieryGalleryL in loadout) and jumpAble and (Morph in loadout) and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and (canUseBombs or (Screw in loadout) or (SpeedBooster in loadout)):
                loadout.append(HollowChamberR)
                loadout.append(other)
            elif (RagingPitL in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and (Ice in loadout):
                loadout.append(HollowChamberR)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 2)) and (Ice in loadout):
                loadout.append(HollowChamberR)
                loadout.append(other)
            elif (SporousNookL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and (Ice in loadout) and (Super in loadout) and underwater:
                loadout.append(HollowChamberR)
                loadout.append(other)
        if (PlacidPoolR not in loadout) :
            other=otherDoor(PlacidPoolR,Connections)
            if (other in loadout) :
                loadout.append(PlacidPoolR)
            elif (FieryGalleryL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and (canUseBombs or (Screw in loadout) or (SpeedBooster in loadout)) and ((Ice in loadout) or canUsePB):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (RagingPitL in loadout) and jumpAble and canUseBombs and  ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and ((Ice in loadout) or canUsePB):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (HollowChamberR in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 2)) and (Ice in loadout):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (SporousNookL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and ((Ice in loadout) or canUsePB) and (Super in loadout) and underwater :
                loadout.append(PlacidPoolR)
                loadout.append(other)
        if (SporousNookL not in loadout) :
            other=otherDoor(SporousNookL,Connections)
            if (other in loadout) :
                loadout.append(SporousNookL)
            elif (FieryGalleryL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and underwater and (canUseBombs or (Screw in loadout) or (Super in loadout) or breakIce):
                loadout.append(SporousNookL)
                loadout.append(other)
            elif (RagingPitL in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and underwater:
                loadout.append(SporousNookL)
                loadout.append(other)
            elif (HollowChamberR in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and (Ice in loadout) and (Super in loadout) and underwater:
                loadout.append(SporousNookL)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and ((Ice in loadout) or canUsePB) and (Super in loadout) and underwater :
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
                loadout: list[Union[Item, AreaDoor]]) -> list[Location]:

    energyCount = 0
    for item in loadout:
        if item == Energy:
            energyCount += 1

    exitSpacePort = True
    jumpAble = exitSpacePort and (GravityBoots in loadout)
    underwater = jumpAble and ((HiJump in loadout) or (GravitySuit in loadout))
    pinkDoor = (Missile in loadout) or (Super in loadout)
    wave = (Wave in loadout) or ((Hypercharge in loadout) and (Charge in loadout))
    vulnar = jumpAble and pinkDoor
    canUseBombs = (Morph in loadout) and ((Bombs in loadout) or (PowerBomb in loadout))
    canUsePB = (Morph in loadout) and (PowerBomb in loadout)
    canFly = jumpAble and ((Morph in loadout) and (Bombs in loadout)) or (SpaceJump in loadout)
    suzi = jumpAble and (Super in loadout) and canUsePB and (Wave in loadout) and (GravitySuit in loadout) and (SpeedBooster in loadout) and (Grapple in loadout)
    breakIce = (Plasma in loadout) or ((Charge in loadout) and (Hypercharge in loadout))
    icePod= ((Ice in loadout) and pinkDoor) or ((Charge in loadout) and (Hypercharge in loadout))
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
                (Super in loadout)
                ),
        "Ocean Vent Supply Depot":
            (
                ((OceanShoreR in loadout) or
                 (EleToTurbidPassageR in loadout)) and
                pinkDoor and
                underwater and
                (Morph in loadout) and
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
                jumpAble and
                pinkDoor and
                canUseBombs
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
                (Morph in loadout)
                ),
        "Eribium Apparatus Room":
            (
                (FieldAccessL in loadout) and
                jumpAble and
                pinkDoor and
                canUseBombs
                ),
        "Hot Spring":
            (
                ((SporousNookL in loadout) or
                 ((EleToTurbidPassageR in loadout) and
                  ((Varia in loadout) or
                   energyCount >5))) and
                jumpAble and
                canUseBombs and
                ((GravitySuit in loadout) or
                 (Speedball in loadout) or
                 ((HiJump in loadout) and
                  (Ice in loadout)))
                ),
        "Epiphreatic Crag":
            (
                (ConstructionSiteL in loadout) and
                jumpAble and
                (Morph in loadout) and
                (((Speedball in loadout) and
                  (HiJump in loadout)) or
                 (GravitySuit in loadout))
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
                ((Varia in loadout) or
                 (energyCount > 8)) and
                (MetroidSuit in loadout)
                ),
        "Burning Depths Cache":
            (
                (MagmaPumpAccessR in loadout) and
                jumpAble and
                canUsePB and
                ((Varia in loadout) or
                 (energyCount > 5)) and
                (MetroidSuit in loadout) and
                ((Spazer in loadout) or
                 (Wave in loadout) or
                 ((Charge in loadout) and
                  (Bombs in loadout)))
                ),
        "Mining Cache":
            (
                (((EleToTurbidPassageR in loadout) and
                  ((Varia in loadout) or
                   (energyCount > 5))) or
                 ((SporousNookL in loadout) and
                  ((GravitySuit in loadout) or
                   (Speedball in loadout) or
                   ((HiJump in loadout) and
                    (Ice in loadout))))) and
                jumpAble and
                (Super in loadout) and
                canUseBombs
                ),
        "Infested Passage":
            (
                jumpAble and
                ((Varia in loadout) or
                 (energyCount > 4)) and
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
                 ((Varia in loadout) or
                  (energyCount > 4)) and
                 icePod) or
                ((SequesteredInfernoL in loadout) and
                 ((MetroidSuit in loadout) or
                  ((Charge in loadout) and
                   (Hypercharge in loadout))) and
                 pinkDoor and
                 ((Varia in loadout) or
                  (energyCount > 3))) or
                ((CollapsedPassageR in loadout) and
                 (Super in loadout) and
                 ((Varia in loadout) or
                  (energyCount > 7)) and
                 canUsePB and
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
                  ((Varia in loadout) or
                   (energyCount > 7))) or
                 ((SequesteredInfernoL in loadout) and
                  ((MetroidSuit in loadout) or
                   ((Charge in loadout) and
                    (Hypercharge in loadout))) and
                  pinkDoor and
                  ((Varia in loadout) or
                   (energyCount > 7))))
                ),
        "Ancient Shaft":
            (
                jumpAble and
                canUsePB and
                (((Varia in loadout) and
                  (energyCount > 6)) or
                 (MetroidSuit in loadout)) and
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
                (((Varia in loadout) or
                  energyCount > 6)) and
                (Grapple in loadout) and
                ((VulnarDepthsElevatorEL in loadout) and
                 canUseBombs and
                 icePod) or
                ((SequesteredInfernoL in loadout) and
                 ((MetroidSuit in loadout) or
                  ((Hypercharge in loadout) and
                   (Charge in loadout))) and
                 (Morph in loadout))
                ),
        "Electromechanical Engine":
            (
                jumpAble and
                (Grapple in loadout) and
                ((Varia in loadout) or
                 energyCount > 3) and
                (Morph in loadout) and
                (((ReservoirMaintenanceTunnelR in loadout) and
                  canUseBombs and
                  ((GravitySuit in loadout) or
                   (HiJump in loadout) or
                   (Ice in loadout)) and
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
                  ((GravitySuit in loadout) or
                   (HiJump in loadout) or
                   (Ice in loadout)) and
                  (Screw in loadout)) or
                 ((ThermalReservoir1R in loadout) and
                  ((Varia in loadout) or
                   energyCount > 3) and
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
                jumpAble
                ),
        "Chamber Of Wind":
            (
                (NorakBrookL in loadout) and
                jumpAble and
                pinkDoor and
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
                (SpeedBooster in loadout)
                ),
        "Crocomire's Energy Station":
            (
                (NorakBrookL in loadout) and
                jumpAble and
                (Super in loadout) and
                (SpeedBooster in loadout)
                ),
        "Wellspring Cache":
            (
                (ElevatorToWellspringL in loadout) and
                jumpAble and
                ((GravitySuit in loadout) or
                 (HiJump in loadout) or
                 (Speedball in loadout) or
                 (Ice in loadout)) and
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
                   (energyCount > 3)) or
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
                (canFly or
                 (SpeedBooster in loadout)) and
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
                (canFly or
                 (SpeedBooster in loadout)) and
                canUseBombs
                ),
        "Ocean Shore: bottom":
            (
                OceanShoreR in loadout
                ),
        "Ocean Shore: top":
            (
                (OceanShoreR in loadout) and
                jumpAble
                ),
        "Sandy Burrow: ETank":  # top
            (
                (OceanShoreR in loadout) and
                underwater and
                (((GravitySuit in loadout) and
                  ((Screw in loadout) or
                   canUseBombs)) or
                 (((Speedball in loadout) or
                   (HiJump in loadout)) and
                  canUseBombs))
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
                ((GravitySuit in loadout) or
                 ((HiJump in loadout) and
                  (Ice in loadout)) or
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
                (Morph in loadout)
                ),
        "Sensor Maintenance: AmmoTank":  # back
            (
                vulnar and
                canUseBombs
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
                ((Varia in loadout or
                  (energyCount > 8))) and
                (MetroidSuit in loadout)                  
                ),
        "Generator Manifold":
            (
                jumpAble and
                (Super in loadout) and
                canUseBombs and
                (((ReservoirMaintenanceTunnelR in loadout) and
                  ((GravitySuit in loadout) or
                   (HiJump in loadout) or
                   (Ice in loadout))) or
                 ((GeneratorAccessTunnelL in loadout) and
                  canUsePB and
                  (MetroidSuit in loadout) and
                  (Screw in loadout)) or
                 ((ThermalReservoir1R in loadout) and
                  ((Varia in loadout) or
                   (energyCount >2)) and
                  (MetroidSuit in loadout)
                  and (Screw in loadout)))
                ),
        "Fiery Crossing Cache":
            (
                (RagingPitL in loadout) and
                jumpAble and
                ((Varia in loadout) or
                 (energyCount >5)) and
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
                ((Varia in loadout) or
                   (energyCount > 7)) and
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
                ((HiJump in loadout) or
                 (GravitySuit in loadout) or
                 (Ice in loadout)) and
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
                (energyCount >3)
                ),
        "Tower Rock Lookout":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                pinkDoor and
                (energyCount >3) and
                (GravitySuit in loadout) and
                canFly
                ),
        "Reef Nook":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                pinkDoor and
                (energyCount >3) and
                (GravitySuit in loadout) and
                canFly
                ),
        "Saline Cache":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                pinkDoor and
                (energyCount >3) and
                (GravitySuit in loadout) and
                canFly and
                (Super in loadout)
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
                (Spazer in loadout)
                ),
        "Sandy Burrow: AmmoTank":  # bottom
            (
                (OceanShoreR in loadout) and
                ((GravitySuit in loadout) or
                 ((HiJump in loadout) and
                   ((Speedball in loadout) or
                    (Ice in loadout)))) and
                (Morph in loadout)
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
                  (DarkVisor in loadout)) or
                 ((FieldAccessL in loadout) and
                  pinkDoor and
                  wave and
                  canUseBombs) or
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
                 ((Varia in loadout) or
                  (energyCount>5)) or
                 ((SporousNookL in loadout) and
                  ((GravitySuit in loadout) or
                   (Speedball in loadout) or
                   ((HiJump in loadout) and
                    (Ice in loadout)))))
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
                (Varia in loadout) and  #BATH ENERGY COUNT??
                (MetroidSuit in loadout) and
                canUseBombs
                ),
        "Hive Main Chamber":
            (
                (VulnarDepthsElevatorEL in loadout) and
                jumpAble and
                ((Varia in loadout) or
                 (energyCount>6)) and
                canUseBombs
                ),
        "Crossway Cache":
            (
                ((VulnarDepthsElevatorEL in loadout) and
                 jumpAble and
                 ((Varia in loadout) or
                  (energyCount>6)) and
                 canUseBombs and
                 icePod) or
                ((SequesteredInfernoL in loadout) and
                 ((Varia in loadout) or
                  (energyCount>3)) and
                 (((Hypercharge in loadout) and
                   (Charge in loadout)) or
                  (MetroidSuit in loadout))) or
                ((CollapsedPassageR in loadout) and
                 (Super in loadout) and
                 ((Varia in loadout) or
                  (energyCount > 7)) and
                 canUsePB and
                 wave)                                   
                ),
        "Slag Heap":  #Sequestered Inferno w Metroid Suit is simplest
            (
                canUseBombs and
                jumpAble and
                (MetroidSuit in loadout) and #Possibly a no-Metroid version?
                ((Varia in loadout) or
                 (energyCount>9)) and
                (((VulnarDepthsElevatorEL in loadout) and
                  ((Ice in loadout) or
                   ((Hypercharge in loadout) and
                    (Charge in loadout)))) or
                 ((SequesteredInfernoL in loadout) and
                  (((Hypercharge in loadout) and
                    (Charge in loadout)) or
                   (MetroidSuit in loadout))) or
                 ((CollapsedPassageR in loadout) and
                  (Super in loadout) and
                  canUsePB and
                  wave))                                     
                ),
        "Hydrodynamic Chamber":
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
                (energyCount > 3)
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
                (energyCount > 3) and
                canUsePB and
                (Super in loadout)
                ),
        "Obscured Vestibule":
            (
                (TramToSuziIslandR in loadout) and
                jumpAble and
                (energyCount > 3) and
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
                (Speedball in loadout)
                ),
        "Magma Chamber":
            (
                (ElevatorToMagmaLakeR in loadout) and
                jumpAble and
                canUsePB and
                (((Varia in loadout) and
                  (Charge in loadout)) or
                 ((MetroidSuit in loadout) and
                  energyCount > 6))
                ),
        "Equipment Locker":
            (
                (WestCorridorR in loadout) and
                jumpAble and
                pinkDoor and
                (underwater or
                 canUseBombs) and
                ((MetroidSuit in loadout) or
                 (Morph in loadout))
                ),
        "Antelier":  # spelled "Antilier" in subversion 1.1
            (
                ((WestCorridorR in loadout) and
                 underwater and
                 ((pinkDoor and
                   (Morph in loadout)) or
                  (Super in loadout))) or
                ((FoyerR in loadout) and
                 underwater and
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
                (SpeedBooster in loadout)
                ),
    }

    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = logic[thisLoc['fullitemname']]

    return unusedLocations
