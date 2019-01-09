import neural_network as network
from game_environment import game
import copy

#species determined by combination of traits; hidden_layer, hidden_width, and act_func
class Life:
    def __init__(self):
        #Array of all networks regardless of species
        self.individuals = []

        #list of lists. each list has a specific species list. 
        #Species are determined by 2 most popular moves when a specific board is fed in
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
            new_network = copy.deepcopy(self.individuals[ind_index])
            new_network.mutate()
            new_population.append(new_network)
        #Disregard The rest

        #Create new population
        self.individuals = new_population
    
    def classify_life(self):
        ''''
        Classications:
           -----2 most prevelant output descriptions-----
           - up, down: 0
           - up, left: 1
           - up, right: 2
           - down, left: 3
           - down, right: 4
           - left, right: 5
           ------tie between output descriptions (3 descriptions are needed)-----
           - up, down, left : 6
           - up, down, right: 7
           - up, left, right: 8
           - down, left, right: 9
           -----Tie between all 4 descriptions-------
           - up, down, left, right: 10
        '''
        #goes through all networks in the list. 
        #If it does not have a species classify it and assign it to the appropriate list
        for network in self.individuals:
            if network.species == -1:
                network.species = self.classify_network(network)
    
    def classify_network(self, network):
        paths = []
        #Gets all the neuron paths in the network
        for input_node in network.inputs:
            result = network.find_paths(input_node, [], [x.desc for x in network.outputs], [])
            if result != None:
                paths += result

        #Counts how many paths end in a certain output node
        output_count = [0 for x in network.outputs]
        poss_outputs = [x.desc for x in network.outputs]
        #For each path increase the corresponding output associated with it
        for path in paths:
            output_node_desc = path[-1].desc
            inc_index = poss_outputs.index(output_node_desc)
            output_count[inc_index] += 1

        #Determine the species number
        species = self.determine_species_number(output_count, poss_outputs)

        return species
    
    def determine_species_number(self, output_count, poss_outputs):
        VALUE = 0
        DESC = 1
        max_outputs = []
        #classify the spec7ies according to the outputs
        output_results = [[output_count[x], poss_outputs[x]] for x in range(len(output_count))]
        #Sort the results
        output_results.sort(key=lambda x: x[0], reverse=True)
        #Find the maxes
        max_outputs.append(output_results[0])
        max_outputs.append(output_results[1])
        
        #Determine if other maxes exist
        if output_results[2][VALUE] == max_outputs[1][VALUE]:
            max_outputs.append(output_results[2])

        if output_results[3][VALUE] == max_outputs[1][VALUE]:
            max_outputs.append(output_results[3])

        #Sort the max outputs by lexicographical order to help classification
        max_outputs.sort(key=lambda x: x[DESC][0])

        key = ""
        for output in max_outputs:
            key += output[DESC]
        
        return self.SPECIES_KEY[key], key

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
MAX_GENERATIONS = 100
RUNS_PER_IND = 5

all_life.run(MAX_GENERATIONS, RUNS_PER_IND)

all_life.run_visualization(5)

all_life.print_top_performers()
