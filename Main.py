import random
import sys
import argparse
import struct
import shutil
import os
import io
import csv
import logicCasual
import logicExpert
import logicExpertArea
import fillSpeedrun
import fillMedium
import fillMajorMinor
import areaRando

g_rom : io.BufferedIOBase

def commandLineArgs(sys_args) :
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--casual', action="store_true", help='Casual logic, easy setting matching the vanilla Subversion experience, Default')
    parser.add_argument('-e', '--expert', action="store_true", help='Expert logic, hard setting comparable to Varia.run Expert difficulty')
    parser.add_argument('-s', '--speedrun', action="store_true", help='Speedrun fill, fast setting comparable to Varia.run Speedrun fill algorithm, Default')
    parser.add_argument('-m', '--medium', action="store_true", help='Medium fill, medium speed setting that places low-power items first for increased exploration')
    parser.add_argument('-mm', '--majorminor',  action="store_true", help='Major-Minor fill, using unique majors and locations')
    parser.add_argument('-area',  action="store_true", help='Area rando shuffles major areas of the game, expert logic only')
    args = parser.parse_args(sys_args)
    #print(args)
    return args

def createWorkingFileCopy(origFile, newFile) -> io.BufferedIOBase:
    global g_rom
    if not os.path.exists(origFile):
        raise Exception(f'origFile not found: {origFile}')
    with open(origFile, 'rb') as orig:
        g_rom = open(newFile, 'wb') # wb = write, binary
        # copy original to new before we edit new
        while True:
            chunk = orig.read(16384) # or any amount
            if chunk == b"":
                break
            g_rom.write(chunk)

def writeItem(address : int, plmid, ammoAmount = b"\x00"):
    global g_rom
    if len(plmid) != 2 or len(ammoAmount) != 1:
        raise Exception(f'plmid length ({len(plmid)}) must be 2 and ammoAmount length ({len(ammoAmount)}) must be 1')
    g_rom.seek(address)
    g_rom.write(plmid)
    g_rom.seek(address+5)
    g_rom.write(ammoAmount)

def writeBytes(address : int, data):
    global g_rom
    g_rom.seek(address)
    g_rom.write(data)

def finalizeRom():
    global g_rom
    g_rom.close()
    g_rom = None

def plmidFromHiddenness(itemArray, hiddenness):
    if hiddenness == "open":
        plmid = itemArray[1]
    elif hiddenness == "chozo":
        plmid = itemArray[2]
    else:
        plmid = itemArray[3]
    return plmid

def itemPlace(location,itemArray) :
    #provide a locRow as in and the item array such as Missile, Super, etc
    # write all rom locations associated with the item location
    plmid = plmidFromHiddenness(itemArray, location['hiddenness'])
    for address in location['locids']:
        writeItem(address, plmid, itemArray[4])
    for address in location['alternateroomlocids']:
        if location['alternateroomdifferenthiddenness'] == "":
            # most of the alt rooms go here, having the same item hiddenness as the corresponding "pre-item-move" item had
            plmid_altroom = plmid
        else:
            plmid_altroom = plmidFromHiddenness(itemArray, location['alternateroomdifferenthiddenness'])
        writeItem(address, plmid_altroom, itemArray[4])

def pullCSV():
    csvdict = {}
    def commentfilter(line):
        return (line[0] != '#')
    with open('subversiondata12.csv', 'r') as csvfile:
        reader = csv.DictReader(filter(commentfilter, csvfile))
        for row in reader:
            # commas within fields -> array
            row['locids']              = row['locids'].split(',')
            row['alternateroomlocids'] = row['alternateroomlocids'].split(',')
            # hex fields we want to use -> int
            row['locids']              = [int(locstr, 16) for locstr in row['locids'] if locstr != '']
            row['alternateroomlocids'] = [int(locstr, 16) for locstr in row['alternateroomlocids'] if locstr != '']
            row['plmtypeid']  = int(row['plmtypeid'], 16)
            row['plmparamhi'] = int(row['plmparamhi'], 16)
            row['plmparamlo'] = int(row['plmparamlo'], 16)
            # new key: 'inlogic'
            row['inlogic'] = False
            csvdict[row['fullitemname']] = row
    return csvdict

#main program
if __name__ == "__main__":
    workingArgs=commandLineArgs(sys.argv[1:])
    if workingArgs.expert :
        logicChoice = "E"
    elif workingArgs.area :
        logicChoice = "AR" #EXPERT area rando
    else :
        logicChoice = "C" #Default to casual logic
    if workingArgs.medium :
        fillChoice = "M"
    elif workingArgs.majorminor :
        fillChoice = "MM"
    elif workingArgs.area :
        fillChoice = "EA" #EXPERT area rando 
    else :
        fillChoice = "S"
    #hudFlicker=""
    #while hudFlicker != "Y" and hudFlicker != "N" :
    #    hudFlicker= input("Enter Y to patch HUD flicker on emulator, or N to decline:")
    #    hudFlicker = hudFlicker.title()
    seeeed=random.randint(1000000,9999999)
    random.seed(seeeed)
    rom1_path = "roms/Sub"+logicChoice+fillChoice+str(seeeed)+".sfc"
    rom_clean_path = "roms/Subversion12.sfc"
    #you must include Subversion 1.2 in your roms folder with this name^
    spoiler_file = open("spoilers/Sub"+logicChoice+fillChoice+str(seeeed)+".sfc.spoiler.txt", "w")

    csvdict = pullCSV()
    locArray = [csvdict[key] for key in csvdict]
    #Item = Name, Visible, Chozo, Hidden, AmmoQty
    Missile = ["Missile",
               b"\xdb\xee",
               b"\x2f\xef",
               b"\x83\xef",
               b"\x00"]
    Super = ["Super Missile",
             b"\xdf\xee",
             b"\x33\xef",
             b"\x87\xef",
             b"\x00"]
    PowerBomb = ["Power Bomb",
                 b"\xe3\xee",
                 b"\x37\xef",
                 b"\x8b\xef",
                 b"\x00"]
    Morph = ["Morph Ball",
             b"\x23\xef",
             b"\x77\xef",
             b"\xcb\xef",
             b"\x00"]
    GravityBoots = ["Gravity Boots",
                    b"\x40\xfd",
                    b"\x40\xfd",
                    b"\x40\xfd",
                    b"\x00"]   
    Speedball = ["Speed Ball",
                 b"\x03\xef",
                 b"\x57\xef",
                 b"\xab\xef",
                 b"\x00"]
    Bombs = ["Bombs",
             b"\xe7\xee",
             b"\x3b\xef",
             b"\x8f\xef",
             b"\x00"]
    HiJump = ["HiJump",
              b"\xf3\xee",
              b"\x47\xef",
              b"\x9b\xef",
              b"\x00"]
    GravitySuit = ["Gravity Suit",
                   b"\x0b\xef",
                   b"\x5f\xef",
                   b"\xb3\xef",
                   b"\x00"]
    DarkVisor = ["Dark Visor",
                 b"\xb0\xfd",
                 b"\xb0\xfd",
                 b"\xb0\xfd",
                 b"\x00"]
    Wave = ["Wave Beam",
            b"\xfb\xee",
            b"\x4f\xef",
            b"\xa3\xef",
            b"\x00"]
    SpeedBooster = ["Speed Booster",
                    b"\xf7\xee",
                    b"\x4b\xef",
                    b"\x9f\xef",
                    b"\x00"]
    Spazer = ["Spazer",
              b"\xff\xee",
              b"\x53\xef",
              b"\xa7\xef",
              b"\x00"]
    Varia = ["Varia Suit",
             b"\x07\xef",
             b"\x5b\xef",
             b"\xaf\xef",
             b"\x00"]
    Ice = ["Ice Beam",
           b"\xef\xee",
           b"\x43\xef",
           b"\x97\xef",
           b"\x00"]
    Grapple = ["Grapple Beam",
               b"\x17\xef",
               b"\x6b\xef",
               b"\xbf\xef",
               b"\x00"]
    MetroidSuit = ["Metroid Suit",
                   b"\x20\xfe",
                   b"\x20\xfe",
                   b"\x20\xfe",
                   b"\x00"]
    Plasma = ["Plasma Beam",
              b"\x13\xef",
              b"\x67\xef",
              b"\xbb\xef",
              b"\x00"]
    Screw = ["Screw Attack",
             b"\x1f\xef",
             b"\x73\xef",
             b"\xc7\xef",
             b"\x00"]
    Hypercharge = ["Hypercharge",
                   b"\x80\xf7",
                   b"\x80\xf7",
                   b"\x80\xf7",
                   b"\x00"]
    Charge = ["Charge Beam",
              b"\xeb\xee",
              b"\x3f\xef",
              b"\x93\xef",
              b"\x00"]
    Xray = ["X-Ray Scope",
            b"\x0f\xef",
            b"\x63\xef",
            b"\xb7\xef",
            b"\x00"]
    SpaceJump = ["Space Jump",
                 b"\x1b\xef",
                 b"\x6f\xef",
                 b"\xc3\xef",
                 b"\x00"]
    Energy = ["Energy Tank",
              b"\xd7\xee",
              b"\x2b\xef",
              b"\x7f\xef",
              b"\x00"]
    Refuel = ["Refuel Tank",
              b"\x27\xef",
              b"\x7b\xef",
              b"\xcf\xef",
              b"\x00"]
    SmallAmmo = ["Small Ammo",
                 b"\x00\xf9",
                 b"\x04\xf9",
                 b"\x08\xf9",
                 b"\x05"]
    LargeAmmo = ["Large Ammo",
                 b"\x00\xf9",
                 b"\x04\xf9",
                 b"\x08\xf9",
                 b"\x0a"]
    DamageAmp = ["Damage Amp",
                 b"\x7e\xf8",
                 b"\x7e\xf8",
                 b"\x7e\xf8",
                 b"\x00"]
    ChargeAmp = ["Charge Amp",
                 b"\xa0\xf0",
                 b"\xa0\xf0",
                 b"\xa0\xf0",
                 b"\x00"]
    SpaceJumpBoost = ["Space Jump Boost",
                      b"\xc0\xfc",
                      b"\xc0\xfc",
                      b"\xc0\xfc",
                      b"\x00"]
    spaceDrop = ["Space Drop","","","",""]
    createWorkingFileCopy(rom_clean_path, rom1_path)
    spacePortLocs=["Ready Room",
               "Torpedo Bay",
               "Extract Storage",
               "Gantry",
               "Docking Port 4",
               "Docking Port 3",
               "Weapon Locker",
               "Aft Battery",
               "Forward Battery"]
    
    seedComplete = False
    randomizeAttempts = 0
    while seedComplete == False:
        if fillChoice == "EA" : #area rando no logic
            g_rom,Connections=areaRando.RandomizeAreas(g_rom) 
            #print(Connections) #test    
        randomizeAttempts += 1
        if randomizeAttempts > 1000 :
            print("Giving up after 1000 attempts. Help?")
            break
        print("Starting randomization attempt:",randomizeAttempts)
        spoilerSave = ""
        spoilerSave += "Starting randomization attempt:"+str(randomizeAttempts)+"\n"
        #now start randomizing
        unusedLocations=[]
        unusedLocations.extend(locArray)
        availableLocations=[]
        visitedLocations=[]
        loadout=[]
        #use appropriate fill algorithm for initializing item lists
        if fillChoice == "M" :
            itemLists=fillMedium.initItemLists()
        elif fillChoice == "MM" :
            itemLists=fillMajorMinor.initItemLists()
        elif fillChoice == "EA" : #area rando uses medium fill
            itemLists=fillMedium.initItemLists()
        else :
            itemLists=fillSpeedrun.initItemLists()
        while len(unusedLocations) != 0 or len(availableLocations) != 0:
            #print("loadout contains:")
            #print(loadout)
            for a in loadout:
                #print("-",a[0])
                uu=0 #just do nothing
                
            #update logic by updating unusedLocations
            #using helper function, modular for more logic options later
            #unusedLocations[i]['inlogic'] holds the True or False for logic
            if logicChoice == "E" :
                logicExpert.updateLogic(unusedLocations, locArray, loadout)
            elif logicChoice == "AR" :
                loadout = areaRando.updateAreaLogic(availableLocations, locArray, loadout, Connections)
                logicExpertArea.updateLogic(unusedLocations, locArray, loadout)
            else :
                logicCasual.updateLogic(unusedLocations, locArray, loadout)
                    
            #update unusedLocations and availableLocations
            for i in reversed(range(len(unusedLocations))): # iterate in reverse so we can remove freely
                if unusedLocations[i]['inlogic'] == True :
                    #print("Found available location at",unusedLocations[i]['fullitemname'])
                    availableLocations.append(unusedLocations[i])
                    unusedLocations.pop(i)
            #print("Available locations sits at:",len(availableLocations))
            for al in availableLocations :
                #print(al[0])
                uu=0
            #print("Unused locations sits at size:",len(unusedLocations))
            #print("unusedLocations:")
            for u in unusedLocations :
                #print(u['fullitemname'])
                uu=0

            if availableLocations == [] and unusedLocations != [] :
                print(f'Item placement was not successful. {len(unusedLocations)} locations remaining.')
                spoilerSave+=f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
                break

            #split here for different fill algorithms
            if fillChoice == "M" :
                placePair=fillMedium.placementAlg(availableLocations, locArray, loadout, itemLists)
            elif fillChoice == "MM" :
                placePair=fillMajorMinor.placementAlg(availableLocations, locArray, loadout, itemLists)
            elif fillChoice == "EA" : #area rando
                placePair=fillMedium.placementAlg(availableLocations, locArray, loadout, itemLists)
            else :
                placePair=fillSpeedrun.placementAlg(availableLocations, locArray, loadout, itemLists)
            #it returns your location and item, which are handled here
            placeLocation=placePair[0]
            placeItem=placePair[1]
            if (placeLocation in unusedLocations) :
                unusedLocations.remove(placeLocation)
            if placeLocation == "Fail" :
                print(f'Item placement was not successful due to majors. {len(unusedLocations)} locations remaining.')
                spoilerSave+=f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
                break
            itemPlace(placeLocation,placeItem)
            availableLocations.remove(placeLocation)
            for itemPowerGrouping in itemLists :
                if placeItem in itemPowerGrouping :
                    itemPowerGrouping.remove(placeItem)
                    break
            loadout.append(placeItem)
            if ((placeLocation['fullitemname'] in spacePortLocs) == False) and ((spaceDrop in loadout) == False):
                loadout.append(spaceDrop)
            spoilerSave+=placeLocation['fullitemname']+" - - - "+placeItem[0]+"\n"
            #print(placeLocation['fullitemname']+placeItem[0])

            if availableLocations == [] and unusedLocations == [] :
                print("Item placements successful.")
                spoilerSave += "Item placements successful.\n"
                seedComplete = True
                break
            
    #add area transitions to spoiler
    for item in Connections :
        spoilerSave+=item[0][2]+" "+item[0][3]+" << >> "+item[1][2]+" "+item[1][3]+"\n"

    # Suit animation skip patch
    writeBytes(0x20717, b"\xea\xea\xea\xea")
    # Flickering hud removal patch
    #if hudFlicker == "Y" :
        #writeBytes(0x547a, b"\x02")
        #writeBytes(0x547f, b"\x00")
        #uu=0
    # Morph Ball PLM patch (chozo, hidden)
    writeBytes(0x268ce, b"\x04")
    writeBytes(0x26e02, b"\x04")
    # skip intro (asm edits) TODO turn this into asm and a proper hook
    writeBytes(0x16eda, b"\x1f") # initial game state set by $82:eeda
    writeBytes(0x16ee0, b"\x06\x00") # initial game area = 6 (ceres)
    writeBytes(0x16ee3, b"\x9f\x07") # $079f Area index
    writeBytes(0x16ee5, b"\xa9\x05\x00\x8f\x14\xd9\x7e\xea\xea") # $7e:d914 = 05 Main
    writeBytes(0x16eee, b"\xad\x52\x09\x22\x00\x80\x81") # jsl save game (param in A: save slot)
    writeBytes(0x16ed0, b"\x24") # adjust earlier branch to go +6 bytes later to rts
    writeBytes(0x16ed8, b"\x1c") # adjust earlier branch to go +6 bytes later to rts
    # disable demos (asm opcode edit). because the demos show items
    writeBytes(0x59f29, b"\xad")
    # make always flashing doors out of vanilla gray 'animals saved' doors:
    #   edit in function $84:BE30 'gray door pre: go to link instruction if critters escaped', which is vanilla and probably not used anyway
    #   use by writing 0x18 to the high byte of a gray door plm param, OR'ed with the low bit of the 9-low-bits id part
    writeBytes(0x23e33, b"\x38\x38\x38\x38") # set the carry bit (a lot)
    finalizeRom()
    print("Done!")
    print("Filename is "+"Sub"+logicChoice+fillChoice+str(seeeed)+".sfc")
    spoiler_file.write("RNG Seed: {}\n".format(str(seeeed))+"\n")
    spoiler_file.write("\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n")
    spoiler_file.write(spoilerSave)    
    print("Spoiler file is "+"Sub"+logicChoice+fillChoice+str(seeeed)+".sfc.spoiler.txt")




