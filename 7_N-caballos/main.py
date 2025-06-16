from deap import base, creator, tools
import random

# — Parámetros —
N = 5                # Tablero de N x N con N caballos
POBLACION = 20       # Tamaño de la población
GENERACIONES = 2     # Número de generaciones
PC = 0.8             # Probabilidad de cruce (80%)
# Mutación interna siempre se aplica con probabilidad en mutar()

# — Configuración del Fitness y del Individuo —
creator.create("Evaluacion", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.Evaluacion)

# — Generación de un individuo: coloca N caballos en posiciones aleatorias —
def generar_individuo():
    # Inicializamos un tablero plano de ceros
    tablero = [0] * (N * N)
    # Seleccionamos N posiciones únicas
    for pos in random.sample(range(N * N), N):
        tablero[pos] = 1
    return creator.Individual(tablero)

# — Función de evaluación: cuenta pares de caballos en conflicto —
def evaluar(individual):
    conflictos = 0
    for i in range(N):
        for j in range(N):
            if individual[i * N + j] == 1:
                for di, dj in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]:
                    x, y = i + di, j + dj
                    if 0 <= x < N and 0 <= y < N and individual[x * N + y] == 1:
                        conflictos += 1
    # Cada par se cuenta dos veces
    return (conflictos // 2,)

# — Mutación: mueve un caballo de una casilla ocupada a una vacía —
def mutar(individual):
    inds = individual[:]  # copia la lista interna
    ocupadas = [idx for idx, v in enumerate(inds) if v == 1]
    vacias = [idx for idx, v in enumerate(inds) if v == 0]
    if ocupadas and vacias:
        src = random.choice(ocupadas)
        dst = random.choice(vacias)
        inds[src], inds[dst] = 0, 1
    # Retornamos un objeto Individual con la nueva lista
    return creator.Individual(inds),

# — Registrar operadores en el Toolbox —
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, generar_individuo)
toolbox.register("evaluate", evaluar)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutar)
toolbox.register("select", tools.selTournament, tournsize=3)

# — Crear población inicial usando tools.initRepeat directamente —
poblacion = tools.initRepeat(list, toolbox.individual, n=POBLACION)

# — Bucle evolutivo —
for gen in range(1, GENERACIONES + 1):
    print(f"\n=== Generación {gen} ===")

    # Mostrar cada individuo
    for idx, ind in enumerate(poblacion, 1):
        print(f"Ind{idx}: {ind}")

    # Evaluar población
    print("\nConflictos:")
    for idx, ind in enumerate(poblacion, 1):
        if not ind.fitness.valid:
            ind.fitness.values = toolbox.evaluate(ind)
        print(f" Ind{idx}: {int(ind.fitness.values[0])}")

    # Selección por torneo
    padres = toolbox.select(poblacion, len(poblacion))
    hijos = []

    # Cruce y mutación por pares
    for p1, p2 in zip(padres[::2], padres[1::2]):
        # Cruce
        if random.random() < PC:
            o1, o2 = toolbox.mate(p1, p2)
            del o1.fitness.values, o2.fitness.values
        else:
            o1, o2 = creator.Individual(p1), creator.Individual(p2)
        # Mutación
        o1, = toolbox.mutate(o1)
        o2, = toolbox.mutate(o2)
        del o1.fitness.values, o2.fitness.values
        hijos.extend([o1, o2])

    poblacion = hijos

# — Mostrar mejor solución final —
mejor = toolbox.select(poblacion, 1)[0]
if not mejor.fitness.valid:
    mejor.fitness.values = toolbox.evaluate(mejor)
print(f"\n→ Mejor tablero: {mejor}")
print(f"   Conflictos: {int(mejor.fitness.values[0])}")
