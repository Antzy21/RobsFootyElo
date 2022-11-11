import sys
import math

def eloPrediction(homeElo, awayElo, powerBase = math.e):
    
    homeAdvantage = 0.169
    footballSeasonalAdjustment = 0.252
    
    eloDif = homeElo - awayElo
    
    print("\nBase is:", powerBase,"\n")
    
    H = 1 - (1/(1+powerBase**(eloDif/400+homeAdvantage-footballSeasonalAdjustment)))
    A = (1/(1+powerBase**(eloDif/400+homeAdvantage+footballSeasonalAdjustment)))
    D = 1 - (H + A)
    
    
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

print("Home:",t1,"Away:", t2)

if len(sys.argv) == 4:
    try:
        powerBase = int(sys.argv[3])
        eloPrediction(t1, t2, powerBase)
    except:
        print("Error passing powerbase")
else:
    eloPrediction(t1, t2)
