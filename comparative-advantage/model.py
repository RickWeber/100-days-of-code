# Libraries
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def utility_reporter(agent):
    """How much utility does agent have right now?"""
    return agent.utility()


def specialization_reporter(agent):
    """How much of agent's time is spent on their most popular good?"""
    return agent.plan.max() / agent.plan.sum()


def reverse_trade(deal):
    new_deal = {"buying": deal["selling"],
                "selling": deal["buying"]}
    return new_deal


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
            agent_reporters={"Utility": utility_reporter,
                             "Specialization": specialization_reporter}
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
        self.endowment = np.ones(model.K) * 3  # not sure if this will simplify
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
        self.consume(1/2)

    def consume(self, ratio=1):
        """Use up goods based on weighted probability"""
        prob = self.utility_params / sum(self.utility_params)
        consumption = self.model.agent_productivity / self.model.K
        consumption = int(consumption * ratio)
        for i in range(consumption):
            good = np.random.choice(range(self.model.K),
                                    1,
                                    p=prob)
            self.endowment[good] -= 1
        return self

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
        if self.eval_trade_both(partner, deal):
            self.make_trade(deal)
            self.model.history.append(deal)
            self.update_plans(partner)
        else:
            self.update_plan(np.random.randint(self.model.K))

    # def multi_trade(self, partner, n_offers, n_trades):
    #     offers = []
    #     gains = []
    #     for o in range(n_offers):
    #         offer = self.random_trade
    #         if self.eval_trade_both(partner, offer):
    #             offers.append(offer)
    #             up = (offer["buying"]/self.ppf).sum()
    #             down = (offer["selling"]/self.ppf).sum()
    #             gains.append(up - down)
    #     index = gains.argsort()
    #     offers = offers[index]
    #     for t in range(n_trades):
    #         if offers.len() < 1:
    #             pass
    #         else:
    #             deal = offers[t]
    #             self.make_trade(offers[t])
    #             offers = offers[1:]
    #             self.model.history.append()
    # def multi_trade(self, partner, n_trades):

    def null_trade(self):
        deal = {"buying": np.zeros(self.model.K),
                "selling": np.zeros(self.model.K)}

    def random_trade(self):
        deal = self.null_trade()
        buyer_gives = np.random.randint(self.model.K)
        seller_gives = np.random.randint(self.model.K)
        # deal["buying"][buyer_gives] = 1
        # deal["selling"][seller_gives] = 1
        deal["buying"][buyer_gives] = 1
        x = self.ppf[seller_gives] / self.ppf[buyer_gives]
        deal["selling"][seller_gives] = x * self.generosity
        return deal

    def day_trade(self, partner):
        if partner:
            deal = {"buying": partner.calc_production(),
                    "selling": self.calc_production()}
        else:
            deal = False
        return deal

    def eval_trade(self, deal):
        (deal["buying"]/self.ppf).sum() > (deal["selling"]/self.ppf).sum()

    def eval_trade_both(self, partner, deal):
        self.eval_trade(deal) and partner.eval_trade(reverse_trade(deal))

    def compare_trades(self, deal1, deal2):
        D1 = (deal1["buying"]/self.ppf).sum()/(deal1["selling"]/self.ppf).sum()
        D2 = (deal2["buying"]/self.ppf).sum()/(deal2["selling"]/self.ppf).sum()
        if D1 > D2:
            return D1
        else:
            return D2

    def eval_trade_old(self, deal, reverse=False):
        """ Make sure my utility increases with a trade. """
        if not deal:
            return False
        if reverse:
            deal = self.reverse_trade(deal)
        U1 = self.utility()
        U2 = self.make_trade(deal).utility()
        # I'm pretty sure I've got to fix that syntax.
        prod_ratio = self.ppf[deal["buying"]] / self.ppf[deal["selling"]]
        buy_ratio = deal["buying"] / deal["selling"]
        if prod_ratio < buy_ratio:
            U2 = 0
        self.make_trade(self.reverse_trade(deal))
        return U2 > U1

    def make_trade(self, deal):
        for i in deal["buying"]:
            self.endowment[i] += deal["buying"]
            # partner.endowment[i] -= deal["buying"]
        for j in deal["selling"]:
            # partner.endowment[j] += deal["selling"]
            self.endowment[j] -= deal["selling"]
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


def money_model(model):
    model.schedule.agents.ppf[0] = 0
    model.schedule.agents.endowment[0] = 1000
    model.schedule.agents.util_params[0] = 0
    # trade only occurs via good 0

    def money_trade(self, good, price):
        deal = self.null_trade()
        deal["buying"][good] = 1
        deal["selling"][good] = price
        return deal

    return True
