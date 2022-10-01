import random
import sys
import argparse
import struct
import shutil
import os
import io
import pullCSV
import logicCasual

#"roomname","roomid","area","locid","plmtypeid","plmparam","xy","plmtypename","state","alternateroomid","alternateroomlocids"

g_rom : io.BufferedIOBase

def createWorkingFileCopy(origFile, newFile) -> io.BufferedIOBase:
    if not os.path.exists(origFile):
        raise Exception(f'origFile not found: {origFile}')
    g = open(newFile, 'wb') # wb = write, binary
    shutil.copyfile(origFile, newFile)
    return g

def writeItem(address : int, plmid, ammoAmount = b"\x00"):
    if len(plmid) != 2 or len(ammoAmount) != 1:
        raise Exception(f'plmid length ({len(plmid)}) must be 2 and ammoAmount length ({len(ammoAmount)}) must be 1')
    g_rom.seek(address)
    g_rom.write(plmid)
    g_rom.seek(address+5)
    g_rom.write(ammoAmount)

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
    seeeed=random.randint(1000000,9999999)
    random.seed(seeeed)
    rom1_path = "../SubversionRando/roms/Sub"+str(seeeed)+"a3.smc"
    rom_clean_path = "../SubversionRando/roms/Subversion.smc"
    #you must include Subversion 1.1 in your roms folder with this name^
    
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
    #the first 3 items to place. First item should be morph or missile
    #extra items can be placed in order
    extraItemList=[Hypercharge,
                   Xray,
                   DamageAmp,DamageAmp,DamageAmp,DamageAmp,DamageAmp,DamageAmp,
                   ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,ChargeAmp,
                   Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy,
                   Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy,Energy,
                   Refuel,Refuel,Refuel,Refuel,Refuel,Refuel,Refuel,
                   SpaceJumpBoost,SpaceJumpBoost,SpaceJumpBoost,SpaceJumpBoost,
                   SpaceJumpBoost,SpaceJumpBoost,SpaceJumpBoost,SpaceJumpBoost,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,SmallAmmo,
                   SmallAmmo,SmallAmmo,SmallAmmo,
                   LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,
                   LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,
                   LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,LargeAmmo,
                   LargeAmmo,LargeAmmo,LargeAmmo]
    g_rom = createWorkingFileCopy(rom_clean_path, rom1_path)
    
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
        earlyItemList=[Missile,
                       Morph,
                       GravityBoots]
        progressionItemList=[Super,
                         Grapple,
                         PowerBomb,
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
                         MetroidSuit,
                         Plasma,
                         Screw,
                         SpaceJump,
                         Charge]
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

            if availableLocations[0][0] == "TORPEDO BAY" :
                randomIndex = random.randint(0,1)
                firstItems = [Missile, Morph]
                placeItem = firstItems[randomIndex]
                #print(availableLocations[0][0]," - - - ",placeItem[0])
                spoilerSave += availableLocations[0][0]+" - - - "+placeItem[0]+"\n"
                earlyItemList.pop(randomIndex)
                itemPlace(availableLocations[0],placeItem)
                availableLocations.pop()
                loadout.append(placeItem)
                
            if earlyItemList != [] and availableLocations != []:
                randomIndex=0
                if len(earlyItemList) > 1 :
                    randomIndex = random.randint(0,len(earlyItemList)-1)
                placeItem = earlyItemList[randomIndex]
                earlyItemList.pop(randomIndex)
                randomIndex=0
                if len(availableLocations) > 1 :
                    randomIndex = random.randint(0,len(availableLocations)-1)
                placeLocation = availableLocations[randomIndex]
                visitedLocations.append(availableLocations[randomIndex])
                availableLocations.pop(randomIndex)
                #print(placeLocation[0]," - - - ",placeItem[0])
                spoilerSave+=placeLocation[0]+" - - - "+placeItem[0]+"\n"
                itemPlace(placeLocation,placeItem)
                loadout.append(placeItem)
            if earlyItemList == [] and progressionItemList != [] and availableLocations != [] :
                randomIndex=0
                if len(progressionItemList) > 1 :
                    randomIndex = random.randint(0,len(progressionItemList)-1)
                placeItem = progressionItemList[randomIndex]
                progressionItemList.pop(randomIndex)
                randomIndex=0
                if len(availableLocations) > 1 :
                    randomIndex = random.randint(0,len(availableLocations)-1)
                placeLocation = availableLocations[randomIndex]
                visitedLocations.append(availableLocations[randomIndex])
                availableLocations.pop(randomIndex)
                #print(placeLocation[0]," - - - ",placeItem[0])
                spoilerSave+=placeLocation[0]+" - - - "+placeItem[0]+"\n"
                itemPlace(placeLocation,placeItem)
                loadout.append(placeItem)
            if earlyItemList == [] and progressionItemList == [] and availableLocations != []:
                randomIndex=0
                if len(extraItemList) > 1 :
                    randomIndex = random.randint(0,len(extraItemList)-1)
                if extraItemList[randomIndex] in loadout :
                    randomIndex = 50 #rather than duplicate Xray or Hypercharge, small ammo
                placeItem = extraItemList[randomIndex]
                randomIndex=0
                if len(availableLocations) > 1 :
                    randomIndex = random.randint(0,len(availableLocations)-1)
                placeLocation = availableLocations[randomIndex]
                visitedLocations.append(availableLocations[randomIndex])
                availableLocations.pop(randomIndex)
                #print(placeLocation[0]," - - - ",placeItem[0])
                spoilerSave+=placeLocation[0]+" - - - "+placeItem[0]+"\n"
                itemPlace(placeLocation,placeItem)
                if placeItem[0] == "Xray" or placeItem[0] == "Hypercharge" :
                    loadout.append(placeItem)


    # Suit animation skip patch
    g_rom.seek(0x27017)
    g_rom.write(b"\xea\xea\xea\xea")
    g_rom.close()
    print("Done!")
    print("Filename is "+"Sub"+str(seeeed)+"a3.smc")
    spoiler_file = open("../SubversionRando/spoilers/aSub"+str(seeeed)+"a3.smc.spoiler.txt", "w")
    spoiler_file.write("RNG Seed: {}\n".format(str(seeeed))+"\n")
    spoiler_file.write("\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n")
    spoiler_file.write(spoilerSave)    
    print("Spoiler file is "+"Sub"+str(seeeed)+"a3.smc.spoiler.txt")




