from helpers.classes import *
from datetime import datetime
from dateutil.parser import parse
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

def tryGetCell(names: list[str], row, default):
    if len(names) == 0:
        return 1
    try:
        return row[names[0]]
    except:
        return tryGetCell(names[1:], row, default)

def parseGame(row, teams):
    date = parse(row['Date'])
    homeTeamName = row['HomeTeam']
    awayTeamName = row['AwayTeam']
    homeGoals = int(row['FTHG'])
    awayGoals = int(row['FTAG'])
    homeBet = float(tryGetCell(['BbMxH', 'MaxH'], row, 1))
    drawbet = float(tryGetCell(['BbMxD', 'MaxD'], row, 1))
    awayBet = float(tryGetCell(['BbMxA', 'MaxA'], row, 1))

    if homeTeamName not in teams:
        teams[homeTeamName] = Team(homeTeamName)
    if awayTeamName not in teams:
        teams[awayTeamName] = Team(awayTeamName)

    bet = Bet(homeBet, drawbet, awayBet)

    return Game(
        date,
        teams[homeTeamName],
        teams[awayTeamName],
        homeGoals,
        awayGoals,
        bet)

def parseSeasonsAndTeams(
    csvDicts: dict[list[dict[str, str]]],
    ) -> tuple[list[Season], dict[str, Team]]:
    seasons : list[Season] = []
    teams : dict[str, Team] = {}
    for i, seasonName in enumerate(csvDicts):
        season = Season(seasonName, i)
        for row in csvDicts[seasonName]:
            game = parseGame(row, teams)
            season.addGame(game)
        seasons.append(season)
    return (seasons, teams)

def constructTeamCsv(
    outputFileName: str,
    dict: dict[datetime, dict[str]],
    teams: list[Team],
    printLine: bool = False
    ):
    print(f"Writing to {outputFileName}.csv")
    
    with open(f'outputCsvs/{outputFileName}.csv', "w") as outputFile:
        line = 'Game Week, '+ ','.join([team for team in teams])
        outputFile.write(line+'\n')
        if printLine:
            print(line)
            
        for key in dict:
            row = dict[key]
            line = f"{key}"
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

def constructGamesCsv(
    outputFileName: str,
    seasons: list[Season],
    printLine: bool = False
    ):
    # Now we have run all the data through the elo calculators
    # Time to print out our results to an output csv 
    print(f"Writing to {outputFileName}.csv")
    
    with open(f'outputCsvs/{outputFileName}.csv', "w") as outputFile:
        line = "Season,Date,Home,Away"
        line += ",Score,Result,Home Elo,Away Elo"
        line += ",Home Odds,Draw Odds,Away Odds"
        line += ",Home Win Prob,Draw Prob,Away Win Prob"
        line += ",Bet Home,Bet Draw,Bet Away"
        line += ",Bet Size Home,Bet Size Draw,Bet Size Away"
        line += ",Net Change"
        outputFile.write(line+"\n")
        if printLine:
            print(line)
        
        for season in seasons:
            for game in season.games:
                line = f"{season.number}~{game.week},{game.date}"
                line += f",{game.home.name},{game.away.name},{game.homeGoals}:{game.awayGoals}"
                line += f",{game.homeEloBefore},{game.awayEloBefore}"
                line += f",{game.bet.homeOdds},{game.bet.drawOdds},{game.bet.awayOdds}"
                line += f",{game.probabilities.homeWin},{game.probabilities.draw},{game.probabilities.awayWin}"
                line += f",{game.bet.homekelly},{game.bet.drawkelly},{game.bet.awaykelly}"
                line += f",{game.bet.homeKellyBetSize},{game.bet.drawKellyBetSize},{game.bet.awayKellyBetSize}"
                line += f",{game.bet.netChange}"
                if printLine:
                    print(line)
                line += "\n"
                outputFile.write(line)
