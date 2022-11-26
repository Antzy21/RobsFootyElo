from datetime import datetime
import time
import helpers.eloMath
from helpers.csvHelpers import *
from helpers.classes import *
from helpers.manipulateData import *
from math import exp

startingElo = 1000
print("Starting Elo:", startingElo)

csvList = [
    "15_16Season.csv",
    "16_17Season.csv",
    "17_18Season.csv",
    #"18_19Season.csv",
]

seasons, teams = readCsvs(csvList)
calculateElos(seasons, teams, startingElo)

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
    return 1-1/(exp(homeAdv+drawAdj))

drawProb = draws / draws+homeWins+awayWins
homeWinProb = homeWins / total

for B in range(0, 100):
    b = B/100
    for A in range(0, 100):
        a = A/100
        dProb = drawsFromAdjustmentValue(a,b)
        hwProb = calcHomeAdvantage(a,b)
        if abs(dProb - drawProb) < 0.01:
            if abs(hwProb - homeWinProb) < 0.1:
                print("a: ",a," - b:",b)

print("drawProb: ", drawProb)
drawAdj = 0.52



print("homeWinProb: ", homeWinProb)