import random
import io

from romWriter import RomWriter
from item_data import items_unpackable

#RandomizeAreas shuffles the locations and checks that the ship connects to daphne properly
#updateAreaLogic is like a logic updater for area doors connecting to other area doors
# -this is done before the item locations are updated

#second version uses
#[0]the door pointer this door needs to send with
#[1]the data that is needed to go to this door


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

def VanillaAreas() :

    return [[CraterR,WestTerminalAccessL],
            [SunkenNestL,OceanShoreR],
            [RuinedConcourseBL,TransferStationR],
            [RuinedConcourseTR,MezzanineConcourseL],
            [CausewayR,ExcavationSiteL],
            [SporeFieldTR,FieldAccessL],
            [SporeFieldBR,SporousNookL],
            [EleToTurbidPassageR,FieryGalleryL],
            [PileAnchorL,TramToSuziIslandR],
            [WestCorridorR,LoadingDockSecurityAreaL],
            [FoyerR,VulnarCanyonL],
            [ConstructionSiteL,CellarR],
            [AlluringCenoteR,NorakPerimeterBL],
            [SubbasementFissureL,VulnarDepthsElevatorER],
            [CanyonPassageR,NorakBrookL],
            [ElevatorToCondenserL,IntakePumpR],
            [ElevatorToWellspringL,CollapsedPassageR],
            [NorakPerimeterTR,RockyRidgeTrailL],
            [VulnarDepthsElevatorEL,PlacidPoolR],
            [HiveBurrowL,ThermalReservoir1R],
            [SequesteredInfernoL,ReservoirMaintenanceTunnelR],
            [MagmaPumpL,MagmaPumpAccessR],
            [GeneratorAccessTunnelL,HollowChamberR],
            [ElevatorToMagmaLakeR,RagingPitL]]

def RandomizeAreas(romWriter : RomWriter) :
    #Each location holds
    #[0]the data of its door
    #[1]the data of the vanilla door that goes here
    #[2]the area
    #[3]the name of the door
    #[4]region

    def findDaphne(fromDoor) :
        #print("fromDoor:",fromDoor[3])
        #print("pathToDaphne:",pathToDaphne)
        testcases=[]
        for item in Connections :
            #print("The first item:",len(item),item)
            if (fromDoor in item) :
                otherDoor=item[0]
                if fromDoor == otherDoor :
                    otherDoor=item[1]
                #print("Declaring otherDoor: ",otherDoor)
        #print("otherDoor:",otherDoor[3])
        if (otherDoor == RockyRidgeTrailL) :
            #print("FoundDaphne:")
            for item in pathToDaphne :
                #print("  ",item[3])
                uu=0
            return True
        if (otherDoor in pathToDaphne) :
            #print("Circling back on",otherDoor)
            return False
        if (otherDoor in [RuinedConcourseBL,RuinedConcourseTR,CausewayR,SporeFieldTR,SporeFieldBR]) :
            testcases = [RuinedConcourseBL,RuinedConcourseTR,CausewayR,SporeFieldTR,SporeFieldBR]
        if (otherDoor in [OceanShoreR,EleToTurbidPassageR,PileAnchorL]) :
            testcases = [OceanShoreR,EleToTurbidPassageR,PileAnchorL]
        if (otherDoor in [WestTerminalAccessL,MezzanineConcourseL,VulnarCanyonL,CanyonPassageR]) :
            testcases = [WestTerminalAccessL,MezzanineConcourseL,VulnarCanyonL,CanyonPassageR]
        if (otherDoor in [ElevatorToWellspringL,NorakBrookL,NorakPerimeterTR,NorakPerimeterBL]) :
            testcases = [ElevatorToWellspringL,NorakBrookL,NorakPerimeterTR,NorakPerimeterBL]            
        if (otherDoor in [ExcavationSiteL,WestCorridorR,FoyerR,ConstructionSiteL,AlluringCenoteR]) :
            testcases = [ExcavationSiteL,WestCorridorR,FoyerR,ConstructionSiteL,AlluringCenoteR]
        if (otherDoor in [FieldAccessL,TransferStationR,CellarR,SubbasementFissureL]) :
            testcases = [FieldAccessL,TransferStationR,CellarR,SubbasementFissureL]
        if (otherDoor in [VulnarDepthsElevatorEL,VulnarDepthsElevatorER,SequesteredInfernoL,CollapsedPassageR]) :
            testcases = [VulnarDepthsElevatorEL,VulnarDepthsElevatorER,SequesteredInfernoL,CollapsedPassageR]
        if (otherDoor in [MagmaPumpL,ReservoirMaintenanceTunnelR,IntakePumpR,ThermalReservoir1R,GeneratorAccessTunnelL]) :
            testcases = [MagmaPumpL,ReservoirMaintenanceTunnelR,IntakePumpR,ThermalReservoir1R,GeneratorAccessTunnelL]
        if (otherDoor in [ElevatorToMagmaLakeR,MagmaPumpAccessR]) :
            testcases = [ElevatorToMagmaLakeR,MagmaPumpAccessR]
        if (otherDoor in [FieryGalleryL,RagingPitL,HollowChamberR,PlacidPoolR,SporousNookL]) :
            testcases = [FieryGalleryL,RagingPitL,HollowChamberR,PlacidPoolR,SporousNookL]            
        soFar = False
        if testcases == [] :
            return False
        pathToDaphne.append(otherDoor)
        for eachOtherExit in testcases:
            if (eachOtherExit in pathToDaphne) == False :
                pathToDaphne.append(eachOtherExit)
                check = findDaphne(eachOtherExit)
                soFar = (soFar or check)
        return soFar
    
    areaAttempts = 0    
    connected=False
    while connected == False :
        areaAttempts += 1
        if areaAttempts > 1000 :
            print("Tried 1000 times. help?")
            connected = True #This is a lie, but it breaks the loop
        print("**********Trying to get a good escape attempt:",areaAttempts)

        OpenNodesR=[CraterR,
                   RuinedConcourseTR,
                   CausewayR,
                   SporeFieldTR,
                   SporeFieldBR]
        OpenNodesL=[SunkenNestL,
                    RuinedConcourseBL]
        VisitedAreas=['Early']
        Connections=[]
        
        RightSideDoorsList=[OceanShoreR,
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

        LeftSideDoorsList=[PileAnchorL,
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
        #for h in RightSideDoorsList :
            #print(h[2],h[3])
            
        #for h in LeftSideDoorsList :
            #print(h[2],h[3])
            
        while RightSideDoorsList != [] or LeftSideDoorsList != [] :
            #print("Lengths: OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))
            CombinedDoorsList=RightSideDoorsList+LeftSideDoorsList
            #This case is for making sure all areas make it into the map
            #Then all other connections happen later
            randomIndex=0
            if len(CombinedDoorsList) > 1 :
                randomIndex=random.randint(0,len(CombinedDoorsList)-1)
            selectedDoor=CombinedDoorsList[randomIndex]
            if (selectedDoor in RightSideDoorsList) and OpenNodesL != [] :
                #It is a right door and there are open Left nodes to connect to
                #if it fails, the loop will try again with no change
                RightSideDoorsList.remove(selectedDoor)
                #Choose a random Left node to connect to
                randomNode=0
                if len(OpenNodesL) > 1 :
                    randomNode=random.randint(0,len(OpenNodesL)-1)
                Connections.append([selectedDoor,OpenNodesL[randomNode]])
                #for DEBUG
                #print('RightSideDoorsList')
                #print('pairing',selectedDoor[2],selectedDoor[3],"--",OpenNodesL[randomNode][2],OpenNodesL[randomNode][3])
                OpenNodesL.remove(OpenNodesL[randomNode])
                #Now add the area to the visitedareas
                #and all nodes from that area
                VisitedAreas=VisitedAreas+[selectedDoor[2]]
                for doorSearch in RightSideDoorsList :
                    if doorSearch[2] in VisitedAreas :
                        OpenNodesR+=[doorSearch]
                for doorClean in OpenNodesR :
                    if doorClean in RightSideDoorsList :
                        RightSideDoorsList.remove(doorClean)
            elif (selectedDoor in LeftSideDoorsList) and OpenNodesR != [] :
                #It is a left door and there are open right nodes to connect to
                #if it fails, the loop will try again with no change
                LeftSideDoorsList.remove(selectedDoor)
                #Choose a random Right node to connect to
                randomNode=0
                if len(OpenNodesR) > 1 :
                    randomNode=random.randint(0,len(OpenNodesR)-1)
                Connections.append([selectedDoor,OpenNodesR[randomNode]])
                #for DEBUG
                #print('LeftSideDoorsList')
                #print('pairing',selectedDoor[2],selectedDoor[3],"--",OpenNodesR[randomNode][2],OpenNodesR[randomNode][3])
                OpenNodesR.remove(OpenNodesR[randomNode])
                #Now add the area to the visitedareas
                #and all nodes from that area
                VisitedAreas=VisitedAreas+[selectedDoor[2]] #add the area string
                for doorSearch in LeftSideDoorsList :
                    if doorSearch[2] in VisitedAreas :
                        OpenNodesL+=[doorSearch]
                for doorClean in OpenNodesL :
                    if doorClean in LeftSideDoorsList :
                        LeftSideDoorsList.remove(doorClean)
                #print(len(VisitedAreas),"areas visited")
                #print(VisitedAreas)
        #print("Before connecting OpenNodes")
        #print("Lengths: OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))
        #This section is when all areas have been placed and we just need
        #To connect nodes from OpenNodesL and OpenNodesR
        #print("While connecting OpenNodes:")
        while OpenNodesL != [] and OpenNodesR != [] :
            #Should only need to keep track of one since they should match 1:1
            randomL=0
            if len(OpenNodesL) > 1 :
                randomL=random.randint(0,len(OpenNodesL)-1)
            chosenNodeL=OpenNodesL[randomL]
            randomR=0
            if len(OpenNodesR) > 1 :
                randomR=random.randint(0,len(OpenNodesR)-1)
            chosenNodeR=OpenNodesR[randomR]
            Connections.append([chosenNodeL,chosenNodeR])
            OpenNodesL.remove(chosenNodeL)
            OpenNodesR.remove(chosenNodeR)
            #print("    Lengths: OpenNodesL",len(OpenNodesL)," and OpenNodesR",len(OpenNodesR))
        #print("LeftoverL  ",OpenNodesL)
        #print("LeftoverR  ",OpenNodesR)
        #print(len(Connections),"Connections created:")
        #for item in Connections :
            #print(item[0][2],item[0][3]," << >> ",item[1][2],item[1][3])
        pathToDaphne=[CraterR,SunkenNestL]
        #check for valid area configuration
        if findDaphne(CraterR) or findDaphne(SunkenNestL) :
            connected = True

    

    #then connect the doors together

    #Now I need to read the OG Subversion rom for 12 bytes at address:Node1[1]
    #and write it into the 12 bytes at Node2[0]
    #Also read the OG Subversion Rom for 12 bytes at address:Node2[1]
    #and write it into the 12 bytes at Node1[0]
    #Tada, area rando
    #But I need to do all the reading before I do any writing so that
    #I am getting the pure original Subversion data
    
    #do a round of reading the door data for each node
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
    for pair in Connections :
        node1=pair[0]
        node2=pair[1]
        #place data for node1 sending
        romWriter.writeBytes(int(node1[0],16), int(node2[1],16).to_bytes(12, 'big'))
        #place data for node2 sending
        romWriter.writeBytes(int(node2[0],16), int(node1[1],16).to_bytes(12, 'big'))
        if node1[4] != node2[4] :
            romWriter.writeBytes(int(node1[0],16)+2, b"\x40")
            romWriter.writeBytes(int(node2[0],16)+2, b"\x40")

    #Area rando done?

    #coloring some doors to be flashing
    colorDoorsR=['3fff70',
                 '3fffa8',
                 '3fe37c',
                 '3ff15e',
                 '3ff1f8',
                 '3fe668',
                 '3fe66e']


    colorDoorsL=['3ffec4',
                 '3fe352',
                 '3fe35a',
                 '3fe686',
                 '3ffa2c']


    for doorlocid in colorDoorsR:
        romWriter.writeBytes(int(doorlocid,16),   b"\x42") # gray type door
        romWriter.writeBytes(int(doorlocid,16)+5, b"\x98") # animals subtype
    for doorlocid in colorDoorsL:
        romWriter.writeBytes(int(doorlocid,16),   b"\x48") # gray type door
        romWriter.writeBytes(int(doorlocid,16)+5, b"\x98") # animals subtype

    return Connections

def otherDoor(door,Connections) :
    for pair in Connections :
        if (door in pair) :
            other = pair[0]
            if door == other :
                other = pair[1]
    return other
#return these to top later
