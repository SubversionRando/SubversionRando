import random
import sys
import argparse
import struct
import shutil
import os
import io
import csv
import logicCasual
import fillSpeedrun

g_rom : io.BufferedIOBase

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

def itemPlace(location,itemArray) :
    #provide a locRow as in and the item array such as Missile, Super, etc
    if location['hiddenness'] == "open":
        plmid = itemArray[1]
    elif location['hiddenness'] == "chozo":
        plmid = itemArray[2]
    else:
        plmid = itemArray[3]
    # write all rom locations associated with the item location
    for address in location['locids']:
        writeItem(address, plmid, itemArray[4])
    for address in location['alternateroomlocids']:
        writeItem(address, plmid, itemArray[4])

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
    #logicChoice=""
    #while logicChoice != "C" and logicChoice != "E" :
    #    logicChoice= input("Enter C for Casual or E for Expert logic:")
    #    logicChoice = logicChoice.title()
    logicChoice="C"
    #hudFlicker=""
    #while hudFlicker != "Y" and hudFlicker != "N" :
    #    hudFlicker= input("Enter Y to patch HUD flicker on emulator, or N to decline:")
    #    hudFlicker = hudFlicker.title()
    hudFlicker = "Y" #for now
    seeeed=random.randint(1000000,9999999)
    random.seed(seeeed)
    rom1_path = "../SubversionRando/roms/Sub"+logicChoice+str(seeeed)+".sfc"
    rom_clean_path = "../SubversionRando/roms/Subversion12.sfc"
    #you must include Subversion 1.2 in your roms folder with this name^
    spoiler_file = open("../SubversionRando/spoilers/aSub"+logicChoice+str(seeeed)+".sfc.spoiler.txt", "w")

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

    createWorkingFileCopy(rom_clean_path, rom1_path)
    
    seedComplete = False
    randomizeAttempts = 0
    while seedComplete == False:
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
        #can split this to have different fill algorithms
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
                #print(u[0])
                uu=0

            if availableLocations == [] and unusedLocations != [] :
                print(f'Item placement was not successful. {len(unusedLocations)} locations remaining.')
                spoilerSave+=f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
                break

            #can split here for different fill algorithms
            placePair=fillSpeedrun.placementAlg(availableLocations, locArray, loadout, itemLists)
            #it returns your location and item, which are handled here
            placeLocation=placePair[0]
            placeItem=placePair[1]
            itemPlace(placeLocation,placeItem)
            availableLocations.remove(placeLocation)
            for itemPowerGrouping in itemLists :
                if placeItem in itemPowerGrouping :
                    itemPowerGrouping.remove(placeItem)
                    break
            loadout.append(placeItem)
            spoilerSave+=placeLocation['fullitemname']+" - - - "+placeItem[0]+"\n"

            if availableLocations == [] and unusedLocations == [] :
                print("Item placements successful.")
                spoilerSave += "Item placements successful.\n"
                seedComplete = True
                break
            
            


    # Suit animation skip patch
    writeBytes(0x20717, b"\xea\xea\xea\xea")
    # Flickering hud removal patch
    if hudFlicker == "Y" :
        #writeBytes(0x547a, b"\x02")
        #writeBytes(0x547f, b"\x00")
        uu=0
    # Morph Ball PLM patch (chozo, hidden)
    writeBytes(0x268ce, b"\x04")
    writeBytes(0x26e02, b"\x04")
    finalizeRom()
    print("Done!")
    print("Filename is "+"Sub"+logicChoice+str(seeeed)+".sfc")
    spoiler_file.write("RNG Seed: {}\n".format(str(seeeed))+"\n")
    spoiler_file.write("\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n")
    spoiler_file.write(spoilerSave)    
    print("Spoiler file is "+"Sub"+logicChoice+str(seeeed)+".sfc.spoiler.txt")




