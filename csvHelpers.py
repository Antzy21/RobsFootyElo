from classes import *
from datetime import datetime
import csv

def readCsvs(csvs: list[str]) -> tuple[list[Season], dict[str, Team]]:
    seasons : list[Season] = []
    teams : dict[str, Team] = {}
    for i, seasonCsv in enumerate(csvs):
        season = Season(seasonCsv, i)
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

def constructGameCsv(
    outputFileName: str,
    weekDict: dict[datetime, dict[str]],
    teams: list[Team],
    printLine: bool = False
    ):
    print(f"Writing to {outputFileName}.csv")
    
    with open(f'{outputFileName}.csv', "w") as outputFile:
        line = 'Game Week, '+ ','.join([team for team in teams])+'\n'
        outputFile.write(line)
        if printLine:
            print(line)
        # for season in seasons:
        #     for game in season.games:
        #         line = f"{season.number}-{game.week}"
        #         for team in teams:
        #             if team == game.home.name:
        #                 line += f",{game.homeEloAfter}"
        #             elif team == game.away.name:
        #                 line += f",{game.awayEloAfter}"
        #             else:
        #                 line += ","
        #         line += "\n"
        #         outputFile.write(line)
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
    printLine: bool = True
    ):
    # Now we have run all the data through the elo calculators
    # Time to print out our results to an output csv 
    print(f"Writing to {outputFileName}.csv")
    
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
                line += f",{value}"
            if printLine:
                print(line)           
            line += "\n"
            outputFile.write(line)            
    