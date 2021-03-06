import cmath
import math
import random

"""
Pioneers of game theory on terms
*game*, *play*, *move*, *strategy*, and *choice*:

THEORY OF GAMES AND ECONOMIC BEHAVIOR
By JOHN VON NEUMANN, and OSKAR MORGENSTERN
pp.48--49

6.1. Explanation of the Termini Technici
6.1. Before an exact definition of the combinatorial concept of a game
can be given, we must first clarify the use of some termini. There are
some notions which are quite fundamental for the discussion of games,
but the use of which in everyday language is highly ambiguous. The words
which describe them are used sometimes in one sense, sometimes in another,
and occasionally worst of all as if they were synonyms. We must
therefore introduce a definite usage of *termini technici*, and rigidly adhere
to it in all that follows.
  First, one must distinguish between the abstract concept of a *game*,
and the individual *plays* of that game. The *game* is simply the totality
of the rules which describe it. Every particular instance at which the
game is played in a particular way from beginning to end, is a *play*.
  Second, the corresponding distinction should be made for the moves,
which are the component elements of the game. A move is the occasion
of a choice between various alternatives, to be made either by one of the
players, or by some device subject to chance, under conditions precisely
prescribed by the rules of the game. The *move* is nothing but this abstract
"occasion," with the attendant details of description, i.e. a component
of the *game*. The specific alternative chosen in a concrete instance i.e.
in a concrete *play* is the *choice*. Thus the moves are related to the
choices in the same way as the game is to the play. The game consists
of a sequence of moves, and the play of a sequence of choices.
  Finally, the *rules* of the game should not be confused with the *strategies*
of the players. Exact definitions will be given subsequently, but the
distinction which we stress must be clear from the start. Each player
selects his strategy i.e. the general principles governing his choices freely.
While any particular strategy may be good or bad provided that these
concepts can be interpreted in an exact sense (cf. 14.5. and 17.8-17.10.)
it is within the player's discretion to use or to reject it. The rules of the
game, however, are absolute commands. If they are ever infringed, then
the whole transaction by definition ceases to be the game described by those
rules. In many cases it is even physically impossible to violate them.
"""

EPSILON = 0.00001

def Coordinated(Game):
    """
    Returns the general form of a coordinated game:
    replaces each leaf value <payoff> with vector (<payoff>,...,<payoff>)
    of length N, where N is the number of players
    """
    g = Game
    N = 0
    while type(g) not in (int,float):
        g = g[0]
        N += 1
    u = lambda g: [g]*N if type(g) in (int,float) else list(map(u, g))
    return u(Game)

def NormalizedToOne(weights:list[float]) -> list[float]:
    """
    Returns a vector const*weights, which sums up to one.
    The resulting vector can serve as a probability distribution over a finite
    set.
    """
    assert weights, "Empty sequence of weights"
    absw = [abs(w) for w in weights]
    s = sum(absw)
    return [1/len(absw)]*len(absw) if s<EPSILON else [w/s for w in weights]

def WeightedChoice(weights:list[float]) -> int:
    """
    A random integer 0...len(weights)-1, w.r.t. given distribution (weights).
    """
    r = random.uniform(0, sum(weights))
    upto = 0
    for i,w in enumerate(weights):
        if upto+w >= r: return i
        upto += w
    assert False, "Random overflow"

def RandomBasis(d:int) -> list[list[float]]:
    """
    Gram-Schmidt-orthonormalized random real d-dimensional -1..1-vectors.
    """
    b = [None]*d
    inner = [None]*d
    for i in range(d):
        b[i] = [None]*d
        while True:
           for j in range(d):
               b[i][j] = random.random()*2-1
           for j in range(i):
               innerij = 0
               for k in range(d):
                   innerij += b[i][k]*b[j][k]
               for k in range(d):
                   b[i][k] -= innerij/inner[j]*b[j][k]
           inner[i] = 0
           for k in range(d):
               inner[i] += b[i][k]**2
           if inner[i]>0.00001:
               break
    for i in range(d):
        for k in range(d):
            b[i][k] /= inner[i]**0.5
    return b

def Unitary(theta:list[float], phi=None, gamma=None) -> list[list[complex]]:
    """
    Parameterized NxN unitary matrix.

    Returns NxN unitary matrix, where N is determined according to the sizes
    of theta, phi and gamma.

    All N(N-1)/2 + N(N-1)/2 + N = N^2 parameters are -1..1-values.

    theta: list of N(N-1)/2 real rotation angles, each for a subplane
           generated by two standard basis vectors e_i and e_j

    phi: list of N(N-1)/2 complex rotation angles, each for a subplane
         generated by two standard basis vectors e_i and e_j

    gamma: list of N phasors for each of N columns

    Can be also called with only one parameter, which encapsulates N^2 values
    of theta, phi and gamma.
    """
    if (phi is None) and (gamma is None):
        N = int(len(theta)**0.5+0.1)
        theta, phi, gamma = theta[:-N:2], theta[1:-N:2], theta[-N:]
    N = len(gamma)
    U = [[int(i==j) for i in range(N)] for j in range(N)]
    k = 0
    for j1 in range(N-1):
        for j2 in range(j1+1,N):
            ep, st, ct = cmath.exp(1j*math.pi*phi[k]), math.sin(math.pi*theta[k]), math.cos(math.pi*theta[k])
            U[j1], U[j2] = [U[j1][i]*ct+U[j2][i]*st*ep for i in range(N)], [U[j1][i]*st/ep-U[j2][i]*ct for i in range(N)]
            k += 1
    for j in range(N):
        for i in range(N):
            U[j][i] *= cmath.exp(1j*math.pi*gamma[i])
    return U

def test_unitary():
    repr_complex = lambda c: ('{0.real:.2f}' if abs(c.imag)<0.001 else ('{0.imag:.2f}j' if abs(c.real)<0.001 else '{:.2f}')).format(c)
    repr_unitary = lambda U: '| '+(' |\n| '.join([''.join(['{:^12}'.format(repr_complex(item)) for item in row]) for row in U]))+' |'
    print("Identity 3x3:\n" + repr_unitary(Unitary([0,0,0,0,0,0,0,1,0])))
    print("Identity 2x2:\n" + repr_unitary(Unitary([0,0,0,1])))
    print("CNOT gate:\n" + repr_unitary(Unitary([0,0,0,0,0,0,0,0,0,0,0.5,0,0,1,0,0])))
    print("Hadamard gate:\n" + repr_unitary(Unitary([0.25,0,0,0])))
    print("X:\n" + repr_unitary(Unitary([0.5,0,0,0])))
    print("Y:\n" + repr_unitary(Unitary([0.5,-0.5,0,0])))
    print("Z:\n" + repr_unitary(Unitary([0,0,0,0])))
    print("sqrt(NOT):\n" + repr_unitary(Unitary([-0.25,-0.5,0.25,-0.75])))
    print("Phase shift R_(0.1π):\n" + repr_unitary(Unitary([0,0,0,0.1-1])))

# test_unitary(); exit()

class Correlation:
    """
    A Correlation object establishes an arbitrary shared randomness
    between two or more agents (e.g. learning automata).

    Shared randomness in game theory serves as a public signal which helps
    players to elaborate a correlated equilibrium.
    Like it happens in reality, each agent should be free in their decision
    to unilaterally regard or disregard any signal from the shared randomness.

    Proper use of a Correlation instance after registering all the agents:
    - Prepare()
    - LocalOperation(<Agent1>, <Parameters1>), ...
    - Observe()
    - get values Observables(<Agent1>), ...
    This is one typical turn of play, and it is supposed to be repeated
    by the same Agents many times, with different Parameters
    """

    def __init__(self, RegisterSize:int) -> None:
        """
        Like it happens in reality, amount of correlation can be limited.
        <RegisterSize> stands for the amount of shared randomness per one play.
        """
        self.RegisterSize = RegisterSize
        self._Agents = dict()

    def RegisterAgent(self, AgentId:int) -> None:
        """
        Grants access to the shared randomness for a given Agent.
        Each registered agent will be able to observe a
        <RegisterSize>-dimensional variable.
        """
        assert AgentId not in self._Agents, f"Duplicate Agent {AgentId}"
        self._Agents[AgentId] = len(self._Agents)

    def Prepare(self) -> None:
        """
        Generates a new public signal for the next play.
        """
        raise NotImplementedError

    def LocalOperationParametersCount(self) -> int:
        """
        Should return dimensionality of the parameter space of local operations
        for a correlation (e.g. classical or quantum).
        See LocalOperation() method.
        """
        raise NotImplementedError

    def LocalOperation(self, AgentId:int, Parameters:list[float]) -> None:
        """
        Applies a local operation of a given Agent.
        All local operations for each agent should be applied after Prepare()
        and applied before Observe().
        """
        assert AgentId in self._Agents, f"Unknown Agent {AgentId}"
        assert len(Parameters)==self.LocalOperationParametersCount(), f"Incorrect local operation for Agent {AgentId}"

    def Observe(self) -> None:
        """
        Makes all observables explicitly deterministic.
        Observation should be made before accessing a local variable.
        In classical physics it may correspond to coin tossing or a similar
        stochastic process. The conventional quantum physical analogue is
        collapse of the wave function to one of component states of a quantum
        system.
        """
        pass

    def Observable(self, AgentId) -> list[float]:
        """
        Provides access to the shared randomness for a given Agent.
        Should be called after Observe().
        """
        assert AgentId in self._Agents, f"Unknown Agent {AgentId}"
        return self._Observables[self._Agents[AgentId]]


class ClassicalCorrelation(Correlation):

    def Prepare(self) -> None:
        """
        Generates a new public signal for the next play.
        In classical correlations,
        identical copies of the register should be broadcasted to all agents.
        All local operations are impartial by default.
        """
        self._Operations = [[1/self.RegisterSize]*self.RegisterSize for _ in self._Agents]
        self._Register = tuple(random.uniform(0,1) for _ in range(self.RegisterSize))

    def LocalOperationParametersCount(self) -> int:
        """
        Returns dimensionality of the parameter space of local operations for
        a classical correlation.
        Each Agent's observables may depend on each value of the Register, so
        weights vector should have <RegisterSize> dimensions.
        """
        return self.RegisterSize

    def LocalOperation(self, AgentId:int, Parameters:list[float]) -> None:
        """
        Applies a local operation of a given Agent.
        All local operations for each agent should be applied after Prepare()
        and applied before Observe().
        In classical correlations,
        a local operation is just a list of weights for values in the Register
        """
        super().LocalOperation(AgentId, Parameters)
        self._Operations[self._Agents[AgentId]] = Parameters

    def Observe(self) -> None:
        """
        Makes all observables explicitly deterministic.
        Observation should be made before accessing a local variable.
        In classical physics it may correspond to coin tossing or a similar
        stochastic process.
        """
        self._Observables = []
        for operation in self._Operations:
            weights = [self._Register[i]*abs(operation[i]) for i in range(self.RegisterSize)]
            self._Observables.append(max(range(self.RegisterSize), key=lambda i:weights[i]))

class QuantumCorrelation(Correlation):

    def Prepare(self) -> None:
        """
        Generates a new public signal for the next play.
        In quantum correlation,
        when agents do not perform local operations, they should have no
        difference from classical shared randomness.
        It is convenient to represent this "default randomness" as a uniform
        quantum-entangled state
        (|11...1> + |22...2> + ... + |rr...r>) / Sqrt(r),
        where    r = <RegisterSize>
        and each |ii...i> contains #<Agents> digits i
        """
        self._Matrices = [[[int(i==j) for i in range(self.RegisterSize)] for j in range(self.RegisterSize)] for _ in self._Agents]
        self._QuantumState = [0] * self.RegisterSize**len(self._Agents)
        step = sum(self.RegisterSize**a for a in self._Agents.values())
        self._QuantumState[::step] = [self.RegisterSize**-0.5] * self.RegisterSize

    def LocalOperationParametersCount(self) -> int:
        """
        Returns dimensionality of the parameter space of local operations for
        a quantum correlation.
        An NxN unitary matrix could be parameterized with N^2 real values.
        """
        return self.RegisterSize**2

    def LocalOperation(self, AgentId:int, Parameters:list[float]) -> None:
        """
        Applies a local operation of a given Agent.
        All local operations for each agent should be applied after Prepare()
        and applied before Observe().
        In quantum correlations,
        a local operation is usually represented as a unitary matrix.
        """
        super().LocalOperation(AgentId, Parameters)
        self._Matrices[self._Agents[AgentId]] = Unitary(Parameters)

    def Observe(self) -> None:
        """
        Makes all observables explicitly deterministic.
        Observation should be made before accessing a local variable.
        In quantum physics it corresponds to the collapse of the wave function
        to one of component states of a quantum system.
        Technically, Observe() multiplies quantum state vector by the tensor
        product of all local operations, which are unitary matrices.
        """
        state = [0] * self.RegisterSize**len(self._Agents)
        for j in range(len(state)):
            for i in range(len(state)):
                tensor_ji, tj, ti = 1, j, i
                for a in range(len(self._Agents)-1,-1,-1):
                    tensor_ji *= self._Matrices[a][tj%self.RegisterSize][ti%self.RegisterSize]
                    tj //= self.RegisterSize
                    ti //= self.RegisterSize
                state[i] += self._QuantumState[j]*tensor_ji
        probabilities = [abs(amplitude**2) for amplitude in state]
        measurement = WeightedChoice(probabilities)
        self._Observables = [None] * len(self._Agents)
        for a in range(len(self._Agents)-1,-1,-1):
            self._Observables[len(self._Agents)-1-a] = measurement % self.RegisterSize
            measurement //= self.RegisterSize
        assert measurement==0, "Observable was too large"

def test_correlations():
    # try some arbitrary classical local operations
    def classical_probabilities(LO_1, LO_2):
        Pr = {(0,0):0,(0,1):0,(1,0):0,(1,1):0}
        # Pr[reg_0*lo_0 > reg_1*lo_1] = (lo_0/lo_1)/2 or (assuming reg_0,reg_1 are uniformly from 0..1)
        if LO_1[0]<=LO_1[1] and LO_2[0]<=LO_2[1]:
            Pr[(0,0)] = min(LO_1[0]/LO_1[1], LO_2[0]/LO_2[1]) / 2
            Pr[(0,1)] = LO_1[0]/LO_1[1]/2 - Pr[(0,0)]
            Pr[(1,0)] = LO_2[0]/LO_2[1]/2 - Pr[(0,0)]
            Pr[(1,1)] = 1 - sum(Pr.values())
        elif LO_1[0]>=LO_1[1] and LO_2[0]>=LO_2[1]:
            Pr[(1,1)] = min(LO_1[1]/LO_1[0], LO_2[1]/LO_2[0]) / 2
            Pr[(1,0)] = LO_1[1]/LO_1[0]/2 - Pr[(1,1)]
            Pr[(0,1)] = LO_2[1]/LO_2[0]/2 - Pr[(1,1)]
            Pr[(0,0)] = 1 - sum(Pr.values())
        else: # LO_1[0]<=LO_1[1] != LO_2[0]<=LO_2[1]
            Pr[(0,0)] = min(LO_1[0]/LO_1[1], LO_2[0]/LO_2[1]) / 2
            Pr[(1,1)] = min(LO_1[1]/LO_1[0], LO_2[1]/LO_2[0]) / 2
            Pr[(0,1) if LO_1[0]+LO_2[1]>LO_1[1]+LO_2[0] else (1,0)] = 1 - sum(Pr.values())
        return Pr
    def classical_statistics(LO_1, LO_2, trials=10000):
        classical = ClassicalCorrelation(RegisterSize=2)
        classical.RegisterAgent(AgentId=1)
        classical.RegisterAgent(AgentId=2)
        stats = {(0,0):0, (0,1):0, (1,0):0, (1,1):0}
        for _ in range(10000):
            classical.Prepare()
            classical.LocalOperation(AgentId=1, Parameters=LO_1)
            classical.LocalOperation(AgentId=2, Parameters=LO_2)
            classical.Observe()
            stats[(classical.Observable(1), classical.Observable(2))] += 1
        total = sum(stats.values())
        for key in stats.keys(): stats[key] /= total
        return stats
    def quantum_statistics(LO_1, LO_2, trials=10000):
        quantum = QuantumCorrelation(RegisterSize=2)
        quantum.RegisterAgent(AgentId=1)
        quantum.RegisterAgent(AgentId=2)
        stats = {(0,0):0, (0,1):0, (1,0):0, (1,1):0}
        for _ in range(10000):
            quantum.Prepare()
            quantum.LocalOperation(AgentId=1, Parameters=LO_1)
            quantum.LocalOperation(AgentId=2, Parameters=LO_2)
            quantum.Observe()
            stats[(quantum.Observable(1), quantum.Observable(2))] += 1
        total = sum(stats.values())
        for key in stats.keys(): stats[key] /= total
        return stats
    LO_1 = [0.9,0.1] # Classical Local operation of Agent 1
    LO_2 = [0.3,0.7] # Classical Local operation of Agent 2
    probabilities = classical_probabilities(LO_1, LO_2)
    statistics = classical_statistics(LO_1, LO_2, 10000)
    print("\nClassical correlation (stats ~= Pr):\n"+"\n".join("(%d,%d): %g ~= %g"%(a,b,statistics[(a,b)],probabilities[(a,b)]) for (a,b) in statistics))
    LO_1 = [0.4,0.6] # Classical Local operation of Agent 1
    LO_2 = [0.5,0.5] # Classical Local operation of Agent 2
    probabilities = classical_probabilities(LO_1, LO_2)
    statistics = classical_statistics(LO_1, LO_2, 10000)
    print("\nClassical correlation (stats ~= Pr):\n"+"\n".join("(%d,%d): %g ~= %g"%(a,b,statistics[(a,b)],probabilities[(a,b)]) for (a,b) in statistics))
    LO_1 = [0.0, 0.0, 0.0, 1.0] # Quantum Local operation of Agent 1: Identity
    LO_2 = [0.5, 0.0, 0.0, 0.0] # Quantum Local operation of Agent 2: NOT
    statistics = quantum_statistics(LO_1, LO_2, 10000)
    print("\nQuantum correlation (Identity,NOT):\n"+"\n".join("(%d,%d): %g"%(a,b,statistics[(a,b)]) for (a,b) in statistics))
    LO_1 = [0.5, 0.0, 0.0, 0.0] # Quantum Local operation of Agent 1: NOT
    LO_2 = [0.5, 0.0, 0.0, 0.0] # Quantum Local operation of Agent 2: NOT
    statistics = quantum_statistics(LO_1, LO_2, 10000)
    print("\nQuantum correlation (NOT,NOT):\n"+"\n".join("(%d,%d): %g"%(a,b,statistics[(a,b)]) for (a,b) in statistics))
    LO_1 = [0.0, 0.0, 0.0, 1.0] # Quantum Local operation of Agent 1: Identity
    LO_2 = [0.25, 0.0, 0.0, 0.0] # Quantum Local operation of Agent 2: Hadamard
    statistics = quantum_statistics(LO_1, LO_2, 10000)
    print("\nQuantum correlation (Identity,Hadamard):\n"+"\n".join("(%d,%d): %g"%(a,b,statistics[(a,b)]) for (a,b) in statistics))
    LO_1 = [0.25, 0.0, 0.0, 0.0] # Quantum Local operation of Agent 1: Hadamard
    LO_2 = [0.25, 0.0, 0.0, 0.0] # Quantum Local operation of Agent 2: Hadamard
    statistics = quantum_statistics(LO_1, LO_2, 10000)
    print("\nQuantum correlation (Hadamard,Hadamard):\n"+"\n".join("(%d,%d): %g"%(a,b,statistics[(a,b)]) for (a,b) in statistics))
    LO_1 = [0.0, 0.0, 0.0, 0.0] # Quantum Local operation of Agent 1: Almost identity
    LO_2 = [0.1, 0.0, 0.0, 0.0] # Quantum Local operation of Agent 2: Rotation by 0.1π
    statistics = quantum_statistics(LO_1, LO_2, 10000)
    print("\nQuantum correlation (Almost Identity,Rotation by 0.1π):\n"+"\n".join("(%d,%d): %g"%(a,b,statistics[(a,b)]) for (a,b) in statistics))

# test_correlations(); exit()

class LearningAutomaton:
    """
    A Learning Automaton plays an arbitrary game and tries to maximize its
    payoff.

    Its strategy consists of two parts:
      1) Local operation allowed by a given Correlation;
      2) Linear map from the space of values of Correlation observables
         to the space of probability distributions of choices.

    Development of a strategy is based on the historical data (records of plays)
    limited by the parameter MemorySize.

    In the space of strategies, the next strategy should not be too far from
    the previous one. The distance between them should be kept equal to the
    parameter LearningRate, when it is possible.
    """
    def __init__(self, correlation:Correlation, ChoicesCount:int, MemorySize:int=100, LearningRate:float=0.01) -> None:
        """
        <correlation> should implement LocalOperation() and Observe() methods to
        model some kind of correletion between two or more interacting agents.
        Usually classical or quantum correlations are being studied, but any
        model can be given for a Learning Automaton.

        A Learning Automaton is intended to play a game with a finite number of
        [pure] choices. This number is denoted by <ChoicesCount>.
        Thus an automaton makes a choice by just announcing an integer C:
        0 <= C < ChoicesCount.

        Memory of an automaton is intended for keeping its previous experience.
        <MemorySize> denotes the number of last plays and corresponding payoffs
        to be remembered.

        An automaton can be sensitive or less sensitive to new experience.
        <LearningRate> is a tradeoff between
        (A) speed of learning ("sensitivity") and
        (B) sustainability + better precision ("insensitivity").

        <_Memory> keeps records of previous plays
        <_Strategy> stands for current set of strategy-defining parameters.
        <_TotalPayoff> and <_TotalPlayed> are intended for statistical purposes.
        """
        correlation.RegisterAgent(AgentId=id(self))
        self._Correlation = correlation
        self._ChoicesCount = ChoicesCount
        self._MemorySize = MemorySize
        self._LearningRate = LearningRate
        self._LocalOperationParametersCount = correlation.LocalOperationParametersCount()
        self._Memory = []
        self._Strategy = [0.0]*(self._LocalOperationParametersCount+correlation.RegisterSize*ChoicesCount)
        self._TotalPayoff = 0
        self._TotalPlayed = 0
        ### self._Plots = DynamicPlots((2,2))

    def PredictLocalOperationPayoff(self, strategy:list[float]) -> float:
        """
        Predicts payoff after local operations of a given <strategy>,
        based on previous experience.

        Only local operation parameters should be given in <strategy>.
        """
        result, weight = 0.0, 0.0
        coincidents = []
        for _,local_operation,_,payoff in self._Memory:
            distance2 = sum(((s1-s2)**2 for s1,s2 in zip(strategy,local_operation)))
            if distance2 < EPSILON:
                coincidents.append(payoff)
            elif not coincidents:
                w = 1 / distance2
                result += payoff*w
                weight += w
        ### if coincidents: print("COINCIDENTS!", coincidents)
        return sum(coincidents)/len(coincidents) if coincidents else result/max(weight,EPSILON)

    def PredictMixedChoicePayoff(self, strategy:list[float]) -> float:
        """
        Predicts payoff after local operations of a given <strategy>,
        based on previous experience.

        Only weights for <self._Observable> should be given in <strategy>.
        """
        result, weight = 0.0, 0.0
        coincidents = []
        for observable,local_operation,mixed_choice,payoff in self._Memory:
            if observable != self._Observable: continue
            distance2 = sum(((s1-s2)**2 for s1,s2 in zip(strategy,mixed_choice)))
            distance2 += sum(((s1-s2)**2 for s1,s2 in zip(self._Strategy[:self._LocalOperationParametersCount],local_operation)))
            if distance2 < EPSILON:
                coincidents.append(payoff)
            elif not coincidents:
                w = 1 / distance2
                result += payoff*w
                weight += w
        ### if coincidents: print("COINCIDENTS!", coincidents)
        return sum(coincidents)/len(coincidents) if coincidents else result/max(weight,EPSILON)

    def Operate(self) -> None:
        """
        Deals with "public signal" from the Correlation

        Searches for a better strategy nearby in the space of strategies.
        If it is not better than a strategy picked uniformly at random,
        selects the random strategy.

        Then performs the corresponding local operation.
        """
        self._Strategy[:self._LocalOperationParametersCount] = max(
            # [[random.random()*2-1 for _ in range(self._LocalOperationParametersCount)]] +
            [[S+d*t for S,d in zip(self._Strategy[:self._LocalOperationParametersCount],direction)] for direction in RandomBasis(self._LocalOperationParametersCount) for t in (+self._LearningRate,-self._LearningRate)],
            key = self.PredictLocalOperationPayoff)
        self._Correlation.LocalOperation(id(self), self._Strategy[:self._LocalOperationParametersCount])

    def Choose(self) -> list[float]:
        """
        Makes a choice according to the obtained observable.
        distribution over the set of choices.

        Searches for a better strategy nearby in the space of strategies.
        If it is not better than a strategy picked uniformly at random,
        selects the random strategy.

        Thjen returns a mixed strategy.
        """
        self._Observable = self._Correlation.Observable(id(self))
        a = self._LocalOperationParametersCount + self._ChoicesCount*self._Observable
        b = a + self._ChoicesCount
        self._Strategy[a:b] = max(
            # [[random.random()*2-1 for _ in range(self._ChoicesCount)]] +
            [[S+d*t for S,d in zip(self._Strategy[a:b],direction)] for direction in RandomBasis(self._ChoicesCount) for t in (+self._LearningRate,-self._LearningRate)],
            key = self.PredictMixedChoicePayoff)
        return NormalizedToOne(tuple(map(abs, self._Strategy[a:b])))

    def Remember(self, payoff:float) -> None:
        """
        Makes a record about the last used Strategy and the resulting <payoff>.
        This record will help in estimations of the further strategies.

        Also updates statistics.
        """
        self._Memory.append((
            self._Observable,
            tuple(self._Strategy[:self._LocalOperationParametersCount]),
            tuple(self._Strategy[self._LocalOperationParametersCount+self._ChoicesCount*self._Observable:][:self._ChoicesCount]),
            payoff
        ))
        self._Memory = self._Memory[-self._MemorySize:]
        self._TotalPayoff += payoff
        self._TotalPlayed += 1

    def MeanPayoff(self) -> float:
        """
        Returns mean payoff over all history of playing.
        """
        return self._TotalPayoff/max(1,self._TotalPlayed)

def play(Game, correlation:Correlation, LearningRate:float=0.01, MemorySize:int=100, iterations:int=100, adversarial:bool=False):
    """
    Plays <iterations> rounds of a given Game between <correlation>-related
    Learning Automata.

    <Game> is a nested list with tuples of payoffs on its leaves:
    Game[Type_1]...[Type_N][Choice_1]...[Choice_N] = (Payoff1,...,PayoffN),
    where Type_i is type of the i-th player in a Bayesian game,
          Choice_i is the choice of the i-th player,
    and   N is the number of players.
    [Type_1]...[Type_N] can be omitted for a non-Bayesian game.

    <correlation> provides some kind of coordination for the players.
    Usually this is a nonlocal correlation -- classical or quantum.

    <adversarial> plays assume selecting the least beneficial types for players.

    Returns mean payoff over all automata at each step of iteration.
    """
    nest = Game
    nest_lengths = []
    while type(nest) not in (int,float):
        nest_lengths.append(len(nest))
        nest = nest[0]
    N = nest_lengths[-1] # number of players == length of vector of payoffs
    if len(nest_lengths) == N+1:
        for _ in range(N): Game = [Game] # make a non-Bayesian game Bayesian
        types_count = [1]*N
        choices_count = nest_lengths[:-1]
    elif len(nest_lengths) == 2*N+1: # leave a Bayesian game as is
        types_count = nest_lengths[:N]
        choices_count = nest_lengths[N:-1]
    else:
        raise Exception(f"Misdefined Game: {nest_lengths}")
    automata = [[LearningAutomaton(correlation,choices_count[i],LearningRate=LearningRate,MemorySize=MemorySize) for t in range(types_count[i])] for i in range(N)]
    all_types = lambda i: tuple((a,) for a in range(types_count[i])) if i==N-1 else tuple((a,)+b for a in range(types_count[i]) for b in all_types(i+1))
    types_stats = {t:[0,0] for t in all_types(0)} # types --> [total_sum_of_payoffs, total_plays]
    progress = [] # iteration --> mean_payoff_over_all_automata
    for iteration in range(iterations):
        correlation.Prepare()
        if adversarial and random.random()>0.01:
            types = min(types_stats.keys(), key=lambda t:-math.inf if types_stats[t][1]==0 else types_stats[t][0]/types_stats[t][1])
        else:
            types = tuple(random.randrange(t) for t in types_count)
        for i,t in enumerate(types): automata[i][t].Operate()
        correlation.Observe()
        choices = [automata[i][t].Choose() for i,t in enumerate(types)]
        payoffs = Game
        for t in types: payoffs = payoffs[t]
        ExpectedPayoffs = lambda i,pp: pp if i==N else map(sum,zip(*([p*Pr for p in ExpectedPayoffs(i+1,pp[c])] for c,Pr in enumerate(choices[i]))))
        payoffs = tuple(ExpectedPayoffs(0, payoffs))
        ### floats = lambda ff: "["+" ".join((f"{f:.2f}" if type(f) in (float,int) else floats(f) for f in ff))+"]"
        ### print(types, [automata[0][types[0]]._Observable, automata[1][types[1]]._Observable], floats(choices), floats(payoffs))
        for i,t in enumerate(types): automata[i][t].Remember(payoffs[i])
        types_stats[types][0] += sum(payoffs)
        types_stats[types][1] += 1
        progress.append(sum((a.MeanPayoff() for automaton in automata for a in automaton)) / sum(map(len,automata)))
    ### print(types_stats)
    return progress

