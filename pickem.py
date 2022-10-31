teamNames = {'ari': "cardinals", 'atl' : "falcons", 'bal' : "ravens", 'buf':"bills", 'car':"panthers", 
'chi':"bears", 'cin':"bengals", 'cle':"browns", 'dal':"cowboys",'den':"broncos", 'det':"lions", 
'gb':"packers", 'hou':"texans", 'ind':"colts", 'jax':"jaguars", 'kc':"chiefs", 'lv':"raiders", 
'lar':'rams', 'lac':'chargers', 'mia':'dolphins', 'min':'vikings', 'ne':'patriots', 'no':'saints', 
'nyg':'giants', 'nyj':'jets', 'phi':'eagles', 'pit':'steelers', 'sf':'49ers', 'sea':'seahawks'
, 'tb':'buccaneers', 'ten':'titans', 'wsh':'commanders'}

# picksPool is the file where picks are made, recordsPool is output, winnersFileName is 
# where winners from the week are, weekbyweek is a boolean
# for how you want the output to look
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

    if weekByWeek:
        for name in sortedNames:
            records_f.write(name + "\n")
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
            records_f.write(name + "\n")
            records_f.write("Total: " + str(recordsHash[name][0]) + "-" + str(recordsHash[name][1]))
            if recordsHash[name][2] == 0:
                records_f.write(" (" + "{:.2f}".format(percentageHash[name]) + "%)\n")
            else:
                records_f.write("-" + str(recordsHash[name][2]) + " (" 
                + "{:.2f}".format(percentageHash[name]) + "%)\n")
            records_f.write("Last week: " + (str(recordsHash[name][len(recordsHash[name]) - 1]).split())[2] + "\n\n")

while True:
    weekByWeek = input("Every week?(y/n) ")
    if weekByWeek.lower() == "y":
        break
    elif weekByWeek.lower() == "n":
        weekByWeek = False
        break
