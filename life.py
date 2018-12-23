import neural_network as network
from game_environment import game
import copy

#species determined by combination of traits; hidden_layer, hidden_width, and act_func
class Life:
    def __init__(self):
        #Array of all networks regardless of species
        self.individuals = []

        #list of lists. each list has a specific species list
        self.species_list = []
    
    def classify_life(self):
        #goes through all networks in the list. If it does not have a species classify it and assign it to the appropriate list
        pass

    def print_individuals(self):
        #Prints all individuals
        for network in self.individuals:
            network.print_s()
        print()
    
def get_move(active_game, active_network):
    return active_network.feed(active_game.curr_board.matrix)

#Have max heaps (species) of 20 individuals max. At each stage:
#   Mate top 4 perfomers and keep original: +10
#   Keep next top 5 original: +5
#   Mutate Next top 5: +5
#   Disregard 5 lowest performers

all_life = Life()
all_life.individuals = network.create_init_population(20, [
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0
                ], ["up", "down", "left", "right"])
MAX_GENERATIONS = 1


#Run the simulation for MAX_GENERATIONS iterations
for iteration in range(MAX_GENERATIONS):
    #Generate a board to use for all networks
    dummy_game_board = game.Game_Visual()
    init_board = dummy_game_board.curr_board.matrix
    #Test all individuals on the same board
    for individual in all_life.individuals:
        test_game = game.Game_Visual(init_board=init_board.copy())
        individual.fitness = test_game.run(all_life.individuals.index(individual), get_move, test_game, individual)

    #sort the results
    all_life.individuals.sort(key=lambda x: x.fitness, reverse=True)

    #------------Test Print Function--------------#
    all_life.print_individuals()

    #Perform Breeding/Mutating
    new_population = []
    #Mate top 4 performers -> add their 6 childred plus the 4 parents 
    #------------MUTATING NETWORKS BECAUSE BREEDING FUNCTION IS NOT WRITTEN-------#
    for ind_index in range(5):
        new_network = copy.deepcopy(all_life.individuals[ind_index])
        new_population.append(all_life.individuals[ind_index])
        new_population.append(new_network.mutate())
    #Keep next top 5 the same
    for ind_index in range(5, 10):
        new_population.append(all_life.individuals[ind_index])
    #Mutate next top 5:
    for ind_index in range(10, 15):
        new_network = copy.deepcopy(all_life.individuals[ind_index])
        new_population.append(new_network.mutate())
    #Disregard lowest 5 performers


    



