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
    #Compute extra stimuli apart from board
    inbetween = []
    return active_network.feed(active_game.curr_board.matrix + inbetween)

#Have max heaps (species) of 20 individuals max. At each stage:
#   Mate top 4 perfomers and keep original: +10
#   Keep next top 5 original: +5
#   Mutate Next top 5: +5
#   Disregard 5 lowest performers

#Let input neurons be the board, the rows if a move is available, and the columns if a move is available

all_life = Life()
all_life.individuals = network.create_init_population(20, [
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,


                ], ["up", "down", "left", "right"])
MAX_GENERATIONS = 50
RUNS_PER_IND = 5
top_performers = []

#Run the simulation for MAX_GENERATIONS iterations with a population size of 20
for iteration in range(MAX_GENERATIONS):
    #Generate a board to use for all networks
    dummy_game = game.Game()
    init_board = dummy_game.curr_board.matrix
    #Test all individuals on the same board
    for individual in all_life.individuals:
        run_total = 0
        for run in range(RUNS_PER_IND):
            test_game = game.Game(init_board=init_board.copy())
            run_total += test_game.run(all_life.individuals.index(individual), get_move, individual)
            individual.fitness = run_total // RUNS_PER_IND
        #-----------------print("Network:", all_life.individuals.index(individual) + 1, " | Fitness:", individual.fitness)

    #sort the results to get the highest performers ranked at the top
    all_life.individuals.sort(key=lambda x: x.fitness, reverse=True)

    #------------Test Print Function--------------#
    #------------all_life.print_individuals()
    print("Finished Generation:", iteration + 1)

    #Keep track of top performers from each generation for analytic purposes
    top_performer = "Generation: " + str(iteration + 1) + " | Max Score: " + str(all_life.individuals[0].fitness)
    top_performers.append(top_performer)

    #Perform Breeding/Mutating
    new_population = []
    #Mate top 4 performers -> add their 6 childred plus the 4 parents 
    #------------MUTATING NETWORKS BECAUSE BREEDING FUNCTION IS NOT WRITTEN-------#
    for ind_index in range(5):
        new_network = copy.deepcopy(all_life.individuals[ind_index])
        new_population.append(all_life.individuals[ind_index])
        new_network.mutate()
        new_population.append(new_network)
    #Keep next top 5 the same
    for ind_index in range(5, 10):
        new_population.append(all_life.individuals[ind_index])
    #Mutate next top 5:
    for ind_index in range(10, 15):
        new_network = copy.deepcopy(all_life.individuals[ind_index])
        new_network.mutate()
        new_population.append(new_network)
    #Disregard lowest 5 performers
    #Create new population
    all_life.individuals = new_population

'''
#Testing without using darwinism
#Run iterations where we mutate all networks
for iteration in range(MAX_GENERATIONS):
    dummy_game = game.Game()
    init_board = dummy_game.curr_board.matrix
    for individual in all_life.individuals:
        test_game = game.Game(init_board=init_board.copy())
        individual.fitness = test_game.run(all_life.individuals.index(individual), get_move, individual)
        individual.mutate()
'''


#Run a visualization through the top 5 networks
print("--------------------- PRINTING TOP 5 ---------------------")
dummy_game = game.Game()
init_board = dummy_game.curr_board.matrix
for individual in all_life.individuals[:5]:
    test_game = game.Game_Visual(init_board=init_board.copy())
    print("-----------NETWORK ", all_life.individuals.index(individual) + 1,"-------------")
    individual.fitness = test_game.run(all_life.individuals.index(individual) + 1, get_move, individual)
    print()
    individual.print()

#sort the results to get the highest performers ranked at the top
all_life.individuals.sort(key=lambda x: x.fitness, reverse=True)
print("Latest Generation:")
all_life.print_individuals()
print("Top performers from each generation:")
for performer in top_performers:
    print(performer)