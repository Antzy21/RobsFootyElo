# imports csv module into this Python script (csv module part of Python's standard library - so you will have it if you have Python)
from datetime import datetime
import time
import helpers.eloMath
from helpers.csvHelpers import *
from helpers.classes import *
from helpers.manipulateData import *

startingElo = 1000
print("Starting Elo:", startingElo)

csvList = [
    "15_16Season.csv",
    "16_17Season.csv",
    "17_18Season.csv",
    "18_19Season.csv",
]

seasons, teams = readCsvs(csvList)
calculateElos(seasons, teams, startingElo)

eloByDates = eloByDate(seasons)
constructDateCsv("EloRatings", eloByDates, teams, printLine = False)
winProbByDates = winProbabilityByDate(seasons, teams)
constructDateCsv("Probabilities", winProbByDates, teams, printLine = False)
eloByMatchWeeks = eloByMatchWeek(seasons)
constructGameCsv("EloRatingsByGame", eloByMatchWeeks, teams)

logValues, logTotal = logEvaluationForSeason(seasons[-1])

for logValue in logValues:
    print(logValue,": ",logValues[logValue])

print(logTotal)
