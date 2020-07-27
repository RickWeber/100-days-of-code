from mesa import Agent, Model
import numpy as np
# from mesa.time import RandomActivation
# from mesa.space import SingleGrid
# from mesa.datacollection import DataCollector


class BarterAgent(Agent):
    """An agent with ability to produce and trade."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.plan = np.ones(model.num_goods)
        self.ppf = np.random.randint(4, size=(model.num_goods))
        self.util_params = np.ones(model.num_goods) / model.num_goods
        self.endowment = np.zeros(model.num_goods)
        self.discount_rate = 0.05
        self.trade_params = np.zeros(model.num_goods)
        # self.bias = np.ones(model.num_goods) # the idea here is to
        # over/understate willingness to buy/sell, possibly based on
        # observations about one's trading partner. But what I really
        # want is a bag of bias vectors and some mapping function.
        # but that sounds too complicated for right now.

    def step(self):
        self.produce()
        # print(str(self.unique_id) + ":" + str(self.endowment))
        partner = self.model.random.choice(self.model.schedule.agents)
        # deal = rand_trade()
        if self.propose_trade(partner):
            self.trade(partner)
            self.trade_params = self.trade_params  # some kind of
            # update...

        # self.propose_trade(partner)
        # self.trade(partner)

    def produce(self):
        production = (self.plan * self.ppf) / sum(self.plan)
        self.endowment = self.endowment + production

    def utility(self):
        utils = 0
        for i in range(self.model.num_goods):
            utils += self.endowment[i] ** self.util_params[i]
        return utils  # I can make this nicer later.

    def propose_trade(self, partner):
        deal = self.rand_trade + self.trade_params
        self.eval_trade(deal) and partner.eval_trade(-deal)

    def trade(self, partner, deal):
        self.make_trade(deal)
        partner.make_trade(-deal)

    def make_trade(self, deal):
        self.endowment = self.endowment + deal

    def rand_trade(self):
        trade = np.random.uniform(-1, 1, size=(self.model.num_goods))
        trade = np.dot(trade,self.ppf)
        return trade

    def eval_trade(self, deal):
        # Do I benefit from the trade
        self.utility() < self.make_trade(deal).utility()
        # Can I make the trade?

# NOTE:
# I could allow exchanges to involve a timing vector. e.g. I pay
# today for something to be received in the future. Or I borrow today
# and pay in the future

    def make_trade(self, deal):
        self.endowment = self.endowment + deal




class MarketModel(Model):
    """A barter economy with N agents and K goods"""
    def __init__(self, N, K):
        self.num_agents = N
        self.num_goods = K
        # create agents
        for i in range(self.num_agents):
            a = BarterAgent(i, self)
