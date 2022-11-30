# imports csv module into this Python script (csv module part of Python's standard library - so you will have it if you have Python)
from datetime import datetime
import time
import helpers.eloMath
from helpers.csvHelpers import *
from helpers.classes import *
from helpers.manipulateData import *

csvList = [
    "12_13.csv",
    "13_14.csv",
    "14_15.csv",
    "15_16.csv",
    "16_17.csv",
    "17_18.csv",
    "18_19.csv",
]

startingElo = 1000
print("Starting Elo:", startingElo)
kWeight = 20

# for k in range(10, 30):
#     seasons, teams = readCsvs(csvList)
#     calculateElos(seasons, teams, startingElo, k)

#     logValues, logTotal = logEvaluationForSeason(seasons[-1])
#     #for logValue in logValues:
#         #print(logValue,": ",logValues[logValue])
#     print("k: ",k, "log: ",logTotal)

seasons, teams = readCsvs(csvList)
calculateElos(seasons, teams, startingElo, kWeight)

constructDateCsv("EloRatings", eloByDate(seasons), teams)
constructDateCsv("Probabilities", winProbabilityByDate(seasons, teams), teams)
constructGameCsv("EloRatingsByGame", eloByMatchWeek(seasons), teams)
constructGameCsv("ProbabilitiesByGame", winProbByMatchWeek(seasons), teams)
constructGameCsv("LogEvalByGame", logEvalByMatchWeek([seasons[-1]], teams), teams)
constructGameCsv("GoalDifByGame", goalDifByMatchWeek([seasons[-1]], teams), teams)

