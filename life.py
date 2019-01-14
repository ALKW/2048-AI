import neural_network as network
from game_environment import game
import copy

#species determined by combination of traits; hidden_layer, hidden_width, and act_func
class Life:
    #Dictionary for classifying species. If 50%+ of the genes match the original creator of the species, then that species is the same.
    #The key is all of the genes of the founding network with each gene separated by a space
    #If the species doesnt match any then a new species is created 
    species = dict()
    #The next available number to assign to a species
    curr_species_num = 0
    def __init__(self):
        #Array of all networks regardless of species
        self.individuals = []

        #list of lists. each list has a specific species list. 
        self.species_list = []

        #List of top performers from each generation
        self.top_performers = []

        self.SPECIES_KEY = dict()
        self.SPECIES_KEY["downup"] = 0
        self.SPECIES_KEY["leftup"] = 1
        self.SPECIES_KEY["rightup"] = 2
        self.SPECIES_KEY["downleft"] = 3
        self.SPECIES_KEY["downright"] = 4
        self.SPECIES_KEY["leftright"] = 5
        self.SPECIES_KEY["downleftup"] = 6
        self.SPECIES_KEY["downrightup"] = 7
        self.SPECIES_KEY["leftrightup"] = 8
        self.SPECIES_KEY["downleftright"] = 9
        self.SPECIES_KEY["downleftrightup"] = 10

    def run(self, MAX_GENERATIONS, RUNS_PER_IND):
        #Run the simulation for MAX_GENERATIONS iterations with a population size of 20
        for iteration in range(MAX_GENERATIONS):
            #Generate a board to use for all networks
            dummy_game = game.Game()
            init_board = dummy_game.curr_board.matrix
            #Test all individuals on the same board
            for individual in self.individuals:
                run_total = 0
                for run in range(RUNS_PER_IND):
                    test_game = game.Game(init_board=init_board.copy())
                    run_total += test_game.run(self.individuals.index(individual), get_move, individual)
                    individual.fitness = run_total // RUNS_PER_IND
                '''
                #-----------------Print the network details--------
                print("Network:", self.individuals.index(individual) + 1, " | Fitness:", individual.fitness)
                '''

            #sort the results to get the highest performers ranked at the top
            self.individuals.sort(key=lambda x: x.fitness, reverse=True)

            '''
            #------------Test Print Function--------------#
            self.print_individuals()
            '''

            print("Finished Generation:", iteration + 1)

            #Classify each new network species
            self.classify_life()

            #fill in generation numbers
            for individual in self.individuals:
                if individual.generation == -1:
                    individual.generation = iteration

            #Keep track of top performers from each generation for analytic purposes
            top_performer = "Generation: " + str(iteration + 1) +  " | Max Score: " + str(self.individuals[0].fitness) + " | Species: " + str(self.individuals[0].species)
            self.top_performers.append(top_performer)

            #IF we reach the last generation, then break
            if iteration == (MAX_GENERATIONS - 1):
                return
            else:
                self.mutate_population()

    def mutate_population(self):
        '''
        mutates/breeds the appropriate members of the population
        '''
        #Perform Breeding/Mutating
        new_population = []
        
        #Mate top 5 performers -> add their 10 childred plus the 5 parents 
        for first_index in range(5):
            #Append first parent in the pair
            new_population.append(self.individuals[first_index])
            for second_index in range(first_index + 1, 5):
                #Create and append the child in the pair
                child = self.individuals[first_index].breed_with(self.individuals[second_index])
                new_population.append(child)
            
            
        #------------MUTATE NETWORKS-------#
        for ind_index in range(5, 20):
            self.individuals[ind_index].mutate()
            new_population.append(self.individuals[ind_index])
        #Disregard The rest

        #Create new population
        self.individuals = new_population
    
    def classify_life(self):
        ''''
        Classifies the species of all networks
        '''
        #goes through all networks in the list. 
        #If it does not have a species classify it and assign it to the appropriate list
        for network in self.individuals:
            if network.species == -1:
                network.species = self.classify_network(network)
    
    def classify_network(self, network):
        '''
        Finds the species for the network
        '''
        count = 0
        for species_key in Life.species:
            genes = species_key.split()
            #Go through the genes and determine the percentage of matches
            for gene in genes:
                #If gene is in the network then increase match percentage
                if gene in network.genes:
                    count+= 1
                #If over 50% match then the network is of that species
                if count >= len(species_key) // 2:
                    return Life.species[species_key]
            #If we make it through reset
            count = 0

        #If we make it through all species without a classification, then this is a new species
        #Create the key for the new species
        species_key = ""
        for gene in network.genes[:-1]:
            species_key += str(gene) + " "
        species_key += str(network.genes[-1])

        #Create the new key and add it to the dictionary
        Life.species[species_key] = Life.curr_species_num
        #Increment to the next available number
        Life.curr_species_num += 1

        return Life.species[species_key]

    def run_visualization(self, amount):
        #Run a visualization through the top 5 networks
        if amount > len(self.individuals):
            print("Not Valid, exceeds individual count")
            return
        
        print("--------------------- PRINTING TOP ", amount, "---------------------")
        dummy_game = game.Game()
        init_board = dummy_game.curr_board.matrix
        for individual in self.individuals[:amount]:
            test_game = game.Game_Visual(init_board=init_board.copy())
            print("-----------NETWORK ", self.individuals.index(individual) + 1,"-------------")
            individual.fitness = test_game.run(self.individuals.index(individual) + 1, get_move, individual)
            print()
            individual.print()

    def print_top_performers(self):
        #Print the highest results from each generation and the results from the latest generation
        self.individuals.sort(key=lambda x: x.fitness, reverse=True)
        print("Top performers from each generation:")
        for performer in self.top_performers:
            print(performer)

    def print_individuals(self):
        #Prints all individuals
        print("Latest Generation:")
        for network in self.individuals:
            network.print_s()
        print()
    
def get_move(active_game, active_network):
    stimuli = []
    
    for entry in active_game.curr_board.matrix:
        if entry == 0:
            stimuli.append(0)
        else:
            stimuli.append(1)

    other_stimuli = classify_board(active_game.curr_board)

    stimuli += other_stimuli
    return active_network.feed(stimuli)

def classify_board(board):
    '''
    classifies the rows and columns of the matrix with a 1 if there is an available move and 0 if there isnt
    Args:
        board (Board Object) - the current game board object
    Returns:
        stimuli (list) - the results of the algorithm, the first four are the rows and the last four are the columns
    Raises:
        None
    '''
    to_return = []
    #For each row, determine if its possible to move
    for row_slice in board.rows:
        row = board.matrix[row_slice]
        if 0 in row:
            to_return.append(1)
        elif can_move(row):
            to_return.append(1)
        else:
            to_return.append(0)
    
    #For each column, determine if its possible to move
    for column_slice in board.columns:
        column = board.matrix[column_slice]
        if 0 in column:
            to_return.append(1)
        elif can_move(column):
            to_return.append(1)
        else:
            to_return.append(0)
    
    return to_return

def can_move(data):
    curr = data[0]
    for entry in data[1:]:
        if curr == entry:
            return True
        else:
            curr = entry
    return False

#Have max heaps (species) of 20 individuals max. At each stage:
#   Mate top 4 perfomers and keep original: +10
#   Keep next top 5 original: +5
#   Mutate Next top 5: +5
#   Disregard 5 lowest performers

#Let input neurons be the board, the rows if a move is available, and the columns if a move is available

all_life = Life()
all_life.individuals = network.create_init_population(30, [
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0
                ], ["up", "down", "left", "right"])
MAX_GENERATIONS = 10
RUNS_PER_IND = 5

all_life.run(MAX_GENERATIONS, RUNS_PER_IND)

all_life.run_visualization(5)

all_life.print_top_performers()

print("Gene Key:", network.Network.gene_key, "\n")

print("Species Key:", Life.species)
