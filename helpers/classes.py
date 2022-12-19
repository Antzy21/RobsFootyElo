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

    def placeKellyBets(self, result: str, capital: int):
        self.preBetCapital = capital
        if self.homekelly > 0:
            self.homeKellyBetSize = capital*self.homekelly
            capital -= self.homeKellyBetSize
            if result == "H":
                capital += self.kellyBetSize*self.homeOdds
        if self.drawkelly > 0:
            self.drawKellyBetSize = capital*self.drawkelly
            capital -= self.drawKellyBetSize
            if result == "D":
                capital += self.kellyBetSize*self.drawOdds
        if self.awaykelly > 0:
            self.awayKellyBetSize = capital*self.awaykelly
            capital -= self.awayKellyBetSize
            if result == "A":
                capital += self.kellyBetSize*self.awayOdds
        self.postBetCapital = capital
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

    def getSeasonWeekName(self):
        return f"{self.season.number}~{self.week+1}"

    def setElos(self, homeGoals, awayGoals, k):
        self.homeEloBefore = self.home.elo
        self.awayEloBefore = self.away.elo
        homeNew, awayNew = eloCalculation(self.home.elo, self.away.elo, homeGoals, awayGoals, k)
        self.home.updateElo(homeNew, self.season)
        self.away.updateElo(awayNew, self.season)
        self.homeEloAfter = homeNew
        self.awayEloAfter = awayNew

    def playMatch(self, kWeight, overrideEarlyGamesK = None):
        if overrideEarlyGamesK is not None:
            try:
                if self.home.matchesPlayed[self.season] < 5:
                    kWeight = overrideEarlyGamesK
            except:
                kWeight = overrideEarlyGamesK
        self.setElos(self.homeGoals, self.awayGoals, kWeight)
        self.week = self.home.matchesPlayed[self.season] + 1

    def makePredictionsForGame(self, defaultElo = 1000):
        homeWinProb, drawProb, awayWinProb = eloPrediction(self.home.elo, self.away.elo)
        self.probabilities = Probabilities(homeWinProb, drawProb, awayWinProb)
        self.bet.calculateKellyValues(homeWinProb, drawProb, awayWinProb)

    def betOnGame(self, capital: int):
        return self.bet.placeKellyBets(self.result, capital)


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
    
    def playMatches(self, kWeight, defaultElo = 1000, capital = 1000, betAfterDate: datetime = datetime(1950,1,1)):
        for game in self.games:
            if game.home.elo is None:
                game.home.elo = defaultElo
            if game.away.elo is None:
                game.away.elo = defaultElo
            game.makePredictionsForGame()
            game.playMatch(kWeight = kWeight)
            if game.date > betAfterDate:
                print("capital:", capital)
                capital = game.betOnGame(capital)
        return capital
