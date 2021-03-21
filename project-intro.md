# A short overview of the project No.1.1.1.2/VIAA/1/16/099 "Optimal quantum-entangled behavior under unknown circumstances"
From December 2018 to November 2020, we continued exploring the features of quantum information for more effective game analysis and more effective behavior under uncertain circumstances.

At the beginning of this period, two main areas of research were figured out: (1) analysis of data obtained from simulating the behavior of correlated automata in Blind correlated games; and (2) efficient solving of games by using quantum algorithms. This report summarizes the progress made so far in both areas.

## Blind correlated games
In game theory, games with incomplete information are used to model and study many important economic situations in which participants may generally be unaware of the details of the environment. These details may include:

- Payoffs;
- Interests of other players;
- Abilities of other players;
- Information awareness of other players.

Most often, [Bayesian games](https://en.wikipedia.org/wiki/Bayesian_game) are considered for these purposes, where players *a priori* have some information about the possible results of their choice, although these results can also depend on the types and choices of other participants in the game.

In some sense, we are looking at an even more information-incomplete kind of games -- we call them *Blind games*. Unlike Bayesian games, in Blind games, all information about player's payoffs can only be obtained *a posteriori*, i.e. by experiment. Such games are considered in the context of learning agents in repetitive situations, where a player develops a suitable strategy on the basis of the previous experience.

Since at least 1960-ies there have been known experiments with finite automata that act independently of each other and arrive at Nash equilibria in Blind games. In our work, we investigate the activity of such learning automata under some rather specific circumstances. First, automata in the learning process can and should regard a random signal (more accurately, *shared randomness*), which allows, generally speaking, to develop an arbitrary *correlated Nash equilibrium*, which is sometimes [much more preferable](https://en.wikipedia.org/wiki/Chicken_\(game\)#Correlated_equilibrium_and_the_game_of_chicken) than any other meaningful solution. Second, this signal can be represented not only in the form of classical information, but also can have quantum nature. The difference between classical and quantum correlations in the context of learning automata is of our main interest.

### Models of learning automata
It is rather easy to formulate a natural model of finite automaton that acts in a game with a finite set of choices. This should be either a finite-state transducer or a Turing machine, that accepts the payoff of the previous round of the game as an input, and returns the choice number for the next round as an output. Most often, this approach is implemented as a Turing machine with 2×*S* memory cells (where *S* is the number of choices), which are used to store (1) the number of applications of each choice; (2) the total sum of payoffs after each choice. Each time the automaton selects the choice with the highest expected payoff, based on the accumulated statistics. This way it naturally converges to a Nash equilibrium in the game, where the probability of making a particular choice is proportional to the number of applications of this choice made during the overall learning process.

In contrast, formulating a model of automaton which would be suitable for both quantum and classical correlation is a non-trivial task. The main difficulty is that an arbitrary correlation is generally representable by a real number (or several real numbers). The simple model of finite-state automata is not enough for handling the continuous values. One common approach to such tasks is known as [Hybrid automaton model](https://en.wikipedia.org/wiki/Hybrid_automaton). Unfortunately, we failed to find a similar natural model which would be suitable for implementing learning automata for our purposes. In this regard, another model was chosen -- a Turing machine, which saves several recent strategies and the corresponding resulting payoffs. On the basis of this data, the automaton predicts the expected payoff for each possible strategy and selects the one for which this prediction promises the biggest payoff.

The selected model of automaton has been implemented and intensively tested. For ease of use, the corresponding framework has been rewritten in Python and documented in detail. It is currently available as a GitHub repository at <https://github.com/quantum-games/CorrelatedAutomata>.

### The learning rate
We have experimented with a number of different Blind Bayesian games. We note that for most games, non-correlating automata typically are able to learn faster and act more efficiently, compared to those more complex automata that should regard shared randomness or measurements of quantum entangled particles when deciding on the next choice. Besides that, dealing with measurements of quantum particles should be represented by an even larger number of parameters, compared to the dealing with only a shared randomness, and this factor furthermore slows down the learning progress of quantum correlated automata.

However, for some set of games, where correlated solutions significantly outperform non-correlated Nash equilibria, and quantum correlations provide a greater advantage over the classical ones, we do observe a more efficient behavior of quantum correlated automata. A typical learning scenario for the two kinds of automata consists of four stages:

1. At the beginning, both kinds of automata behave randomly and thus get random payoffs.
2. After a short period of time, the more simply arranged classical deterministic automata quickly increase their payoffs, while the quantum automata take a long time to optimize the parameters for dealing with quantum measurements.
3. At the middle distance, quantum automata, due to their wider capabilities, begin to produce better results.
4. Having passed a long way of learning, classical automata begin to approach from below the payoffs of quantum automata, but seemingly never reach them.

The Python code for simulation of these processes for the well-known game [CHSH](https://en.wikipedia.org/wiki/Quantum_refereed_game#CHSH_Refereed_Game) is available at the [GitHub repository](https://github.com/quantum-games/CorrelatedAutomata). Also the graphic demo is available at the website <http://quantumgames.pythonanywhere.com/>. Note that the former resource is more convenient to use for a detailed study of behavior of automata in different games, while the latter one is limited to only two players, only two Bayesian types of players, and only two choices available for each player.

## Efficient solving of games by using quantum algorithms

Apart from the correlated games, we also aim to show that quantum computers can be useful in computational game theory. In quantum game theory, a subset of [Subtraction games](https://en.wikipedia.org/wiki/Subtraction_game) became the first explicitly defined class of zero-sum combinatorial games with provable separation between quantum and classical complexity of solving them.

A Subtraction game is similar to a canonical [Nim game](https://en.wikipedia.org/wiki/Nim). The difference is that, in the former game the players deal with just one heap of stones but with certain limitations imposed on the number of stones they can take from the heap. Nim is a very notable game in game theory, mainly because it serves as a "base case" for the famous [Sprague–Grundy theorem](https://en.wikipedia.org/wiki/Sprague–Grundy_theorem). Many games are known to be reducible to some Nim games, and also many games on graphs can be reduced to some Subtraction games.

The most common limitation for Subtraction games is defining maximum for the number of stones to be removed, and this kind of games has nice combinatorial solutions. As an example, let us consider a two-player Subtraction game with a heap of 10 stones and the limitation of maximal number of 3 stones to be removed the heap. Then the first player has the only winning strategy: (1) remove 2 stones at the first turn -- so as to leave 8 stones in the heap; (2) after the opponent removes 1, 2 or 3 stones, the first player removes respectively 3, 2 or 1 stone -- so as to leave 4 stones in the heap; (3) finally, after the opponent removes again 1, 2 or 3 stones, the first player removes all the remainder and thus wins the game.

We study a much more general class of such limitations and thus a broader class of Subtraction games. When defining the rules of a game, for each possible number of stones *j* in the heap, we allow to impose any of 2*​^j^* possible limitations on the set of legal moves. Thus for initial number of stones _N_, one should provide *N*(*N*+1)/2 bits of information to define the rules of a Subtraction game.

Although it is not always necessary to know values of all *N*(*N*+1)/2 bits of the game definition, we can prove that substantial number of Subtraction games require querying a large share of them, in order to solve the game. The resulting high deterministic (as well as probabilistic) query complexity implies at least linear computational cost, whereas appropriate running a series of [Grover's search algorithm](https://en.wikipedia.org/wiki/Grover%27s_algorithm) allows to solve the game in sublinear --- yet polinomial --- time. We provide the formal proof of this separation between quantum and deterministic complexity for games of arbitrary size and arbitrary number of players in [two](https://arxiv.org/abs/1808.03494) [papers](https://arxiv.org/abs/2006.06965).

