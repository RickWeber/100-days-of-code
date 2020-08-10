# Libraries
import numpy as np
# import copy
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class Market(Model):
    """An economy with N agents and K goods"""
    def __init__(self, N, K, width, height, rand_trade=False):
        super().__init__()
        self.N = N
        self.K = K
        self.rand_trade = rand_trade
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.agent_productivity = K * 3
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
        self.plan = np.ones(model.K)
        self.ppf = np.zeros(model.K)
        for i in range(model.agent_productivity):
            self.ppf[np.random.randint(model.K)] += 1
        self.plan = np.ones(model.K)
        self.endowment = np.zeros(model.K)
        self.utility_params = np.random.rand(model.K)
        self.move_preference = np.random.randint(100)

    def step(self):
        self.produce()
        self.prob_move()
        if self.trade(self.model.rand_trade):
            return True
        else:
            self.move_preference += 1
            if not self.prob_move():
                self.produce(0.1)

    def produce(self, factor=1):
        prod = np.multiply(self.plan, self.ppf)
        prod = np.multiply(prod, factor)
        self.endowment += prod
        return True

    def move(self):  # ripped off from mesa tutorial
        possible_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)
        return True

    def prob_move(self):
        if np.random.randint(100) < self.move_preference:
            self.move()
            return True
        else:
            return False

    def find_partner(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) < 1:
            return False
        return self.random.choice(cellmates)

    # this could be prettier...
    def trade(self, random=False):
        partner = self.find_partner()
        if not partner:
            self.update_plan(np.random.randint(self.model.K))
            return partner
        if random:
            deal = self.random_trade(partner)
            if not deal:
                self.update_plan(np.random.randint(self.model.K))
                return deal
            else:
                self.update_plan(deal[0][0])
                partner.update_plan[deal[1][0]]
        else:
            self.day_trade(partner)
            self.update_plans(partner)
        return True

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
        return [[good_buy, q_buy], [good_sell, q_sell]]

    def day_trade(self, partner):
        prod1 = self.calc_production()
        prod2 = partner.calc_production()
        # diff = np.subtract(prod1, prod2)
        self.endowment = np.subtract(self.endowment, prod1)
        partner.endowment = np.subtract(partner.endowment, prod2)
        self.endowment = np.add(self.endowment, prod2)
        partner.endowment = np.add(partner.endowment, prod1)
        return True

    def inc_plan(self, good, up=True):
        if up:
            self.plan[good] += 1
        else:
            self.plan[good] -= 1
        return True

    def calc_production(self):
        return np.multiply(self.ppf, self.plan)

    def utility(self):
        U = 0
        for i in range(self.model.K):
            U = U + self.endowment[i] ** self.utility_params[i]
        return U

    def update_plan(self, k):
        baseline = self.utility()
        self.inc_plan(k)
        # reset if this doesn't increase utility
        if self.utility <= baseline:
            self.inc_plan(k, False)
            return False
        return True

    def update_plans(self, partner):
        k1 = np.random.randint(self.model.K)
        k2 = np.random.randint(self.model.K)
        alt1 = BarterAgent(0, self.model)
        alt1.inc_plan(k1)
        if alt1.utility() > self.utility():
            self.inc_plan(k1)
            return True
        alt2 = BarterAgent(0, self.model)
        alt2.inc_plan(k2)
        if alt2.utility() > partner.utility():
            partner.inc_plan(k2)
            return True
        return False


def easy_model():
    model = Market(2, 2, 1, 1, False)
    for i in range(2):
        A = model.schedule.agents[i]
        A.move_prefence = 0
        A.utility_params = np.divide(np.ones(model.K), model.K)
        if i % 2 == 0:
            A.ppf = [4, 1]
        else:
            A.ppf = [1, 4]
    return model
