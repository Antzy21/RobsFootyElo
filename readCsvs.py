from classes import *
from datetime import datetime
import csv

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