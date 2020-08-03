# libraries
import numpy as np
import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from mesa.datacollection import DataCollector


class BarterAgent(Agent):
    def __init__(self, unique_id, model):
        """
        An agent with capacities, plans, expectations (about prices).
        """
        super().__init__(unique_id, model)
        self.model = model
        self.plan = np.ones(3)
        self.production_plan = np.ones(model.num_goods)
        self.ppf = np.random.randint(4, size=(model.num_goods))
        self.util_params = np.ones(model.num_goods) / model.num_goods
        self.endowment = np.zeros(model.num_goods)
        self.discount_rate = np.random.uniform(0.01, 0.25)
        self.learning_rate = np.random.uniform(0.01, 0.25)
        self.prices = np.divide(self.ppf, self.ppf[0])
        self.next_step = "produce"
        # self.network connections and chance of someone else randomly?
        # self.net = model.schedule.agents etc.

    def step(self):
        if self.next_step == "produce":
            self.produce()
        if self.next_step == "trade":
            partner = self.find_partner()
            self.make_offer(partner)
        if self.next_step == "move":
            self.move()
        moves = ["produce", "trade", "move"]
        # There should be a way to update self.plan
        # but I can solve that later
        self.next_step = random.choices(moves, self.plan)[0]

    def inc_plan(self, move="produce"):
        if move == "produce":
            self.plan[0] += 1
        if move == "trade":
            self.plan[1] += 1
        if move == "move":
            self.plan[2] += 1

    def inc_prod_plan(self, good=0):
        self.production_plan[good] += 1

    def agent_state_dict(self):
        return({
            "model": self.model,
            "plan": self.plan,
            "production_plan": self.production_plan,
            "ppf": self.ppf,
            "util_params": self.util_params,
            "endowment": self.endowment,
            "discount_rate": self.discount_rate,
            "learning_rate": self.learning_rate,
            "prices": self.prices,
            "next_step": self.next_step
        })

    def import_state_dict(self, params_dict):
        for p in params_dict:
            self.p = params_dict[p]

    def mutate_state(self):
        """export current state with noise"""
        out = self.agent_state_dict
        # out = out + noise
        return out

    def combine_states(self, partner):
        my_params = self.agent_state_dict()
        partner_params = partner.agent_state_dict()
        for p in my_params:
            my_params[p] += partner_params[p]
        return my_params

    def utility(self):
        utils = 0
        for i in range(self.model.num_goods):
            utils += self.endowment[i] ** self.util_params[i]
        return utils  # I can make this nicer later.

    def produce(self):
        production = np.dot(self.plan, self.ppf) / sum(self.plan)
        self.endowment = self.endowment + production

    def dU(self):
        U = self.utility()
        out = []
        for i in range(self.model.num_goods):
            Ui = self.endowment[i] ** self.util_params[i]
            Ui_prime = self.endowment[i] ** (self.util_params[i] - 1)
            out[i] = (U * Ui_prime) / Ui
        return out

    def find_partner(self):
        return self.random_partner()

    def random_partner(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) < 1:
            return
        self.random.choice(cellmates)

    def make_offer(self, partner):
        deal = Contract(self, partner)  # null trade
        utils_per_dollar = self.dU / self.prices
        buying = np.argmax(utils_per_dollar)
        prices = self.convert_prices(buying)
        deal.quantities[not buying] = prices[not buying]
        deal.quantities[buying] = -1  # is this right?
        selling = partner.pick_best_offer(deal.quantities)
        # If what they're being asked to give up is more valuable
        # than anything on offer, buying==selling
        if buying == selling:
            # reduce likelihood of trying to trade in the future
            # make this nicer in the future
            self.inc_plan("produce")
            self.inc_plan("move")
            return False  # nothing to trade here
        deal.quantities[not buying and not selling] = 0
        deal.execute()
        self.update_prices(deal)
        partner.update_prices(deal)
        True

    def pick_best_offer(self, price_vector):
        """
        Given offers of quantities of units to receive, decide which is worth
        the most in terms of my own price vector.

        given price_vector = [1 2 -1 3 1/2]
        and self.prices = [1 3 12 3 48]
        calculate consider = [1 6 12 9 24]
        return: 4

        given price_vector = [1 2 -1 3 1/2]
        and self.prices = [1 3 12 3 2]
        calculate consider = [1 6 12 9 1]
        return: 2
        """
        consider = np.multiply(self.prices, np.absolute(price_vector))
        # Do I need to return False if there aren't any good enough offers?
        return np.argmax(consider)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True
        )
        # I could add some bias or a simple program to change how they move...
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

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

    # def evaluate_trade(self, deal):
    #     self.utility() < self.make_trade(deal).utility()
    # I'm pretty sure I don't need this, but I like it enough to wait

    # Save this for when I build time in to the model
    def make_trade(self, deal):
        dQ = np.ma.masked_where(deal.times == 0, deal.quantities)
        self.endowment += dQ
        return


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

    def execute(self):
        self.A1.endowment += self.quantities
        self.A2.endowment -= self.quantities


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
