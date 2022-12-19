from helpers.classes import *
from datetime import datetime
from helpers import eloMath

def getLowestElo(teams: list[Team]) -> int:
    eloList = [teams[team].elo for team in teams if (teams[team].elo is not None)]
    eloList.sort()
    return eloList[0]

def eloByMatchWeek(seasons : list[Season]) -> dict[datetime, dict[str]]:
    weeks : dict[str, dict[str]] = {}
    for season in seasons:
        for game in season.games:
            week = game.getSeasonWeekName()
            try:
                weeks[week][game.home.name] = game.homeEloAfter
                weeks[week][game.away.name] = game.awayEloAfter
            except:
                weeks[week] = {}
                weeks[week][game.home.name] = game.homeEloAfter
                weeks[week][game.away.name] = game.awayEloAfter
    return weeks

def winProbByMatchWeek(seasons : list[Season]) -> dict[datetime, dict[str]]:
    weeks : dict[str, dict[str]] = {}
    for season in seasons:
        for game in season.games:
            week = game.getSeasonWeekName()
            try:
                H, D, A = eloMath.eloPrediction(game.homeEloBefore, game.awayEloBefore)
                weeks[week][game.home.name] = H*100
                weeks[week][game.away.name] = A*100
            except:
                weeks[week] = {}
                H, D, A = eloMath.eloPrediction(game.homeEloBefore, game.awayEloBefore)
                weeks[week][game.home.name] = H*100
                weeks[week][game.away.name] = A*100
    return weeks

def logEvalByMatchWeek(seasons : list[Season]) -> dict[str, int]:
    weeks : dict[str, dict[str]] = {}
    for season in seasons:
        for game in season.games:
            week = game.getSeasonWeekName()
            logValue = eloMath.logEvaluationValue(game.homeEloAfter, game.awayEloAfter, game.result)
            try:
                weeks[week][game.home.name] = logValue
                weeks[week][game.away.name] = logValue
            except:
                weeks[week] = {}
                weeks[week][game.home.name] = logValue
                weeks[week][game.away.name] = logValue
    return weeks

def goalDifByMatchWeek(seasons : list[Season]) -> dict[str, int]:
    weeks : dict[str, dict[str]] = {}
    for season in seasons:
        for game in season.games:
            week = game.getSeasonWeekName()
            value = game.homeGoals-game.awayGoals
            try:
                weeks[week][game.home.name] = value
                weeks[week][game.away.name] = -value
            except:
                weeks[week] = {}
                weeks[week][game.home.name] = value
                weeks[week][game.away.name] = -value
    return weeks