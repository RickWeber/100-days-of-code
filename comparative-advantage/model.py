# Libraries
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
# from mesa.space import MultiGrid
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
    def __init__(self, N, K):  # , width=1, height=1):
        super().__init__()
        self.N = N
        self.K = K
        # self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True  # for BatchRunner()
        self.agent_productivity = K * 3
        self.allow_trade = True
        self.history = []
        self.trades_undertaken = 0
        self.trades = 50
        # create agents
        for i in range(N):
            a = BarterAgent(i, self)
            self.schedule.add(a)
        # collect data
        self.datacollector = DataCollector(
            model_reporters={"Number of trades": "self.trades_undertaken"},
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
        self.endowment = np.ones(model.K) * 10
        u_params = np.random.randint(4, size=model.K) + 1
        self.u_params = u_params / u_params.sum()
        # self.memory = np.zeros(model.K)  # might be something here...
        self.learning_rate = 0.05
        self.trades = np.random.randint(-3, 3, size=(model.trades, model.K))
        self.trade_plan = np.ones(model.trades)

    def step(self):
        """What happens each time step"""
        self.produce(2)
        if sum(self.endowment > 0) < self.model.K:
            self.produce()
        else:
            self.trade()
        self.consume(1)

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
        print(dealnum)  # make sure this code is working properly.
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
        # consumption = self.model.agent_productivity
        # consumption = int(consumption * ratio)
        # print(consumption)
        consumption = 5
        if self.endowment.min() < consumption:
            return self
        probs = self.u_params  # / self.u_params.sum()
        eat = np.random.choice(range(self.model.K),
                               size=consumption,
                               replace=True,
                               p=probs)
        for e in eat:
            self.endowment[e] -= 1
        return self

    def update(self, deal):
        """Update production plans in light of this deal"""
        update = self.learning_rate * deal
        self.plan -= update  # pretty sure that should be negative...
        self.plan[self.plan < 0] = 0.01
        return self

    def find_partner(self):
        """Choose another agent unless nobody is close enough."""
        prtnr = self.model.schedule.agents[np.random.randint(self.model.N)]
        if prtnr == self:
            prtnr = self.find_partner()
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


def compare(vect, basis):
    """Compare a vector to some basis. Used to map a deal and an agent's ppf
    to a real number. If that number is positive, it means they come out ahead
    on the deal relative to no ability to trade."""
    out = vect * (basis[0] / basis)
    return out.sum()  # check this.


def main():
    model = Market(2, 2)
    agent1 = model.schedule.agents[0]
    agent2 = model.schedule.agents[1]
    agent1.u_params = np.array([1/2, 1/2])
    agent2.u_params = np.array([1/2, 1/2])
    agent1.ppf = np.array([4, 1])
    agent2.ppf = np.array([1, 4])
    return model


if __name__ == "__main__":
    model = main()

if __name__ == "model":
    simple_model = main()
