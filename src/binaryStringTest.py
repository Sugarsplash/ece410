from pyevolve import G1DBinaryString, Scaling
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators

from math import sin, pi

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
	x = 0.0
	# iterate over the chromosome
	power = len(chromosome)
	for i in range(power):
		if chromosome[i] == 1:
			x = x + 2**(power-1)

	xval = 1.0 + x * (3/2**22 - 1)

	score = xval * sin(10*pi*xval) + 1.0

	return score

# Genome instance
genome = G1DBinaryString.G1DBinaryString(22)

# The evaluator function (objective function)
genome.evaluator.set(eval_func)
genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GTournamentSelector)

#Change scaling method
pop = ga.getPopulation()
pop.scaleMethod.set(Scaling.SaturatedScaling)

ga.setGenerations(100)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=10)

# Best individual
best = ga.bestIndividual()
print best