import neural_network as network
from game_environment import game
import copy

#species determined by combination of traits; hidden_layer, hidden_width, and act_func
class Life:
    def __init__(self):
        #Array of all networks regardless of species
        self.individuals = []

        #list of lists. each list has a specific species list. 
        # Species are determined by 2 most popular moves when a specific board is fed in
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
        '''
        #-----------------Print the network details--------
        print("Network:", all_life.individuals.index(individual) + 1, " | Fitness:", individual.fitness)
        '''

    #sort the results to get the highest performers ranked at the top
    all_life.individuals.sort(key=lambda x: x.fitness, reverse=True)

    '''
    #------------Test Print Function--------------#
    all_life.print_individuals()
    '''

    print("Finished Generation:", iteration + 1)

    #Keep track of top performers from each generation for analytic purposes
    top_performer = "Generation: " + str(iteration + 1) + " | Max Score: " + str(all_life.individuals[0].fitness)
    top_performers.append(top_performer)

    #Perform Breeding/Mutating
    new_population = []
    
    #Mate top 5 performers -> add their 10 childred plus the 5 parents 
    for first_index in range(5):
        #Append first parent in the pair
        new_population.append(all_life.individuals[first_index])

        for second_index in range(first_index + 1, 4):
            #Create and append the child in the pair
            child = all_life.individuals[first_index].breed_with(all_life.individuals[second_index])
            new_population.append(child)
        
         
    #------------MUTATE NETWORKS-------#
    for ind_index in range(5, 20):
        new_network = copy.deepcopy(all_life.individuals[ind_index])
        new_network.mutate()
        new_population.append(new_network)

    #Disregard The rest

    #Create new population
    all_life.individuals = new_population


#Run a visualization through the top 5 networks
print("--------------------- PRINTING TOP 5 ---------------------")
dummy_game = game.Game()
init_board = dummy_game.curr_board.matrix
for individual in all_life.individuals[:5]:
    test_game = game.Game_Visual(init_board=init_board.copy())
    print("-----------NETWORK ", all_life.individuals.index(individual) + 1,"-------------")
    '''
    individual.fitness = test_game.run(all_life.individuals.index(individual) + 1, get_move, individual)
    print()
    '''
    individual.print()


#Print the highest results from each generation and the results from the latest generation
all_life.individuals.sort(key=lambda x: x.fitness, reverse=True)
print("Latest Generation:")
all_life.print_individuals()
print("Top performers from each generation:")
for performer in top_performers:
    print(performer)
