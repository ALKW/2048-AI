import neural_network as network
from game_environment import game

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
    
def get_move(active_game, active_network):
    return active_network.feed(active_game.curr_board.matrix)

#Have max heaps (species) of 20 individuals max. At each stage:
#   Delete 5 lowest performers: -5 
#   Mate top 5 perfomers and keep original: +15
#   Mutate Next top 5 and keep original: +10

all_life = Life()
all_life.individuals = network.create_init_population(20, [
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0
                ], ["up", "down", "left", "right"])
MAX_GENERATIONS = 10


#Run the simulation for MAX_GENERATIONS iterations
for iterations in range(MAX_GENERATIONS):
    #Generate a board to use for all networks
    dummy_game_board = game.Game()
    init_board = dummy_game_board.curr_board.matrix
    #Test all individuals on the same board
    for individual in all_life.individuals:
        test_game = game.Game(init_board=init_board.copy())
        individual.fitness = test_game.run(get_move, test_game, individual)

    #sort the results
    all_life.individuals.sort(key=lambda x: x.fitness, reverse=True)

    #------------Test Print Function--------------#
    all_life.print_individuals()

    #Delete lowest 5 performers, 
    #Mate top 5 performers -> add their 10 childred plus the 5 parents, 
    #Mutate next top 5 and keep the original
    



