import inspect
import os
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir) 

from Snapshots import snapshotgen as ssgen
from Snapshots import snapshotparse as sspar
from NNetwork import life
from NNetwork import neural_network as network

MAX_GENERATIONS = 1
RUNS_PER_IND = 1

al = life.Life()
al.population = network.create_init_population(10, 
                        [
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0
                        ], 
                        ["up", "down", "left", "right"])

# Mutate each network to allow complex parsing and allow internal nodes to be generated
for individual in al.population:
    individual.mutate()

# Generate a snapshot
generator = ssgen.Snapshot(al.population, life.Life.species, network.Network.gene_to_innovation_key)
filename = generator.create_snapshot()


# Generate a world from the snapshot
parser = sspar.Parser(filename)
al_re = parser.build_world()

# Test if they are the same
for index in range(len(al.population)):
    print("\nNetwork " + str(index))
    al.population[index].print_s()
    al_re.population[index].print_s()

os.remove(filename)