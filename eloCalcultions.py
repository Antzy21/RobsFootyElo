# imports csv module into this Python script (csv module part of Python's standard library - so you will have it if you have Python)
import csv
from datetime import datetime
import time
import eloPrediction

# This is a function for caculating new elo scores based on current elo and the match result
# This can be modified to allow for a "thrashing" boost to the elo score changes, based on whatever model we would like to try!
# Inputs are t1, t2 (elo scores), match result (goals), K value
# Outputs the two new elo scores respectively.
def eloCalculation(t1, t2, result : tuple[int, int], weightK=32):
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

class Team:
    def __init__(self, name) -> None:
        self.name = name
        self.elo = None
        self.matchesPlayed = 0
    def updateElo(self, elo):
        self.elo = elo
        self.matchesPlayed += 1

class Game:
    def __init__(self, season, date, home, away, score) -> None:
        self.season = season
        self.date = date
        self.home : Team = home
        self.away : Team = away
        self.score : tuple[int, int] = score
        self.homeEloBefore = None
        self.homeEloAfter = None
        self.awayEloBefore = None
        self.awayEloAfter = None
    def playMatch(self):
        self.homeEloBefore = self.home.elo
        self.awayEloBefore = self.away.elo
        homeNew, awayNew = eloCalculation(self.home.elo, self.away.elo, self.score)
        self.home.updateElo(homeNew)
        self.away.updateElo(awayNew)
        self.homeEloAfter = homeNew
        self.awayEloAfter = awayNew

class Season:
    def __init__(self, name) -> None:
        self.name = name
        self.games : list[Game] = []
    def addGame(self, game: Game):
        self.games.append(game)

def readCsvs(csvs: list[str]) -> tuple[list[Season], dict[str, Team]]:
    seasons : list[Season] = []
    teams : dict[str, Team] = {}
    for seasonCsv in csvs:
        season = Season(seasonCsv)
        with open(seasonCsv, newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(csvReader):
                # Headers of csv, not data - so skip
                if i == 0:
                    pass
                # The data leaves rows blank inbetween days of matches, which is checked here - skip
                elif ''.join(row) == '' :
                    pass
                # Each row is a match - time to record it and caculate elo!
                else:
                    # Record date
                    year, month, day = row[2].split("-")
                    date = datetime(int(year), int(month), int(day))
                    # Get teams
                    homeTeamName = row[4]
                    awayTeamName = row[6]
                    
                    if homeTeamName not in teams:
                        teams[homeTeamName] = Team(homeTeamName)
                    if awayTeamName not in teams:
                        teams[awayTeamName] = Team(awayTeamName)
                        
                    # Gets the score as two numbers in a tuple, first is for team1's goal count, second for team 2's goal count 
                    score = (int(row[5][0]), int(row[5][-1]))
                    game = Game(seasonCsv, date, teams[homeTeamName], teams[awayTeamName], score)
                    season.addGame(game)
        seasons.append(season)
    return (seasons, teams)

def calculateElos(seasons: list[Season], teams: dict[str, Team], startingElo: int) -> None:
    print("Running Calculations")
    time.sleep(1)
    lowestElo = startingElo
    for season in seasons:
        for game in season.games:
            if game.home.elo is None:
                game.home.elo = lowestElo
            if game.away.elo is None:
                game.away.elo = lowestElo
            game.playMatch()
        # Gets current lowest elo score (so when new season start (new csv) new teams join with it)
        eloList = [teams[team].elo for team in teams]
        lowestElo = 100000
        for elo in eloList:
            if elo is not None and elo < lowestElo:
                lowestElo = elo
     
def eloByDate(seasons : list[Season], teams : dict[str, Team]):
    dates : dict[datetime, dict[str]] = {}
    currentDate = None
    for season in seasons:
        for game in season.games:
            if currentDate is None or game.date > currentDate:
                currentDate = game.date
                dates[currentDate] = {}
            dates[currentDate][game.home.name] = game.homeEloAfter
            dates[currentDate][game.away.name] = game.awayEloAfter
    
    return dates
     
def winProbabilityByDate(seasons : list[Season], teams : dict[str, Team]):
    dates : dict[datetime, dict[str]] = {}
    currentDate = None
    for season in seasons:
        for game in season.games:
            if currentDate is None or game.date > currentDate:
                currentDate = game.date
                dates[currentDate] = {}
            H, D, A = eloPrediction.eloPrediction(game.homeEloBefore, game.awayEloBefore)
            dates[currentDate][game.home.name] = H*100
            dates[currentDate][game.away.name] = A*100
    
    return dates
    
def constructDateCsv(outputFileName: str, datesDict: dict[datetime, dict[str]]):
    # Now we have run all the data through the elo calculators
    # Time to print out our results to an output csv 
    print(f"Writing to {outputFileName}.csv")
    time.sleep(1)
    
    with open(f'{outputFileName}.csv', "w") as outputFile:
        # Print header - "Date" and all the team names
        line = 'Dates, '+ ', '.join([team for team in teams])+'\n'
        outputFile.write(line)
        print(line)
        
        for date in datesDict:
            row = datesDict[date]
            line = f"{date}"
            for team in teams:
                try:
                    value = round(row[team], 1)
                except:
                    value = ""
                line += f", {value}"
            print(line)           
            line += "\n"
            outputFile.write(line)            
    
startingElo = 1000
csv_15_16 = "15_16Season.csv"
csv_16_17 = "16_17Season.csv"
csv_17_18 = "17_18Season.csv"
csv_18_19 = "18_19Season.csv"

print("Starting Elo:", startingElo)

time.sleep(1)

csvList = [
    csv_18_19,
    csv_17_18,
    csv_16_17,
    csv_15_16,
]

seasons, teams = readCsvs(csvList)

calculateElos(seasons, teams, startingElo)

eloByDates = eloByDate(seasons, teams)
constructDateCsv("EloRatings", eloByDates)

winProbByDates = winProbabilityByDate(seasons, teams)
constructDateCsv("Probabilities", winProbByDates)

input("Press any key to exit")