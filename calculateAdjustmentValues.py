from datetime import datetime
import time
import helpers.eloMath
from helpers.csvHelpers import *
from helpers.classes import *
from helpers.manipulateData import *
from math import exp


csvList = [
    "12_13.csv",
    "13_14.csv",
    "14_15.csv",
    "15_16.csv",
    "16_17.csv",
    "17_18.csv",
    "18_19.csv",
]

startingElo = 2000
print("Starting Elo:", startingElo)

kWeight = 680
print("Weight K:", kWeight)

csvDicts = csvsToDictionary(csvList)
seasons, teams = buildSeasonsAndTeams(csvDicts)
calculateElos(seasons, teams, startingElo, kWeight)

homeWins = 0
awayWins = 0
draws = 0
for season in seasons:
    homeWins += season.homeWins
    awayWins += season.awayWins
    draws += season.draws
total = homeWins+awayWins+draws

print("homeWins: ",homeWins)
print("awayWins: ",awayWins)
print("draws: ",draws)
print("total: ",total)

def drawsFromAdjustmentValue(homeAdv, drawAdj):
    return 1/(1+exp(homeAdv-drawAdj)) - 1/(1+exp(homeAdv+drawAdj))

def calcHomeAdvantage(homeAdv, drawAdj):
    return 1-1/(1+exp(homeAdv-drawAdj))

drawProb = draws / total
homeWinProb = homeWins / total
print("\ndrawProb:",round(drawProb,3))
print("homeWinProb:",round(homeWinProb,3),'\n')

for B in range(0, 1000):
    b = B/1000
    for A in range(0, 1000):
        a = A/1000
        dProb = drawsFromAdjustmentValue(a,b)
        hwProb = calcHomeAdvantage(a,b)
        if abs(dProb - drawProb) < 0.0005:
            if abs(hwProb - homeWinProb) < 0.0005:
                print("a: ",a," - b:",b)

drawAdj = 0.504
homeAdvAdj = 0.33