# Libraries
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class Market(Model):
    """An economy with N agents and K goods"""
    def __init__(self, N, K, width=1, height=1, rand_trade=False):
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
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.plan = np.ones(model.K)
        self.ppf = np.ones(model.K)
        for i in range(model.agent_productivity - model.K):
            self.ppf[np.random.randint(model.K)] += 1
        self.endowment = np.ones(model.K) * 3
        u_params = np.random.randint(4, size=model.K)
        self.u_params = u_params / u_params.sum()
        self.generosity = np.random.normal(0.95, 0.025)
        self.memory = np.zeros(model.K)
        self.learning_rate = 0.05
        sell = (np.random.rand((10, model.K)) - 0.5) < 0
        self.trades = np.random.randint(3, size=(10, model.K))  # 10 vectors
        self.trades[sell] *= -1
        self.trade_plan = np.ones(10)

    def step(self):
        self.produce(2)
        # partner, deal, dealnum = self.trade()
        self.trade()
        self.consume()
        self.move()

    def produce(self, factor=1):
        prod = np.multiply(self.plan, self.ppf)
        prod = np.multiply(prod, factor)
        self.endowment += prod
        return True

    def trade(self):
        partner = self.find_partner()
        prob = self.trade_plan / self.trade_plan.sum()
        dealnum = np.random.choice(range(10),
                                   1,
                                   p=prob)
        deal = self.trades[dealnum]
        good_for_goose = compare(deal, self.ppf) > 0
        good_for_gander = compare(-deal, partner.ppf) > 0
        if not good_for_goose or not good_for_gander:
            deal = np.zeros(self.model.K)
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
        prob = self.u_params / sum(self.u_params)
        consumption = self.model.agent_productivity
        consumption = int(consumption * ratio)
        for i in range(consumption):
            good = np.random.choice(range(self.model.K),
                                    1,
                                    p=prob)
            self.endowment[good] -= 1
        return self

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

    def update(self, deal):
        update = self.learning_rate * deal
        self.plan += update
        self.plan[self.plan < 0] = 0.1
        return self

    def find_partner(self):
        if self.model.grid.width + self.model.grid.height < 10:
            return self.model.schedule.agents[np.random.randint(self.model.N)]
        else:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            if len(cellmates) < 1:
                return self
            return self.random.choice(cellmates)

    def utility(self):
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


def compare(vect, basis):
    out = vect * (basis[0] / basis)
    out.sum()
