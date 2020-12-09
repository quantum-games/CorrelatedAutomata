import CorrelatedAutomata as CA

LearningRate = 0.01
MemorySize   = 20
iterations   = 1000
adversarial  = False
tests_count  = 100

EQUAL = [[+1,-1],[-1,+1]]
XOR = [[-1,+1],[+1,-1]]
CHSH = [[CA.Coordinated(EQUAL), CA.Coordinated(EQUAL)],
        [CA.Coordinated(EQUAL), CA.Coordinated(XOR)]]

qq, cc = [[] for i in range(iterations)], [[] for i in range(iterations)]
for tests in range(tests_count):
    c = CA.play(CHSH, CA.ClassicalCorrelation(RegisterSize=2), LearningRate, MemorySize, iterations)
    q = CA.play(CHSH, CA.QuantumCorrelation(RegisterSize=2), LearningRate, MemorySize, iterations)
    for i,x in enumerate(c): cc[i].append(x)
    for i,x in enumerate(q): qq[i].append(x)
    print(f"{tests+1}\t{c[-1]}\t{q[-1]}")

with open(f"chsh_{tests}_averages.csv", "w") as stats:
    stats.write(f"Step\tAverage payoff of Classical automata\ttAverage payoff (over of Quantum automata\n")
    for step, (average_payoff_classical, average_payoff_quantum) in enumerate(zip(cc,qq)):
        average_payoff_classical = sum(average_payoff_classical) / len(average_payoff_classical)
        average_payoff_quantum = sum(average_payoff_quantum)/len(average_payoff_quantum)
        stats.write(f"{step+1}\t{average_payoff_classical}\t{average_payoff_quantum}\n")
