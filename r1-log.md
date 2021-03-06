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

### R1D7 - 2020-08-04

Okay, the code should document itself, but it's not there. So I'm going to
describe it here, then mush it around in the model file. Remember: the goal is
"minimum viable model" by week's end. And I've got to send an abstract to NYSEA.
But that's later.

Here's the model as it should be:

A market contains N agents
Those agents can produce K goods
Agents differ in their ability and preferences
(Although maybe I want the option to have homogeneous preferences and/or utility)
They have some idea of how many of any one good goes for one unit of good 0
They encounter each other *somehow*
(Eventually I want a path dependent network, a fixed network, and spatial encounters)
For now, they match up randomly
The agent initiating the trade looks to buy one unit of one good
They're buying the good with greatest marginal utility per "dollar"
They offer to give their partner one of the K-1 other goods
The quantities they offer are based on their expectation of prices
(perhaps they should have a modifier... i.e. whether they lowball or highball offers)
So if they're looking to buy one unit of good 0, they're offer their vector of prices
The partner considers an offer vector and compares it to their price vector
The best offer is whichever converts to the most units of good 0 
If the best offer is item they're being asked to sell, they won't
They accept a deal where they sell one good to another agent 
If accepted, the buyer gains one unit of a good and gives up some of another
And the reverse for the seller
They learn something as a result of the (non)exchange
If no trade, buyer increases estimated price of what they wanted to buy
If no trade, seller revises price estimates towards buyer's estimates


(I need an arbitrage function to allow middle man specialization. Not just buying
for consumption, but buying because the agent knows someone's willing to pay more)


(At some point I want agents to shift their allocation of effort between
producing, trading, and searching)
(I'm noticing that there isn't much opportunity for agents to observe their
environment and decide behavior accordingly.)

#### Digression
Okay, I took a second to adjust the utility function so that good 0 is treated
differently than the others. I should look in Varian to see if that's a decent
move. I'm not going to worry about it for now though. But while I was adding
that code I think I noticed something different about python compared to R. 

In order to keep the text editor from complaining about lines being too long, I
had to define a variable that I was going to use once and never again. In R, I'd
want to ls() on the console and see what's there. In my code I'd want to get
rm() stuff I don't need. Is this what garbage collection is about? I'm just
supposed to drop garbage on the floor and trust the interpreter to not get
bogged down with stuff? I'm not going to distract myself with this. I'll learn
the truth at some point, but the thought's worth having before then.

#### Back to it!

Sometimes an agent might want to arbitrage. What does that look like?

get an estimate of the distribution of other agents' price vectors. Start buying
from anyone with especially low prices and hold on to goods with the hope of
selling to people with especially high prices (for any given good).

For this to work, an agent basically needs two or three price vectors. A min,
max, and average. A utility seeking consumer might look at their average vector
to decide what to try to buy. But an arbitraging trader will look to a) find out
what prices people have and b) try to keep items in stock to sell.

#### Actually, let's take a quick break...

Okay, I've had a think and I'm realizing a few things, most importantly, that
the model needs time. 

Agents should decide to either buy with the intent to consume, or buy with the
intent to sell at a higher price later.

This is going to make utility harder. I might have to look through my textbooks
to figure this out. Agents will be asking about their expected utility, and that
can't be as simple as getting utility for everything they own because they might
be planning on selling most of it. 

Maybe I drop the utility() method and just have agents try to maximize how much
numeraire they get.

### R1D7 - 2020-08-04 (next day update)

Big storm yesterday led to a blackout. I did some more work on paper, so I'm
counting the day as a success overall.

### R1D8 - 2020-08-05

Each agent has the following key attributes:
* a PPF (what they're capable of producing)
* a vector or prices (possibly more than one, or a vector of average prices plus
  a vector of variance of prices)
* a buy/sell plan vector
i.e. for each product, what is the probability the agent goes out to try to buy
it (in order to consume), or that they intend to buy or produce it in order to
sell to someone else.

Here's a simple step() function:
Choose a good. If the plan is to sell that good, then find a trading partner and
either buy from them (if their price is low enough) or sell to them (if their
price is high enough)
If the plan is to buy the good, then make them an offer and let them decide
which good they'll accept in exchange (based on their price vector)
Then update the plan (the buy/sell vector, price info, etc.)

I'll come back to this later. Or maybe I'll push the rest of today's work to
tomorrow. We'll see how I feel after class. 

### R1D8 - 2020-08-05 part 2

My brain just isn't wanting this right now. But I've got to do something, so I'm
going to do the next coding item on today's todo list: I'm going to follow along
with someone's TidyTuesday R broadcast. Less time on python, less time on this
project, but a chance to reset my brain a little bit.

### R1D9 - 2020-08-06 

Okay, I've been throwing stuff at the wall to see what sticks, but now I've got
a mess, so I'm backing up what I've got and starting from scratch(ish) again. 

I think I want agents to have some idea of average prices, but also some idea of
variation in prices (i.e. is it worth while to buy from someone with extra low
prices?) So I'm going to learn about incremental algorithms for calculating variance.

Okay, I've found a useful wikipedia page: https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Weighted_incremental_algorithm

I think I'll need to fix it to use numpy, but I can do that later.

### R1D9 - 2020-08-06

I'm over-complicating the model. At least as of right now. Tomorrow I'll
simplify. Forget about all this price stuff. Let the trades be two randomly
selected goods, and let the quantities be proportional to each agent's
capabilities, then update production plans in the direction of what the agent
successfully sells. It means no arbitrageurs, but it means a simple model that
works. I can layer on complexity later.

### R1D10 - 2020-08-07

Alright, I just reduced model.py from 280 lines to 80. "Works" is maybe too
strong a word, but I'm actually pulling the code into the REPL, so it's a whole
lot better than what I had at the start of the week!

### R1D11 - 2020-08-08

As long as everyone's PPF sums to the same number, I should be able to induce
gains from specialization by making the default trade be one day's productivity
from one agent for one day's productivity form the other. Although, I'm not sure
how to update agent behavior in that case... Not without making a lot more
complexity. 

Okay, here's what I've done today (might do more later):
created two trade methods: the random trade I had built into trade() and a trade
of one day's work in either direction. Those are called after finding a partner.
The code is at least a bit more modular now. 

I've also got a method to increment the production plan, but it's not really
saving much. I wonder if I should make it take the trading partner as input,
calculate tradeoffs, then update both agents appropriately. That could make it
useful for the day_trade method. 

The model is simple right now, but it should basically work. What I need to do
next is figure out the data collector.

### R1D12 - 2020-08-10

Took Sunday off. I think I'll let that be the norm. It's good to have a head
clearing day.

Alright, I've got a couple plan updating methods. I'm assuming that agents want
to maximize the sum of squared production. For the individual plan update (when
there's no trade to be had), choose one good at random, and see what happens to
the utility function (which is just the dot product of production). 
I'm going to rename that method utility to avoid confusion later on.

Alright, I've got a slightly wonky implementation set up. It's just about ready
to take for a spin! But first let me wrap my head around what I've got:

A market with N agents and K goods and some size.
Agents produce some of the goods, possibly move, then attempt to trade.
If they don't trade successfully, they increase their chance of moving, then
either move or produce again--but only a fraction of a day's production.

That's a bit more complexity than necessary, but it shouldn't mess things up too
much right now. And later on I can make it tuneable.

My produce and move methods seem fine (though I don't know how well move() will
work in a 1 pixel world).

I think my day_trade() method forces their hand. I should give agents an out if
they don't gain from trade. But I can do that later.

I also think agents will end up with infinite quantities of each good as it
currently stands.

I've been struggling against a list comprehension that doesn't want to sum.
Ultimately I just (for now) put in a for loop. Got through that. Sorted some
other bugs. And I've got something that will (basically) run!

It's not there yet, but it's doing something. Plan for tomorrow: write up the
abstract and start outlining the paper.

### R1D13 - 2020-08-11

I'm simplifying my methods, but things are a bit of a mess at the moment. I'm
also not sure if I like using a dictionary to hold deal information. Maybe I'll
fix that tomorrow.

In any case, here's what I've got:

First, a simpler step method. Produce, move (probably... that's just to make it
easier to avoid moving in a 1 pixel world), then trade (unless the model forbids
it)

If there's no trade, agents update production plans to enhance their utility.

If there is trade, they look for a partner, propose a deal (either one day of my
work for one day of yours, or one unit of a random item for some of another
item, based on the initiating agent's ppf).

If both agents are okay with the deal, they make the trade. Otherwise, they
consider if producing more of some item would increase their utility.

#### Things to look out for/fix:
Make sure I don't end up with infinite units of all goods.

Make sure that when we evaluate possible changes, we aren't changing
plans/endowments/whatever without changing it back when necessary

Built in some reporters for running experiments.

### R1D14 - 2020-08-12

I think I want to look at the trade evaluation method more closely. Perhaps
what's needed is for the agent to convert everything into terms of the
numeraire. For the random_trade, the method seems fine. For a trade of A for B,
compare that to the slope of my PPF between those dimensions. But for a trade
with more than two goods, converting everything to the numeraire might be a
better solution than the utility function. I'd prefer not to have that utility
function do too much heavy lifting

I do want to set things up to allow for time to matter; bringing the discount
rate in to let agents think about the future more carefully. But I should
probably leave that for the time being. 

Okay, I'm getting trade evaluation in terms of the numeraire good instead of
utility. I'll leave the utility reporter, particularly for the anarkic agents
that might turn out to exist. But trades are evaluated in terms of tradeoffs.
For now. In the future I'll generalize to allow agents to compare a deal's terms
to some price vector (perhaps one returned by some other function) rather than
just the agent's own PPF.

I also need to tune the amount of trading happening relative to production. But
I'm probably getting ahead of myself. 

In any case, I continue the process of both adding and reducing entropy in the
script. Tomorrow might need to be a slash and burn day.

I'm also getting a bit ahead of myself here, but just to put it down, I made a
little function to make good 0 into a fixed resource with no use value. It would
mess up evaluation functions, but the model as a whole could be reworked to
allow trade with money using this sort of functionality.

### R1D15 - 2020-08-13

In an effort to simplify, I've rebuilt the agent class. Most importantly, I went
back to thinking of a trade as a vector of positive and negative numbers. I'll
use integers just to shrink the search space.

I reduced the agent class from 20 methods to just 9. It's a lot easier to read
now, and it saved 100 lines of code.

### R1D16 - 2020-08-14 

Definitely a few steps closer. Tried to actually get the model running,
unsuccessfully. Looks like syntax issues that mean digging into documentation
more. Fair enough; it had to happen some time.

I'm 80% sure I've got the money_model() thing figured out. Just update each
agent's list of possible trades so their trades are either positive for the 0th
item and negative for the rest or the other way around. That's an upside of
giving each agent an exogenous list of possible trades. It's sort of silly, but
it does make this somewhat easier. What I need is a way for the set of
conceivable trades to update over time. Maybe that's where the GA element will
come in. Each generation gets better at specializing their production and across
generations they get better at trading. 

### R1D16 - 2020-08-25 

Okay, summer vacation is officially over and I've got to get back in to this. 

Let me start by dumping some ideas out:

What I *really* want to make is a super general model of agents interacting to
create their own emergently ordered political-economic system. But that's too
big for right now. But thinking about such a model makes me think I like the
idea of having a contract object. Something that takes a set of agents, some
notion of time (i.e. as a sequence of actions and payoffs), and maps agent
actions to outcomes. In the comparative advantage case, that's going to mean
some agents decide to part with some of their endowments in order to get some
part of the other agents' contributions.

Okay, I built a class and a function to create a null contract. I should update
the agent definition so their list of random trades works with these contracts
(maybe with some sort of placeholder)... Basically I'm defining a contract as a
list of agents and some set of exchange vectors for each agent. Eventually I
could think of those vectors as matrices involving different commitments at
different points in time. 

The current build (should I just back it up and start from scratch again? Might
be best to avoid confusing myself after taking a couple weeks off) gives each
agent a list of predetermined exchanges. I'm going to comment out what's there
and replace it with something using my contract 

... on the other hand... what I left behind is simpler than what I'm thinking of
right now. It's only one on one exchange, but I should get that running before I
add more features. 

Okay, I've got to actually read through the code I've currently got.

I've got a market object that has some space, N agents, K goods, and a history
that updates over time. Each agent will get some defined number of trades.

The agents produce, trade, consume, move, and update their plans based on
previous outcomes. The list of possible trades each agent has is fixed, meaning
I've either got to find a way to mutate those trades over time, or create and
mutate duplicate agents.

Each round, they produce some amount (which I can modify if necessary, e.g. make
them produce 10 days worth of output at a time). Agents with enough to sell will
attempt to make a trade. Then each turtle consumes and moves. 

Production is straight forward: just cross multiply production plans by
production capabilities and add that vector to their endowment.

Trading starts by approaching a partner. Then choose one of your pre-determined
trades (chosen by a weighted probability based on past success). That trade will
be a vector of numbers on the interval [-1,1] which will correspond with ...
Scratch that! The numbers are random integers on [-3,3] which should correspond
fairly well with the productive capacity of agents. There will be some balancing
to make sure that the probability of a good deal corresponds with general
productivity... i.e. if a good trade is very unlikely, trade will only determine
something like 0.000001 of their overall wealth. And if a good trade is super
likely, they might end up with negative endowments as they sell goods they don't
have. 

So a trade says "I'll give you x, y, and z if you give me a, b, and c," and each
agent considers how that trade compares with autarky... eventually I want them
to form expectations about prices, but for now it's good enough that they just
compare to their own productivity. If the trade isn't mutually beneficial,
nothing happens.

When it comes time to consume, they look at their cobb douglas utility function
and consume integer quantities from their endowment (never consuming something
they don't have) drawn with utility-weighted probability.

The movement functionality is a bit unnecessary right now. I want to have some
movement at some point (and let them navigate a tradeoff between exploring the
world and staying in one place to produce more). But I'm going to ignore it for
now. 

A good trade will lead to production plans moving in the direction of
comparative advantage implied by that trade. i.e. make less of the things I buy
and more of the things I sell. A good trade also becomes more likely to be tried
again in the future (e.g. with other agents.)

Essentially I've got agents learning what sorts of trades to make, and what to produce.

Okay, I feel pretty good with what I've got. I see lots of ways forward, but
none I *need* to make now. I think what I've got to do is get it running and
spitting out data.

### R1D17 - 2020-08-26 

Alright, I want to put in a main() function...

I've done some tidying in the model. Made at least one section of 3 lines into
just 1 line. It's back down to 180 lines of code, and I think it's pretty much
just what I need left in there. I've been getting errors on the repl though.
It's having trouble with something calling len() which I think I've eliminated.
But It's still showing up. I'll restart the REPL and try again tomorrow. But now
it's time to take Lola to the store. 

### R1D18 - 2020-08-27 

Just got out of class. In office hours now. We'll see how well I can stream and
code at the same time.

Okay, I'm getting new errors! That means I'm solving the old ones. I'm looking
at the agents' list of possible trades and realizing a) I'm getting a lot of
trades where all elements are negative, and b) I could probably just create a
list of all possible trades rather than randomizing. At least for small values
of K. 

### R1D19 - 2020-08-28

Having a hard time pulling myself into the work. But I'm going to at least show
up and make an entry. Inch by inch I'll at least establish showing up then build
on that. 

So I imported the model, and the error it gave me on mod.step() was from the
consume() method. Here's what I want: consume integer quantities of goods where
the probability of consuming one at any given time is weighted by their marginal
impact on the agents' utility. 

I'm not totally on board with saying "consume x units" now that I think of it
though. But whatever. Right now it's a constant amount that's the same for all
agents so it should be fine. I can think about that problem later. 

Okay, I'm fixing the problem with np.random.choice not liking my use of range().
It feels like it should work, but maybe I need to use pandas too? This
particular block of code would be much easier in R. But I'll make do with a
hacky solution for the time being. A loop over a range to turn it into a list.
There should be a better way. But I don't need it right now.

Here's where I'm stuck...
Around line 131, I'm looking at an agent's endowment ...
never mind. I think I fixed it!

And I got an idea for introducing time into the model... an agent could forgo
consumption now and get discounted utility from a future round by having us
redefine their utility method to be 0.95 of its former self. I'm not sure if
that would be a useful way to go about it. There's probably a simpler method.
But, just by starting to write about my problem I saw the solution and
apparently fixed it. 

Never mind. It's still broken.

Here's what I'm after: make sure the agent has enough to consume in their
endowment, then subtract goods from their endowment. I'm having trouble with
converting the endowment vector, apparently. 

I keep throwing myself at this and I keep coming up short. I'll have to pick at
it later with the python documentation at hand. 


### R1D20 - 2020-08-31

Did I miss the whole weekend? I'm going to have to figure out a schedule that
works this semester.

Alright, last time I was able to create an instance of the model in the REPL but
was having problems stepping the model forward. Let me start by writing some
convenience functions.

caught a bug in the produce() method. Uncaught it would have meant more and more
production over time. But for some reason it's not importing properly... I'll
have to check this later.

### R1D21 - 2020-09-01

I'm going to split up the model.py file. I'm looking at the mesa example for the
wolf sheep model and they do it that way. I think that'll make it easier to organize.

Okay, I'm rebuilding the BarterAgent class and tearing things up.

I'm going to leave it in a bit of a mess while I get ready for class. I'll have
to read through it and explain everything that's there later on.

### R1D22 - 2020-09-02

Current status:

I've got two scripts I'm working on (and I really should put some of the other
stuff, like helper functions, into another script... but I'm not going to do
that yet): agents.py and model.py.

Model sets up the market class and some of the helper functions. Agents sets up
the BarterAgent class


The market holds on to a list of all possible two good trades (e.g. fish for
coconuts, beer for pizza, pizza for beer, etc.). 
Agents learn which trades work well for them (e.g. no point in buying fish if
you have comparative advantage in fish).
In evaluating any given trade, agents know what the maximum price per unit is
based on their ppf.

Went through most of the code. 

To check on next:
* around line 89 of agents.py and updating agents' plans.

### R1D23 - 2020-09-03

Okay, the thing to worry about right now is updating plans. But let me start by
learning a bit more about pandas. 

Okay, I like the look of pandas. I should use it to hold onto the trades
variable that's local to the trade() method. 

I also need to flip the direction of trades when updating the partner's history.
I've got histories stored at agent and market levels in pandas dataframes. I
like that. It will make it easier to limit memory and also to calculate things
from the memory. I should build explicit methods for having agents access the
market's history, maybe let them sample from the history to form imperfect
expectations about prices. But not today. Today I just want to make sure I'm
updating histories correctly. Then I've got to make sure the model runs.

### R1D24 - 2020-09-04

I've tidied up some code and got agents and market taking better advantage of
pandas. I'm also wrapping my head around pandas... it's sort of like the
tidyverse but without piping. Or, I guess, piping takes the form of tacking
methods on to a statement.

I think I've got agents.py where I want it. I've got to get it spitting out data
and make sure it operates, but I can do that another time. I'm pretty happy with
what I've got right now. I'll have to double check line 143 almost certainly.
But otherwise I should have a viable model with agents moving towards their
comparative advantage when they trade and getting more utility out of the deal

### R1D25 - 2020-09-08

Fell off the wagon for labor day weekend. Let's get back to it...

I think it's time to create a separate repository for the project. This repo
will hold old versions plus this journal, but a) I want to share the model
separately from 100 Days pretty soon, and b) I should probably just retype the
whole thing to wrap my head around it again.

Alright, did a lot of copying which allowed a decent amount of tidying up. I
should really order a copy of Pragmatic Programmer and get a better idea of how
to do this stuff. In any case, I put in the time for the day! So that's a win. 


### R1D26 - 2020-09-09

Okay, I've built in some functionality for reproduction and mutation. What I've
really got to do is figure out how to put the whole thing together in a way
that's easy to let it run and see what data it spits out.

### R1D27 - 2020-09-10

Finally pulling the code into the REPL and finding problems with my pandas work.
Ugh. I'd better go get more coffee.

I've been bashing my head against this to no avail. It keeps having a problem
with initiating agents. Maybe I'll root around with the REPL open and rebuild
this afternoon.

### R1D27 - 2020-09-11

Opened it up, got distracted, felt overwhelmed, and walked away. But since I'm
here now, let me set myself up for success next time...

I think I've got to strip it down to the bare essentials. Start with a blank
file and build in the minimal mechanics of this model.

### R1D28 - 2020-09-12

Okay, at least for now I've copied all my code into working_file.py. That should
reduce my confusion with imports. I've done a bit of fiddling, but mostly I'm
just setting it up for now. Time to go get some breakfast first.

### R1D29 - 2020-09-14

Tidying up some code. From now on, history will be stored by the Market and
Agents will look it up instead of keeping their own record.

Part of me wants to make exchanges their own class, but it's probably too early.

### R1D30 - 2020-09-16

Back on the wagon! The conference is happening soon so I've got to get this
running ASAP so I can put together a presentation.

Finally solved that pd renaming problem! It turns out '0' != 0

At some point recently I was thinking about price vectors and updating them by
exponential moving average.... Just want to record that somewhere....

I'm cleaning up a bunch of pandas stuff. Getting more comfortable. I'm realizing
how much I've been spoiled by R's dataframes and tibbles.

In any case, I got some work done, cleaned some stuff up, and it should be that
much closer to functioning when I get back to it.

### R1D31 - 2020-09-18

Another missed day. I've got to make it a priority to get on this in the
mornings. Especially while I've got this deadline looming. 

Okay, I'm taking yet another swing at simplifying. What I've got to figure out
is the utility thing. I've got to clear their endowment out every once in a
while. Not every tick, but maybe every 10 (or 100). What I really want to do is
have them report utility so I can watch the distribution move right as they
refine their production plans in the direction of their comparative advantage.

Stuff I need TODO:
* double check this delta = give/take stuff
   * as it is it sort of pushes them in the direction of CA, which is probably
     fine for now. But I sort of feel like it's assuming the outcome. 
     * Perhaps I need a) the possibility of eliminating trade or updating
       production plans, or b) a different way to mutate behavior.

In any case, I feel surprisingly good about this.

### R1D32 - 2020-09-19

Keeping the streak alive!

Looking around line 30, I've got two agents trading a day's production, but
there's no guarantee that both partners gain from trade. The midpoint of the ppf
should do the trick if all agents' ppfs sum to the same production level.
Preferences might make some goods more valuable, but it's otherwise fine. 

So I could do (at least) two things:

1. Compare a model where they blindly trade to one where they blindly don't.
2. Let agents veto trades and expect longer convergence to the efficient outcome.

I also still haven't built a way for non-trading agents to update production
based on their utility function alone.

In any case, what I really want to do for updating production isn't give/take.
It's give minus take! That alone makes this a successful coding session even if
it's a short one.

Also, I forgot to have the mkt class create the agents!


### R1D33 - 2020-09-21
Okay, I at least touched the code. I updated the doc string for the trade
method. Right now I'm just going to have them trade a day's production for a
day's production. There's no guarantee that it's mutually beneficial, but the
expected value of each agent's PPF is a vector of the same magnitude so it
should be fine for now. I can make the model more complex in the future.

### R1D34 - 2020-09-23
I'm touching the code. Can't promise much more than that, but I've got to have
some sort of forward momentum.

At the very least, I made learning rate an agent variable. 

### R1D35 - 2020-09-24

Okay, I'm doing a Pandas course on Datacamp. 

The current version doesn't have a history. Do I want to build that back in? I
think I've got a good enough sense of Pandas to get it in pretty smoothly. 


### R1D36 - 2020-09-25

Alright, I'm trying to pull this into the repl but I'm getting a weird error. In
the model init it's saying "arry() missing required argument 'object' (pos 1)"
when I run the easy_model() function to create a simple 2x2.

In [43]: mod = M.easy_model()
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-43-a8e222e1911e> in <module>
----> 1 mod = M.easy_model()

~/Programs/comparative_advantage/working_file.py in easy_model()

~/Programs/comparative_advantage/working_file.py in __init__(self, N, K)
    143 #     out = vect * (basis[0] / basis)
    144 #     return out.sum()  # check this.
--> 145 
    146 
    147 def easy_model():

~/Programs/comparative_advantage/working_file.py in __init__(self, unique_id, model)

TypeError: array() missing required argument 'object' (pos 1)

In [44]: 

The relevant init is way up on line 16. So why is it missing something? I
deleted some functions that I don't need. Now it's not giving a line, but it
looks like the problem is in the agent class. I'm not seeing anything wrong with
any of my np calls.

I think I should go back and work through a mesa tutorial...


### R1D37 - 2020-09-26

Playing around with the idea of creating an explicit class for exchanges. The
simplest type of exchange is just a transfer of a vector of goods from one agent
to another. An exchange is just two of these with the partners changing places
between each transfer. 

I can use an exchange class method to make a random exchange or do an exchange
that's in the model's history.

``` python
class transfer(exchange):
    def __init__(self, sender, recipient, goods)
        super().__init__()
        self.model = sender.model
        self.sender = sender
        self.recipient = recipient
        self.goods = goods
        
    def undertake(self):
        self.recipient.endowment += self.goods
        self.sender.endowment -= self.goods

class exchange():
    def __init__(self, p1, p2, g1, g2, model):
        self.p1 = p1
        self.p2 = p2
        self.g1 = g1
        self.g2 = g2
        self.model = model
    
    def rand_exchange(self):
        if self.model.money:
            goods1 = np.zeros(self.model.K)
            goods1[0] = 1
            goods2 = np.random.choice(range(1,self.model.K))
        else:
            goods1 = self.random_goods()
            goods2 = self.random_goods()
        return exchange(p1, p2, goods1, goods2, self.model)
    
    def null_exchange(self, p1, p2)
    
class ant():
...
    def rand_historical_trade(self, own=True):
        history = self.model.history
        if own:
            keep = history["p1"] == self or history["p2"] == self
            history = history[keep]
        return np.random.choice(history)
...
```

There's some tidying to do in there, but basically the class would be a place to
create and undertake exchanges. By building together transfers I can make
exchanges of arbitrary complexity. I could even have agents ask other agents to
make transfers to third agents (or from?)

### R1D38 - 2020-09-28

I think I did a bit yesterday, but whatever. No record, I'll treat today as the
next day.

So I've finally got it in the repl. I think I've got the model basically where I
want it. I want to add visualization for the conference (and to make it easy to
start and re-run while displaying data). But right now I'm running into casting
problems with np.

Pretty good coding day. I've got it where I want it right now. I can make it
more complicated later. But right now I need plain vanilla in time to make the
presentation. 


From tutorial: 


chart = ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
                    Do for specialization and endowment

server = ModularServer(MoneyModel,
                       [grid, chart],
                       "Money Model",
                       {"N":100, "width":10, "height":10})


### R1D39 - 2020-09-29
Mostly worked through the Mesa Tutorial. I think I've got to think about ripping
off the Schelling code as a basic framework to cram my model in. 

### R1D40 - 2020-09-30
Didn't do much, but I at least touched the project

### R1D41 - 2020-10-01
Not much time left. I've got to build in visualization and generate some results

I just had the idea! How to make the exchange class more generalizable...

Let's say we have an exchange between 3 agents. Each agent has to declare what
it gives to each of the other two agents. Maybe it would be simpler if they also
had a null vector of goods to "give" to themselves. 

In any case, that can wait.

Update: I've got the model running in the browser! It's not really doing
anything yet, but I've got a switch and a couple sliders. The plots are there
but not generating the appropriate output.

I'd like the visualization of the agents to show something besides random
movement. But more important is getting these plots to update with useful
values. But first I'm going to have something to eat.

Okay, I see what's wrong. The charts are pulling an agent level item, but I
probably need to specify which agent. Bigger problem: running with and without
trade for 30 rounds I've got higher utility without trade than with trade. 

Okay, let's really go eat now.

### R1D42 - 2020-10-02

Decided to move my work into netlogo for now. It's just faster for ABM
prototyping. And it's a lot of fun! Mostly that's just my own fluency, but
still. I'll get some ideas sorted in NetLogo, get it spitting out results, then
bring that back into the python version next week

### R1D43-44 - 2020-10-04

Presented the model in NetLogo. I've got to get the utility stuff sorted out
because it's been returning higher average scores with trade disallowed. Also,
there are some things that aren't right, like the max_u production planning
which implicitly assumes equal prices... although, statisitically speaking that
is the expected value of the equilibrium prices. As N -> infinity, it would
actually be the utility maximizing allocation.

Though now that I think of it now, what I really want the turtles to be doing is
trying to *get* a split of goods based on u_params, whether by production or
purchase. So they need some expectation of their own production, and the net
impact of their trading plan. So a turtle making a lot of good 0, but also
selling a lot of good 0 needs to predict that they'll be able to use the
proceeds to buy the appropriate amounts of the other goods.

I've just put in some framework for turtles to have a set of strategies they run
through a GA. I don't know exactly what they're going to look like, but it
should involve setting expectations about what they'll make and what they'll
buy/sell. I might want more than one learning function in each agent.

I watched this video yesterday: https://www.youtube.com/watch?feature=youtu.be&v=MacVqujSXWE&app=desktop
And I want to remember to revisit those ideas as I sort out GAs in my model.
Also, I should look at the El Farol code a few more times.

### R1D45 - 2020-10-05

Have I considered dropping production? The POW camp economy had regular inputs,
but essentially no real production. I could do something like that and have a
variant of the model where 

### R1D46 2020-10-13

Lost a week. The code is a bit of a mess because I dropped lots of stuff in
without getting it functional. Time for a refactor.

Here's a thought... since the links are already holding on to trade histories
and strength parameters, why not let them hold on to a default trade between two
agents? I don't need to keep the whole history. I can just have it start with
some sensible trade and have it update in the direction of comparative
advantage. 

What I really want the machine to learn is a mapping from any given internal
state to the appropriate link to activate (to buy what they need or sell what
they've got too much of, or whatever.)

I've commented out most of the code (I'm keeping some of it, because some of it
is good!). But I'm mostly building this thing back up from scratch. I'm thinking
of the links as holding a vector of units (including direction of trade). Each
trading round we'll choose between that and a mutation.

As I'm working in NetLogo I'm simultaneously realizing how nice an IDE NetLogo
is (as far as checking code, for sure), and how much I like vim keybindings that
actually work. Rstudio's vim keybindings are more infuriating than just not
using them. Maybe. They're crappy, anyways. I just want real vim in Rstudio. 

Alright, it's been a bit of a scattered day, but I'm feeling good with the
project in NetLogo. What I've got to do at this point is improve the production
update functionality. Right now turtles change their production plans in the
direction of the deal they just undertook. 

I should also have them check to see if a trade is good for both agents.

### R1D47 2020-10-14

I have at least touched this project! I think i did fiddle with the learning
rate a little earlier on. If it's too high, some turtles lose utility. 
 
I'm also putting in a placeholder for solo updating. Turtles will have to update
their production plans in the direction of what maximizes their utility.

Will reading this help me clarify my program?
https://www.analyticsvidhya.com/blog/2017/01/introduction-to-reinforcement-learning-implementation/

### R1D48 2020-10-15

Okay, the solo_update procedure is sort of funny. I've got to figure out how to
give an agent the chance to try on a strategy and only adopt it if they like the
looks of it. 

I've set that up to hatch copies of a turtle, mutate one of them, compare their
utility, then compare their utility before killing them both. The original
turtle updates its production plan if the mutant got more utility.

Well, whatever I've done, it's broken the model. It works, but they're not
moving towards comparative advantage.

### R1D49 2020-10-17

Touching the project.

Okay, let's look through what I've got. 

The go loop has turtles producing, trading, updating parameter values, consuming
(eventually), checking to make sure production plans are all positive values,
then recoloring links. Not bad. 

I've got to check on the trade-update process, and the no-trade-update process. 

Undertaking trades and producing look fine. 

I might modify the mutation procedure so it only ever adds. That will mean less
impact of mutations over time. I still also would like to try cross over and
setting up a GA among the agents.

Okay, let's do something concrete... I'm going to make a strictly positive
mutation function.

Alright, that was actually sort of easy.

Now I've done a bit of organizing. That should make it easier to update the code
in the future. It's still a bit of a mess, but it's less of a mess.

### R1D50 2020-10-18 
 
 Poked around a bit today. It's sort of messy. I'll have to do some serious
 refactoring this week.

### R1D51 2020-10-22

It's been hard to get to this at all. And I've got a headache. But I literally
got rid of one typo, so I can't say I've done nothing today. Or this week.

Also added a point mutation reporter

### R1D52 2020-10-23

Alright, let's poke around...

The current version has trade data held in the links. Between any two turtles
there's basically one possible trade, but it will update over time. I could do
an in link and an out link, but that seems unnecessarily complicated.

### R1D53-54 2020-10-23 and 24

Didn't work on this project, but I did poke around an R problem:
http://www.rosettacode.org/wiki/15_Puzzle_Game
Implementing that in R.


### R1D55 2020-10-28

Oof, it's obviously mid semester because I'm missing a bunch of days. 

Let's get into the model. It looks like I've been working on the trade
procedure. It's pulling a default trade out of the link between two turtles. But
I also want to check some random stuff. 

Maybe I'll make a probabilistic mutation...

Okay, I've got mutations happening with decreasing probability over time. And
I've got a reporter that gives an agent's best option out of a set of possible
trades.

There's still a lot to sort out, but I'm moving forward!

Current problem: sometimes the `undertake` procedure is getting an incomplete
list. It must have something to do with the `cross_over_mutation` procedure


### R1D56 2020-10-29

I'm off track, but at least I'm coding. Did some register machine stuff this
morning and some netlogo stuff this afternoon. Followed by more netlogo and more rodrego.

### R1D57 2020-10-30

dang, we should get some halloween candy! 

I didn't really do much coding, but I did help a student with R. So I'm counting
that as a day. It's better than nothing.

### R1D58 2020-11-03

It's been a while! Let's see what's here... 

Well, if I get nothing else done today, at least I got rid of a line of code
that didn't do anything. 

Also set it up so agents have limited connectivity and find_partner only returns
links turtles. So that's good.

Fixed a bug in my cross_over_mutation function!

Big thing I'm missing: I'm not ensuring trades are mutually beneficial. 

I've got reporters to generate random deals. And I can have agents evaluate
those random deals. I'm trying to make a set of options then filter them down
those that are beneficial for both partners. But it keeps spitting out trades
that couldn't be mutually beneficial (e.g. trades where one agent gives a bunch
of stuff to the other agent).

Now that I think of it, I eliminated the direction of the links and I think that
was a mistake. A deal should make sense one way, but direction shouldn't depend
on which turtle initiates the trade. Each should initiate their own deal.

Okay, I think I fixed the directionality. I still have the issue of choosing a
set of mutually beneficial deals. And the more pressing problem of getting
empty partners in the trading process. 

### R1D59 2020-11-04
Did an R day. Rvest is super cool for webscraping! I won't write too much here
because when I get back I want to make sure I read yesterday's notes on the CA model.

### R1D60 2020-11-05
What's going on now...

I've got to make sure trades are mutually beneficial. And whatever is causing
trades with nobody as a partner.

I've at least touched the code though. 

Even better, I'm building evaluate_deal to not depend on who is asking for the
evaluation. But it's only going to work if there's a link. So evaluating
possible deals is going to require some extra work.

I'll look at it more closely tomorrow. This morning I put together an R script
to pull data from the Predictit API. I've got to figure out how to get it
running as a cronjob. Apparently it's not as straight forward as I'd expected.

### R1D61 2020-11-06

I think I sorted out the cronjob. Or maybe I haven't...

### R1D62 2020-11-09

It was a big R day. I spent the whole day prepping for class, then doing a class
walking through a tutorial with `rvest` to scrape from Wikipedia.

After class I spent some time poking at the code trying to make it faster. I
don't think I was successful. But leaving it running for 4 hours got me a 45000
page data set. 

What are the most connected pages?

Classical Hollywood Cinema (degree 3614)
Catholic, Roman Catholic, Roman Catholic Church, and Catholics (all 3383)
List of Statistical Topics, List of Statistics Articles, List of Statistics
Topics (2806)
Nitrous Oxide (2733)
Metabolism (2717)
New York City
Russia
Invited Address at the International Congress of Mathematicians
List of LGBT related films
Europe
Italy
List of University of Cambridge People
David Hume

### R1D63 2020-11-13

Busy week! But I've at least touched the code!

Looks like my last thing was to sort out evaluating if a trade is mutually beneficial.

I put in some kind of crappy code that might could do the trick. And introduced
some new errors. And I should really sort them out. But there would be too much
to load into my brain and I'm not really ready to focus right now. But here's
what I've got to figure out:

1. A generic method to encapsulate a multi-agent exchange 
2. A way to loop through the agents in such an exchange and ask each one of them
   if the trade is at least better than no possibility of trade.
   
Beyond that I can build in some degree of strategery. But I also think it's a
tad too complicated right now. This might be a good time to gut it entire and
start again from scratch. 


### R1D64 2020-11-15

Did some R stuff. Working on an assignment for tomorrow. Playing around with
tidygraph. But the dataset I'm working on is just enormous, so it's taking
forever. I should use a restricted dataset, but it's in the middle of a bunch of
calculations and I think I should just let it run overnight. 

### R1D65 2020-11-16

It failed! I didn't have the right libraries loaded and it decided not to fail
until the very end. I'm also coming to realize that the random walk centrality
measure takes forever to run.

### R1D66 2020-11-17

Just spent some time streaming my streamlining of the wikipedia code. It still
takes a lot of time to run through. It's downloading thousands (millions) of
pages and stripping them for links. I've got an iteration of it running that
will go through 5 levels. Starting from graph theory, then anything linked to by
that, anything linked to by those, etc. There are only 6 million articles, so I
guess that's the limit. I wonder if I might accidentally get the whole link
structure of English wikipedia? We'll see, I guess.

### R1D67 2020-11-18

Didn't get much done. Tweaked the R code which failed last night. It's been
running for a few hours. Fingers crossed.

### R1D68 2020-11-19

A slow morning, but an important skill: error exceptions in R. Hopefully that's
what's necessary to get my R wiki network data working properly. I looked at
yesterday's progress and it gets a 404 error before giving me back nothing at
all. So now it's going to try getting links and if it fails return an empty
vector. It's running now, hopefully by tomorrow I'll have some results!

Alright, coming back to it in the afternoon I'm making some progress. I'm
getting category data. It's going to take a ton of extra space. But whatever.
It's fine for now. I've set it up to download a bunch, save a csv, and start
randomly from one of the pages in the last bunch of data.

One chunk of data I pulled has 113,243 links across 2,244 categories. Most
popular category: "Articles with short description"

### R1D69 2020-11-20

I just can't put this wikipedia project down. I'm currently figuring out
downloading the whole encyclopedia through dumps.wikipedia.org. There's plenty
of interesting looking stuff including page views. I'm going to start with the
links. It looks like I can get links and categories and have already set up an R
filter to get them out of the latest data folder. 

Jeez, just the categorylinks file is 2.9GB compressed. I'd better be careful not
to crash my computer (more than necessary). 

They downloaded. 6.6GB of pagelinks and 2.8GB of category links. Now I've got to
figure out how to connect a database. Hopefully tidygraph works with dbplyr.

### R1D70 2020-11-21

Well, I'm unzipping these databases and so far the 2.9 GB file expanded to 21
GB. So this is going to take a ton of memory. I wonder if I can access the
compressed file without decompressing it? I guess that would have to hurt
performance though.

The pagelinks are about to pass 20 GB, still decompressing. That should go up to
60ish, right? 

Well, at least I learned a) the command to extract gzips (`gzip -l *.gz`), and
b) how to run a command from R (`system2(cmd)`).

Okay, it's *only* 49 GB! I'm following a stack overflow question and reading in
the sql file as text and fixing some comment lines. 

hmmm.... what I need to do is recover a mysql dump. That might be best done
outside of R. And of course I've got some problem in my apt settings that's
getting in the way. 

Found this tool. if I'm lucky, this will take the text file that I've got, and
put it into a database I can get into with DBI.
https://github.com/dumblob/mysql2sqlite

### R1D71 2020-11-23

It's not code, but it's relevant: Today I'm learning about databases. I'm 80%
sure I already knew that there were database programs optimized for reading
("OLAP"/Analytical), and others optimized for writing ("OLTP"/transactional).
But I'm noticing a weird shift in my attitude to databases. I remember a million
years ago looking at a CS curriculum, seeing the section on databases and
thinking "well that sounds boring". But now I know enough to realize that data
storage is far from trivial. Maybe it's that at 33 I have acquired more
information ("learned") than I can hold in my head at one time without
assistance. Or at least it's more obvious than it was when I was 25 or 20 or
whatever. 

I keep bumping into my storage limits on dropbox and pcloud. And maintaining a
backup of my computer is proving to be a bit of a pain. I'm contemplating
setting up a NAS or something so I can just dump everything I've got into
something and start again from scratch. I guess that was the idea with this
external hard drive. But that's a distraction from a distraction, so let's get
back to the useful one...

I had zero idea of what database engines might be transactional vs analytical.
It turns out most of the ones I've heard of are transactional. Including sqlite.
So for this wikipedia project, it's possible that I need an analytical
alternative to deal with the many GB of data. On the other hand, maybe searching
through paths requires the transactional end of things? Well, if that's the
case, sqlite will do the job. But if not, it looks like duckdb might be what I'm
after. 

On the other hand, the sql dump is from mysql. And I have to fix something to
allow my computer to install/update properly. Maybe I'll do that this week...
In any case, it does look like duckdb could be useful for other data projects.

### R1D72 2020-12-02

Okay, once this semester is done I've got to go through this journal and see
what's been slipping through the cracks! I've been doing plenty of coding
lately, but not keeping records. And I've fallen way behind on the comparative
advantage model. But plenty of R as 390 winds down. Last night and this morning
was doing some web scraping. Today I'm going to learn some R OOP by simulating
(or at least starting to) Monopoly. 

### R1D73 2020-12-08

Another week! I've been doing R stuff pretty frequently, but I'm not counting
that towards my 100 days because I didn't record it here. I guess I could go
over git commit logs and figure out what I did when, but let's just call them
free days. Right now I'm going through the homework for the first week of
Statistical Rethinking (in R).

### R1D74 2020-12-09

Spent a bunch of time going through students' initial submissions for 390.
They've got a week left and I hope they get something interesting. But for most
of them I've been able to push them forward. 

### R1D75 2020-12-14

I've been doing a bit of R code. Today I've got to do some work on the
Statistical Rethinking homework.

### R1D76 2021-01-05

Going to follow along with Robinson's Tidy Tuesday screen cast. Oh yeah, and at
some point I've got to get back into that Stat Rethinking homework.

I should also ask myself if I should start a new round for 100 days of code. Or
do I want to keep track of my progress in some other way? Maybe just keeping it
in my usual journal will make it easier for me to record little things. I should
do that probably.
