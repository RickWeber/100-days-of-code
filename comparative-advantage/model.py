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
        self.agent_productivity = K * 2
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
        # self.ppf = np.random.randint(4, size=(model.K))
        self.ppf = np.zeros(model.K)
        self.plan = np.ones(model.K)
        for i in range(model.agent_productivity):
            self.ppf[np.random.randint(model.K)] += 1
        self.plan = np.ones(model.K)
        self.endowment = np.zeros(model.K)

    def step(self):
        self.trade()

    def produce(self):
        prod = np.multiply(self.plan, self.ppf)
        self.endowment += prod

    def find_partner(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) < 1:
            return False
        self.random.choice(cellmates)

    # this could be prettier...
    def trade(self):
        partner = self.find_partner()
        if not partner:
            return False
        buyer_gives = np.random.randint(self.model.K)
        seller_gives = np.random.randint(self.model.K)
        if buyer_gives == seller_gives:
            return False
        q_buy = self.ppf[buyer_gives]
        q_sell = partner.ppf[seller_gives]
        if (q_buy == 0) or (q_sell == 0):
            return False
        buyer_tradeoff = self.ppf[buyer_gives] / self.ppf[seller_gives]
        seller_tradeoff = self.ppf[seller_gives] / self.ppf[buyer_gives]
        if buyer_tradeoff > (q_buy / q_sell):
            return False
        if seller_tradeoff > (q_sell / q_buy):
            return False
        self.endowment[buyer_gives] -= q_buy
        partner.endowment[seller_gives] -= q_sell
        partner.endowment[buyer_gives] += q_buy
        self.endowment[seller_gives] += q_sell
        self.plan[buyer_gives] += 1
        partner.plan[seller_gives] += 1
