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
        self.produce()
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
        self.day_trade(partner)
        # I'm not sure how to update behavior for day_trade
        self.random_trade(partner)
        self.update_plans(partner)

    def random_trade(self, partner):
        buyer_gives = np.random.randint(self.model.K)
        seller_gives = np.random.randint(self.model.K)
        q_buy = self.ppf[buyer_gives]
        q_sell = partner.ppf[seller_gives]
        if (q_buy == 0) or (q_sell == 0):
            return False
        buyer_tradeoff = self.ppf[buyer_gives] / self.ppf[seller_gives]
        seller_tradeoff = self.ppf[seller_gives] / self.ppf[buyer_gives]
        good_buy = buyer_tradeoff > (q_buy / q_sell)
        good_sell = seller_tradeoff > (q_sell / q_buy)
        if not good_sell or not good_buy:
            return False
        self.endowment[buyer_gives] -= q_buy
        partner.endowment[seller_gives] -= q_sell
        self.endowment[seller_gives] += q_sell
        partner.endowment[buyer_gives] += q_buy
        # self.plan[buyer_gives] += 1
        # partner.plan[seller_gives] += 1
        self.inc_plan(buyer_gives)  # is this really better than above?
        partner.inc_plan(seller_gives)

    def day_trade(self, partner):
        prod1 = np.multiply(self.ppf, self.plan)
        prod2 = np.multiply(partner.ppf, partner.plan)
        # diff = np.subtract(prod1, prod2)
        self.endowment = np.subract(self.endowment, prod1)
        partner.endowment = np.subract(partner.endowment, prod2)
        self.endowment = np.add(self.endowment, prod2)
        partner.endowment = np.add(partner.endowment, prod1)

    def inc_plan(self, good):
        self.plan[good] += 1

    def update_plans(self, partner):
        # update production plans in direction of comparative advantage
        return True
