from helpers.eloMath import *
from helpers.kellyBetting import kellyformula
from datetime import datetime

class Team:
    def __init__(self, name) -> None:
        self.name: str = name
        self.matchesPlayed: dict[int, int] = {}
        self.elo = None

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

    def calculateKellyValues(self, HomeWinProbability, DrawProbability, AwayWinProbability):
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
        homeGoals: int,
        awayGoals: int,
        bet: Bet) -> None:
        self.date: datetime = date
        self.home: Team = home
        self.away: Team = away
        self.homeGoals: int = homeGoals
        self.awayGoals: int = awayGoals
        if homeGoals > awayGoals:
            self.result = "H"
        elif homeGoals < awayGoals:
            self.result = "A"
        elif homeGoals == awayGoals:
            self.result = "D"
        self.bet: Bet = bet

    def setElos(self, homeGoals, awayGoals, k):
        self.homeEloBefore = self.home.elo
        self.awayEloBefore = self.away.elo
        homeNew, awayNew = eloCalculation(self.home.elo, self.away.elo, homeGoals, awayGoals, k)
        self.home.updateElo(homeNew, self.season)
        self.away.updateElo(awayNew, self.season)
        self.homeEloAfter = homeNew
        self.awayEloAfter = awayNew

    def playMatch(self, k = 32, capital = 100, defaultElo = 1000, overrideEarlyGamesK = False):
        if overrideEarlyGamesK:
            earlyGameK = 32
            try:
                if self.home.matchesPlayed[self.season] < 5:
                    k = earlyGameK
            except:
                k = earlyGameK
        
        if self.home.elo is None:
            self.home.elo = defaultElo
        if self.away.elo is None:
            self.away.elo = defaultElo

        homeWinProb, drawProb, awayWinProb = eloPrediction(self.home.elo, self.away.elo)
        self.probabilities = Probabilities(homeWinProb, drawProb, awayWinProb)
        self.bet.calculateKellyValues(homeWinProb, drawProb, awayWinProb)

        self.setElos(self.homeGoals, self.awayGoals, k)
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
        if game.homeGoals > game.awayGoals:
            self.homeWins += 1
        elif game.homeGoals < game.awayGoals:
            self.awayWins += 1
        elif game.homeGoals == game.awayGoals:
            self.draws += 1
    
    def run(self, startingElo = 1000):
        for game in self.games:
            game.playMatch(defaultElo= startingElo)