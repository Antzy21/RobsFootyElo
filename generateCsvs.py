from helpers.csvHelpers import *
from helpers.classes import *
from helpers.manipulateData import *

def runallcsvs(seasons,teams):
    constructTeamCsv("EloRatings", eloByDate(seasons), teams)
    constructTeamCsv("Probabilities", winProbabilityByDate(seasons, teams), teams)
    constructTeamCsv("EloRatingsByGame", eloByMatchWeek(seasons), teams)
    constructTeamCsv("ProbabilitiesByGame", winProbByMatchWeek(seasons), teams)
    constructTeamCsv("LogEvalByGame", logEvalByMatchWeek([seasons[-1]], teams), teams)
    constructTeamCsv("GoalDifByGame", goalDifByMatchWeek([seasons[-1]], teams), teams)
    constructBetCsv("BettingResult", seasons)
    constructkellybetcsv("kellyBettingResult", seasons)
