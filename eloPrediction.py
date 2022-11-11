import sys

def eloPrediction(homeElo, awayElo):
    
    homeAdvantage = 0.169
    footballSeasonalAdjustment = 0.252
    
    eloDif = homeElo - awayElo
    
    H = 1 - (1/(1+10**(eloDif/400+homeAdvantage-footballSeasonalAdjustment)))
    A = (1/(1+10**(eloDif/400+homeAdvantage+footballSeasonalAdjustment)))
    D = 1 - (H + A)
    
    print("total:", D+H+A)
    
    # Returns (W, D, L) probability
    print("Home:",H)
    print("Draw:",D)
    print("Away:",A)

try:
    t1 = int(sys.argv[1])
except:
    t1 = int(input("Please provide elo for home team"))
    
try:
    t2 = int(sys.argv[2])
except:
    t2 = int(input("Please provide elo for away team"))

print("home:",t1,"away:", t2)
eloPrediction(t1, t2)