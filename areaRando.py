import random
from romWriter import RomWriter
from item_data import items_unpackable

# RandomizeAreas shuffles the locations and checks that the ship connects to daphne properly
# updateAreaLogic is like a logic updater for area doors connecting to other area doors
# -this is done before the item locations are updated

# second version uses
# [0]the door pointer this door needs to send with
# [1]the data that is needed to go to this door


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


def RandomizeAreas(romWriter: RomWriter):
    # Each location holds
    # [0]the data of its door
    # [1]the data of the vanilla door that goes here
    # [2]the area
    # [3]the name of the door
    # [4]region

    def findDaphne(fromDoor):
        # print("fromDoor:",fromDoor[3])
        # print("pathToDaphne:",pathToDaphne)
        testcases = []
        for item in Connections:
            #print("The first item:",len(item),item)
            if (fromDoor in item):
                otherDoor = item[0]
                if fromDoor == otherDoor:
                    otherDoor = item[1]
                #print("Declaring otherDoor: ",otherDoor)
        # print("otherDoor:",otherDoor[3])
        if (otherDoor == RockyRidgeTrailL):
            # print("FoundDaphne:")
            for item in pathToDaphne:
                #print("  ",item[3])
                uu = 0
            return True
        if (otherDoor in pathToDaphne):
            #print("Circling back on",otherDoor)
            return False
        if (otherDoor in [RuinedConcourseBL, RuinedConcourseTR, CausewayR, SporeFieldTR, SporeFieldBR]):
            testcases = [RuinedConcourseBL, RuinedConcourseTR,
                         CausewayR, SporeFieldTR, SporeFieldBR]
        if (otherDoor in [OceanShoreR, EleToTurbidPassageR, PileAnchorL]):
            testcases = [OceanShoreR, EleToTurbidPassageR, PileAnchorL]
        if (otherDoor in [WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR]):
            testcases = [WestTerminalAccessL, MezzanineConcourseL,
                         VulnarCanyonL, CanyonPassageR]
        if (otherDoor in [ElevatorToWellspringL, NorakBrookL, NorakPerimeterTR, NorakPerimeterBL]):
            testcases = [ElevatorToWellspringL, NorakBrookL,
                         NorakPerimeterTR, NorakPerimeterBL]
        if (otherDoor in [ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR]):
            testcases = [ExcavationSiteL, WestCorridorR,
                         FoyerR, ConstructionSiteL, AlluringCenoteR]
        if (otherDoor in [FieldAccessL, TransferStationR, CellarR, SubbasementFissureL]):
            testcases = [FieldAccessL, TransferStationR,
                         CellarR, SubbasementFissureL]
        if (otherDoor in [VulnarDepthsElevatorEL, VulnarDepthsElevatorER, SequesteredInfernoL, CollapsedPassageR]):
            testcases = [VulnarDepthsElevatorEL, VulnarDepthsElevatorER,
                         SequesteredInfernoL, CollapsedPassageR]
        if (otherDoor in [MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR, ThermalReservoir1R, GeneratorAccessTunnelL]):
            testcases = [MagmaPumpL, ReservoirMaintenanceTunnelR,
                         IntakePumpR, ThermalReservoir1R, GeneratorAccessTunnelL]
        if (otherDoor in [ElevatorToMagmaLakeR, MagmaPumpAccessR]):
            testcases = [ElevatorToMagmaLakeR, MagmaPumpAccessR]
        if (otherDoor in [FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR, SporousNookL]):
            testcases = [FieryGalleryL, RagingPitL,
                         HollowChamberR, PlacidPoolR, SporousNookL]
        soFar = False
        if testcases == []:
            return False
        pathToDaphne.append(otherDoor)
        for eachOtherExit in testcases:
            if (eachOtherExit in pathToDaphne) == False:
                pathToDaphne.append(eachOtherExit)
                check = findDaphne(eachOtherExit)
                soFar = (soFar or check)
        return soFar

    areaAttempts = 0
    connected = False
    while connected == False:
        areaAttempts += 1
        if areaAttempts > 1000:
            print("Tried 1000 times. help?")
            connected = True  # This is a lie, but it breaks the loop
        print("**********Trying to get a good escape attempt:", areaAttempts)

        OpenNodesR = [CraterR,
                      RuinedConcourseTR,
                      CausewayR,
                      SporeFieldTR,
                      SporeFieldBR]
        OpenNodesL = [SunkenNestL,
                      RuinedConcourseBL]
        VisitedAreas = ['Early']
        Connections = []

        RightSideDoorsList = [OceanShoreR,
                              EleToTurbidPassageR,
                              WestCorridorR,
                              FoyerR,
                              AlluringCenoteR,
                              TransferStationR,
                              CellarR,
                              CanyonPassageR,
                              NorakPerimeterTR,
                              VulnarDepthsElevatorER,
                              CollapsedPassageR,
                              ReservoirMaintenanceTunnelR,
                              IntakePumpR,
                              ThermalReservoir1R,
                              ElevatorToMagmaLakeR,
                              MagmaPumpAccessR,
                              HollowChamberR,
                              PlacidPoolR,
                              TramToSuziIslandR]

        LeftSideDoorsList = [PileAnchorL,
                             ExcavationSiteL,
                             ConstructionSiteL,
                             FieldAccessL,
                             SubbasementFissureL,
                             WestTerminalAccessL,
                             MezzanineConcourseL,
                             VulnarCanyonL,
                             ElevatorToCondenserL,
                             LoadingDockSecurityAreaL,
                             ElevatorToWellspringL,
                             NorakBrookL,
                             NorakPerimeterBL,
                             VulnarDepthsElevatorEL,
                             HiveBurrowL,
                             SequesteredInfernoL,
                             MagmaPumpL,
                             GeneratorAccessTunnelL,
                             FieryGalleryL,
                             RagingPitL,
                             SporousNookL,
                             RockyRidgeTrailL]
        for h in RightSideDoorsList:
            # print(h[2],h[3])
            uu = 0
        for h in LeftSideDoorsList:
            # print(h[2],h[3])
            uu = 0

        while RightSideDoorsList != [] or LeftSideDoorsList != []:
            #print("Lengths: OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))
            CombinedDoorsList = RightSideDoorsList+LeftSideDoorsList
            # This case is for making sure all areas make it into the map
            # Then all other connections happen later
            randomIndex = 0
            if len(CombinedDoorsList) > 1:
                randomIndex = random.randint(0, len(CombinedDoorsList)-1)
            selectedDoor = CombinedDoorsList[randomIndex]
            if (selectedDoor in RightSideDoorsList) and OpenNodesL != []:
                # It is a right door and there are open Left nodes to connect to
                # if it fails, the loop will try again with no change
                RightSideDoorsList.remove(selectedDoor)
                # Choose a random Left node to connect to
                randomNode = 0
                if len(OpenNodesL) > 1:
                    randomNode = random.randint(0, len(OpenNodesL)-1)
                Connections.append([selectedDoor, OpenNodesL[randomNode]])
                # for DEBUG
                # print('RightSideDoorsList')
                # print('pairing',selectedDoor[2],selectedDoor[3],"--",OpenNodesL[randomNode][2],OpenNodesL[randomNode][3])
                OpenNodesL.remove(OpenNodesL[randomNode])
                # Now add the area to the visitedareas
                # and all nodes from that area
                VisitedAreas = VisitedAreas+[selectedDoor[2]]
                for doorSearch in RightSideDoorsList:
                    if doorSearch[2] in VisitedAreas:
                        OpenNodesR += [doorSearch]
                for doorClean in OpenNodesR:
                    if doorClean in RightSideDoorsList:
                        RightSideDoorsList.remove(doorClean)
            elif (selectedDoor in LeftSideDoorsList) and OpenNodesR != []:
                # It is a left door and there are open right nodes to connect to
                # if it fails, the loop will try again with no change
                LeftSideDoorsList.remove(selectedDoor)
                # Choose a random Right node to connect to
                randomNode = 0
                if len(OpenNodesR) > 1:
                    randomNode = random.randint(0, len(OpenNodesR)-1)
                Connections.append([selectedDoor, OpenNodesR[randomNode]])
                # for DEBUG
                # print('LeftSideDoorsList')
                # print('pairing',selectedDoor[2],selectedDoor[3],"--",OpenNodesR[randomNode][2],OpenNodesR[randomNode][3])
                OpenNodesR.remove(OpenNodesR[randomNode])
                # Now add the area to the visitedareas
                # and all nodes from that area
                VisitedAreas = VisitedAreas + \
                    [selectedDoor[2]]  # add the area string
                for doorSearch in LeftSideDoorsList:
                    if doorSearch[2] in VisitedAreas:
                        OpenNodesL += [doorSearch]
                for doorClean in OpenNodesL:
                    if doorClean in LeftSideDoorsList:
                        LeftSideDoorsList.remove(doorClean)
                #print(len(VisitedAreas),"areas visited")
                # print(VisitedAreas)
        #print("Before connecting OpenNodes")
        #print("Lengths: OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))
        # This section is when all areas have been placed and we just need
        # To connect nodes from OpenNodesL and OpenNodesR
        #print("While connecting OpenNodes:")
        while OpenNodesL != [] and OpenNodesR != []:
            # Should only need to keep track of one since they should match 1:1
            randomL = 0
            if len(OpenNodesL) > 1:
                randomL = random.randint(0, len(OpenNodesL)-1)
            chosenNodeL = OpenNodesL[randomL]
            randomR = 0
            if len(OpenNodesR) > 1:
                randomR = random.randint(0, len(OpenNodesR)-1)
            chosenNodeR = OpenNodesR[randomR]
            Connections.append([chosenNodeL, chosenNodeR])
            OpenNodesL.remove(chosenNodeL)
            OpenNodesR.remove(chosenNodeR)
            #print("    Lengths: OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))
        #print("LeftoverL  ",OpenNodesL)
        #print("LeftoverR  ",OpenNodesR)
        print(len(Connections), "Connections created:")
        for item in Connections:
            print(item[0][2], item[0][3], " << >> ", item[1][2], item[1][3])
            uu = 0
        pathToDaphne = [CraterR, SunkenNestL]
        # check for valid area configuration
        if findDaphne(CraterR) or findDaphne(SunkenNestL):
            connected = True

    # then connect the doors together

    # Now I need to read the OG Subversion rom for 12 bytes at address:Node1[1]
    # and write it into the 12 bytes at Node2[0]
    # Also read the OG Subversion Rom for 12 bytes at address:Node2[1]
    # and write it into the 12 bytes at Node1[0]
    # Tada, area rando
    # But I need to do all the reading before I do any writing so that
    # I am getting the pure original Subversion data

    # do a round of reading the door data for each node
#    for pair in Connections :
#        for node in pair :
#            addressSending=int(node[0],16)
#            addressReceiving=int(node[1],16)
#            rom.seek(addressSending)
#            sendingBytes=rom.read(12)
#            node.append(sendingBytes) #this becomes node[3]
#            rom.seek(addressReceiving)
#            receivingBytes=rom.read(12)
#            node.append(receivingBytes)    #this becomes node[4]
    for pair in Connections:
        node1 = pair[0]
        node2 = pair[1]
        # place data for node1 sending
        romWriter.writeBytes(int(node1[0], 16), int(
            node2[1], 16).to_bytes(12, 'big'))
        # place data for node2 sending
        romWriter.writeBytes(int(node2[0], 16), int(
            node1[1], 16).to_bytes(12, 'big'))
        if node1[4] != node2[4]:
            romWriter.writeBytes(int(node1[0], 16)+2, b"\x40")
            romWriter.writeBytes(int(node2[0], 16)+2, b"\x40")

    # Area rando done?

    # coloring some doors to be flashing
    colorDoorsR = ['3fff70',
                   '3fffa8',
                   '3fe37c',
                   '3ff15e',
                   '3ff1f8',
                   '3fe668',
                   '3fe66e']

    colorDoorsL = ['3ffec4',
                   '3fe352',
                   '3fe35a',
                   '3fe686',
                   '3ffa2c']

    for doorlocid in colorDoorsR:
        romWriter.writeBytes(int(doorlocid, 16),   b"\x42")  # gray type door
        romWriter.writeBytes(int(doorlocid, 16)+5, b"\x98")  # animals subtype
    for doorlocid in colorDoorsL:
        romWriter.writeBytes(int(doorlocid, 16),   b"\x48")  # gray type door
        romWriter.writeBytes(int(doorlocid, 16)+5, b"\x98")  # animals subtype

    return Connections


def otherDoor(door, Connections):
    for pair in Connections:
        if (door in pair):
            other = pair[0]
            if door == other:
                other = pair[1]
    return other
# return these to top later


def updateAreaLogic(availableLocations, locArray, loadout, Connections):
    exitSpacePort = True
    jumpAble = exitSpacePort and (GravityBoots in loadout)
    underwater = jumpAble and ((HiJump in loadout) or (GravitySuit in loadout))
    pinkDoor = (Missile in loadout) or (Super in loadout)
    canUseBombs = (Morph in loadout) and (
        (Bombs in loadout) or (PowerBomb in loadout))
    canUsePB = (Morph in loadout) and (PowerBomb in loadout)
    canFly = canUseBombs or (SpaceJump in loadout)
    wave = (Wave in loadout) or (
        (Charge in loadout) and (Hypercharge in loadout))
    breakIce = (Plasma in loadout) or (
        (Charge in loadout) and (Hypercharge in loadout))
    energyCount = 0
    for item in loadout:
        if item == Energy:
            energyCount += 1
    movement = False  # check if loadout keeps increasing
    while movement == False:
        tempLoadout = []
        tempLoadout.extend(loadout)
        if (SunkenNestL in loadout) == False:
            other = otherDoor(SunkenNestL, Connections)
            loadout.append(SunkenNestL)
            loadout.append(other)
        if (CraterR in loadout) == False:
            other = otherDoor(CraterR, Connections)
            if canFly and canUsePB:
                loadout.append(CraterR)
                loadout.append(other)
        if (RuinedConcourseBL in loadout) == False:
            other = otherDoor(RuinedConcourseBL, Connections)
            if (other in loadout):
                loadout.append(RuinedConcourseBL)
            elif jumpAble and (Missile in loadout) and (Morph in loadout):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (RuinedConcourseTR in loadout) and jumpAble and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (CausewayR in loadout) and jumpAble and canUseBombs and ((SpeedBooster in loadout) or (Speedball in loadout)):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (SporeFieldTR in loadout) and jumpAble and (Morph in loadout):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
            elif (SporeFieldBR in loadout) and jumpAble and (Morph in loadout):
                loadout.append(RuinedConcourseBL)
                loadout.append(other)
        if (RuinedConcourseTR in loadout) == False:
            other = otherDoor(RuinedConcourseTR, Connections)
            if (other in loadout):
                loadout.append(RuinedConcourseTR)
            elif (jumpAble and (Missile in loadout) and (Morph in loadout) and (SpeedBooster in loadout)):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (RuinedConcourseBL in loadout) and jumpAble and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (CausewayR in loadout) and jumpAble and canUseBombs and (SpeedBooster in loadout) and (Energy in loadout):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (SporeFieldTR in loadout) and jumpAble and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
            elif (SporeFieldBR in loadout) and jumpAble and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout):
                loadout.append(RuinedConcourseTR)
                loadout.append(other)
        if (CausewayR in loadout) == False:
            other = otherDoor(CausewayR, Connections)
            if (other in loadout):
                loadout.append(CausewayR)
            elif (jumpAble and (Missile in loadout) and (Morph in loadout) and ((SpeedBooster in loadout) or (Speedball in loadout))):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (RuinedConcourseBL in loadout) and jumpAble and (Morph in loadout) and (SpeedBooster in loadout) and (Energy in loadout):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (RuinedConcourseTR in loadout) and jumpAble and canUseBombs and (SpeedBooster in loadout) and (Energy in loadout):
                loadout.append(CausewayR)
                loadout.append(other)
            elif (SporeFieldTR in loadout) and jumpAble and (Morph in loadout) and ((SpeedBooster in loadout) or (Speedball in loadout)) and canUseBombs:
                loadout.append(CausewayR)
                loadout.append(other)
            elif (SporeFieldBR in loadout) and jumpAble and (Morph in loadout) and ((SpeedBooster in loadout) or (Speedball in loadout)) and canUseBombs:
                loadout.append(CausewayR)
                loadout.append(other)
        if (OceanShoreR in loadout) == False:
            other = otherDoor(OceanShoreR, Connections)
            if (other in loadout):
                loadout.append(OceanShoreR)
            elif (EleToTurbidPassageR in loadout) and jumpAble and (Morph in loadout) and underwater and ((GravitySuit in loadout) or (Speedball in loadout)) and (((DarkVisor in loadout) and pinkDoor and wave) or ((Screw in loadout) and pinkDoor) or (Super in loadout) or ((GravitySuit in loadout) and canUsePB)):
                loadout.append(OceanShoreR)
                loadout.append(other)
            elif (PileAnchorL in loadout) and jumpAble and (GravitySuit in loadout) and canUsePB and (Super in loadout) and (SpeedBooster in loadout) and (Grapple in loadout) and pinkDoor:
                loadout.append(OceanShoreR)
                loadout.append(other)
        if (EleToTurbidPassageR in loadout) == False:
            other = otherDoor(EleToTurbidPassageR, Connections)
            if (other in loadout):
                loadout.append(EleToTurbidPassageR)
            elif (OceanShoreR in loadout) and jumpAble and (Morph in loadout) and underwater and ((GravitySuit in loadout) or (Speedball in loadout)) and (((DarkVisor in loadout) and pinkDoor and wave) or ((Screw in loadout) and pinkDoor) or (Super in loadout) or ((GravitySuit in loadout) and canUsePB)):
                loadout.append(EleToTurbidPassageR)
                loadout.append(other)
            elif (PileAnchorL in loadout) and jumpAble and (GravitySuit in loadout) and canUsePB and (Super in loadout) and (SpeedBooster in loadout) and (Grapple in loadout) and (Super in loadout):
                loadout.append(EleToTurbidPassageR)
                loadout.append(other)
        if (PileAnchorL in loadout) == False:
            other = otherDoor(EleToTurbidPassageR, Connections)
            if (other in loadout):
                loadout.append(PileAnchorL)
            elif (OceanShoreR in loadout) and jumpAble and (GravitySuit in loadout) and canUsePB and (Super in loadout) and (SpeedBooster in loadout) and (Grapple in loadout):
                loadout.append(PileAnchorL)
                loadout.append(other)
            elif (EleToTurbidPassageR in loadout) and jumpAble and (GravitySuit in loadout) and canUsePB and (Super in loadout) and (SpeedBooster in loadout) and (Grapple in loadout):
                loadout.append(PileAnchorL)
                loadout.append(other)
        if (ExcavationSiteL in loadout) == False:
            other = otherDoor(ExcavationSiteL, Connections)
            if (other in loadout):
                loadout.append(ExcavationSiteL)
            elif (WestCorridorR in loadout) and jumpAble and pinkDoor:
                loadout.append(ExcavationSiteL)
                loadout.append(other)
            elif (FoyerR in loadout) and jumpAble and ((canUsePB and underwater and wave and (Bombs in loadout)) or (pinkDoor and underwater and (Morph in loadout) and (Screw in loadout))):
                loadout.append(ExcavationSiteL)
                loadout.append(other)
            elif (ConstructionSiteL in loadout) and jumpAble and pinkDoor and (canUsePB or (pinkDoor and underwater and (Morph in loadout) and (Screw in loadout) and wave and (Bombs in loadout))):
                loadout.append(ExcavationSiteL)
                loadout.append(other)
            elif (AlluringCenoteR in loadout) and jumpAble and pinkDoor and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)) and ((wave and (Bombs in loadout)) or ((Screw in loadout) and underwater)):
                loadout.append(ExcavationSiteL)
                loadout.append(other)
        if (WestCorridorR in loadout) == False:
            other = otherDoor(WestCorridorR, Connections)
            if (other in loadout):
                loadout.append(WestCorridorR)
            elif (ExcavationSiteL in loadout) and jumpAble and pinkDoor:
                loadout.append(WestCorridorR)
                loadout.append(other)
            elif (FoyerR in loadout) and jumpAble and pinkDoor and ((canUsePB and underwater and wave and (Bombs in loadout)) or (pinkDoor and underwater and (Morph in loadout) and (Screw in loadout))):
                loadout.append(WestCorridorR)
                loadout.append(other)
            elif (ConstructionSiteL in loadout) and pinkDoor and jumpAble and (canUsePB or (pinkDoor and underwater and (Morph in loadout) and (Screw in loadout) and wave and (Bombs in loadout))):
                loadout.append(WestCorridorR)
                loadout.append(other)
            elif (AlluringCenoteR in loadout) and jumpAble and pinkDoor and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)) and ((wave and (Bombs in loadout)) or ((Screw in loadout) and underwater)):
                loadout.append(WestCorridorR)
                loadout.append(other)
        if (FoyerR in loadout) == False:
            other = otherDoor(FoyerR, Connections)
            if (other in loadout):
                loadout.append(FoyerR)
            elif (ExcavationSiteL in loadout) and jumpAble and pinkDoor:
                loadout.append(FoyerR)
                loadout.append(other)
            elif (WestCorridorR in loadout) and jumpAble and pinkDoor and ((canUsePB and underwater and wave and (Bombs in loadout)) or (pinkDoor and underwater and (Morph in loadout) and (Screw in loadout))):
                loadout.append(FoyerR)
                loadout.append(other)
            elif (ConstructionSiteL in loadout) and pinkDoor and jumpAble and (canUsePB or (pinkDoor and underwater and (Morph in loadout) and (Screw in loadout) and wave and (Bombs in loadout))):
                loadout.append(FoyerR)
                loadout.append(other)
            elif (AlluringCenoteR in loadout) and jumpAble and pinkDoor and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)) and ((wave and (Bombs in loadout)) or ((Screw in loadout) and underwater)):
                loadout.append(FoyerR)
                loadout.append(other)
        if (ConstructionSiteL in loadout) == False:
            other = otherDoor(ConstructionSiteL, Connections)
            if (other in loadout):
                loadout.append(ConstructionSiteL)
            elif (ExcavationSiteL in loadout) and jumpAble and pinkDoor and ((canUsePB and underwater and wave and (Bombs in loadout)) or (pinkDoor and underwater and (Morph in loadout) and (Screw in loadout))):
                loadout.append(ConstructionSiteL)
                loadout.append(other)
            elif (WestCorridorR in loadout) and jumpAble and pinkDoor and ((canUsePB and underwater and wave and (Bombs in loadout)) or (pinkDoor and underwater and (Morph in loadout) and (Screw in loadout))):
                loadout.append(ConstructionSiteL)
                loadout.append(other)
            elif (FoyerR in loadout) and jumpAble and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)) and ((wave and (Bombs in loadout)) or ((Screw in loadout) and underwater)):
                loadout.append(ConstructionSiteL)
                loadout.append(other)
            elif (AlluringCenoteR in loadout) and jumpAble and pinkDoor and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)) and ((wave and (Bombs in loadout)) or ((Screw in loadout) and underwater)):
                loadout.append(ConstructionSiteL)
                loadout.append(other)
        if (AlluringCenoteR in loadout) == False:
            other = otherDoor(AlluringCenoteR, Connections)
            if (other in loadout):
                loadout.append(AlluringCenoteR)
            elif (ExcavationSiteL in loadout) and jumpAble and pinkDoor and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)) and ((wave and (Bombs in loadout)) or ((Screw in loadout) and underwater)):
                loadout.append(AlluringCenoteR)
                loadout.append(other)
            elif (WestCorridorR in loadout) and jumpAble and pinkDoor and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)) and ((wave and (Bombs in loadout)) or ((Screw in loadout) and underwater)):
                loadout.append(AlluringCenoteR)
                loadout.append(other)
            elif (FoyerR in loadout) and jumpAble and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)):
                loadout.append(AlluringCenoteR)
                loadout.append(other)
            elif (ConstructionSiteL in loadout) and jumpAble and pinkDoor and canUsePB and (Grapple in loadout) and (SpeedBooster in loadout) and (Speedball in loadout) and ((Screw in loadout) or (MetroidSuit in loadout)) and ((wave and (Bombs in loadout)) or ((Screw in loadout) and underwater)):
                loadout.append(AlluringCenoteR)
                loadout.append(other)
        if (FieldAccessL in loadout) == False:
            other = otherDoor(FieldAccessL, Connections)
            if (other in loadout):
                loadout.append(FieldAccessL)
            elif (TransferStationR in loadout) and jumpAble and pinkDoor and (DarkVisor in loadout) and wave and canUseBombs:
                loadout.append(FieldAccessL)
                loadout.append(other)
            elif (CellarR in loadout) and jumpAble and (Super in loadout) and canUsePB and (DarkVisor in loadout) and wave:
                loadout.append(FieldAccessL)
                loadout.append(other)
            elif (SubbasementFissureL in loadout) and jumpAble and (Super in loadout) and canUsePB and wave:
                loadout.append(FieldAccessL)
                loadout.append(other)
        if (TransferStationR in loadout) == False:
            other = otherDoor(TransferStationR, Connections)
            if (other in loadout):
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
        if (CellarR in loadout) == False:
            other = otherDoor(CellarR, Connections)
            if (other in loadout):
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
        if (SubbasementFissureL in loadout) == False:
            other = otherDoor(SubbasementFissureL, Connections)
            if (other in loadout):
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
        if (WestTerminalAccessL in loadout) == False:
            other = otherDoor(WestTerminalAccessL, Connections)
            if (other in loadout):
                loadout.append(WestTerminalAccessL)
            elif (MezzanineConcourseL in loadout) and jumpAble and (canFly or (SpeedBooster in loadout) or (HiJump in loadout) or (Ice in loadout)):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(WestTerminalAccessL)
                loadout.append(other)
        if (MezzanineConcourseL in loadout) == False:
            other = otherDoor(MezzanineConcourseL, Connections)
            if (other in loadout):
                loadout.append(MezzanineConcourseL)
            elif (WestTerminalAccessL in loadout) and jumpAble and (canFly or (SpeedBooster in loadout) or (HiJump in loadout) or (Ice in loadout)):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(MezzanineConcourseL)
                loadout.append(other)
        if (VulnarCanyonL in loadout) == False:
            other = otherDoor(VulnarCanyonL, Connections)
            if (other in loadout):
                loadout.append(VulnarCanyonL)
            elif (WestTerminalAccessL in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (MezzanineConcourseL in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (CanyonPassageR in loadout) and jumpAble:
                loadout.append(VulnarCanyonL)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(VulnarCanyonL)
                loadout.append(other)
        if (CanyonPassageR in loadout) == False:
            other = otherDoor(CanyonPassageR, Connections)
            if (other in loadout):
                loadout.append(CanyonPassageR)
            elif (WestTerminalAccessL in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (MezzanineConcourseL in loadout) and jumpAble and (SpeedBooster in loadout):
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (VulnarCanyonL in loadout) and jumpAble:
                loadout.append(CanyonPassageR)
                loadout.append(other)
            elif (ElevatorToCondenserL in loadout) and jumpAble and canUseBombs and breakIce and underwater and ((Ice in loadout) or (GravitySuit in loadout) or (Grapple in loadout)):
                loadout.append(CanyonPassageR)
                loadout.append(other)
        if (ElevatorToCondenserL in loadout) == False:
            other = otherDoor(ElevatorToCondenserL, Connections)
            if (other in loadout):
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
        if (LoadingDockSecurityAreaL in loadout) == False:
            other = otherDoor(ElevatorToCondenserL, Connections)
            if (other in loadout):
                loadout.append(LoadingDockSecurityAreaL)
        if (ElevatorToWellspringL in loadout) == False:
            other = otherDoor(ElevatorToWellspringL, Connections)
            if (other in loadout):
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
        if (NorakBrookL in loadout) == False:
            other = otherDoor(NorakBrookL, Connections)
            if (other in loadout):
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
        if (NorakPerimeterTR in loadout) == False:
            other = otherDoor(NorakPerimeterTR, Connections)
            if (other in loadout):
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
        if (NorakPerimeterBL in loadout) == False:
            other = otherDoor(NorakPerimeterBL, Connections)
            if (other in loadout):
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
        if (VulnarDepthsElevatorEL in loadout) == False:
            other = otherDoor(VulnarDepthsElevatorEL, Connections)
            if (other in loadout):
                loadout.append(VulnarDepthsElevatorEL)
            elif (VulnarDepthsElevatorER in loadout):
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
            elif (SequesteredInfernoL in loadout) and jumpAble and pinkDoor and canUseBombs and (energyCount > 4) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
            elif (CollapsedPassageR in loadout) and jumpAble and canUsePB and (Super in loadout) and (energyCount > 7):
                loadout.append(VulnarDepthsElevatorEL)
                loadout.append(other)
        if (VulnarDepthsElevatorER in loadout) == False:
            other = otherDoor(VulnarDepthsElevatorER, Connections)
            if (other in loadout):
                loadout.append(VulnarDepthsElevatorER)
            elif (VulnarDepthsElevatorEL in loadout):
                loadout.append(VulnarDepthsElevatorER)
                loadout.append(other)
            elif (SequesteredInfernoL in loadout) and jumpAble and pinkDoor and canUseBombs and (energyCount > 4) and ((MetroidSuit in loadout) or ((Charge in loadout) and (Hypercharge in loadout))):
                loadout.append(VulnarDepthsElevatorER)
                loadout.append(other)
            elif (CollapsedPassageR in loadout) and jumpAble and canUsePB and (Super in loadout) and (energyCount > 7):
                loadout.append(VulnarDepthsElevatorER)
                loadout.append(other)
        if (SequesteredInfernoL in loadout) == False:
            other = otherDoor(SequesteredInfernoL, Connections)
            if (other in loadout):
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
        if (CollapsedPassageR in loadout) == False:
            other = otherDoor(CollapsedPassageR, Connections)
            if (other in loadout):
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
        if (MagmaPumpL in loadout) == False:
            other = otherDoor(MagmaPumpL, Connections)
            if (other in loadout):
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
        if (ReservoirMaintenanceTunnelR in loadout) == False:
            other = otherDoor(ReservoirMaintenanceTunnelR, Connections)
            if (other in loadout):
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
        if (IntakePumpR in loadout) == False:
            other = otherDoor(IntakePumpR, Connections)
            if (other in loadout):
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
        if (ThermalReservoir1R in loadout) == False:
            other = otherDoor(ThermalReservoir1R, Connections)
            if (other in loadout):
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
        if (GeneratorAccessTunnelL in loadout) == False:
            other = otherDoor(GeneratorAccessTunnelL, Connections)
            if (other in loadout):
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
        if (ElevatorToMagmaLakeR in loadout) == False:
            other = otherDoor(ElevatorToMagmaLakeR, Connections)
            if (other in loadout):
                loadout.append(ElevatorToMagmaLakeR)
            elif (MagmaPumpAccessR in loadout) and jumpAble and underwater and (MetroidSuit in loadout) and canUsePB:
                loadout.append(ElevatorToMagmaLakeR)
                loadout.append(other)
        if (MagmaPumpAccessR in loadout) == False:
            other = otherDoor(MagmaPumpAccessR, Connections)
            if (other in loadout):
                loadout.append(MagmaPumpAccessR)
            elif (ElevatorToMagmaLakeR in loadout) and jumpAble and underwater and (MetroidSuit in loadout) and canUsePB:
                loadout.append(MagmaPumpAccessR)
                loadout.append(other)
        if (FieryGalleryL in loadout) == False:
            other = otherDoor(FieryGalleryL, Connections)
            if (other in loadout):
                loadout.append(FieryGalleryL)
            elif (RagingPitL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and canUseBombs and (Super in loadout):
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
        if (RagingPitL in loadout) == False:
            other = otherDoor(RagingPitL, Connections)
            if (other in loadout):
                loadout.append(RagingPitL)
            elif (FieryGalleryL in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout):
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (HollowChamberR in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and (Ice in loadout):
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (PlacidPoolR in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and ((Ice in loadout) or canUsePB):
                loadout.append(RagingPitL)
                loadout.append(other)
            elif (SporousNookL in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and underwater:
                loadout.append(RagingPitL)
                loadout.append(other)
        if (HollowChamberR in loadout) == False:
            other = otherDoor(HollowChamberR, Connections)
            if (other in loadout):
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
        if (PlacidPoolR in loadout) == False:
            other = otherDoor(PlacidPoolR, Connections)
            if (other in loadout):
                loadout.append(PlacidPoolR)
            elif (FieryGalleryL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and (canUseBombs or (Screw in loadout) or (SpeedBooster in loadout)) and ((Ice in loadout) or canUsePB):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (RagingPitL in loadout) and jumpAble and canUseBombs and ((Varia in loadout) or (energyCount > 4)) and (Super in loadout) and ((Ice in loadout) or canUsePB):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (HollowChamberR in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 2)) and (Ice in loadout):
                loadout.append(PlacidPoolR)
                loadout.append(other)
            elif (SporousNookL in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and ((Ice in loadout) or canUsePB) and (Super in loadout) and underwater:
                loadout.append(PlacidPoolR)
                loadout.append(other)
        if (SporousNookL in loadout) == False:
            other = otherDoor(SporousNookL, Connections)
            if (other in loadout):
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
            elif (PlacidPoolR in loadout) and jumpAble and ((Varia in loadout) or (energyCount > 4)) and ((Ice in loadout) or canUsePB) and (Super in loadout) and underwater:
                loadout.append(SporousNookL)
                loadout.append(other)
        if loadout == tempLoadout:
            movement = True
    return loadout
