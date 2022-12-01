from helpers.classes import *
from datetime import datetime
import csv

def csvsToDictionary(csvs: list[str]) -> dict[list[dict[str, str]]]:
    outputs : dict[list[dict[str, str]]] = {}
    for i, seasonCsv in enumerate(csvs):
        output : list[dict[str, str]] = []
        with open(f"seasonCsvs/{seasonCsv}", newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(csvReader):
                if i == 0:
                    headers = row
                else:
                    rowDict : dict[str, str] = {}
                    for j, cell in enumerate(row):
                        rowDict[headers[j]] = cell
                    output.append(rowDict)
        outputs[seasonCsv] = output
    return outputs

def buildSeasonsAndTeams(csvDicts: dict[list[dict[str, str]]]) -> tuple[list[Season], dict[str, Team]]:
    seasons : list[Season] = []
    teams : dict[str, Team] = {}
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
                teams[homeTeamName] = Team(homeTeamName)
            if awayTeamName not in teams:
                teams[awayTeamName] = Team(awayTeamName)
                
            # Gets the score as two numbers in a tuple, first is for team1's goal count, second for team 2's goal count 
            score = (int(row['FTHG']), int(row['FTAG']))

            HomeBet = float(row['BbMxH'])
            Drawbet = float(row['BbMxD'])
            AwayBet = float(row['BbMxA'])
            bet = Bet(HomeBet, Drawbet, AwayBet)

            game = Game(seasonName, date, teams[homeTeamName], teams[awayTeamName], score, bet)
            season.addGame(game)
        seasons.append(season)
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
                line += f",{game.bet.homeBet},{game.bet.drawBet},{game.bet.awayBet}"
                line += f",{game.homeWinProb},{game.drawProb},{game.awayWinProb},{game.bet.result}"
                if printLine:
                    print(line)
                line += "\n"
                outputFile.write(line)
    