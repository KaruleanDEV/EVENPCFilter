#EVERecruitmentFilter Developed by Karulean Valkyrie
#Version: 0.2 ALPHA
#---------------------[IMPORT MODULES]
import requests
import json
import os

#---------------------[DATA]
sourceTranquility = '/?datasource=tranquility'
NPCCORP = 'https://esi.evetech.net/latest/corporations/npccorps'
GETCHARACTERINFO = 'https://esi.evetech.net/latest/characters/{}' #https://esi.evetech.net/latest/characters/character_id/?datasource=tranquility
CHARACTER = 'https://zkillboard.com/autocomplete/' #We use zkillboard to find the character ID

#------------------------------------------------------------------------
#LIbrary
#return a list ID from NPCCORP using requests and write them to a txt file call NPCCORPID.txt
def NPCCORPIDUPDATE():
    r = requests.get(NPCCORP + sourceTranquility, headers={"Cache-Control": "no-cache"})
    if r.status_code == 200:
        data = r.json()
        with open('NPCCORPID.txt', 'w') as f:
            for item in data:
                f.write("%s\n" % item)
        f.close()
        print("List of NPC corporations has been updated.")
    else: 
        print(r.status_code, r.reason)

#Clean dataset for zkill
def CleanDATASET():
    if os.path.exists('CharacterNameProcess.txt'):
        os.remove('CharacterNameProcess.txt')
        print("CharacterNameProcess.txt removed")
    with open('CharacterName.txt', 'r') as f:
        for line in f:
            line = line.replace(" ", "%20")
            with open('CharacterNameProcess.txt', 'a') as f2:
                f2.write(line)
    f.close()
    print("CharacterName.txt cleaned and saved as CharacterNameProcess.txt")

#convert CharacterNameProcess.txt to ID using zkillboard
def CharacterID():
    with open('CharacterNameProcess.txt', 'r') as f:
        if os.path.exists('CharacterID.txt'):
            os.remove('CharacterID.txt')
            print("CharacterID.txt removed")
        for line in f:
            r = requests.get(CHARACTER + line)
            if r.status_code == 200:
                data = r.json()
                for key in data:
                    if key['type'] == 'character':
                        with open('CharacterID.txt', 'a') as f2:
                            f2.write(str(key['id']) + "\n")
                            print(str(key['id']))
                    else:
                        print("- No character ID Found -")
                        break
            else:
                print(r.status_code)

def DATASETCHECK():
    npccorp = open("NPCCORPID.txt", "r")
    #append npccorp.txt into an array without \n
    npccorparray = []
    for line in npccorp:
        npccorparray.append(line.rstrip())
    print("List of NPC corporations: ", npccorparray)
    rdata = open("CharacterID.txt", "r")
    newlineappend = 0
    with rdata as newData:
        for character in newData:
            newData.seek(0)
            charfix = newData.read().splitlines()
            if str(character) in charfix:
                print("\n Character: {} BLACKLISTED".format(character))
                
            else:
			    #Send ID to ESI for PublicData
                #accept request header json
                idline = character.rstrip()
                url = 'https://esi.evetech.net/latest/characters/{}/?datasource=tranquility'.format(idline)
                fetchPublic = requests.get(url)
                getPublic = fetchPublic.json()
                idCorporation = getPublic["corporation_id"]
                idName = getPublic["name"]
			    #sorttrue
                
                datacore = str(idCorporation).rstrip()
                if str(datacore) in npccorparray:
                    print("ID:", character, "| Name:", idName, "| Corporation:", idCorporation, "| NPC Corporation: True")
                    results = open("result.txt", "a+")
                    blacklist = open("Blacklist.txt", "a+")
                    #<font size="12" color="#bfffffff"></font><font size="12" color="#ffd98d00"><loc><a href="showinfo:1386//97143141">01 Chaos</a></font><font size="12" color="#bfffffff">,</loc></font>
                    results.writelines('\n\n<font size="12" color="#bfffffff"></font><font size="12" color="#ffd98d00"><loc><a href="showinfo:1386//{}">{}</a></font><font size="12" color="#bfffffff">,</loc></font>'.format(character, idName))
                    blacklist.writelines("{}".format(character))
                    blacklist.close()
                    results.close()
                    newlineappend +=1 #check

			    #sortfalse
                else:
                    print("ID:", character, "| Name:", idName, "| Corporation:", idCorporation, "| NPC Corporation: False")

			
			    #spaced every 50th lines
                if newlineappend == 50:
                    newlineappend = 0
                    results = open("result.txt", "a+")
                    results.writelines("\n\n STOP COPYING [50th Pilot in set] \n\n")
                    results.close()
    
#runfunction
def run():
    print('Updating List of NPC Corporation....')
    NPCCORPIDUPDATE()
    print('Updating Character Name....')
    CleanDATASET()
    print('Updating Character ID....')
    CharacterID()
    print('Checking for ID....')
    if os.path.exists('CharacterID.txt'):
        print('ID found.')
    else:
        exit()
    DATASETCHECK()
#------------------------------------------------------------------------
print("EVERecruitmentFilter v0.2 ALPHA")

while True:
    cinput = input(">>> Enter run to start the program. || Enter quit to exit the program. <<< \n")
    if cinput == "quit":
        break
    if cinput == "run":
        run()