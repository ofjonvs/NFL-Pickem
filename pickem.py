teamNames = {'ari': "cardinals", 'atl' : "falcons", 'bal' : "ravens", 'buf':"bills", 'car':"panthers", 
'chi':"bears", 'cin':"bengals", 'cle':"browns", 'dal':"cowboys",'den':"broncos", 'det':"lions", 
'gb':"packers", 'hou':"texans", 'ind':"colts", 'jax':"jaguars", 'kc':"cheifs", 'lv':"raiders", 
'lar':'rams', 'lac':'chargers', 'mia':'dolphins', 'min':'vikings', 'ne':'patriots', 'no':'saints', 
'nyg':'giants', 'nyj':'jets', 'phi':'eagles', 'pit':'steelers', 'sf':'49ers', 'sea':'seahawks'
, 'tb':'buccaneers', 'ten':'titans', 'wsh':'commanders'}

picks_f = open("picks.txt", "r")
winners_f = open("winners.txt", "r")
records_f = open("/Users/jonas/Library/Mobile Documents/com~apple~CloudDocs/records.txt", "r+")
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
        winners_f = open("winners.txt", "r")
        for i in range(0, week):
            winners = winners_f.readline().lower().split()
        name = line[0].lower()
        if recordsHash.get(name) == None:
            recordsHash[name] = [0, 0]

        for i in range (1, len(line)):
            if line[i] in winners:
                wins += 1
            else:
                losses += 1

        recordsHash[name].append("Week " + str(week) + ": " + str(wins) + "-" + str(losses))
        recordsHash[name][0] += wins
        recordsHash[name][1] += losses
        

for name in recordsHash:
    records_f.write(name.capitalize() + "\n")
    records_f.write("Total: " + str(recordsHash[name][0]) + "-" + str(recordsHash[name][1]) + "\n")
    for i in range(2, len(recordsHash[name])):
        records_f.write(recordsHash[name][i] + '\n')
    records_f.write('\n')
