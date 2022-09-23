teamNames = {'ari': "cardinals", 'atl' : "falcons", 'bal' : "ravens", 'buf':"bills", 'car':"panthers", 
'chi':"bears", 'cin':"bengals", 'cle':"browns", 'dal':"cowboys",'den':"broncos", 'det':"lions", 
'gb':"packers", 'hou':"texans", 'ind':"colts", 'jax':"jaguars", 'kc':"cheifs", 'lv':"raiders", 
'lar':'rams', 'lac':'chargers', 'mia':'dolphins', 'min':'vikings', 'ne':'patriots', 'no':'saints', 
'nyg':'giants', 'nyj':'jets', 'phi':'eagles', 'pit':'steelers', 'sf':'49ers', 'sea':'seahawks'
, 'tb':'buccaneers', 'ten':'titans', 'wsh':'commanders'}

# parameters(text file with picks, text file with picks, text file with winners, boolea that speicifies format you want to output)
def pickProcessing(picksPool, recordsPool, winnersFileName, weekByWeek):
    picks_f = open(picksPool, "r")
    winners_f = open(winnersFileName, "r")
    records_f = open(recordsPool, "r+")
    records_f.truncate(0)
    recordsHash = {}
    for line in picks_f:
        line = line.lower().split()
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

            name = line[0]
            if recordsHash.get(name) == None:
                recordsHash[name] = [0, 0, 0]

            for i in range (1, len(line)):
                if line[i] in winners:
                    wins += 1
                else:
                    losses += 1
            if "tie" in winners:
                losses -= 1
                ties += 1
                recordsHash[name].append("Week " + str(week) + ": " + str(wins) + "-" + str(losses) + "-" + str(ties))
                recordsHash[name][0] += wins
                recordsHash[name][1] += losses
                recordsHash[name][2] += ties
            else:
                recordsHash[name].append("Week " + str(week) + ": " + str(wins) + "-" + str(losses))
                recordsHash[name][0] += wins
                recordsHash[name][1] += losses
            
    if weekByWeek:
        for name in recordsHash:
            records_f.write(name + "\n")
            records_f.write("Total: " + str(recordsHash[name][0]) + "-" + str(recordsHash[name][1]) + "-" + 
            str(recordsHash[name][2]) + "\n")
            for i in range(3, len(recordsHash[name])):
                records_f.write(recordsHash[name][i] + '\n')
            records_f.write('\n')
    else:
        for name in recordsHash:
            records_f.write(name.capitalize() + "\n")
            records_f.write("Total: " + str(recordsHash[name][0]) + "-" + str(recordsHash[name][1]) + "-" + 
            str(recordsHash[name][2]) + "\n")
            records_f.write("Last week: " + (str(recordsHash[name][len(recordsHash[name]) - 1]).split())[2] + "\n\n")

weekByWeek = True
while True:
    weekByWeek = input("Every week?(y/n) ")
    if weekByWeek.lower() == "y":
        break
    elif weekByWeek.lower() == "n":
        weekByWeek = False
        break
