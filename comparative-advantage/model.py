# libraries
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.datacollection import DataCollector


class BarterAgent(Agent):
    def __init__(self, unique_id, model):
        # plan, ppf, util_params, endowment,
        # discount_rate, learning_rate, trade_params):
        super().__init__(unique_id, model)
        self.model = model
        self.plan = np.ones(model.num_goods)
        self.ppf = np.random.randint(4, size=(model.num_goods))
        self.util_params = np.ones(model.num_goods) / model.num_goods
        self.endowment = np.zeros(model.num_goods)
        self.discount_rate = np.random.uniform(0.01, 0.25)
        self.learning_rate = 0.05
        self.trade_params = np.zeros(model.num_goods)

    def step(self):
        self.move()
        self.produce()
        self.trade()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True
        )
        # I could add some bias or a simple program to change how they move...
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def produce(self):
        production = np.dot(self.plan, self.ppf) / sum(self.plan)
        self.endowment = self.endowment + production

    def trade(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) < 1:
            return
        partner = self.random.choice(cellmates)
        # deal = Contract(self, partner).random_trade()
        deal = Contract(self, partner).null_trade(1/10)
        if not self.evaluate_trade(deal):
            return
        if not partner.evaluate_trade(deal.reverse):
            return
        self.make_trade(deal)

    def utility(self):
        utils = 0
        for i in range(self.model.num_goods):
            utils += self.endowment[i] ** self.util_params[i]
        return utils  # I can make this nicer later.

    def evaluate_deal(self, deal):
        self.utility() < self.make_trade(deal).utility()

    def make_trade(self, deal):
        return

    # def learn(self, deal, learning_rate=self.learning_rate):
    #     self.trade_params = self.trade_params + learning_rate * deal.Q
    def learn(self, deal):
        return


class Contract():
    """A class to hold information about a proposed trade"""
    def __init__(self, A1, A2):
        self.A1 = A1
        self.A2 = A2
        self.quantities = np.zeros(A1.model.num_goods)

    def random_trade(self):
        return

    def null_trade(self, fraction):
        return(np.multiply(np.add(self.A1.ppf, self.A2.ppf)), fraction)

    def reverse(self):  # Do I have to be careful about return/update?
        self.quantities = np.multiply(self.quantities, -1)


class MarketModel(Model):
    """A barter economy with N agents and K goods"""
    def __init__(self, N, K, width, height):
        self.num_agents = N
        self.num_goods = K
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # create agents
        for i in range(self.num_agents):
            a = BarterAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()
        # remove unacceptable trades?


model = MarketModel(2, 2, 2, 2)
for i in range(20):
    model.step()
