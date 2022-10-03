import random
import sys
import argparse
import struct
import shutil
import os
import io
import pullCSV
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

def commasToList(entry) :
    #takes a commaed string entry as input, returns a list of the items in the same order without commas
    slicedEntry=[]
    lastcomma=0
    for i in range(0,len(entry)-1) :
        if entry[i] == "," :
            slicedEntry.append(entry[lastcomma:i])
            lastcomma=i+1
    slicedEntry.append(entry[lastcomma:])
    return slicedEntry

def itemPlace(locRow,itemArray) :
    #provide a locRow as in and the item array such as Missile, Super, etc
    for location in locRow[1] :
        writeItem(int(location, 16), itemArray[locRow[2]], itemArray[4]) #updated to preferred visibility

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
    rom_clean_path = "../SubversionRando/roms/Subversion11.sfc"
    #you must include Subversion 1.1 in your roms folder with this name^
    spoiler_file = open("../SubversionRando/spoilers/aSub"+logicChoice+str(seeeed)+".sfc.spoiler.txt", "w")

    csvraw= pullCSV.pullCSV()
    #Item = Name, Visible, Chozo, Hidden
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
             b"\x23\xef",
             b"\x23\xef",
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
    Screw = ["Screw Atttack",
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
    allItemList=[Missile,
             Super,
             PowerBomb,
             Morph,
             GravityBoots,
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
             Grapple,
             MetroidSuit,
             Plasma,
             Screw,
             Hypercharge,
             Charge,
             Xray,
             SpaceJump,
             Energy,
             Refuel,
             SmallAmmo,
             LargeAmmo,
             DamageAmp,
             ChargeAmp,
             SpaceJumpBoost]
    
    createWorkingFileCopy(rom_clean_path, rom1_path)
    
    #parse csvraw
    locArray=[[]] #in the form [y][x]
    x=0
    y=0
    #print("y= 0")
    for rawdata in csvraw :
        #print("x=",x)
        #print("rawdata is",rawdata)
        if x>10 :
            x=0
            #print(locArray[y][0],locArray[y][2],locArray[y][4])
            y+=1
            locArray.append([])
            #print("y=",y)
        if x==0 :
            locArray[y].append(rawdata) #index [y][0] name of location
        if x==3 :
            locArray[y].append(commasToList(rawdata)) #index [y][1] address list of location
            
        if x==4 : #index [y][2] preferred visibility
            #print("seeking in",locArray[y][1][0])
            #bitty=rom.read_from_clean(locArray[y][1][0],2)
            locArray[y].append(1)
            bitty=struct.pack('<H', int(rawdata,16))
            #print(int(rawdata,16))
            for itemcheck in allItemList :
                for indi in range (1,4) :
                    reversei = 4-indi
                    if itemcheck[reversei] == bitty :
                        locArray[y][2]=reversei
        if x==5 :
            locArray[y].append(rawdata) #index [y][3] plm identifier
        if x==10 :
            if commasToList(rawdata) != "" :
                locArray[y][1].extend(commasToList(rawdata)) #index [y][1] extra entries
            for hexi in range(0,len(locArray[y][1])-1) :
                #print("hexi is",hexi,": locArray[",y,"][1][",hexi,"]=",locArray[y][1][hexi])
                locArray[y][1][hexi] = hex(int(locArray[y][1][hexi],16))
            #print("Initialized array:",locArray[y][1])
            if locArray[y][1][len(locArray[y][1])-1] == "" :
                locArray[y][1].pop()
            #print("Corrected initialized array:",locArray[y][1])
            locArray[y].append(False) #start a logic field
            #print("locArray[",y,"] has",len(locArray[y]),"entries. Should be 5.")
        x+=1
    
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
        while unusedLocations is not [] and availableLocations is not [] :
            #print("loadout contains:")
            #print(loadout)
            for a in loadout:
                #print("-",a[0])
                uu=0 #just do nothing
                
            #update logic by updating unusedLocations
            #using helper function, modular for more logic options later
            #unusedLocations[i][4] holds the True or False for logic
            logicCasual.updateLogic(unusedLocations, locArray, loadout)

                    
            #update unusedLocations and availableLocations
            for i in range(0,len(unusedLocations)) :
                if i > len(unusedLocations)-1 :
                    break
                if unusedLocations[i][4] == True :
                    while unusedLocations[i][4] == True :
                        #print("Found available location at",unusedLocations[i][0])
                        availableLocations.append(unusedLocations[i])
                        unusedLocations.pop(i)
                        if i > len(unusedLocations)-1 :
                            break
            #print("Available locations sits at:",len(availableLocations))
            for al in availableLocations :
                #print(al[0])
                uu=0
            #print("Unused locations sits at size:",len(unusedLocations))
            #print("unusedLocations:")
            for u in unusedLocations :
                #print(u[0])
                uu=0

            if availableLocations == [] and unusedLocations == [] :
                print("Item placements successful.")
                spoilerSave += "Item placements successful.\n"
                seedComplete = True
                break

            if availableLocations == [] and unusedLocations != [] :
                print("Item placement was not successful.",len(unusedLocations),"locations remaining.")
                spoilerSave+="Item placement was not successful. "+str(len(unusedLocations))+" locations remaining.\n"
                break

            #can split here for different fill algorithms
            placePair=fillSpeedrun.placementAlg(availableLocations, locArray, loadout, itemLists)
            #it returns your location and item, which are handled here
            placeLocation=placePair[0]
            placeItem=placePair[1]
            itemPlace(placeLocation,placeItem)
            availableLocations.remove(placeLocation)
            for bank in itemLists :
                if placeItem in bank :
                    bank.remove(placeItem)
            loadout.append(placeItem)
            spoilerSave+=placeLocation[0]+" - - - "+placeItem[0]+"\n"
            
            


    # Suit animation skip patch
    writeBytes(0x27017, b"\xea\xea\xea\xea")
    # Flickering hud removal patch
    if hudFlicker == "Y" :
        writeBytes(0x547a, b"\x02")
        writeBytes(0x547f, b"\x00")
    finalizeRom()
    print("Done!")
    print("Filename is "+"Sub"+logicChoice+str(seeeed)+".sfc")
    spoiler_file.write("RNG Seed: {}\n".format(str(seeeed))+"\n")
    spoiler_file.write("\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n")
    spoiler_file.write(spoilerSave)    
    print("Spoiler file is "+"Sub"+logicChoice+str(seeeed)+".sfc.spoiler.txt")




