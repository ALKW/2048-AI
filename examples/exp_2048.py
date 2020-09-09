"""
An example use of the library for the game 2048

Each network plays the game 2048

The training lasts for 10 generations and each network in a generation is run 5 times.
The average is taken of the 5 runs and that is the fitness score for that network in
that generation.

After the training is done, the top 2 networks are run visually so the user can see it
It also prints the genes, and species info of all species that were created duing training

It then generates a snapshot for later use
"""

import sys
import os
import pygame.font as font

sys.path.append(os.getcwd())
sys.path.append("..")

import nnetwork.life as life
import nnetwork.neural_network as network

import snapshots.snapshotgen as ssgen
import snapshots.snapshotparse as sspar

import examples.game_2048.game_AI as game

########################### HELPER FUNCTIONS ################################

def get_move_2048(active_game, active_network):
    '''
    Function to be passed to the game loop that gets the move for the game. It loads the state and
    adds extra based on move status to a total of 24 input nodes

    Args:
        active_game - (Game) - The current game object from which we can read the board
        active_network - (Network) - The current network running the game
    Returns:
        (type) - purpose
    Raises:
        None
    '''
    stimuli = []

    for entry in active_game.curr_board.matrix:
        if entry == 0:
            stimuli.append(0)
        else:
            stimuli.append(1)

    other_stimuli = find_moves_2048_board(active_game.curr_board)

    stimuli += other_stimuli

    # Feed the stimuli into the network and get back the coresponding move for it
    results = active_network.feed(stimuli)

    # Analyze the effectiveness of the move
    fitness_change, move = analyze_move(results, active_game)

    # Add to the fitness of the network
    active_network.fitness += fitness_change

    # Return the highest picked move
    return move

def analyze_move(results, active_game):
    '''
    Analyzes the results and determines the effectiveness (additional fitness) of the move.

    Args:
        results - (tuple) - results of the neural network move passed in
    Returns:
        (int) - the additional fitness to be added to the network
    Raises:
        None
    '''
    max_nodes = results[network.Network.MAX_NODES]
    all_nodes = results[network.Network.ALL_NODES]

    # Adjusting this changes how much fitness is added after each move
    fitness_const = 5

    # Base fitness that is subtracted from based on move rank
    base_fitness = fitness_const * len(network.Network.outputs)

    # Try out all the moves and determine the fitness based on the rank of the move
    for node_index, _ in enumerate(all_nodes):
        move = all_nodes[node_index].desc

        if active_game.curr_board.is_valid(move):
            # Based on the rank of the move
            add_fitness = base_fitness - node_index * fitness_const

            # Adjust based on if the max rank move was tied
            if len(max_nodes) > 1:
                add_fitness -= base_fitness

            # If we find a move that works, then leave
            curr_move = all_nodes[node_index].desc
            break

    return add_fitness, curr_move

def find_moves_2048_board(curr_board):
    '''
    Classifies the rows and columns of the matrix with a 1 if there is an available move and 0 if
    there isnt

    Args:
        curr_board (Board Object) - the current game board object
    Returns:
        stimuli (list) - the results of the algorithm, the first four are the rows and the last
        four are the columns
    Raises:
        None
    '''
    to_return = []
    # For each row, determine if its possible to move
    for row_slice in curr_board.ROWS:
        row = curr_board.matrix[row_slice]
        if 0 in row:
            to_return.append(1)
        elif curr_board.can_move_at_line(row):
            to_return.append(2)
        else:
            to_return.append(0)

    # For each column, determine if its possible to move
    for column_slice in curr_board.COLUMNS:
        column = curr_board.matrix[column_slice]
        if 0 in column:
            to_return.append(1)
        elif curr_board.can_move_at_line(column):
            to_return.append(2)
        else:
            to_return.append(0)

    return to_return

def game_loop(identifier, individual):
    '''
    The game loop for the system that is used for training. The game is not shown during this to
    save resources. This loop is simple due to the custom implementation of the game 2048.
    An ideal loop would be a function that runs in a loop until loss, that is able to read the
    current state inbetween each move

    Args:
        identifier - (int) - identifier of the network. In this case the index in the population
        individual - (Network) - The current neural network being run
    Returns:
        (int) - The fitness for the network
    Raises:
        None
    '''
    test_game = game.Game(init_board=INIT_BOARD.copy())
    individual.identifier = identifier
    return test_game.run(individual, get_move_2048)

def game_loop_vis(identifier, individual):
    '''
    A special version of the game loop for the system that displays the game itself
    This loop is simple due to the custom implementation of the game 2048.
    An ideal loop would be a function that runs in a loop until loss, that is able to read the
    current state inbetween each move

    Args:
        identifier - (int) - identifier of the network. In this case the index in the population
        individual - (Network) - The current neural network being run
    Returns:
       (int) - The fitness for the network
    Raises:
        None
    '''
    test_game = game.GameVisual(init_board=INIT_BOARD.copy())
    individual.identifier = identifier
    return test_game.run_vis(individual, get_move_2048, add_vis)

def add_vis(game_v_obj, screen, individual):
    '''
    The function to be passed to the game visualization loop that prints additional informaiton
    including the fitness, the current network topology and the identifier

    Args:
        None
    Returns:
        None
    Raises:
        None
    '''
    draw_title(game_v_obj, screen, individual)
    draw_fitness(game_v_obj, screen, individual)
    draw_network_topology(game_v_obj, screen, individual)

def draw_title(game_v_obj, screen, individual):
    '''
    Draws the title on the game screen

    Args:
        game_v_obj - (GameVisual) - the game ovject itself so we can add features to it
        screen - (Pygame.screen) - the screen object that we draw on
        individual (Network) - the active network being run
    Returns:
        None
    Raises:
        None
    '''
    text_font = font.SysFont('Arial', 15)
    title = text_font.render("Network: " + str(individual.identifier), True, game.Game.BLACK)
    title_width = title.get_rect().width
    screen.blit(title, (game_v_obj.width // 2 - title_width / 2, 0))

def draw_fitness(game_v_obj, screen, individual):
    '''
    Draws the fitness of the network on the game screen

    Args:
        game_v_obj - (GameVisual) - the game ovject itself so we can add features to it
        screen - (Pygame.screen) - the screen object that we draw on
        individual (Network) - the active network being run
    Returns:
        None
    Raises:
        None
    '''
    text_font = font.SysFont('Arial', 15)
    fitness_title = text_font.render("Fitness: " + str(individual.fitness), True, game.Game.BLACK)
    fitness_width = fitness_title.get_rect().width
    screen.blit(fitness_title, (game_v_obj.width - (fitness_width + 10), 0))

def draw_network_topology(game_v_obj, screen, individual):
    pass


######################## SCRIPT START ##########################
MAX_GENERATIONS = 50
RUNS_PER_IND = 5
MAX_POPULATION = 100
MAX_PER_SPECIES = 20
NUM_VIS_IND = 1
LIFE_PARAMS = (MAX_GENERATIONS, RUNS_PER_IND, MAX_POPULATION, MAX_PER_SPECIES)

# Initialize the game
DUMMY_GAME = game.Game()
INIT_BOARD = DUMMY_GAME.curr_board.matrix

# Determine if we are loading from a snapshot
if len(sys.argv) >= 2:
    PARSER = sspar.Parser(sys.argv[1])
    PARSER.build_world()
    exit()
else:
    ALL_LIFE = life.Life()
    ALL_LIFE.population = network.create_init_population(30,
                                                         [
                                                             0, 0, 0, 0,
                                                             0, 0, 0, 0,
                                                             0, 0, 0, 0,
                                                             0, 0, 0, 0,
                                                             0, 0, 0, 0,
                                                             0, 0, 0, 0
                                                         ],
                                                         ["up", "down", "left", "right"])

# Run the training
ALL_LIFE.run(game_loop, life_params=LIFE_PARAMS)

# Run the top networks to show off results
ALL_LIFE.run_visualization(game_loop_vis, amount=NUM_VIS_IND)

# Print the top performers
ALL_LIFE.print_top_performers()

# Print all the genes
ALL_LIFE.print_genes()

# Print all the species
ALL_LIFE.print_species_info()

# Generate a snapshot after the current run ends
GENERATOR = ssgen.Snapshot(ALL_LIFE.population, life.Life.species,
                           network.Network.gene_to_innovation_key)
GENERATOR.create_snapshot()
