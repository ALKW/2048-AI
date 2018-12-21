import neural_network
from game_environment import game

#species determined by combination of traits; hidden_layer, hidden_width, and act_func
class Life:
    def __init__(self):
        #Array of all networks regardless of species
        self.individuals = []

        #list of lists. each list has a specific species list
        self.species_list = []

    def feed_life(self):
        #Runs all networks through 1 game each and ranks them accordingly within their species
        pass
    
    def classify_life(self):
        #goes through all networks in the list. If it does not have a species classify it and assign it to the appropriate list
        pass
    
def find_move():
    pass

#Have max heaps (species) of 20 individuals max. At each stage:
#   Delete 5 lowest performers: -5 
#   Mate top 5 perfomers and keep original: +15
#   Mutate Next top 5 and keep original: +10

all_life = Life()
all_life.individuals = neural_network.create_init_population_species(20)

test_game = game.Game()
test_game.run()
test_network = neural_network.create_random(act_start=0, act_stop=0)
test_network.print_traits()
print(test_network.feed([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]))

#test_game.run(find_move)

