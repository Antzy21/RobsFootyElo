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
print("Weight K:", kWeight)

seasons, teams = readCsvs(csvList)
calculateElos(seasons, teams, startingElo, kWeight)


logValues, logTotal = logEvaluationForSeason(seasons[-1])
for logValue in logValues:
    print(logValue,": ",logValues[logValue])
    
print("Log total: ", logTotal)