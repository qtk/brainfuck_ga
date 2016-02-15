import string
import random
from datetime import datetime
from brainfuck import brainfuck
#  random.seed(2411)

bf_syntax = string.digits + '>' + '<' + '+' + '-' + '.' + '[' + ']' + ','


def microseconds():
    current_time = datetime.now()
    current_time = current_time.microsecond \
                   + current_time.second * 1000000 \
                   + current_time.minute * 1000000 * 60 \
                   + current_time.hour * 1000000 * 60 * 60 + current_time.day * 1000000 * 60 * 60 * 24
    return current_time


class Evolution:
    def __init__(self, pop_size):
        self.time = microseconds()
        self.evolve(pop_size)
        self.time = microseconds() - self.time
        print("duration:", self.time / 1000000, " seconds")

    def evolve(self, pop_size):
        gen = 0
        population = self.start_population(pop_size)
        population = self.set_pop_fitness(population)
        print(str(gen), "|", str(population[0]['fitness']), ":", ''.join(population[0]['dna']))
        while population[0]['fitness'] != 0:
            gen += 1
            population = self.nextgen(population, pop_size)
            print(str(gen), "|", str(population[0]['fitness']), ":", ''.join(population[0]['dna']))

    def start_population(self, pop_size):
        population = []
        for i in range(pop_size):
            individual = {'fitness': None,
                          'output': None,
                          'dna': [random.choice(bf_syntax) for _ in range(random.randint(10, 32))]}
            population.append(individual)
        return population

    def set_pop_fitness(self, population):
        def fitness(dna):
            fitness = 0
            try:
                for i in range(1, 13):
                    target = i * 10
                    result = brainfuck(dna, bfinput=i)
                    try:
                        result.output = int(''.join(map(str, result.output)))
                    except ValueError:
                        result.output = 0
                    fitness += ((target+target) - result.output) ** 2
                return fitness
            except (ValueError, IndexError):
                fitness += 1000000000  # one billion
                return fitness

        for individual in population:
            individual['fitness'] = fitness(individual['dna'])
        population = sorted(population, key=lambda k: k['fitness'])
        return population

    def nextgen(self, population, pop_size):
        def mutate(child):
            chance = random.random()
            if chance < 0.1:
                for _ in range(0, random.randint(1, 4)):
                    child.append(random.choice(bf_syntax))
            elif chance < 0.8:
                for _ in range(0, random.randint(1, 4)):
                    child[random.randint(0, len(child) - 1)] = random.choice(bf_syntax)
            else:
                for _ in range(0, random.randint(1, 4)):
                    del(child[random.randint(0, len(child) - 1)])
            return child

        def crossover(parent1, parent2):
            if len(parent1) < len(parent2):
                crossover_point = random.randint(0, len(parent1) - 1)
            else:
                crossover_point = random.randint(0, len(parent2) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2

        def tournament(population):
            opponent1, opponent2 = population[random.randint(0, pop_size - 1)], population[random.randint(1, pop_size - 1)]
            if opponent1['fitness'] < opponent2['fitness']:
                parent = opponent1
            else:
                parent = opponent2
            return parent['dna']

        nextgen = []
        for i in range(pop_size // 2):
            chance = random.random()
            parent1 = tournament(population)
            parent2 = tournament(population)
            # ensure dna doesn't reach zero
            if len(parent1) < 10:
                parent1 = parent1 + parent2
            if len(parent2) < 10:
                parent2 = parent2 + parent1

            if chance < 0.8:
                child1, child2 = crossover(parent1, parent2)
            elif chance < 0.85:
                child1, child2 = parent1, parent2
            else:
                child1, child2 = mutate(parent1), mutate(parent2)

            # ensure dna doesn't reach zero
            if len(child1) < 10:
                child1 = child1 + child2
            if len(child2) < 10:
                child2 = child2 + child1
            # prevent bloat
            if len(child1) > 32:
                child1 = child1[:len(child1) // 2]
            if len(child2) > 32:
                child2 = child1[:len(child2) // 2]

            child1 = {'fitness': None,
                      'output': None,
                          'dna': child1}
            child2 = {'fitness': None,
                      'output': None,
                          'dna': child2}
            nextgen.append(child1)
            nextgen.append(child2)
        nextgen = self.set_pop_fitness(nextgen)
        return nextgen


if __name__ == '__main__':
    Evolution(pop_size=100)
