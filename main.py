import numpy as np
from beautifultable import BeautifulTable
import matplotlib.pyplot as mpl

import Utils as utl


# POPULATION    == GENERATION
# POPULATION    contain List of INDIVIDUAL
# INDIVIDUAL    contain Fitness and KROMOSOM
# KROMOSOM      contain List of GEN
# GEN           Type {Binary, Integer, Real, Permutation}

def createPopulation(populationSize):
    population = []
    for _ in range(populationSize):
        population.append(utl.createIndividual(list(utl.createKromosom())))

    return population

def showPopulation(population):
    table = BeautifulTable(maxwidth=150)
    table.set_style(BeautifulTable.STYLE_BOX_DOUBLED)
    table.columns.header = ["Fitness", "x", "y", "Kromosom"]
    tabRowHeader = []
    for i in range(len(population)):
        tabRowHeader.append(str(i+1))
        x, y = utl.decodeForBinary(interval_x=utl.interval_x_y[0], interval_y=utl.interval_x_y[1], kromosom=population[i]['kromosom'])
        table.rows.append([population[i]['fitness'], x, y, population[i]['kromosom']])

    table.rows.header = tabRowHeader
    print(table)

def getBestKromosom(population):
    return max([individual for individual in population], key=lambda x: x['fitness'])

def getMinKromosom(population):
    return min([individual for individual in population], key=lambda x: x['fitness'])

if __name__ == '__main__':
    population_size = 10  # the individu will generate in one population
    generation = 50  # the generation for generate solution
    xover_prob = 0.9
    mutation_prob = 0.01

    population_list = createPopulation(population_size)

    for gene in range(generation):
        print(f"*--------------------------------Generation {gene}--------------------------------*")
        showPopulation(population_list)
        best_individual = getBestKromosom(population_list)
        print(f"----------Best Kromosom for Generation {gene}----------")
        print(f"Fitness\t\t: {best_individual['fitness']:.3f}")
        print(f"Kromosom\t: {best_individual['kromosom']}")

        print("\nCreating new Generation...")
        new_population_list = []
        for i in range(len(population_list)//2):  # len(child_list) < population_size
            print(f"---------->Mating Pool {i + 1}")
            krom_parent_1, krom_parent_2 = utl.tournamentSelection(population_list)
            krom_child_1, krom_child_2 = utl.xoverBinerOnePoint(krom_parent_1, krom_parent_2, prob=xover_prob)
            print(f"Parent 1 {krom_parent_1}\nParent 2 {krom_parent_2}")
            print(f"\tChild 1 {krom_child_1}\n\tChild 2 {krom_child_2}")
            krom_child_1, mutasi1 = utl.mutasiBiner(krom_child_1, mutation_prob)
            krom_child_2, mutasi2 = utl.mutasiBiner(krom_child_2, mutation_prob)
            new_population_list.append(utl.createIndividual(krom_child_1))
            new_population_list.append(utl.createIndividual(krom_child_2))
            print(f"\t----------Mutasi----------")
            print(f"\tChild 1 Mutation : {krom_child_1} ({'Termutasi' if mutasi1 else 'Secure'})\n\tChild 2 Mutation : {krom_child_2} ({'Termutasi' if mutasi2 else 'Secure'})")

        worst_individual = getMinKromosom(new_population_list)
        new_population_list.remove(worst_individual)
        new_population_list.append(best_individual)
        population_list = new_population_list

    print(f"*--------------------------------Generation {gene + 1}--------------------------------*")
    showPopulation(population_list)
    # add best individu ke newPop untuk dijadikan generasi baru / proses elitisme
    best_individual = getBestKromosom(population_list)
    # newPop.append(bstIndividual)
    print(f"----------Best Kromosom for Generation {gene + 1}----------")
    print(f"Fitness\t\t: {best_individual['fitness']:.3f}")
    print(f"Kromosom\t: {best_individual['kromosom']}")
    x, y = utl.decodeForBinary(interval_x=utl.interval_x_y[0], interval_y=utl.interval_x_y[1], kromosom=best_individual['kromosom'])
    print(f"x : {x}\ny : {y}")
