import random
from deap import base, creator, tools

# ————— CONFIGURACIÓN DEL GA CON DEAP —————
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("DeapInd", list, fitness=creator.FitnessMin)

# Generador de individuo de 10 bits
def _gen_deap():
    return [random.randint(0, 1) for _ in range(10)]

# Evaluación: suma de bits (minimizar)
def _eval_deap(ind):
    return sum(ind),

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.DeapInd, _gen_deap)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", _eval_deap)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

# Ejecutamos DEAP GA
pop_deap = toolbox.population(n=10)
for gen in range(5):
    print(f"\n=== DEAP: Generación {gen+1} ===")
    # Evaluar población
    for idx, ind in enumerate(pop_deap, 1):
        if not ind.fitness.valid:
            ind.fitness.values = toolbox.evaluate(ind)
        print(f"Ind{idx}: {ind} → aptitud {ind.fitness.values[0]}")
    # Selección, cruce y mutación
    sel = toolbox.select(pop_deap, len(pop_deap))
    nxt = []
    for i in range(0, len(sel), 2):
        p1, p2 = sel[i], sel[i+1]
        if random.random() < 0.8:
            c1, c2 = toolbox.mate(p1, p2)
            del c1.fitness.values, c2.fitness.values
        else:
            c1, c2 = creator.DeapInd(p1), creator.DeapInd(p2)
        c1 = toolbox.mutate(c1)[0]; del c1.fitness.values
        c2 = toolbox.mutate(c2)[0]; del c2.fitness.values
        nxt += [c1, c2]
    pop_deap = nxt

best_deap = toolbox.select(pop_deap, 1)[0]
if not best_deap.fitness.valid:
    best_deap.fitness.values = toolbox.evaluate(best_deap)
print(f"\n→ Mejor DEAP: {best_deap} con aptitud {best_deap.fitness.values[0]}")

# ————— CONFIGURACIÓN DEL GA MANUAL —————
n_bits, n_pop, n_gens = 6, 10, 4
p_cruce, p_mut = 0.8, 0.1

# Inicializamos población de 6 bits
pop_man = [[random.randint(0,1) for _ in range(n_bits)] for _ in range(n_pop)]

for gen in range(n_gens):
    print(f"\n=== Manual: Generación {gen+1} ===")
    # Evaluar
    fitness = []
    for idx, ind in enumerate(pop_man, 1):
        x = int("".join(str(b) for b in ind), 2)
        f = x**2 + 1
        fitness.append(f)
        print(f"Ind{idx}: {ind} → x={x}, f(x)={f}")
    # Torneo
    seleccionados = []
    for _ in range(n_pop):
        i1, i2 = random.randrange(n_pop), random.randrange(n_pop)
        seleccionados.append(pop_man[i1] if fitness[i1] > fitness[i2] else pop_man[i2])
    # Cruce y mutación
    nueva = []
    for i in range(0, n_pop, 2):
        p1, p2 = seleccionados[i], seleccionados[i+1]
        if random.random() < p_cruce:
            pt = random.randrange(1, n_bits)
            c1 = p1[:pt] + p2[pt:]
            c2 = p2[:pt] + p1[pt:]
        else:
            c1, c2 = p1[:], p2[:]
        # mutación bit-flip
        c1 = [1-b if random.random() < p_mut else b for b in c1]
        c2 = [1-b if random.random() < p_mut else b for b in c2]
        nueva += [c1, c2]
    pop_man = nueva

# Mejor solución manual
fitness = [ (int("".join(str(b) for b in ind),2)**2 + 1) for ind in pop_man ]
best_man = pop_man[fitness.index(max(fitness))]
x_best = int("".join(str(b) for b in best_man),2)
print(f"\n→ Mejor Manual: {best_man} → x={x_best}, f(x)={x_best**2+1}")
