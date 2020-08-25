# Libraries
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


# def null_contract(agents):
#     model = agents[0].model
#     exchanges = [np.zeros(model.K) for a in agents]
#     C = Contract(agents, exchanges, model)
#     return C


# class Contract():
#     """A contract mapping actions to payoffs for some agents"""
#     def __init__(self, agents, exchanges, model):
#         self.model = model
#         self.agents = agents
#         self.exchanges = exchanges

#     def mutate_contract(self, mutation="noise", noise_factor=1, donor=None):
#         """Given a contract, mutate it in some way."""
#         change = np.zeros(size=self.exchanges.size)
#         if mutation == "noise":
#             change = np.random.randn(size=self.exchanges.size,
#                                      mean=0, sd=noise_factor)
#         if mutation == "cross" and donor is not None:
#             for g in self.model.trades:
#                 if np.random.rand() > 0.5:
#                     change[g] = donor.trades[g]
#         self.exchanges += change
#         return self


class Market(Model):
    """An economy with N agents and K goods"""
    def __init__(self, N, K, width=1, height=1):
        super().__init__()
        self.N = N
        self.K = K
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True  # for BatchRunner()
        self.agent_productivity = K * 3
        self.allow_trade = True
        self.history = []
        self.trades = 10
        # create agents
        for i in range(N):
            a = BarterAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        # collect data
        self.datacollector = DataCollector(
            # Not sure why this is giving me problems...
            model_reporters={"Number of trades": self.history.len()},
            agent_reporters={"Utility": utility_reporter,
                             "Specialization": specialization_reporter}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


class BarterAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.plan = np.ones(model.K)
        self.ppf = np.ones(model.K)
        for i in range(model.agent_productivity - model.K):
            self.ppf[np.random.randint(model.K)] += 1
        self.endowment = np.ones(model.K) * 3
        u_params = np.random.randint(4, size=model.K) + 1
        self.u_params = u_params / u_params.sum()
        self.generosity = np.random.normal(0.95, 0.025)
        # self.generosity = np.random.rand(0.95, 1)
        self.memory = np.zeros(model.K)
        self.learning_rate = 0.05
        # Something here is acting like a tuple...
        sell = np.random.rand(model.trades, model.K) - 0.5 < 0
        self.trades = np.random.randint(3, size=(model.trades, model.K))
        self.trades[sell] *= -1
        self.trade_plan = np.ones(model.trades)

    def step(self):
        """What happens each time step"""
        self.produce(2)
        if sum(self.endowment > 0) < self.model.K:
            self.produce()
        else:
            self.trade()
        self.consume(1)
        self.move()

    def produce(self, factor=1):
        """Produce based on production plan"""
        prod = np.multiply(self.plan, self.ppf)
        prod = np.multiply(prod, factor)
        self.endowment += prod
        return self

    def trade(self):
        """Find a partner and try to make a deal."""
        partner = self.find_partner()
        prob = self.trade_plan / self.trade_plan.sum()
        dealnum = np.random.choice(range(self.model.trades),
                                   1,
                                   p=prob)
        deal = self.trades[dealnum]
        good_for_goose = compare(deal, self.ppf) > 0
        good_for_gander = compare(-deal, partner.ppf) > 0
        if not good_for_goose or not good_for_gander:
            return self
        else:
            self.model.history.append((self.unique_id,
                                       partner.unique_id,
                                       deal))
            self.endowment += deal
            partner.endowment -= deal
            self.update(deal)
            partner.update(-deal)
            self.trade_plan[dealnum] += 1
        return self

    def consume(self, ratio=1):
        """Use up goods based on weighted probability"""
        params = self.u_params
        consumption = self.model.agent_productivity
        consumption = int(consumption * ratio)
        for i in range(consumption):
            have_enough = self.endowment > 0
            prob = params[have_enough] / sum(params[have_enough])
            good = np.random.choice(range(self.model.K)[have_enough],
                                    1,
                                    p=prob)
            self.endowment[good] -= 1
        return self

    def move(self):
        """Move to an adjacent grid cell"""
        possible_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        if possible_moves.len() < 1:
            return False
        new_position = self.random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)
        return True

    def update(self, deal):
        """Update production plans in light of this deal"""
        update = self.learning_rate * deal
        self.plan -= update  # pretty sure that should be negative...
        self.plan[self.plan < 0] = 0.01
        return self

    def find_partner(self):
        """Choose another agent unless nobody is close enough."""
        if self.model.grid.width + self.model.grid.height < 10:
            prtnr = self.model.schedule.agents[np.random.randint(self.model.N)]
            if prtnr == self:
                prtnr = self.find_partner()
        else:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            if len(cellmates) < 1:
                return self
            prtnr = self.random.choice(cellmates)
        return prtnr

    def utility(self):
        """Calculate utility based on endowment and Cobb-Douglas preferences"""
        (self.endowment ** self.u_params).sum()


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


def easy_model(N=2):
    model = Market(N, N, 1, 1)
    for i in range(N):
        A = model.schedule.agents[i]
        A.u_params = np.divide(np.ones(N), N)
        A.ppf = np.ones(N)
        A.ppf[i] = 4
    return model


def money_model(model):
    """Modify the model so good 0 is fixed, contributes nothing to the agents'
    utility, and is used to buy other goods (no barter)."""
    model.schedule.agents.ppf[0] = 0
    model.schedule.agents.endowment[0] = 1000
    model.schedule.agents.util_params[0] = 0
    # trade only occurs via good 0
    for i in model.schedule.agents:
        i.trades = i.trades.abs()
        buys = np.random.rand(model.trades) - 0.5 < 0
        # I'm pretty sure I need to tune the random numbers
        # to match endowment size.
        i.trades[buys, 0] = np.random.randint(3, size=(model.trades, 1))
        i.trades[buys, 1:] = np.zeros((model.trades, model.K-1))
        i.trades[not buys, 0] = np.zeros((model.trades, 1))
        i.trades[not buys, 1:] = np.random.randint(3, (model.trades, model.K-1))
    return model


def compare(vect, basis):
    """Compare a vector to some basis. Used to map a deal and an agent's ppf
    to a real number. If that number is positive, it means they come out ahead
    on the deal relative to no ability to trade."""
    out = vect * (basis[0] / basis)
    out.sum()
