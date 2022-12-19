from helpers.csvHelpers import constructTeamCsv, constructGamesCsv
from helpers.manipulateData import *

def runallcsvs(seasons,teams):
    print("\nWrite Csvs")
    constructTeamCsv("EloRatingsByGame", eloByMatchWeek(seasons), teams)
    constructTeamCsv("ProbabilitiesByGame", winProbByMatchWeek(seasons), teams)
    constructTeamCsv("LogEvalByGame", logEvalByMatchWeek([seasons[-1]]), teams)
    constructTeamCsv("GoalDifByGame", goalDifByMatchWeek([seasons[-1]]), teams)
    constructGamesCsv("BettingResult", seasons)
