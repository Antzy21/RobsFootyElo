# imports csv module into this Python script (csv module part of Python's standard library - so you will have it if you have Python)
from datetime import datetime
import time
import eloMath
from readCsvs import readCsvs
from classes import *

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
     
def eloByDate(seasons : list[Season]):
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
            H, D, A = eloMath.eloPrediction(game.homeEloBefore, game.awayEloBefore)
            dates[currentDate][game.home.name] = H*100
            dates[currentDate][game.away.name] = A*100
    
    return dates
    
def constructDateCsv(
    outputFileName: str,
    datesDict: dict[datetime, dict[str]],
    printLine: bool = True
    ):
    # Now we have run all the data through the elo calculators
    # Time to print out our results to an output csv 
    print(f"Writing to {outputFileName}.csv")
    time.sleep(1)
    
    with open(f'{outputFileName}.csv', "w") as outputFile:
        # Print header - "Date" and all the team names
        line = 'Dates, '+ ', '.join([team for team in teams])+'\n'
        outputFile.write(line)
        if printLine:
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
            if printLine:
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

eloByDates = eloByDate(seasons)
constructDateCsv("EloRatings", eloByDates, printLine = False)

winProbByDates = winProbabilityByDate(seasons, teams)
constructDateCsv("Probabilities", winProbByDates, printLine = False)

input("Press any key to exit")