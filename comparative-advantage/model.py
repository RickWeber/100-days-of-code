# Libraries
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class Market(Model):
    """An economy with N agents and K goods"""
    def __init__(self, N, K, width, height):
        super().__init__()
        self.N = N
        self.numeraire = 0  # numeraire good is good 0
        self.K = K
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # create agents
        for i in range(N):
            a = BarterAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()


class BarterAgent(Agent):
    """An agent with capacities and price expectations"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.ppf = np.random.randint(4, size=(model.N))
        self.price_avg = np.divide(self.ppf, self.ppf[0])
        # self.price_var = np.zeros(model.N)
        self.observations = 0
        self.price_S = np.zeros(model.N)
        self.price_SS = np.zeros(model.N)
        self.update_prices(self.price_avg)

    def update_prices(self, new_prices):
        self.observations += 1
        self.price_S += new_prices
        self.price_SS += new_prices * new_prices

    def price_var(self):
        # This is the naive algorithm on the wikipedia page for
        # "Algorithms for calculating variance"
        if self.observations <= 1:
            out = np.zeros(self.model.N)
        else:
            x1 = self.price_SS
            x2 = self.price_S * self.price_S
            x2 = x2 / self.observations
            out = (x1 - x2) / (self.observations - 1)
        return np.sqrt(out)

    def step(self):
        next
