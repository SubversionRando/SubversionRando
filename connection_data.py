""" data for the connections in area rando """
from typing import Union
from item_data import Item, Items
from logicCommon import canUsePB
from logic_shortcut import LogicShortcut


AreaDoor = tuple[str, str, str, str, int]
"""
 - [0] the data of its door
 - [1] the data of the vanilla door that goes here
 - [2] the area
 - [3] the name of the door
 - [4] region
"""


area_doors_unpackable: tuple[AreaDoor, ...] = (
    ('1c678', '5BBB00056E06060000800000', 'Early', 'CraterR', 0),
    ('1c7a4', '2CBA00040106000000800000', 'Early', 'SunkenNestL', 0),
    ('1caf8', 'C2970004115601050080CCA9', 'Early', 'RuinedConcourseBL', 1),
    ('1cbc4', 'C29700051E0601000080B6A9', 'Early', 'RuinedConcourseTR', 1),
    ('1a1e4', '2FA300013E06030000800000', 'Early', 'CausewayR', 1),
    ('1c8c4', '578800052E06020000800000', 'Early', 'SporeFieldTR', 1),
    ('1a2ec', '578800053E4603040080E4A6', 'Early', 'SporeFieldBR', 1),
    ('1ca74', '0F8500057E26070200800000', 'SandLand', 'OceanShoreR', 0),
    ('1c15c', '73CC00050E26000200800000', 'SandLand', 'EleToTurbidPassageR', 2),
    ('1c66c', '879F00040116000100800000', 'SandLand', 'PileAnchorL', 0),
    ('1a130', '19EC00000206000000800000', 'PirateLab', 'ExcavationSiteL', 1),
    ('1bed4', 'B7E100050E16000100800000', 'PirateLab', 'WestCorridorR', 3),
    ('197c4', 'CD8A00051E06010000800000', 'PirateLab', 'FoyerR', 3),
    ('1c900', 'EB9E00040136000300800000', 'PirateLab', 'ConstructionSiteL', 1),
    ('194b8', '3CBF00056E06060000800000', 'PirateLab', 'AlluringCenoteR', 3),
    ('1a454', '71A000040106000000800000', 'ServiceSector', 'FieldAccessL', 1),
    ('1a0f4', 'B89B00051E06010000800000', 'ServiceSector', 'TransferStationR', 1),
    ('1c8f4', '3A8100052E06020000800000', 'ServiceSector', 'CellarR', 1),
    ('1c864', 'CC9300040126000200800000', 'ServiceSector', 'SubbasementFissureL', 1),
    ('1c6e4', 'C78100040126000200800000', 'SkyWorld', 'WestTerminalAccessL', 0),
    ('1a4f0', '93A200040146000400800000', 'SkyWorld', 'MezzanineConcourseL', 1),
    ('19788', '598B00044166040600800000', 'SkyWorld', 'VulnarCanyonL', 3),
    ('195d8', '9F8B00012E06020000800000', 'SkyWorld', 'CanyonPassageR', 3),
    ('1c2f4', 'BAED00040136000300800000', 'SkyWorld', 'ElevatorToCondenserL', 2),
    ('1bf4c', '8B9000040216000120010000', 'SpacePort', 'LoadingDockSecurityAreaL', 3),
    ('1cb7c', '36CD00040126000200800000', 'LifeTemple', 'ElevatorToWellspringL', 2),
    ('1965c', 'E58B00000126000200800000', 'LifeTemple', 'NorakBrookL', 3),
    ('1a0b8', '6F8900051E06010000800000', 'LifeTemple', 'NorakPerimeterTR', 3),
    ('1bad8', '6F890004012600020080ACA7', 'LifeTemple', 'NorakPerimeterBL', 3),
    ('1c87c', 'A9A100040106000000800000', 'FireHive', 'VulnarDepthsElevatorEL', 1),
    ('1c888', 'A9A100050E06000000800000', 'FireHive', 'VulnarDepthsElevatorER', 1),
    ('1bd84', 'E5D500040146000400800000', 'FireHive', 'HiveBurrowL', 2),
    ('1c4b0', '84F300040116000100800000', 'FireHive', 'SequesteredInfernoL', 2),
    ('1cb04', '89CB00051E06010000800000', 'FireHive', 'CollapsedPassageR', 2),
    ('1c2e8', 'A0BE00040106000000800000', 'Geothermal', 'MagmaPumpL', 2),
    ('1c414', 'B0F100051E160101008020A6', 'Geothermal', 'ReservoirMaintenanceTunnelR', 2),
    ('1c4c8', '0FF300052E06020000800000', 'Geothermal', 'IntakePumpR', 2),
    ('1cbac', 'F09C00055E06050000800000', 'Geothermal', 'ThermalReservoir1R', 2),
    ('1c1b0', 'F4CF00043106030000800000', 'Geothermal', 'GeneratorAccessTunnelL', 2),
    ('1c0fc', '67EF00050E06000000800000', 'DrayLand', 'ElevatorToMagmaLakeR', 2),
    ('1c2b8', 'E99700050E06000000800000', 'DrayLand', 'MagmaPumpAccessR', 2),
    ('1c174', 'D7CB00040116000100800000', 'Verdite', 'FieryGalleryL', 2),
    ('1c12c', '2FEE00040116000100800000', 'Verdite', 'RagingPitL', 2),
    ('1c108', '1BD000051E06010000800000', 'Verdite', 'HollowChamberR', 2),
    ('1c8a0', 'CBA300051E06010000800000', 'Verdite', 'PlacidPoolR', 1),
    ('1a340', 'A59300040106000000800000', 'Verdite', 'SporousNookL', 1),
    ('1bac0', 'E38800040116000100800000', 'Daphne', 'RockyRidgeTrailL', 3),
    ('1c7ec', '23A000050E06000000800000', 'Suzi', 'TramToSuziIslandR', 0),
)

area_doors: dict[str, AreaDoor] = {
    door[3]: door
    for door in area_doors_unpackable
}

vanilla_doors: dict[AreaDoor, Union[Item, LogicShortcut]] = {
    area_doors["CraterR"]: canUsePB,
    area_doors["WestTerminalAccessL"]: canUsePB,
    area_doors["VulnarCanyonL"]: canUsePB,
    area_doors["FoyerR"]: Items.Super
}

# to make sure this unpacking list is correct:
# print(f"({', '.join([c[3] for c in connections_unpackable])})")

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


def VanillaAreas() -> list[tuple[AreaDoor, AreaDoor]]:

    return [(CraterR, WestTerminalAccessL),
            (SunkenNestL, OceanShoreR),
            (RuinedConcourseBL, TransferStationR),
            (RuinedConcourseTR, MezzanineConcourseL),
            (CausewayR, ExcavationSiteL),
            (SporeFieldTR, FieldAccessL),
            (SporeFieldBR, SporousNookL),
            (EleToTurbidPassageR, FieryGalleryL),
            (PileAnchorL, TramToSuziIslandR),
            (WestCorridorR, LoadingDockSecurityAreaL),
            (FoyerR, VulnarCanyonL),
            (ConstructionSiteL, CellarR),
            (AlluringCenoteR, NorakPerimeterBL),
            (SubbasementFissureL, VulnarDepthsElevatorER),
            (CanyonPassageR, NorakBrookL),
            (ElevatorToCondenserL, IntakePumpR),
            (ElevatorToWellspringL, CollapsedPassageR),
            (NorakPerimeterTR, RockyRidgeTrailL),
            (VulnarDepthsElevatorEL, PlacidPoolR),
            (HiveBurrowL, ThermalReservoir1R),
            (SequesteredInfernoL, ReservoirMaintenanceTunnelR),
            (MagmaPumpL, MagmaPumpAccessR),
            (GeneratorAccessTunnelL, HollowChamberR),
            (ElevatorToMagmaLakeR, RagingPitL)]
