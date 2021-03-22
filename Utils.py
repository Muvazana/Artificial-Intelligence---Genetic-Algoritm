import numpy as np

interval_x_y = ([-1, 2], [-1, 1])

def myFunc(x, y):
    # this fucntion will return the calculate from your function you have
    return (x ** 2 * np.sin(y ** 2)) + (x + y)

def fitness(f):
    # if we want to get the maxima we use h = f
    # if we wamt to get the minimum output we use 1/(f+a) the var you can assign 0.01 to prevent 0
    return f

def createKromosom():
    # this function create the random Kromosom where the GEN_TYPE is Binary
    # you can change the type of gen to integer where the interval from 0 to 9
    # the kromosom size is size of gen in one kromosom
    gen_type = [0, 1]  # Binary [0,1] / Integer [0,9]
    kromosom_size = 20
    return np.random.choice(gen_type, kromosom_size)

def decodeForBinary(interval_x, interval_y, kromosom):
    # this function will decode and return your kromosom to x and y, where the GEN_TYPE is Binary
    # the interval_x for interval x
    # the interval_y for interval y
    # formula => x = r_b + ((r_a - r_b)/sum(i=1 to N; 2^-i)) * sum(i=1 to N; g_i^-i)
    # for r_a (upper limir) and r_b (bottom_limit)
    krom_x = kromosom[:len(kromosom)//2]
    krom_y = kromosom[len(kromosom)//2:]

    pembagi = 0    # sum(i=1 to N; 2^-i)
    pengali_x = 0  # sum(i=1 to N; g_i^-i) for x
    pengali_y = 0  # sum(i=1 to N; g_i^-i) for y


    for i in range(len(kromosom)//2):
        pembagi += 2 ** -(i+1)
        pengali_x += krom_x[i] * 2 ** -(i+1)
        pengali_y += krom_y[i] * 2 ** -(i+1)

    decodeFormula = lambda interval, pengali: interval[0] + ((interval[1] - interval[0]) / pembagi) * pengali

    return decodeFormula(interval_x, pengali_x), decodeFormula(interval_y, pengali_y)

def createIndividual(kromosom):
    x, y = decodeForBinary(interval_x= interval_x_y[0], interval_y= interval_x_y[1], kromosom=kromosom)
    fit = fitness(myFunc(x, y))

    return {'fitness': fit, 'kromosom': kromosom}

def tournamentSelection(population):
    tournament_size = 2
    parent_1 = max(np.random.choice(population, tournament_size, replace=False), key=lambda x: x['fitness'])
    parent_2 = max(np.random.choice(population, tournament_size, replace=False), key=lambda x: x['fitness'])
    return parent_1['kromosom'], parent_2['kromosom']

def xoverBinerOnePoint(krom_parent_1, krom_parent_2, prob):
    child1, child2 = [], []
    randomProb = np.random.random()
    if randomProb < prob:
        randomPoint = np.random.randint(0, len(krom_parent_1))
        child1[:randomPoint], child1[randomPoint:] = krom_parent_1[:randomPoint], krom_parent_2[randomPoint:]
        child2[:randomPoint], child2[randomPoint:] = krom_parent_2[:randomPoint], krom_parent_1[randomPoint:]
        return child1, child2

    return krom_parent_1, krom_parent_2

def mutasiBiner(kromosom, prob):
    mutated_krom = []
    mutasi = False
    for i in range(len(kromosom)):
        random_prob = np.random.random()
        if random_prob < prob:
            mutasi = True
            mutated_krom.append(0 if kromosom[i] == 1 else 1)
        else:
            mutated_krom.append(kromosom[i])


    return mutated_krom, mutasi