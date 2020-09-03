# Libraries
import numpy as np
import pandas as pd
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import BarterAgent


class Market(Model):
    """An economy with N agents and K goods"""
    def __init__(self, N, K):  # , width=1, height=1):
        super().__init__()
        self.N = N  # number of agents
        self.K = K  # number of goods
        self.schedule = RandomActivation(self)
        self.allow_trade = True
        self.history = pd.DataFrame({
            "partner1": [],
            "partner2": [],
            "deal": [],
            "trades": []
        })
        self.trades_undertaken = 0
        poss_trades = [(x, y) for x in range(K) for y in range(K) if x != y]
        self.possible_trades = np.array(poss_trades)
        # create agents
        for i in range(N):
            a = BarterAgent(self.next_id(), self)
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

    def flip_trade(self, trade_idx):
        """
        Given a trade, return the version corresponding to what
        your trading partner experiences.
        e.g. turn 'buy coconuts, sell fish' into 'buy fish, sell coconuts'
        """
        trade = self.possible_trades[trade_idx]
        g0 = trade[0]
        g1 = trade[1]
        newTrade = np.array([g1, g0])
        newTrade_idx = self.possible_trades[newTrade]  # make this work.
        return newTrade_idx


def utility_reporter(agent):
    """How much utility does agent have right now?"""
    return agent.utility()


def specialization_reporter(agent):
    """How much of agent's time is spent on their most popular good?"""
    return agent.prod_plan.max() / agent.prod_plan.sum()


def compare(vect, basis):
    """Compare a vector to some basis. Used to map a deal and an agent's ppf
    to a real number. If that number is positive, it means they come out ahead
    on the deal relative to no ability to trade."""
    out = vect * (basis[0] / basis)
    return out.sum()  # check this.


def main():
    model = Market(2, 2)
    agent0 = model.schedule.agents[0]
    agent1 = model.schedule.agents[1]
    agent0.u_params = np.array([1/2, 1/2])
    agent1.u_params = np.array([1/2, 1/2])
    agent0.ppf = np.array([4, 1])
    agent1.ppf = np.array([1, 4])
    return model


if __name__ == "__main__":
    model = main()

if __name__ == "model":
    simple_model = main()
