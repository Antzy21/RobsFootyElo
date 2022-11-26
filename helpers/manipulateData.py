from helpers.classes import *
from datetime import datetime
from helpers import eloMath

def calculateElos(seasons: list[Season], teams: dict[str, Team], startingElo: int) -> None:
    print("Running Calculations")
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
    
def eloByDate(seasons : list[Season]) -> dict[datetime, dict[str]]:
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

def eloByMatchWeek(seasons : list[Season]) -> dict[datetime, dict[str]]:
    weeks : dict[str, dict[str]] = {}
    for season in seasons:
        for game in season.games:
            week = f"{season.number}~{game.week}"
            try:
                weeks[week][game.home.name] = game.homeEloAfter
                weeks[week][game.away.name] = game.awayEloAfter
            except:
                weeks[week] = {}
                weeks[week][game.home.name] = game.homeEloAfter
                weeks[week][game.away.name] = game.awayEloAfter
    return weeks

def logEvaluationForSeason(season : Season) -> tuple[dict[str, int], int]:
    weeks : dict[str, int] = {}
    total = 0
    for game in season.games:
        if game.week < 19:
            week = f"{season.number}~{game.week}"
            logValue = eloMath.logEvaluationValue(game.homeEloAfter, game.awayEloAfter, game.score)
            total += logValue
            try:
                weeks[week] += logValue
            except:
                weeks[week] = logValue
    return weeks, total
     
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
    