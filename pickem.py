import time
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from bs4 import BeautifulSoup as bs
import urllib.request

SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

teamNames = {'ari': "cardinals", 'atl' : "falcons", 'bal' : "ravens", 'buf':"bills", 'car':"panthers", 
'chi':"bears", 'cin':"bengals", 'cle':"browns", 'dal':"cowboys",'den':"broncos", 'det':"lions", 
'gb':"packers", 'hou':"texans", 'ind':"colts", 'jax':"jaguars", 'kc':"chiefs", 'lv':"raiders", 
'lar':'rams', 'lac':'chargers', 'mia':'dolphins', 'min':'vikings', 'ne':'patriots', 'no':'saints', 
'nyg':'giants', 'nyj':'jets', 'phi':'eagles', 'pit':'steelers', 'sf':'49ers', 'sea':'seahawks'
, 'tb':'buccaneers', 'ten':'titans', 'wsh':'commanders'}




chats = {
    
}


toBeAdded = {}

def readForm(chatName, week):
    fid = open('/Users/jonas/python-workspace/pickem files/form links.txt', 'r')
    while fid.readline().lower().strip() != 'week ' + str(week): pass

    while True:
        line = fid.readline()
        if chatName in line: 
            id = line.split()[-1]
            break

    result = service.forms().responses().list(formId=id).execute()

    ind = -1
    for i in range(0, len(result['responses'])):
        responseArr = []
        for response in result['responses'][0]['answers']: 
            responseArr.append(result['responses'][i]['answers'][response]['textAnswers']['answers'][0]['value'])

        if ind == -1:
            for r in responseArr:
                if r in chats[chatName][1]:
                    ind = responseArr.index(r)
            if ind == -1: continue
            
        if responseArr[ind] in toBeAdded.keys(): 
            raise ImportError ("duplicate username found in chat " + str(chatName))

        toBeAdded[responseArr[ind]] = ""

        for r in responseArr:
            if r.lower() in teamNames.values():
                toBeAdded[responseArr[ind]] +=  ' ' + r

def addWinners(week):
    f = open('/Users/jonas/python-workspace/pickem files/winners.txt', 'a')
    f.write("\n")
    page = urllib.request.urlopen(f'https://www.espn.com/nfl/scoreboard/_/week/{week}/year/2022/seasontype/2')
    soup = bs(page)
    teams = soup.body.findAll('div', {"class": "ScoreCell__TeamName"})
    scores = soup.body.findAll('div', {"class": "ScoreCell__Score"})

    i = 0
    games = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},]

    for team in teams:
        games[int(i/2)][team.text] = int(scores[i].text)
        i += 1

    winners = set()
    for game in games:
        if game == {}: break
        f.write((max(game, key = game.get)).lower() + " ")
    f.close()



def pickProcessing(picksPool, recordsPool, winnersFileName, weekByWeek, chatName):
    picks_f = open(picksPool, "r")
    winners_f = open(winnersFileName, "r")
    records_f = open(recordsPool, "r+")
    records_f.truncate(0)
    recordsHash = {}
    for line in picks_f:
        line = line.lower().split()
        if len(line) == 0: continue
        if line[0] == "week":
            week = int(line[1])
        winners = ""
        if line[0] != "week":
            wins = 0
            losses = 0
            ties = 0
            winners_f = open(winnersFileName, "r")
            for i in range(0, week):
                winners = winners_f.readline().lower().split()

            line[0] = line[0].capitalize()
            while not line[1] in teamNames.values():
                line[0] += " " + line[1].capitalize()
                line.pop(1)

            name = line[0].lower()
            if recordsHash.get(name) == None:
                recordsHash[name] = [0, 0, 0]

            for team in winners:
                if team in line:
                    wins += 1
                elif team == "tie":
                    ties += 1
                else:
                    losses += 1
            
            if "tie" in winners:
                recordsHash[name].append("Week " + str(week) + ": " + str(wins) + "-" + str(losses) + "-" + str(ties))
                recordsHash[name][0] += wins
                recordsHash[name][1] += losses
                recordsHash[name][2] += ties
            else:
                recordsHash[name].append("Week " + str(week) + ": " + str(wins) + "-" + str(losses))
                recordsHash[name][0] += wins
                recordsHash[name][1] += losses

    # sorting
    percentageHash = {}
    for name in recordsHash:
        percentageHash[name] = (recordsHash[name][0]/(recordsHash[name][0] +
                recordsHash[name][1]))*100
    sortedNames = []
    sorted_keys = sorted(percentageHash, key=percentageHash.get, reverse=True)
    for w in sorted_keys:
        sortedNames.append(w)
    records_f.write(f"@all {chatName} PICKEM\n\n")
    if weekByWeek:
        for name in sortedNames:
            records_f.write("@" + name + "\n")
            records_f.write("Total: " + str(recordsHash[name][0]) + "-" + str(recordsHash[name][1]))
            if recordsHash[name][2] == 0:
                records_f.write(" (" + "{:.2f}".format(percentageHash[name]) + "%)\n")
            else:
                records_f.write("-" + str(recordsHash[name][2]) + " (" 
                + "{:.2f}".format(percentageHash[name]) + "%)\n")

            for i in range(3, len(recordsHash[name])):
                records_f.write(recordsHash[name][i] + '\n')
            records_f.write('\n')
    else:
        for name in sortedNames:
            records_f.write("@" + name + "\n")
            records_f.write("Total: " + str(recordsHash[name][0]) + "-" + str(recordsHash[name][1]))
            if recordsHash[name][2] == 0:
                records_f.write(" (" + "{:.2f}".format(percentageHash[name]) + "%)\n")
            else:
                records_f.write("-" + str(recordsHash[name][2]) + " (" 
                + "{:.2f}".format(percentageHash[name]) + "%)\n")
            records_f.write("Last week: " + (str(recordsHash[name][len(recordsHash[name]) - 1]).split())[2] + "\n\n")
    

def processAllChats(weekByWeek, week):
    for key in chats:
        readForm(key, week)
    for key in chats:
        picks_f = open(chats[key][0], 'a')
        picks_f.write(f"\nWeek {week}\n")
        for name in toBeAdded:
            if name in chats[key][1]:
                picks_f.write(f'{name} {toBeAdded[name]}\n')
        picks_f.close()
    # for key in chats:
    #     pickProcessing(chats[key][0], chats[key][2], winnersFileName, weekByWeek, key)

