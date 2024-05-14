import requests as req
from bs4 import BeautifulSoup as Bsoup
from time import sleep
import traceback ### for easier try-except stuff


def convertStrIntoUrl(name):
    if 'jr' in name or 'junior' in name: ### if "Jr" is in name (The site doesnt use them)
        try:
            name = name.replace('jr', '')
        except Exception as e:
            print(Exception)
            try:
                name = name.remove('junior', '')
            except:
                pass



    convertedName = name

    convertedName = convertedName.replace(' ', '-') ### Converting basic name's space into a "-"

    #print(convertedName)
    return convertedName

def findMostSimilarName(originalFullName, originalSurname, namesGiven):
    print('Player "' + originalFullName + '" is not found, did you mean...')
    allNames = []
    for i in namesGiven:
        ### 12 - the universal end of blank space
        allNames.append(i.text[12:-1]) ### Adding all names into a list to actually have only strings
    

    surNames = []
    allNamesReadable = []
    for i in allNames:
        surNames.append(i.split(',')[0])


    surNamesSimilarities = {} ### Surname -> Similarity Rating
    ### Similarity rating is calculated for how many letters are placed in the same place
    ### so basically if originalSurname[index] == comparedSurname[index]
    ### A flawed system, but a working nonetheless

    for sName in surNames:
        surNamesSimilarities[sName] = 0

        nameToGoThrough = min(sName, originalSurname, key=(len)) ### doing allat jsut to not have to deal with the "index out of bounds" error
        nameToCheckThrough = max(sName, originalSurname, key=(len)) ### getting the non-picked name
        
        if nameToGoThrough.lower() == nameToCheckThrough.lower():
            nameToGoThrough = sName
            nameToCheckThrough = originalSurname
            ### IF both vars are the same, meaning they have the same len, i just assign them to orignial names with no nothing
        
        #eprint(nameToCheckThrough, nameToGoThrough)
        #print(sName)

        for ind in range(len(nameToGoThrough)):
            #print(ind)
            #print(nameToCheckThrough[ind], nameToGoThrough[ind])
            if nameToCheckThrough[ind].lower() == nameToGoThrough[ind].lower():
                #print(nameToCheckThrough[ind], nameToGoThrough[ind])
                #print(nameToCheckThrough, nameToGoThrough)
                #print('similarity point')
                surNamesSimilarities[sName] += 1

        

    SimilarSurnameSorted = dict(sorted(surNamesSimilarities.items(), reverse=True, key = lambda item: item[1]))#sorted(surNamesSimilarities, reverse=True)
    mostSimilarSurname = list(SimilarSurnameSorted.keys())[0]

    mostSimilarFullNames = [] ### A list because there might be multiple players with the same surname. e.g. the Curry brothers


    for i in allNames:
        if mostSimilarSurname in i:
            mostSimilarFullNames.append(i)

    if len(mostSimilarFullNames) == 1:
        print(mostSimilarFullNames[0][0:len(mostSimilarFullNames[0]) - 9] + '?') ###mostSimilarFullNames[0][0:len(mostSimilarFullNames[0]) looks confusing, i know, but it does the same thing as fName[0:len(fName) - 9]
    else:
        allPossibleNamesStr =  ''
        for fName in mostSimilarFullNames:
            allPossibleNamesStr += fName[0:len(fName) - 9] + ' or '

        allPossibleNamesStr = allPossibleNamesStr.removesuffix(' or ')

        allPossibleNamesStr += '?'

        print(allPossibleNamesStr)

    
    

url = 'https://hoopshype.com/player/' ### Site where im taking the info from

urlAllPlayers = 'https://hoopshype.com/players/' ## all players main page, from where i  will try to find "sound-alikes"

NBA_playerName = ''

while NBA_playerName != 'exit' and NBA_playerName != 'end':
    NBA_playerName = input('Input player full name (first name -> last name):').lower()

    response = req.get(url + convertStrIntoUrl(NBA_playerName) + '/2k') ### Searches on the site


    soup = Bsoup(response.text, 'lxml')

    preinfo = soup.find_all('span', class_='player-bio-text-line') ### Searches the explanation e.g. if the player is a "C", will be "Position:"
    info = soup.find_all('span', class_='player-bio-text-line-value') ### The info itself (Position, salary, height, etc.)


    if len(info) == 0 or len(preinfo) ==0: ### if not well spelled input Name
        print("Invalid Player Name")

        try:
            playerSurname = NBA_playerName.split(' ')[1]

            #print(playerSurname)


            ### Start search for similar-sounding names
            ### Incase it was a misinput or something
            allPlayers = req.get(urlAllPlayers)
            soupSimilar = Bsoup(allPlayers.text, 'lxml')
            
            surnameSameLetter = soupSimilar.find('div', id='letter-' + playerSurname[0]) ### Searches the column with the players of the same surname First Letter
            onlyPlayers = surnameSameLetter.find_all('a', class_ = 'player-name') ### Searches exclusively the players from this column
            
            ### onlyPlayers is given out like the HTML-based array with text inside each value

            findMostSimilarName(NBA_playerName, playerSurname, onlyPlayers)

        except Exception as e:
            print(traceback.format_exc())

    else:
        for i in range(len(preinfo) - 1):
            print(preinfo[i].text, info[i].text) ### Prints the exact info on the plr

    
    print('---------')