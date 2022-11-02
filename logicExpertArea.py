from typing import Union

from item_data import Item, items_unpackable
from location_data import Location

# Expert logic updater
# For area rando
# updates unusedLocations

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

(
    Missile, Super, PowerBomb, Morph, GravityBoots, Speedball, Bombs, HiJump,
    GravitySuit, DarkVisor, Wave, SpeedBooster, Spazer, Varia, Ice, Grapple,
    MetroidSuit, Plasma, Screw, Hypercharge, Charge, Xray, SpaceJump, Energy,
    Refuel, SmallAmmo, LargeAmmo, DamageAmp, ChargeAmp, SpaceJumpBoost,
    spaceDrop
) = items_unpackable


Entrance = tuple[str, str, str, str, int]


def updateLogic(unusedLocations: list[Location],
                locArray: list[Location],
                loadout: list[Union[Item, Entrance]]) -> list[Location]:

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
    canFly = (Bombs in loadout) or (SpaceJump in loadout)
    suzi = jumpAble and (Super in loadout) and canUsePB and (Wave in loadout) and (GravitySuit in loadout) and (SpeedBooster in loadout) and (Grapple in loadout)
    breakIce = (Plasma in loadout) or ((Charge in loadout) and (Hypercharge in loadout))
    # onAndOff = ON varia ice PB grapple OFF Hyper charge

    logic = {
        "Impact Crater: AccelCharge":
            exitSpacePort and jumpAble and (Morph in loadout) and (Spazer in loadout) and ((HiJump in loadout) or (SpeedBooster in loadout) or canFly),
        "Subterranean Burrow":
            exitSpacePort and ((Morph in loadout) or (GravityBoots in loadout)),
        "Sandy Cache":
            (OceanShoreR in loadout) and jumpAble and (Missile in loadout) and ((Morph in loadout) or (GravitySuit in loadout)),
        "Submarine Nest":
            (OceanShoreR in loadout) and underwater and pinkDoor,
        "Shrine Of The Penumbra":
            (OceanShoreR in loadout) and jumpAble and pinkDoor and (GravitySuit in loadout) and (canUsePB or (canUseBombs and (DarkVisor in loadout))),
        "Benthic Cache Access":
            ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and underwater and underwater and canUsePB and (Super in loadout),
        "Benthic Cache":
            ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and underwater and underwater and canUseBombs and (Super in loadout),
        "Ocean Vent Supply Depot":
            ((OceanShoreR in loadout) or (EleToTurbidPassageR in loadout)) and underwater and underwater and (Morph in loadout) and ((Super in loadout) or (Screw in loadout)),
        "Sediment Flow":
            (OceanShoreR in loadout) and jumpAble and underwater and (Super in loadout),
        "Harmonic Growth Enhancer":
            (FieldAccessL in loadout) and jumpAble and pinkDoor and canUseBombs,
        "Upper Vulnar Power Node":
            jumpAble and pinkDoor and canUsePB and (Screw in loadout) and (MetroidSuit in loadout),
        "Grand Vault":
            jumpAble and pinkDoor and (Grapple in loadout),
        "Cistern":
            (RuinedConcourseBL in loadout) and jumpAble and canUseBombs,
        "Warrior Shrine: ETank":
            (RuinedConcourseBL in loadout) and jumpAble and pinkDoor and canUsePB,
        "Vulnar Caves Entrance":
            jumpAble and pinkDoor,
        "Crypt":
            (RuinedConcourseBL in loadout) and jumpAble and canUseBombs and pinkDoor and ((Wave in loadout) or (Bombs in loadout)),
        "Archives: SpringBall":  # yes it's actually Speed Ball, uses Spring data
            jumpAble and pinkDoor and (Speedball in loadout),
        "Archives: SJBoost":
            jumpAble and pinkDoor and (Speedball in loadout) and (SpeedBooster in loadout),
        "Sensor Maintenance: ETank":  # front
            vulnar and (Morph in loadout),
        "Eribium Apparatus Room":
            (FieldAccessL in loadout) and jumpAble and pinkDoor and canUseBombs,
        "Hot Spring":
            (((SporousNookL in loadout) and jumpAble and (canUseBombs or (Super in loadout) or (Plasma in loadout))) or ((EleToTurbidPassageR in loadout) and ((Varia in loadout) or energyCount >4))) and ((GravitySuit in loadout) or (Speedball in loadout)) and ((HiJump in loadout) or (Ice in loadout)),
        "Epiphreatic Crag":
            (ConstructionSiteL in loadout) and underwater and (Morph in loadout) and ((Speedball in loadout) or (GravitySuit in loadout)),
        "Mezzanine Concourse":
            (MezzanineConcourseL in loadout) and jumpAble and (WestTerminalAccessL in loadout),
        "Greater Inferno":
            (MagmaPumpAccessR in loadout) and jumpAble and canUsePB and (Super in loadout) and (GravitySuit in loadout) and (Varia in loadout) and (MetroidSuit in loadout) and (canUseBombs or (Speedball in loadout)),
        "Burning Depths Cache":
            (MagmaPumpAccessR in loadout) and jumpAble and canUsePB and (GravitySuit in loadout) and (Varia in loadout) and (MetroidSuit in loadout) and ((Spazer in loadout) or (Wave in loadout)),
        "Mining Cache":
            (((EleToTurbidPassageR in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4))) or ((SporousNookL in loadout) and underwater)) and (Super in loadout) and canUseBombs,
        "Infested Passage":
            jumpAble and ((Varia in loadout) or (energyCount > 4)) and ((VulnarDepthsElevatorEL in loadout) and canUseBombs) or ((SequesteredInfernoL in loadout) and ((MetroidSuit in loadout) or ((Hypercharge in loadout) and (Charge in loadout))) and (Ice in loadout)),
        "Fire's Boon Shrine":
            ((VulnarDepthsElevatorEL in loadout) and jumpAble and canUseBombs and pinkDoor and ((Varia in loadout) or (energyCount > 4)) and (Ice in loadout)) or ((SequesteredInfernoL in loadout) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))) and pinkDoor and ((Varia in loadout) or (energyCount > 3))) or ((CollapsedPassageR in loadout) and (Super in loadout) and ((Varia in loadout) or (energyCount > 7)) and canUsePB and wave),
        "Fire's Bane Shrine":
            ((VulnarDepthsElevatorEL in loadout) and jumpAble and canUseBombs and pinkDoor and ((Varia in loadout) or (energyCount > 7)) and ((Ice in loadout) or ((Hypercharge in loadout) and (Charge in loadout)))) or ((SequesteredInfernoL in loadout) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))) and pinkDoor and ((Varia in loadout) or (energyCount > 7))) or ((CollapsedPassageR in loadout) and (Super in loadout) and ((Varia in loadout) or (energyCount > 7)) and canUsePB and wave),
        "Ancient Shaft":
            jumpAble and ((MetroidSuit in loadout) and ((VulnarDepthsElevatorEL in loadout) and canUseBombs and pinkDoor and ((Varia in loadout) or (energyCount > 7)) and (Ice in loadout)) or ((SequesteredInfernoL in loadout) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))) and pinkDoor and ((Varia in loadout) or (energyCount > 7))) or ((CollapsedPassageR in loadout) and (Super in loadout) and ((Varia in loadout) or (energyCount > 7)) and canUsePB and wave)),
        "Gymnasium":
            (jumpAble and (Grapple in loadout) and ((VulnarDepthsElevatorEL in loadout) and canUseBombs and pinkDoor and ((Varia in loadout) or (energyCount > 7)) and (Ice in loadout)) or ((SequesteredInfernoL in loadout) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))) and pinkDoor and ((Varia in loadout) or (energyCount > 7))) or ((CollapsedPassageR in loadout) and (Super in loadout) and ((Varia in loadout) or (energyCount > 7)) and canUsePB and wave)),
        "Electromechanical Engine":
            jumpAble and (Grapple in loadout) and ((Varia in loadout) or energyCount > 3) and (Morph in loadout) and (((ReservoirMaintenanceTunnelR in loadout) and canUseBombs and underwater and (Screw in loadout)) or((ThermalReservoir1R in loadout) and (MetroidSuit in loadout)) or((GeneratorAccessTunnelL in loadout) and canUsePB and (MetroidSuit in loadout))),
        "Depressurization Valve":
            jumpAble and (Grapple in loadout) and (Morph in loadout) and (((ReservoirMaintenanceTunnelR in loadout) and canUseBombs and underwater and (Screw in loadout)) or ((ThermalReservoir1R in loadout) and ((Varia in loadout) or energyCount > 3) and (MetroidSuit in loadout)) or ((GeneratorAccessTunnelL in loadout) and canUsePB and (MetroidSuit in loadout))),
        "Loading Dock Storage Area":
            (LoadingDockSecurityAreaL in loadout),
        "Containment Area":
            jumpAble and ((FoyerR in loadout) and ((MetroidSuit in loadout) or (Screw in loadout))) or ((AlluringCenoteR in loadout) and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and canUsePB),
        "Briar: SJBoost":  # top
            (NorakBrookL in loadout) and jumpAble and canUsePB,
        "Shrine Of Fervor":
            (NorakBrookL in loadout) and jumpAble,
        "Chamber Of Wind":
            (NorakBrookL in loadout) and jumpAble and pinkDoor and (canUseBombs or ((Screw in loadout) and (Speedball in loadout) and (Morph in loadout)) and (SpeedBooster in loadout)),
        "Water Garden":
            (NorakBrookL in loadout) and jumpAble and (SpeedBooster in loadout),
        "Crocomire's Energy Station":
            (NorakBrookL in loadout) and jumpAble and (Super in loadout) and (SpeedBooster in loadout),
        "Wellspring Cache":
            (ElevatorToWellspringL in loadout) and jumpAble and underwater and (Super in loadout) and (Morph in loadout),
        "Frozen Lake Wall: DamageAmp":
            (ElevatorToCondenserL in loadout) and jumpAble and canUsePB,
        "Grand Promenade":
            (WestTerminalAccessL in loadout) and jumpAble,
        "Summit Landing":
            (WestTerminalAccessL in loadout) and jumpAble and canUseBombs,
        "Snow Cache":
            (WestTerminalAccessL in loadout) and jumpAble and canUseBombs,
        "Reliquary Access":
            (WestTerminalAccessL in loadout) and jumpAble and (Super in loadout) and (DarkVisor in loadout),
        "Syzygy Observatorium":
            (WestTerminalAccessL in loadout) and jumpAble and ((Screw in loadout) or (((Super in loadout) and (MetroidSuit in loadout) and (energyCount > 3)) or ((Hypercharge in loadout) and (Charge in loadout)))),
        "Armory Cache 2":
            (WestTerminalAccessL in loadout) and jumpAble and ((Screw in loadout) or ((Super in loadout) and (DarkVisor in loadout))),
        "Armory Cache 3":
            (WestTerminalAccessL in loadout) and jumpAble and ((Screw in loadout) or ((Super in loadout) and (DarkVisor in loadout))),
        "Drawing Room":
            (WestTerminalAccessL in loadout) and jumpAble and (Super in loadout),
        "Impact Crater Overlook":
            jumpAble and canFly and canUseBombs and (canUsePB or (Super in loadout)),
        "Magma Lake Cache":
            (ElevatorToMagmaLakeR in loadout) and jumpAble and (Ice in loadout) and (Morph in loadout),
        "Shrine Of The Animate Spark":
            (TramToSuziIslandR in loadout) and suzi and canFly and (Hypercharge in loadout) and (Charge in loadout),
        "Docking Port 4":  # (4 = letter Omega)
            ((spaceDrop not in loadout) and (Grapple in loadout)) or ((spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and jumpAble and (MetroidSuit in loadout)),
        "Ready Room":
            ((spaceDrop not in loadout) and (Super in loadout)) or ((spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and jumpAble and (MetroidSuit in loadout) and (Grapple in loadout) and (Super in loadout)),
        "Torpedo Bay":
            True,
        "Extract Storage":
            (canUsePB and (spaceDrop not in loadout)) or ((spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and jumpAble and (Grapple in loadout) and (MetroidSuit in loadout)),
        "Impact Crater Alcove":
            jumpAble and canFly and canUseBombs,
        "Ocean Shore: bottom":
            (OceanShoreR in loadout),
        "Ocean Shore: top":
            (OceanShoreR in loadout) and jumpAble,
        "Sandy Burrow: ETank":  # top
            (OceanShoreR in loadout) and underwater and (((GravitySuit in loadout) and ((Screw in loadout) or canUseBombs)) or ((Speedball in loadout) and canUseBombs)),
        "Submarine Alcove":
            ((OceanShoreR in loadout) and underwater and (Morph in loadout) and (((DarkVisor in loadout) and pinkDoor) or (Super in loadout))) or ((EleToTurbidPassageR in loadout) and (Super in loadout) and underwater and (Morph in loadout) and (Speedball in loadout)),
        "Sediment Floor":
            ((OceanShoreR in loadout) and underwater and (Morph in loadout) and (((DarkVisor in loadout) and pinkDoor) or (Super in loadout))) or ((EleToTurbidPassageR in loadout) and pinkDoor and underwater and (Morph in loadout) and (Speedball in loadout)),
        "Sandy Gully":
            (OceanShoreR in loadout) and underwater and (Super in loadout),
        "Hall Of The Elders":
            (RuinedConcourseBL in loadout) and (underwater or pinkDoor),
        "Warrior Shrine: AmmoTank bottom":
            (RuinedConcourseBL in loadout) and jumpAble and (Morph in loadout) and pinkDoor,
        "Warrior Shrine: AmmoTank top":
            (RuinedConcourseBL in loadout) and jumpAble and canUseBombs and pinkDoor,
        "Path Of Swords":
            vulnar and (canUseBombs or ((Morph in loadout) and (Screw in loadout))),
        "Auxiliary Pump Room":
            vulnar and canUseBombs,
        "Monitoring Station":
            vulnar and (Morph in loadout),
        "Sensor Maintenance: AmmoTank":  # back
            vulnar and canUseBombs,
        "Causeway Overlook":
            (CausewayR in loadout) and jumpAble and canUseBombs,
        "Placid Pool":
            (PlacidPoolR in loadout) and jumpAble and canUsePB and (Ice in loadout),
        "Blazing Chasm":
            (ElevatorToMagmaLakeR in loadout) and jumpAble and canUsePB and (Varia in loadout) and (MetroidSuit in loadout),
        "Generator Manifold":
            jumpAble and (Super in loadout) and canUseBombs and (((ReservoirMaintenanceTunnelR in loadout) and underwater) or ((GeneratorAccessTunnelL in loadout) and canUsePB and (MetroidSuit in loadout) and (Screw in loadout)) or ((ThermalReservoir1R in loadout) and ((Varia in loadout) or (energyCount >2)) and (MetroidSuit in loadout) and (Screw in loadout))),
        "Fiery Crossing Cache":
            (RagingPitL in loadout) and jumpAble and ((Varia in loadout) or (energyCount >5)) and canUsePB,
        "Dark Crevice Cache":
            (ElevatorToMagmaLakeR in loadout) and jumpAble and canUseBombs and canFly and (DarkVisor in loadout),
        "Ancient Basin":
            (((VulnarDepthsElevatorEL in loadout) and jumpAble  and canUseBombs and pinkDoor and ((Varia in loadout) or (energyCount > 7)) and (Ice in loadout)) or ((SequesteredInfernoL in loadout) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))) and pinkDoor and ((Varia in loadout) or (energyCount > 7))) or ((CollapsedPassageR in loadout) and (Super in loadout) and ((Varia in loadout) or (energyCount > 7)) and canUsePB and wave)),
        "Central Corridor: right":
            (FoyerR in loadout) and jumpAble  and ((HiJump in loadout) or (GravitySuit in loadout) or (Ice in loadout)) and canUseBombs,
        "Briar: AmmoTank":  # bottom
            (NorakBrookL in loadout) and jumpAble and (Morph in loadout),
        "Icy Flow":
            (WestTerminalAccessL in loadout) and jumpAble and (SpeedBooster in loadout) and breakIce,
        "Ice Cave":
            (WestTerminalAccessL in loadout) and jumpAble and breakIce,
        "Antechamber":
            (WestTerminalAccessL in loadout) and jumpAble and canUsePB,
        "Eddy Channels":
            (EleToTurbidPassageR in loadout) and underwater and (Speedball in loadout) and (Super in loadout),
        "Tram To Suzi Island":
            (TramToSuziIslandR in loadout) and jumpAble and (Spazer in loadout) and (Morph in loadout),
        "Portico":
            (TramToSuziIslandR in loadout) and jumpAble and (Super in loadout) and (energyCount >3),
        "Tower Rock Lookout":
            (TramToSuziIslandR in loadout) and jumpAble and pinkDoor and (energyCount >3) and (GravitySuit in loadout) and canFly,
        "Reef Nook":
            (TramToSuziIslandR in loadout) and jumpAble and pinkDoor and (energyCount >3) and (GravitySuit in loadout) and canFly and canUseBombs,
        "Saline Cache":
            (TramToSuziIslandR in loadout) and jumpAble and pinkDoor and (energyCount >3) and (GravitySuit in loadout) and canFly and (Super in loadout),
        "Enervation Chamber":
            (TramToSuziIslandR in loadout) and suzi and canFly and (Hypercharge in loadout) and (Charge in loadout),
        "Weapon Locker":
            ((spaceDrop not in loadout) and pinkDoor) or ((spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and jumpAble and (MetroidSuit in loadout) and pinkDoor),
        "Aft Battery":
            ((spaceDrop not in loadout) and (Morph in loadout)) or ((spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and jumpAble and (MetroidSuit in loadout) and (Grapple in loadout) and (Morph in loadout)),
        "Forward Battery":
            ((spaceDrop not in loadout) and pinkDoor and (Morph in loadout)) or ((spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and jumpAble and (MetroidSuit in loadout) and pinkDoor),
        "Gantry":
            ((spaceDrop not in loadout) and pinkDoor) or ((spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and jumpAble and (MetroidSuit in loadout) and pinkDoor),
        "Garden Canal":
            (NorakBrookL in loadout) and jumpAble and canUsePB and (Spazer in loadout) and ((ElevatorToWellspringL in loadout) or ((HiJump in loadout) or (Ice in loadout) or (SpeedBooster in loadout) or canFly)),
        "Sandy Burrow: AmmoTank":  # bottom
            (OceanShoreR in loadout) and underwater and (Morph in loadout) and ((Speedball in loadout) or (GravitySuit in loadout)),
        "Trophobiotic Chamber":
            vulnar and (Morph in loadout) and (Speedball in loadout),
        "Waste Processing":
            (SpeedBooster in loadout) and jumpAble and (((SubbasementFissureL in loadout) and canUsePB) or ((CellarR in loadout) and pinkDoor and canUseBombs and (DarkVisor in loadout)) or ((FieldAccessL in loadout) and pinkDoor and wave and canUseBombs) or ((TransferStationR in loadout) and (DarkVisor in loadout) and wave and canUseBombs)),
        "Grand Chasm":
            (WestTerminalAccessL in loadout) and jumpAble and canUseBombs and (Screw in loadout),
        "Mining Site 1":  # (1 = letter Alpha)
            canUseBombs and jumpAble and pinkDoor and ((EleToTurbidPassageR in loadout) and ((Varia in loadout) or (energyCount>4)) or ((SporousNookL in loadout) and underwater)),
        "Colosseum":  # GT
            (ElevatorToMagmaLakeR in loadout) and jumpAble and (Varia in loadout) and (Charge in loadout),
        "Lava Pool":
            (EleToTurbidPassageR in loadout) and jumpAble and (Varia in loadout) and (MetroidSuit in loadout) and canUseBombs,
        "Hive Main Chamber":
            (VulnarDepthsElevatorEL in loadout) and jumpAble and ((Varia in loadout) or (energyCount>6)) and canUseBombs,
        "Crossway Cache":
            ((VulnarDepthsElevatorEL in loadout) and jumpAble and ((Varia in loadout) or (energyCount>6)) and canUseBombs and (Ice in loadout) or ((SequesteredInfernoL in loadout) and ((Varia in loadout) or (energyCount>3)) and (((Hypercharge in loadout) and (Charge in loadout)) or (MetroidSuit in loadout))) or ((CollapsedPassageR in loadout) and (Super in loadout) and ((Varia in loadout) or (energyCount > 7)) and canUsePB and wave)),
        "Slag Heap":
            canUseBombs and jumpAble and (MetroidSuit in loadout) and (Varia in loadout) and (((VulnarDepthsElevatorEL in loadout) and ((Ice in loadout) or ((Hypercharge in loadout) and (Charge in loadout)))) or ((SequesteredInfernoL in loadout) and (((Hypercharge in loadout) and (Charge in loadout)) or (MetroidSuit in loadout))) or ((CollapsedPassageR in loadout) and (Super in loadout) and canUsePB and wave)),
        "Hydrodynamic Chamber":
            (WestCorridorR in loadout) and underwater and (Morph in loadout) and pinkDoor and (Spazer in loadout),
        "Central Corridor: left":
            (FoyerR in loadout) and jumpAble and (GravitySuit in loadout) and (Speedball in loadout) and (SpeedBooster in loadout) and (Morph in loadout),
        "Restricted Area":
            (FoyerR in loadout) and jumpAble and (MetroidSuit in loadout),
        "Foundry":
            (FoyerR in loadout) and jumpAble,
        "Norak Escarpment":
            (NorakBrookL in loadout) and jumpAble and (canFly or (SpeedBooster in loadout)),
        "Glacier's Reach":
            (WestTerminalAccessL in loadout) and jumpAble and (energyCount > 3),
        "Sitting Room":
            (WestTerminalAccessL in loadout) and jumpAble and canUsePB and (Speedball in loadout),
        "Suzi Ruins Map Station Access":
            (TramToSuziIslandR in loadout) and jumpAble and (energyCount > 3) and canUsePB and (Super in loadout),
        "Obscured Vestibule":
            (TramToSuziIslandR in loadout) and jumpAble and (energyCount > 3) and canUseBombs,
        "Docking Port 3":  # (3 = letter Gamma)
            ((spaceDrop not in loadout) and (Grapple in loadout)) or ((spaceDrop in loadout) and (LoadingDockSecurityAreaL in loadout) and jumpAble and (MetroidSuit in loadout)),
        "Arena":
            (RuinedConcourseBL in loadout) and jumpAble and pinkDoor,
        "West Spore Field":
            vulnar and (canUseBombs or ((Morph in loadout) and (Screw in loadout))) and (Super in loadout) and (Speedball in loadout),
        "Magma Chamber":
            (ElevatorToMagmaLakeR in loadout) and jumpAble and canUsePB and (((Varia in loadout) and (Charge in loadout)) or ((MetroidSuit in loadout) and energyCount > 6)),
        "Equipment Locker":
            (WestCorridorR in loadout) and jumpAble and pinkDoor and (underwater or canUseBombs) and ((MetroidSuit in loadout) or (Morph in loadout)),
        "Antelier":  # spelled "Antilier" in subversion 1.1
            ((WestCorridorR in loadout) and underwater and ((pinkDoor and (Morph in loadout)) or (Super in loadout))) or ((FoyerR in loadout) and underwater and (Screw in loadout)),
        "Weapon Research":
            (FoyerR in loadout) and jumpAble and (wave or (MetroidSuit in loadout)) and (canUseBombs or (Spazer in loadout)),
        "Crocomire's Lair":
            (NorakBrookL in loadout) and jumpAble and (Super in loadout) and (SpeedBooster in loadout),
    }

    # print("Updating logic...")
    for thisLoc in unusedLocations:
        thisLoc['inlogic'] = logic[thisLoc['fullitemname']]

    return unusedLocations
