# imports csv module into this Python script (csv module part of Python's standard library - so you will have it if you have Python)
import csv

# This is a function for caculating new elo scores based on current elo and the match result
# This can be modified to allow for a "thrashing" boost to the elo score changes, based on whatever model we would like to try!
# Inputs are t1, t2 (elo scores), match result (goals), K value
# Outputs the two new elo scores respectively.
def eloCalculation(t1, t2, result, weightK):
    # Step 1
    T1 = 10 ** (t1/400)
    T2 = 10 ** (t2/400)
    # Step 2
    E1 = T1/(T1+T2)
    E2 = T1/(T1+T2)
    # Step 3
    if result[0] > result[1]:
        # if team1 wins (scores more goals)
        S1 = 1
        S2 = 0
    elif result[0] < result[1]:
        # if team2 wins (scores more goals)
        S1 = 0
        S2 = 1
    elif result[0] == result[1]:
        # if draw (scores same amount of goals)
        S1 = 1/2
        S2 = 1/2
    # Step 4
    t1_ = round(t1 + weightK * (S1 - E1))
    t2_ = round(t2 + weightK * (S2 - E2))
    
    return(t1_, t2_)
    
def calculateMatches(csvs, eloOutputFile, headersSet = False):
    # A dictionary of teams, each with values that are their current Elo, and a dictionary their elos in the past
    teamsAndElos = {'Chelsea': [startingElo, {}]}
    # A track of all the dates matches are played on
    allDates = []
    
    lowestElo = startingElo
    for csv in csvs:
        # for each row in the csv, and it's row number i.
        for i, row in enumerate(csv):
            # Headers of csv, not data - so skip
            if i == 0:
                pass
            # The data leaves rows blank inbetween days of matches, which is checked here - skip
            elif ''.join(row) == '' :
                pass
            # Each row is a match - time to record it and caculate elo!
            else:
                # Record date
                currentDate = row[2]
                if currentDate not in allDates:
                    allDates.append(currentDate)
                # Get teams
                team1 = row[4]
                team2 = row[6]
                # Gets the score as two numbers in a tuple, first is for team1's goal count, second for team 2's goal count 
                score = (int(row[5][0]), int(row[5][-1]))
                # Add teams to our records if we haven't seen them yet
                if team1 not in teamsAndElos:
                    teamsAndElos[team1] = [lowestElo, {}]
                if team2 not in teamsAndElos:
                    teamsAndElos[team2] = [lowestElo, {}]
                # Calculate new elos
                team1NewElo, team2NewElo = eloCalculation(teamsAndElos[team1][0], teamsAndElos[team2][0], score, weightK)
                # Record elos in history dictionary
                teamsAndElos[team1][1][currentDate] = team1NewElo
                teamsAndElos[team2][1][currentDate] = team2NewElo
                # Update current elos
                teamsAndElos[team1][0] = team1NewElo
                teamsAndElos[team2][0] = team2NewElo
        # Gets current lowest elo score (so when new season start (new csv) new teams join with it)
        sortedEloList = [teamsAndElos[team][0] for team in teamsAndElos]
        sortedEloList.sort()
        lowestElo = sortedEloList[0]
     
    # Now we have run all the data through the elo calculators
    # Time to print out our results to an output csv 
    
    # Print header - "Date" and all the team names
    eloOutputFile.write('Dates, '+ ', '.join([team for team in teamsAndElos])+'\n')
    for date in allDates:
        line = date
        for team in teamsAndElos:
            historicEloRatingsForTeam = teamsAndElos[team][1]
            try:
                v = historicEloRatingsForTeam[date]
                line += ","+str(v)
            except:
                line += ","
        eloOutputFile.write(line+'\n')
    
          
startingElo = 1000
weightK = 32
csv_16_17 = "16_17Season.csv"
csv_17_18 = "17_18Season.csv"

with open(csv_16_17, newline='') as csvfile_16_17:
    csvreader_16_17 = csv.reader(csvfile_16_17, delimiter=',')    
    with open(csv_17_18, newline='') as csvfile_17_18:
        csvreader_17_18 = csv.reader(csvfile_17_18, delimiter=',')
        with open ('output.csv', "w") as outputFile:
            csvList = [csvreader_16_17, csvreader_17_18]
            calculateMatches(csvList, outputFile)