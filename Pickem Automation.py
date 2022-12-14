from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import time, random
import multiprocessing
from bs4 import BeautifulSoup as bs
import urllib.request
import re


def createSchedule():
    total = 0
    teamNames = {'ari': "cardinals", 'atl' : "falcons", 'bal' : "ravens", 'buf':"bills", 'car':"panthers", 
    'chi':"bears", 'cin':"bengals", 'cle':"browns", 'dal':"cowboys",'den':"broncos", 'det':"lions", 
    'gb':"packers", 'hou':"texans", 'ind':"colts", 'jax':"jaguars", 'kc':"chiefs", 'lv':"raiders", 
    'lar':'rams', 'lac':'chargers', 'mia':'dolphins', 'min':'vikings', 'ne':'patriots', 'no':'saints', 
    'nyg':'giants', 'nyj':'jets', 'phi':'eagles', 'pit':'steelers', 'sf':'49ers', 'sea':'seahawks'
    , 'tb':'buccaneers', 'ten':'titans', 'wsh':'commanders'}

    f = open("schedule.txt", "r")
    schedule = [ [0 for i in range(0) ] for j in range(18) ]
    while True:
        line = f.readline().lower().split()
        if not line:
            break
        team = teamNames.get(line[0])
        for i in range(1, 19):
            currentGame = line[i]
            if(currentGame[0] == '@'):
                currentGame = team.capitalize() + " @ " + str(teamNames.get(line[i].lstrip("@"))).capitalize()
            elif currentGame != "bye":
                currentGame = str(teamNames.get(line[i])).capitalize() + " @ " + team.capitalize()
            if (not currentGame in schedule[i-1]) and (currentGame !=  "bye"):
                schedule[i-1].append(currentGame)
    return schedule

def appendLines(schedule):
    f = open('lines.txt', 'r')
    for line in f:
        if "week" in line:
            week = int(line.split()[-1])
    f.close()

    page = urllib.request.urlopen('https://sportsbook.draftkings.com/leagues/football/nfl')
    soup = bs(page)
    teams = soup.body.findAll('div', {"class": "event-cell__name-text"})
    lines = soup.body.findAll('div', {"class": "sportsbook-outcome-cell__body no-label"})
    hash = {}
    i = 0
    for item in teams:
        hash[item.text.split()[1].lower()] = re.search(r"(\+|-)\d{1,2}(.5)?", lines[i].text).group(0)
        i += 2
        if i >= len(schedule[week]) * 4:
            break

    f = open('/Users/jonas/python-workspace/pickem files/lines.txt', 'a')
    f.write(f'\nweek {week + 1}\n')
    for team in hash:
        if hash[team][0] == '-':
            f.write(f"{team} {hash[team][1:]}\n")
    f.close()

def sundayForm(week, chatName, chat):
    schedule = createSchedule()
    # f = open('/Users/jonas/python-workspace/pickem files/TNF.txt', 'r')
    # for line in f:  
    #     if int(line.split()[0]) == week:
    #         schedule[week-1].remove(" ".join(line.strip().split()[1:]))
    appendLines(schedule)
    lines = {}
    f = open('/Users/jonas/python-workspace/pickem files/lines.txt', 'r')
    for line in f:
        if line.lower().strip() == ('week ' + str(week)):
            break
    for line in f:
        line = line.split()
        lines[line[0].capitalize()] = line[1]

    usernames = []
    for username in chat:
        usernames.append({"value":username})
    print(usernames)

    

    # Request body for creating a form
    form = {
        "info": {
            "title": chatName + " " + "Week " + str(week),
        },
    }


    # Creates the initial form
    result = form_service.forms().create(body=form).execute()

    update = {
    "requests": [{
        "updateFormInfo": {
            "info": {
                "description": "Spreads are just to show favorites. Pick winners straight up"
            },
            "updateMask": "description"
        }
    }]
    }
    # Update the form with a description
    question_setting = form_service.forms().batchUpdate(
        formId=result["formId"], body=update).execute()

    for i in range (0, len(schedule[week - 1])):
        # Request body to add a multiple-choice question
        home = schedule[week - 1][i].split()[2]
        away = schedule[week - 1][i].split()[0]
        homeline = home
        awayline = away
        if home in lines:
            homeline = f"{home} -{lines[home]}"
        elif away in lines:
            awayline = f"-{lines[away]} {away}"
        game = f"{awayline} @ {homeline}"

        NEW_QUESTION = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": game,
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": home},
                                        {"value": away}
                                    ],
                                    "shuffle": True
                                }
                            }
                        },
                    },
                    "location": {
                        "index": 0
                    }
                }
            }]
        }

        # Adds the question to the form
        question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

    NEW_QUESTION = {
        "requests": [{
            "createItem": {
                "item": {
                    "title": "user",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type" : "RADIO",
                                "options": usernames,
                                "shuffle": True
                            }
                        }
                    },
                },
                "location": {
                    "index": 0
                }
            }
        }]

    }

    question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

    NEW_QUESTION = {
        "requests": [{
            "createItem": {
                "item": {
                    "title": "name",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph" : False
                            }
                        }
                    },
                },
                "location": {
                    "index": 0
                }
            }
        }]

    }

    question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

    # Prints the result to show the question has been added
    get_result = form_service.forms().get(formId=result["formId"]).execute()
    url = "docs.google.com/forms/d/" + result["formId"]
    idf = open('/Users/jonas/python-workspace/pickem files/form links.txt', 'a')
    idf.write('\n' + chatName + " " + result["formId"])
    idf.close()
    return url


def sendDMs (usernames, url, loginUsername, loginPassword):
    browser = webdriver.Chrome('chromedriver')
    browser.implicitly_wait(60)
    browser.get('https://www.instagram.com/accounts/login/')
    # browser.get('https://www.instagram.com/direct/new/')
    input_username = browser.find_element(By.NAME, 'username')
    input_password = browser.find_element(By.NAME, 'password')
    input_username.send_keys(loginUsername)
    input_password.send_keys(loginPassword)
    input_password.send_keys(Keys.ENTER)
    browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button')
    browser.get('https://www.instagram.com/direct/new/')
    browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
    for name in usernames : 
        browser.get('https://www.instagram.com/direct/new/')
        input_dm = browser.find_element(By.NAME, 'queryBox')
        input_dm.send_keys(name)
        browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div').click()
        browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()
        dm = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        dm.send_keys(url)
        dm.send_keys(Keys.ENTER)


if __name__ == '__main__':
    SCOPES = "https://www.googleapis.com/auth/forms.body"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/Users/jonas/python-workspace/client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    while True:
        week = int(input("Week: "))
        if week > 0 and week <= 18: break


    
