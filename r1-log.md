# #100DaysOfCode Log - Round 1 - Rick Weber

The log of my #100DaysOfCode challenge. Started on July 27, 2020.

## Log

### R1D0 - 2020-07-27
This is the official start! I just sent out my public commitment tweet.

So, the next 100 days... There's a million things I *want* to do, but if I don't
focus, I'm going to drive myself nuts. So I'm going to focus on my Comparative
Advantage model.

This project serves three main purposes:

1. I've wanted to make this model for a while. That bit of intrinsic motivation
   will help me build momentum.
2. I plan to present this model at NYSEA. That provides some extrinsic
   motivation for the first half of this project.
3. By building the model in Mesa I'll get more hands on experience with python.
   Despite spending plenty of time using Python, it still feels foreign because
   I haven't built anything substantial in it.

So here's my plan:
Over the next 100 days, I'm going to develop my currently scattered thoughts
into a Python program using the Mesa library. This program will be an agent
based model where agents produce and trade with each other. The intention is to
demonstrate the idea of comparative advantage. Ideally the program should be:
* easy to explain/understand,
* open ended enough that a) I'm not imposing conclusions, and b) novel behavior
  can emerge in an unplanned manner,
* clean enough that I can use something like numba to speed up the model and
  allow it to be scaled up to generate large experiments
* general enough that I can add layers of complexity to it, or use it to
  underlie a different economic model.

For the time being, I'm going to start this project fresh in this git repo. As
it develops enough to stand on its own feet, I'll move it into its own repo.

### R1D1 - 2020-07-27

Okay, I may have mistimed this, but I did two blocks of coding (did some mental
loading earlier which helped) on this project. The public end of things helps!
Feels good to get a like on Twitter from an undergrad friend. 

So here's what I've got (essentially): I'm building out agent level functions to
generate and evaluate trades, engage in production, and calculate utility. It's
not fully functional, but there's actually a decent bit of the core logic in
there. It helps that I've been picking at this problem in an unsystematic way
for the last few weeks.

Two ways I want it to be different: 

First, I want agents to look at several options and I want them to adapt the
parameters of those options based on experience.

Second, I want a network structure that isn't just a random network. I'm
picturing a possibility where some agents specialize in going to various
markets, or where agents do a sort of El Farol type thing where they decide
when/if/how often to go to market. 

In any case, I want the model to allow for certain possibilities, and I'd like
to know something about the probability distribution of those possiblities
emerging. Specifically agents that specialize in trade rather than production. 

I also had a thought about the possibility of time preferences. Currently I'm
modeling exchanges as a vector of positive and negative numbers. If there was
also a vector of positive integers, it could allow parts of a trade to happen at
different times. There will need to be some sort of punishing factor (maybe a
hit to reputational points) to prevent agents from just writing bad checks. But
it could also allow the agents to create financial markets.

Maybe they should evaluate the probability of a trade going through along with
the utility effect that the trade would actually have.

Agents might learn functions to map observables about their trading partner, and
the features of the trade to a probability estimate. I would expect rules to
emerge like "if it's too good to be true..."

In any case, I've got lots of ideas to plug in... tomorrow.

### R1D2 - 2020-07-28

Okay, Tuesday, day Tue. 

Learning about classes to see if I can represent a contract with its own type of object
Come to think of it, I think I'd better stop the timer and do some reading. This
is educational, but I'm not going to count it against my coding time.

Okay, I think I'm getting my contract ("trade") class sorted out.

It's still a bit of a mess. Lots of stuff... too much to properly see it all at
once. Need to sort it all out. Why am I not doing this in org mode? Or is there
some other way to fold code in emacs?

In any case, I struggled to keep myself moving. Not really sure why. Just a
pushing against the resistance sort of day, I guess. I've made my hour, but I'm
going to go back in and at least lay out a map of what I've got and what gaps I
need to fill...


### R1D3 - 2020-07-29

Thought from last night: I've got agents' plans and capacities coded as vectors.
I can compare two agents by looking at their cosine similarity...

Thought from this morning: I should have some sort of tests built in to my code
to make sure it's doing everything correctly. But I still don't have any real
experience with systematic testing... I should read up on that.

Okay, I'm definitely feeling good about the production method. But that's the
easy part. I did figure out folding code in spacemacs which is going to make
life easier... zc zo. But there's still a lot of stuff that I need to straighten
out.

I'm nearly at 200 lines, but a lot of it is comments. Let's lay out a plan..

I need the model and agent classes. I think I also want a contract class.
Agents *should* be able to replicate in a way that allows the population to
adapt. Part of me wonders if I want another class to hold all the agents'
parameters. Then I could create some mutation methods in that class, and allow
parent agents to create new agents with mutated copies of their own parameters.

I should also take the chance to go through the methods and rename things. 

Here's what I've got right now:

- Agent Class
  + init
  + step
  + produce
  + findpartner
  + move
  + rand_trade
  + eval_trade
  + make_trade
  + utility
  + learn

- Market Class
  + init
  + step

- Contract Class
  + init
  + step
  + reverse
  + acceptable
  
So, let's sort this out. Hell, I can delete everything and it should be fine
since I've got a git commit!

So here's what I really want:

Agent:
- produce,
- find a partner (either locally, or in an explicit network)
- move and/or update network connections
- propose a trade (a random trade and/or based on costs/benefits and/or
  parameters that update with experience)
- check current utility
- evaluate a prospective trade relative to not taking that trade (this might
  just be a probability of accepting a good trade, perhaps based on current
  endowment or other things)
- update parameters that bias behaviors

A step of the model should involve agents producing, looking for possible
trades, possibly making an exchange, and updating expectations about prices
(perhaps prices in particular locations)
  
I think my current idea of a contract is pretty okay: two agents, quantities to
be exchanged, and the timing of those exchanges.

I made a new scratch file to hold all the code I'm junking, plus the notes
I left myself as comments. I've started cleaning up the code I actually want in
the model.py file. I've left more holes than when I started, but it's also a bit
cleaner. I've got my hour in, but now I've got to get back to work on other stuff...


### R1D4 - 2020-07-30

Okay, throwing myself back in here! Probably going to face interruptions with
plumbers and work meetings.

Learning about numpy.ma module... masked arrays!

37 minutes in and I'm taking a break... got to get ready to see a plumber and
also try to attend a zoom meeting.

Alright, I got my hour in, but the last bit was writing on post it notes. Time
to add those results into the script and report to Twitter.

Here's the main thing I accomplished on post its: 
self.dU gives the partial derivative of the agent's utility function (assuming
Cobb Douglas form) which means I can have agents try to buy whatever yields the
greatest dU/P.

I'm thinking I'll build out the trade mechanics so an agent tries to buy
whatever they expect will be best per dollar. They can then offer stuff based on
their price vector (using good 0 as the numeraire) and let the partner choose
whatever maximizes utility... or based on their price vector.

Although, I should be concerned about the possibility of buying something with
the intent to resell... maybe they'll have some other layer of parameters to
allow buying for use and buying for resale to emerge. Maybe let them flip a
weighted coin to choose between buying for resale or engaging in more production...

### R1D4 - 2020-07-31

Okay, I've got the dU stuff set up from yesterday, let's go make it useful!

I'm bamboozling myself! Do I have too many moving parts? Let me lay out my
thoughts to clear my head:

A1 approaches A2 and says "hey, item 1 would give me the most utils per dollar!
Are you willing to sell?" And initiates an offer with quantities corresponding
to ...

[you know what... maybe I'm distracting myself with the utility stuff... maybe I
want it, but I don't want it to drive behavior? Or maybe I want it to adjust
over time to reflect what an agent learns from good or bad trades?]

... their own price vector (converted in terms of whatever good A1 is looking to
buy). 

A2 looks at this set of offers ("I give item 1, they return either x_0 of item
0, or x_2 of item 2...") and chooses the offer with the best price compared to
their own prices. Which means what, exactly?
In utility terms, we could just multiply partner.dU by offer.prices and choose
the item with the least impact on utility
In price terms... I guess convert each of them back into the numeraire! Okay, I
think that solves my puzzle. I do need to tidy things up, but let's keep
throwing things at the wall as long as lots of it is sticking.

I'm still dyslexing at this. I'm going to go find some lunch and come back to
this shortly

Here's something to archive in the notes:

#+BEGIN_SRC python

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

#+END_SRC

So, I've built a trade mechanism where two agents trade one good for another
based on a) what the buyer wants for utility maximization, and b) what the
seller thinks about the prices offered.

Since agents will both buy and sell, they'll each tend to maximize their utility
as buyer and evaluate things relative to prices as sellers. I'll have to
convince myself that that's totally okay. But first I need to make sure they're
learning appropriately.

Okay, I've left a bit of a mess, especially in the update_prices() method. But
here's what I've got to do next:

* git commit/push
* delete old comments (if I *really* need them, they're in the old commit!)
* write out a reduced form of the model. See what I can throw out
* build that minimal model in, then...
* make it flexible enough that I can throw more crap in!
* But really, get it to actually run!

So, here's a goal for the next week: get the minimum viable model operating!

### R1D5 - 2020-08-01

Putting down the model because it's the weekend. So instead, I'm watching statquest walk through XGBoost in python

### R1D6 - 2020-08-03

Okay, I stumbled this weekend. Lesson learned: don't leave it till the evening.
On the other hand, summer semester has been pretty exhausting and I needed a
break. Next weekend I'll get in a proper coding session at least one of the days.

So, now it's time to go back into the model. I think I might need to gut it
again. Clean it out as I roll the good stuff into its own refactor...

Alright! I think the script makes a lot more sense now. Got rid of some
duplication, built in some functionality for evolution (I have to finish the
noise adding method, but I can at least average two agents.)

I'm back on a roll!
