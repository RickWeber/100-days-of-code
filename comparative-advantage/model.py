# Libraries
import numpy as np
from market import Market


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
