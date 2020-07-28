import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.datacollection import DataCollector


class BarterAgent(Agent):
    """An agent with ability to produce and trade."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.plan = np.ones(model.num_goods)
        self.ppf = np.random.randint(4, size=(model.num_goods))
        self.util_params = np.ones(model.num_goods) / model.num_goods
        self.endowment = np.zeros(model.num_goods)
        self.discount_rate = 0.05
        self.learning_rate = 0.05
        self.trade_params = np.zeros(model.num_goods)
        # self.bias = np.ones(model.num_goods) # the idea here is to
        # over/understate willingness to buy/sell, possibly based on
        # observations about one's trading partner. But what I really
        # want is a bag of bias vectors and some mapping function.
        # but that sounds too complicated for right now.

    def step(self):
        self.produce()
        # possibly move, or otherwise choose not to trade
        # self.move()
        # randomly select a trading partner
        partner = self.model.random.choice(self.model.schedule.agents)
        # in the future this should be a weighted probability based on
        # experience and signals sent by other agents.
        # Make up a random trade
        deal = self.rand_trade(partner)  # creates Trade() object
        # if proposed trade is unacceptable...
        if not deal.acceptable():
            # set values so the trade doesn't happen and it isn't marked as complete
            deal.times = - np.ones(self.model.num_goods)
        if self.propose_trade(partner, deal):
            # actually make the trade
            self.trade(partner, deal)
            # and update the agents
            self.learn(deal)
            partner.learn(deal)

    def produce(self):
        production = (self.plan * self.ppf) / sum(self.plan)
        self.endowment = self.endowment + production

        # right now it's just a blanket offer
    # def __init__(self, A1, A2, quantities, model):
    def rand_trade(self, partner):
        quantities = np.random.normal(size=(self.model.num_goods))
        time = np.zeros(self.model.num_goods)
        deal = Trade(self, partner, quantities, times)
        return deal

    # def propose_trade(self, partner, deal):
    #     # deal = self.rand_trade + self.trade_params
    #     self.eval_trade(deal) and partner.eval_trade(-deal)

    def eval_trade(self, deal):
        # Do I benefit from the trade
        d1 = deal
        d2 = deal.reverse
        u1 = self.utility
        self.make_trade(d1)
        u2 = self.utility()
        self.make_trade(d2)
        u1 < u2
        # self.utility() < self.make_trade(deal).utility()
        # this should really be a forecast of utility if a) I don't make
        # the trade, and b) I've got those resources on hand to possibly
        # make the next trade...
        # Can I make the trade?

    def make_trade(self, deal):
        self.endowment
    # def make_trade(self, deal):
    #     self.endowment = self.endowment + deal
    # I think I've actually got this in the step function of the deal itself

    def utility(self):
        utils = 0
        for i in range(self.model.num_goods):
            utils += self.endowment[i] ** self.util_params[i]
        return utils  # I can make this nicer later.

    def trade(self, partner, deal):
        self.make_trade(deal)
        partner.make_trade(-deal)

    def learn(self, deal):
        self.trade_params = self.trade_params + self.learning_rate * deal


# NOTE:
# I could allow exchanges to involve a timing vector. e.g. I pay
# today for something to be received in the future. Or I borrow today
# and pay in the future


class Trade():
    """A contract between two agents"""
    def __init__(self, A1, A2, quantities, times):
        self.A1 = A1  # The initiator/buyer
        self.A2 = A2  # The receiver/seller
        self.Q = quantities
        self.T = times
        self.complete = False
        self.acceptable = False
        # bring in the timing vector. For now I'll just use a vector of 0s
        # self.times = np.zeros(model.num_goods)

    def step(self):
        if not self.acceptable:
            return  # nothing to do
        for i in range(self.model.num_goods):
            if self.times[i] == 0:
                self.A1.endowment[i] += self.deal[i]
                self.A2.endowment[i] -= self.deal[i]
       if max(self.times <= 0):
           self.complete = True

    def acceptable1(self):
        self.A1.eval_trade(self)

    def acceptable(self):
        self.A1.eval_trade(self) and self.A2.eval_trade(self)

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
