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
        self.prices = np.divide(self.ppf, self.ppf[0])

    def export_params(self):
        return({
            "model": self.model,
            "plan": self.plan,
            "ppf": self.ppf,
            "util_params": self.util_params,
            "endowment": self.endowment,
            "discount_rate": self.discount_rate,
            "learning_rate": self.learning_rate,
            "trade_params": self.trade_params
        })

    def update_params(self, params_dict):
        for p in params_dict:
            self.p = params_dict[p]
            # Ideally I'd have a way to take parent params,
            # mutate, and create a child.

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

    def random_partner(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) < 1:
            return
        self.random.choice(cellmates)

    def U_max_trade(self, partner):  # I don't like this method name
        deal = Contract(self, partner)  # null trade
        utils_per_dollar = self.dU / self.prices
        buying = np.argmax(utils_per_dollar)
        prices = self.convert_prices(buying)
        deal.quantities[not buying] = prices[not buying]
        deal.quantities[buying] = -1
        selling = partner.pick_best_offer(deal.quantities)
        if buying == selling:
            return  # nothing to trade here
        deal.quantites[not buying and not selling] = 0
        self.update_prices(deal)
        partner.update_prices(deal)
        # Q = deal.quantities
        # Q[np.argmax(utils_per_dollar)] = 1
        # Q[not np.argmax(utils_per_dollar)] = self.prices[not np.argmax(utils_per_dollar)]
        return deal

    def update_prices(self, deal):
        """
        The deal.quantities will look like this: [0 0 -1 0 4.5]
        In which case, I want an agent to convert this to the numeraire
        [0 0 some_price 0 some_price]
        Good 2 for good 4, what price did this deal go at?
        """
        bought = np.argmin(deal.quantities)
        sold = np.argmax(deal.quantities)
        if bought == 0:
            prices = abs(deal.quantities)
        if sold == 0:
            prices = abs(1 / deal.quantities)  # probably wrong, will fix later
            # actually, I think that's right!
        prices = deal.quantities / self.prices[bought]
        # prices = deal.quantities / self.prices
        # prices = deal.quantities / self.prices[np.argmin(deal.quantities)]
        # convert the prices to be in terms of the numeraire
        update = self.learning_rate * prices
        self.prices = (1 - self.learning_rate) * self.prices + update

    def convert_prices(self, buying=0):  # pretty sure that's fine...
        return self.prices / self.prices[buying]

    def trade(self):
        partner = self.random_partner()
        deal = self.U_max_trade(partner)
        # deal = Contract(self, partner).random_trade()
        # deal = Contract(self, partner).null_trade(1/10)
        # alternately...
        # try to buy item with max self.dU / self.prices
        # offer to sell any of the other goods in units
        # based on self.prices (i.e. what can I get cheap)
        # let partner accept whatever will maximize their
        # utility
        if not self.evaluate_trade(deal):
            return
        if not partner.evaluate_trade(deal.reverse):
            return
        self.make_trade(deal)
        partner.make_trade(deal.reverse())
        # self.learn()

    def negotiate(self, deal):
        # what does my partner want from me?
        selling = np.argmax(deal.quantities)
        # what item are they offering the best price for?
        # marginal_effects = self.dU / deal.quantities
        # I should turn down the deal entirely if their prices are
        # higher than mine for not selling
        N = self.model.num_goods
        for i in range(N):
            if i == selling:
                next
            if -deal.quantities[i] < self.prices[i]:
                next
            buying = i
        return

    def utility(self):
        utils = 0
        for i in range(self.model.num_goods):
            utils += self.endowment[i] ** self.util_params[i]
        return utils  # I can make this nicer later.

    def dU(self):
        U = self.utility()
        out = []
        for i in range(self.model.num_goods):
            Ui = self.endowment[i] ** self.util_params[i]
            Ui_prime = self.endowment[i] ** (self.util_params[i] - 1)
            out[i] = (U * Ui_prime) / Ui
        return out

    def evaluate_trade(self, deal):
        self.utility() < self.make_trade(deal).utility()

    def make_trade(self, deal):
        dQ = np.ma.masked_where(deal.times == 0, deal.quantities)
        self.endowment += dQ
        return

    # def learn(self, deal, learning_rate=self.learning_rate):
    #     self.trade_params = self.trade_params + learning_rate * deal.Q
    def learn(self, deal, learning_rate="default"):
        if learning_rate == "default":
            learning_rate = self.learning_rate
        update = np.multiply(learning_rate, deal.quantities)
        self.trade_params += update

    def compare_prices(self, price_vector):
        """
        given an offered price vector, this returns a vector of quantities
        representing how many units of the numeraire self would normally
        expect based on self.prices

        So if the offer is [-1 1 25 1/4]
        they're selling the numeraire, so they can directly compare that
        vector to self.prices
        If the offer is [4 -1 2 1/2] then they're selling good 1.
        If self.prices is [1 2 3 4]
        We're dealing with something equivalent to 2 units of numeraire.
        So the offer is to accept 4 units of numeraire to give up something
        worth 2 units. For good 2, the offer is 2 of something worth 3
        numeraire which is a better deal. The final item for offer is
        1/2 unit of good 3 which is only worth 2 units of numeraire.
        """
        # buy = np.argmax(price_vector)
        price_vector = -price_vector
        # buy = np.argmin(price_vector)  # there should be one negative
        # cost = self.prices[buy]  # how many numeraire am I giving up?
        consider = np.multiply(self.prices, price_vector)
        return consider / price_vector
        # sell = np.argmax(consider)  # or min?

    def pick_best_offer(self, price_vector):
        consider = np.multiply(self.prices, price_vector)
        return np.argmax(consider)

class Contract():
    """A class to hold information about a proposed trade"""
    def __init__(self, A1, A2):
        self.A1 = A1
        self.A2 = A2
        self.quantities = np.zeros(A1.model.num_goods)
        self.times = np.zeros(A1.model.num_goods)

    def random_trade(self):
        return

    def null_trade(self, fraction=1/2):  # this should be renamed
        Q = np.multiply(np.add(self.A1.ppf, self.A2.ppf), fraction)
        self.quantities = Q
        self.times = np.zeros(self.A1.model.num_goods)

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


model = MarketModel(2, 2, 1, 1)
for i in range(20):
    model.step()
