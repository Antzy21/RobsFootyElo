from helpers.classes import *
from datetime import datetime
import csv
from pathlib import PurePath, Path

def readCsvs() -> dict[list[dict[str, str]]]:
    outputs : dict[list[dict[str, str]]] = {}
    path = PurePath()
    path = path.parent.joinpath("seasonCsvs")
    #for leaguePath in Path(path).iterdir():
    leaguePath = path.joinpath("PremierLeague")
    for seasonCsvPath in Path(leaguePath).iterdir():
        output : list[dict[str, str]] = []
        with Path(seasonCsvPath).open() as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(csvReader):
                if i == 0:
                    headers = row
                else:
                    rowDict : dict[str, str] = {}
                    for j, cell in enumerate(row):
                        rowDict[headers[j]] = cell
                    output.append(rowDict)
        outputs[seasonCsvPath] = output
        path.parent
        #path.parent
    return outputs

def tryGetCell(names: list[str], row):
    if len(names) == 0:
        raise
    try:
        return row[names[0]]
    except:
        return tryGetCell(names[1:], row)

def runCalculations(
    csvDicts: dict[list[dict[str, str]]],
    startingElo: int = 1000,
    kWeight = 32,
    capital = 100
    ) -> tuple[list[Season], dict[str, Team]]:
    seasons : list[Season] = []
    teams : dict[str, Team] = {}
    lowestElo = startingElo
    for i, seasonName in enumerate(csvDicts):
        season = Season(seasonName, i)
        for row in csvDicts[seasonName]:
            # Record date
            day, month, year = row['Date'].split("/")
            date = datetime(int(year), int(month), int(day))
            # Get teams
            homeTeamName = row['HomeTeam']
            awayTeamName = row['AwayTeam']

            if homeTeamName not in teams:
                teams[homeTeamName] = Team(homeTeamName, lowestElo)
            if awayTeamName not in teams:
                teams[awayTeamName] = Team(awayTeamName, lowestElo)
                
            score = (int(row['FTHG']), int(row['FTAG']))

            try:
                v = tryGetCell(['BbMxH', 'MaxH'], row)
                HomeBet = float(v)
            except:
                HomeBet = 1
                print(f"Err: {season.name} - {date.date()} - {homeTeamName} vs {awayTeamName} - no max home bet")
            try:
                v = tryGetCell(['BbMxD', 'MaxD'], row)
                Drawbet = float(v)
            except:
                Drawbet = 1
                print(f"Err: {season.name} - {date.date()} - {homeTeamName} vs {awayTeamName} - no max draw bet column")
            try:
                v = tryGetCell(['BbMxA', 'MaxA'], row)
                AwayBet = float(v)
            except:
                AwayBet = 1
                print(f"Err: {season.name} - {date.date()} - {homeTeamName} vs {awayTeamName} - no max away bet column")

            bet = Bet(HomeBet, Drawbet, AwayBet)

            game = Game(seasonName, date, teams[homeTeamName], teams[awayTeamName], bet)
            game.playMatch(score, kWeight)

            capital = game.bet.placeKellyBets(capital)
            game.capital = capital
            season.addGame(game)
        seasons.append(season)
        lowestElo = min([teams[team].elo for team in teams])
    return (seasons, teams)

def constructGameCsv(
    outputFileName: str,
    weekDict: dict[datetime, dict[str]],
    teams: list[Team],
    printLine: bool = False
    ):
    print(f"Writing to {outputFileName}.csv")
    
    with open(f'outputCsvs/{outputFileName}.csv', "w") as outputFile:
        line = 'Game Week, '+ ','.join([team for team in teams])+'\n'
        outputFile.write(line)
        if printLine:
            print(line)
        for week in weekDict:
            row = weekDict[week]
            line = f"{week}"
            for team in teams:
                try:
                    value = round(row[team], 1)
                except:
                    value = ""
                line += f",{value}"
            if printLine:
                print(line)       
            line += "\n"
            outputFile.write(line)

def constructDateCsv(
    outputFileName: str,
    datesDict: dict[datetime, dict[str]],
    teams: list[Team],
    printLine: bool = False
    ):
    # Now we have run all the data through the elo calculators
    # Time to print out our results to an output csv 
    print(f"Writing to {outputFileName}.csv")
    
    with open(f'outputCsvs/{outputFileName}.csv', "w") as outputFile:
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
                line += f",{value}"
            if printLine:
                print(line)           
            line += "\n"
            outputFile.write(line)            
    
def constructBetCsv(
    outputFileName: str,
    seasons: list[Season],
    printLine: bool = False
    ):
    # Now we have run all the data through the elo calculators
    # Time to print out our results to an output csv 
    print(f"Writing to {outputFileName}.csv")
    
    with open(f'outputCsvs/{outputFileName}.csv', "w") as outputFile:
        line = 'Season,Date,Home,Away,Score,Home Elo,Away Elo,Home Bet,Draw Bet,Away Bet,Home Win Prob,Draw Prob,Away Win Prob,Bet Results'+'\n'
        outputFile.write(line)
        if printLine:
            print(line)
        
        for season in seasons:
            for game in season.games:
                line = f"{season.number}~{game.week},{game.date}"
                line += f",{game.home.name},{game.away.name},{game.score[0]}-{game.score[1]}"
                line += f",{game.homeEloBefore},{game.awayEloBefore}"
                line += f",{game.bet.homeOdds},{game.bet.drawOdds},{game.bet.awayOdds}"
                line += f",{game.probs.homeWin},{game.probs.draw},{game.probs.awayWin},{game.bet.result}"
                if printLine:
                    print(line)
                line += "\n"
                outputFile.write(line)
    
def constructkellybetcsv(
    outputFileName: str,
    seasons: list[Season],
    printLine: bool = False
    ):
    # Now we have run all the data through the elo calculators
    # Time to print out our results to an output csv 
    print(f"Writing to {outputFileName}.csv")
    
    with open(f'outputCsvs/{outputFileName}.csv', "w") as outputFile:
        line = 'Season,Date,Home,Away,Score,Result,Home Elo,Away Elo,Home Bet,Draw Bet,Away Bet,Home Win Prob,Draw Prob,Away Win Prob,Bet home,Bet draw,Bet away'+'\n'
        outputFile.write(line)
        if printLine:
            print(line)
        
        for season in seasons:
            for game in season.games:
                line = f"{season.number}~{game.week},{game.date}"
                line += f",{game.home.name},{game.away.name}"
                line += f",{game.score[0]} - {game.score[1]},{game.result}"
                line += f",{game.homeEloBefore},{game.awayEloBefore}"
                line += f",{game.bet.homeOdds},{game.bet.drawOdds},{game.bet.awayOdds}"
                line += f",{game.probs.homeWin},{game.probs.draw},{game.probs.awayWin}"
                line += f",{game.bet.homekelly},{game.bet.drawkelly},{game.bet.awaykelly}"
                if printLine:
                    print(line)
                line += "\n"
                outputFile.write(line)
    