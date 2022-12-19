from helpers.eloMath import *
from helpers.kellyBetting import kellyformula
from datetime import datetime

class Team:
    def __init__(self, name) -> None:
        self.name: str = name
        self.matchesPlayed: dict[int, int] = {}
    def updateElo(self, elo, season):
        self.elo = elo
        try:
            self.matchesPlayed[season] += 1
        except:
            self.matchesPlayed[season] = 0

class Bet:
    def __init__(self, homeOdds, drawOdds, awayOdds):
        self.homeOdds = homeOdds
        self.drawOdds = drawOdds
        self.awayOdds = awayOdds
    def betResult(self, HomeWinProbability, DrawProbability, AwayWinProbability, score: tuple[int, int], size = 1):
        if score[0] > score[1]:
            self.result = self.homeOdds * HomeWinProbability
        elif score[0] < score[1]:
            self.result = self.awayOdds * AwayWinProbability
        elif score[0] == score[1]:
            self.result = self.drawOdds * DrawProbability
    def betKelly(self, HomeWinProbability, DrawProbability, AwayWinProbability):
        self.homekelly = kellyformula(self.homeOdds,HomeWinProbability)
        self.drawkelly = kellyformula(self.drawOdds,DrawProbability)
        self.awaykelly = kellyformula(self.awayOdds,AwayWinProbability)
    def placeKellyBets(self, result: str, capital):
        if self.homekelly > 0:
            self.kellyBetSize = capital*self.homekelly
            capital -= self.kellyBetSize
            if result == "H":
                capital += self.kellyBetSize*self.homeOdds
        if self.drawkelly > 0:
            self.kellyBetSize = capital*self.drawkelly
            capital -= self.kellyBetSize
            if result == "D":
                capital += self.kellyBetSize*self.drawOdds
        if self.awaykelly > 0:
            self.kellyBetSize = capital*self.awaykelly
            capital -= self.kellyBetSize
            if result == "A":
                capital += self.kellyBetSize*self.awayOdds
        return capital

class Probabilities:
    def __init__(self, home, draw, away):
        self.homeWin = home
        self.draw = draw
        self.awayWin = away

class Game:
    def __init__(self,
        date: datetime,
        home: Team,
        away: Team,
        homeGoals,
        awayGoals: int,
        bet: Bet) -> None:
        self.date: datetime = date
        self.home: Team = home
        self.away: Team = away
        self.homeGoals: int = homeGoals
        self.awayGoals: int = awayGoals
        self.bet: Bet = bet
        self.probs: Probabilities = None
        self.homeEloBefore = None
        self.homeEloAfter = None
        self.awayEloBefore = None
        self.awayEloAfter = None
    def setElos(self, score, k):
        homeNew, awayNew = eloCalculation(self.home.elo, self.away.elo, score, k)
        self.home.updateElo(homeNew, self.season)
        self.away.updateElo(awayNew, self.season)
        self.homeEloAfter = homeNew
        self.awayEloAfter = awayNew
    def playMatch(self, score, k = 32, capital = 100, overrideEarlyGamesK = False):
        if overrideEarlyGamesK:
            earlyGameK = 32
            try:
                if self.home.matchesPlayed[self.season] < 5:
                    k = earlyGameK
            except:
                k = earlyGameK
        
        self.homeEloBefore = self.home.elo
        self.awayEloBefore = self.away.elo
        
        H, D, A = eloPrediction(self.homeEloBefore, self.awayEloBefore)
        self.probs: Probabilities = Probabilities(H, D, A)
        self.bet.betResult(H, D, A, score)
        self.bet.betKelly(H, D, A, score)

        self.score = score
        if score[0] > score[1]:
            self.result = "H"
        elif score[0] < score [1]:
            self.result = "A"
        elif score[0] == score[1]:
            self.result = "D"

        self.setElos(score, k)
        self.week = self.home.matchesPlayed[self.season] + 1

class Season:
    def __init__(self, name, number) -> None:
        self.number = number
        self.name = name
        self.games : list[Game] = []
        self.homeWins = 0
        self.awayWins = 0
        self.draws = 0
    def addGame(self, game: Game):
        game.season = self
        self.games.append(game)
        if game.score[0] > game.score[1]:
            self.homeWins += 1
        elif game.score[0] < game.score[1]:
            self.awayWins += 1
        elif game.score[0] == game.score[1]:
            self.draws += 1
