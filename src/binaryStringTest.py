from pyevolve import G1DBinaryString, Scaling
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Consts

from math import sin, pi

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
	x = 0.0
	# iterate over the chromosome
	power = len(chromosome) -1
	for i in range(len(chromosome)):
		if chromosome[power-i] == 1:
			x = x + 2**(power-1)

	xval = -1.0 + float(x) * (3.0/float((2**22)-1))

	score = xval * sin(10*pi*xval) + 1.0

	return score

# Genome instance
genome = G1DBinaryString.G1DBinaryString(22)
genome.setParams(rangemin=-1, rangemax=2)

# The evaluator function (objective function)
genome.evaluator.set(eval_func)
genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GTournamentSelector)
ga.minimax = Consts.minimaxType["maximize"]

#Change scaling method
pop = ga.getPopulation()
pop.scaleMethod.set(Scaling.SaturatedScaling)

ga.setGenerations(200)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=10)

# Best individual
best = ga.bestIndividual()
print best
