from helpers.csvHelpers import *
from helpers.classes import Season
from helpers.manipulateData import *
from helpers.eloMath import meanSquaredErrorForGame

def logEvaluationForSeason(season : Season) -> tuple[dict[str, int], int]:
    weeks : dict[str, int] = {}
    total = 0
    for game in season.games:
        if game.week < 19:
            week = f"{season.number}~{game.week}"
            logValue = eloMath.logEvaluationValue(game.homeEloAfter, game.awayEloAfter, game.result)
            total += logValue
            try:
                weeks[week] += logValue
            except:
                weeks[week] = logValue
    return weeks, total

def printLogScore(seasons: list[Season]):
    logValues, logTotal = logEvaluationForSeason(seasons[-1])
    print("Log total: ", logTotal)
    for key in logValues:
        print(f"S~W: {key} - Log: {round(logValues[key], 3)}")

def meanSquaredError(seasons: list[Season]):
    total = 0
    for season in seasons:
        for game in season.games:
            result = meanSquaredErrorForGame(game)
            total += result
    return total