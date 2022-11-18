import math

def eloPrediction(homeElo, awayElo, powerBase = math.e):
    
    homeAdvantage = 0.169
    footballSeasonalAdjustment = 0.252
    
    eloDif = homeElo - awayElo
    
    H = 1 - (1/(1+powerBase**(eloDif/400+homeAdvantage-footballSeasonalAdjustment)))
    A = (1/(1+powerBase**(eloDif/400+homeAdvantage+footballSeasonalAdjustment)))
    D = 1 - (H + A)
    
    return (H, D, A)
