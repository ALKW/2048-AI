from NNetwork import life
from NNetwork import neural_network as network
from Snapshots import snapshotgen as ssgen

#Used for getting the move of a 2048 board
#Tranlsates the 2048 board to a stimuli to pass to the AI
#The stimuli is a list of the inputs for the board
def get_move_2048(active_game, active_network):
    stimuli = []
    
    for entry in active_game.curr_board.matrix:
        if entry == 0:
            stimuli.append(0)
        else:
            stimuli.append(1)

    other_stimuli = find_moves_2048_board(active_game.curr_board)

    stimuli += other_stimuli
    return active_network.feed(stimuli)

def find_moves_2048_board(board):
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
            to_return.append(2)
        else:
            to_return.append(0)
    
    #For each column, determine if its possible to move
    for column_slice in board.columns:
        column = board.matrix[column_slice]
        if 0 in column:
            to_return.append(1)
        elif can_move(column):
            to_return.append(2)
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


MAX_GENERATIONS = 1
RUNS_PER_IND = 5

all_life = life.Life()
all_life.population = network.create_init_population(30, 
                [
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0
                ], ["up", "down", "left", "right"])

all_life.run(MAX_GENERATIONS, RUNS_PER_IND, get_move_2048)

all_life.run_visualization(1, get_move_2048)

all_life.print_top_performers()

print("\nGene Key:", network.Network.innovation_to_gene_key, "\n")

print("Species Key:", life.Life.species, "\n")

all_life.print_species_info()

generator = ssgen.snapshot(all_life.population, all_life.species, network.Network.gene_to_innovation_key)
generator.create_snapshot()