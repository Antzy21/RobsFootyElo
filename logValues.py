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

bestLog = -1000000

for k in range(0,1000,50):
    csvDicts = readCsvs(csvList)
    seasons, teams = runCalculations(csvDicts, startingElo, k)

    logValues, logTotal = logEvaluationForSeason(seasons[-1])
    for logValue in logValues:
        pass#print(logValue,": ",logValues[logValue])
    
    print("Weight K:", k, " - Log total: ", logTotal)
    if logTotal > bestLog:
        bestLog = logTotal
        optimumK = k

print("optimum K:", optimumK, " - Log total: ", bestLog)