from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools



usernames = []

loginUsername = ''
password = ''

def form():
    teamNames = {'ari': "cardinals", 'atl' : "falcons", 'bal' : "ravens", 'buf':"bills", 'car':"panthers", 
'chi':"bears", 'cin':"bengals", 'cle':"browns", 'dal':"cowboys",'den':"broncos", 'det':"lions", 
'gb':"packers", 'hou':"texans", 'ind':"colts", 'jax':"jaguars", 'kc':"cheifs", 'lv':"raiders", 
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
            elif currentGame != "BYE":
                currentGame = str(teamNames.get(line[i])).capitalize() + " @ " + team.capitalize()

            if (not currentGame in schedule[i-1]) and (currentGame !=  "BYE"):
                schedule[i-1].append(currentGame)

    week = int(input("Week: "))

    SCOPES = "https://www.googleapis.com/auth/forms.body"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    # Request body for creating a form
    form = {
        "info": {
            "title": "Week " + str(week),
        },
    }


    # Creates the initial form
    result = form_service.forms().create(body=form).execute()

    for i in range (0, len(schedule[week - 1])):
        # Request body to add a multiple-choice question
        home = schedule[week - 1][i].split()[2]
        away = schedule[week - 1][i].split()[0]
        NEW_QUESTION = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": schedule[week-1][i],
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
    return url

def sendDMs (usernames, url, loginUsername, loginPassword):
    browser = webdriver.Chrome('chromedriver')
    browser.implicitly_wait(60)
    browser.get('https://www.instagram.com/accounts/login/')

    input_username = browser.find_element(By.NAME, 'username')
    input_password = browser.find_element(By.NAME, 'password')
    input_username.send_keys(loginUsername)
    input_password.send_keys(loginPassword)
    input_password.send_keys(Keys.ENTER)
    browser.get('https://www.instagram.com/direct/new/')
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
    for name in usernames : 
        browser.get('https://www.instagram.com/direct/new/')
        input_dm = browser.find_element(By.NAME, 'queryBox')
        input_dm.send_keys(name)
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/div').click()
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()
        dm = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        dm.send_keys(url)
        dm.send_keys(Keys.ENTER)

url = form()
print(url)
# sendDMs(usernames, url)