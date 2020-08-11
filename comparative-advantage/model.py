# Libraries
import numpy as np
# import copy
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def utility(agent):
    return agent.utility()


class Market(Model):
    """An economy with N agents and K goods"""
    def __init__(self, N, K, width, height, rand_trade=False):
        super().__init__()
        self.N = N
        self.K = K
        self.rand_trade = rand_trade
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True  # for BatchRunner()
        self.agent_productivity = K * 3
        self.allow_trade = True
        # create agents
        for i in range(N):
            a = BarterAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        # collect data
        self.datacollector = DataCollector(
            model_reporters={},
            agent_reporters={"Utility": utility}
        )
        self.history = []

    def step(self):
        self.datacollector.collect(self)
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
        self.trading = False
        self.generosity = 0.95

    def step(self):
        self.produce()
        self.prob_move()
        if self.model.allow_trade:
            self.trade(self)
        else:
            self.update_plan(np.random.randint(self.model.K))

    def produce(self, factor=1):
        prod = np.multiply(self.plan, self.ppf)
        prod = np.multiply(prod, factor)
        self.endowment += prod
        return True

    def move(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        if possible_moves.length() < 1:
            return False
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

    def trade(self):
        partner = self.find_partner()
        if self.model.rand_trade:
            deal = self.random_trade()
        else:
            deal = self.day_trade(partner)
        if self.eval_trade(deal) and partner.eval_trade(deal, reverse=True):
            self.make_trade(deal)
            self.update_plans(partner)
        else:
            self.update_plan(np.random.randint(self.model.K))

    def reverse_trade(self, deal):
        new_deal = {"buying": deal["selling"],
                    "selling": deal["buying"],
                    "quantity_buying": deal["quantity_selling"],
                    "quantity_selling": deal["quantity_buying"]}
        return new_deal

    def random_trade(self):
        deal = {"buying": np.zeros(self.model.K),
                "selling": np.zeros(self.model.K),
                "quantity_buying": np.zeros(self.model.K),
                "quantity_selling": np.zeros(self.model.K)}
        buyer_gives = np.random.randint(self.model.K)
        seller_gives = np.random.randint(self.model.K)
        deal["buying"][buyer_gives] = 1
        deal["selling"][seller_gives] = 1
        deal["quantity_buying"][buyer_gives] = 1
        x = self.ppf[seller_gives] / self.ppf[buyer_gives]
        deal["quantity_selling"][seller_gives] = x * self.generosity
        return deal

    def day_trade(self, partner):
        if partner:
            deal = {"buying": np.ones(self.model.K),
                    "selling": np.ones(self.model.K),
                    "quantity_buying": partner.calc_production(),
                    "quantity_selling": self.calc_production()}
        else:
            deal = False
        return deal

    def eval_trade(self, deal, reverse=False):
        """ Make sure my utility increases with a trade. """
        if not deal:
            return False
        if reverse:
            deal = self.reverse_trade(deal)
        U1 = self.utility()
        U2 = self.make_trade(deal).utility()
        # I'm pretty sure I've got to fix that syntax.
        prod_ratio = self.ppf[deal["buying"]] / self.ppf[deal["selling"]]
        buy_ratio = deal["quantity_buying"] / deal["quantity_selling"]
        if prod_ratio < buy_ratio:
            U2 = 0
        self.make_trade(self.reverse_trade(deal))
        return U2 > U1

    def make_trade(self, deal):
        for i in deal["buying"]:
            self.endowment[i] += deal["quantity_buying"]
            # partner.endowment[i] -= deal["quantity_buying"]
        for j in deal["selling"]:
            # partner.endowment[j] += deal["quantity_selling"]
            self.endowment[j] -= deal["quantity_selling"]
        return self  # will this let me pipe stuff? I think it will.

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
