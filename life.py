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

    def run(self, MAX_GENERATIONS, RUNS_PER_IND):
        #Run the simulation for MAX_GENERATIONS iterations with a population size of 20
        for iteration in range(MAX_GENERATIONS):
            #Generate a board to use for all networks
            dummy_game = game.Game()
            init_board = dummy_game.curr_board.matrix

            #Test all individuals on the same board for consistency
            for individual in self.individuals:
                run_total = 0
                for ind_run in range(RUNS_PER_IND):
                    test_game = game.Game(init_board=init_board.copy())
                    run_total += test_game.run(self.individuals.index(individual), get_move, individual)
                    individual.fitness = run_total // RUNS_PER_IND

            #sort the results to get the highest performers ranked at the top
            self.individuals.sort(key=lambda x: x.fitness, reverse=True)

            print("Finished Generation:", iteration + 1)

            #Classify each new network species
            self.classify_life()

            #fill in generation numbers
            for individual in self.individuals:
                if individual.generation == -1:
                    individual.generation = iteration

            #Keep track of top performers from each generation for analytic purposes
            top_performer = "Generation: " + str(iteration + 1) +  " | Max Fitness: " + str(self.individuals[0].fitness) + " | Species: " + str(self.individuals[0].species)
            self.top_performers.append(top_performer)

            #IF we reach the last generation, then break
            if iteration == (MAX_GENERATIONS - 1):
                return
            #Otherwise mate and mutate the population by species. Take top 100 to keep population low
            else:
                self.mutate_population()

            #Classify each new network species that was added
            self.classify_life()

    def mutate_population(self):
        '''
        mutates/breeds the appropriate members of the population

        Each species has its own heap and all members of the population are sorted into
        the heaps through the classify_life() method
       
        Have max heaps (species) of 20 individuals max. At each stage:
            -Mate top 4 perfomers and keep original: +10
            -Keep next top 5 original: +5
            -Mutate Next top 5: +5
            -Disregard 5 lowest performers
        '''
        MAX_PER_SPECIES = 20
        MAX_POPULATION = 100

        #Perform Breeding/Mutating
        new_population = []

        #Used for classifying species within the current population
        species = [[] for x in range(len(Life.species))]
        total_fitness = [0 for x in range(len(Life.species))]
        avg_fitness = [0 for x in range(len(Life.species))]

        #Sort life based on species, then breed/mutate all the species 
        #Keep track of the average fitness for each species
        for network in self.individuals:
            #Add the network to the apporpriate species index
            species_key = network.species
            species[species_key].append(network)
            total_fitness[species_key] += network.fitness

        #Get the average fitness for each species
        for species_index in range(len(species)):
            #If there are no individuals of the species, then disregard it
            if len(species[species_index]) == 0:
                continue

            #Compute the average fitness for the species
            avg_fitness[species_index] = total_fitness[species_index] // len(species[species_index])

        #mutate/breed each species
        for species_t in species:
            #Determine if there are enough members in the species to mate
            mate_max = min(4, len(species_t))
            num_made = 0

            #Mate up to top 4 performers (less if the species doesnt have enough) 
            #-> add their children (max 6) plus the parents (max 4) 
            #-> result is up to 10 networks for the species
            for first_index in range(mate_max):
                #Append first parent in the pair. Because each parent is first at some point we append them all
                new_population.append(species_t[first_index])

                #Mate that network with all other networks it hasnt mated with yet within its species
                for second_index in range(first_index + 1, mate_max):
                    #Create and append the child in the pair
                    child = species_t[first_index].breed_with(species_t[second_index])

                    #set the initial fitness to the average fitness for the species
                    child.fitness = avg_fitness[species.index(species_t)]

                    #Add the child to the new population
                    new_population.append(child)
                    num_made += 1
            
            #The last index in species_t to mutate
            mutate_max = min(len(species_t), mate_max + (MAX_PER_SPECIES - num_made))

            #Mutate the rest of the network so that there is up to 20 individuals made for the new population
            for ind_index in range(mate_max, mutate_max):
                species_t[ind_index].mutate()
                new_population.append(species_t[ind_index])
                num_made += 1

            #Disregard The rest of the species so as not to poplute with 1 species

        #Sort the new population by fitness.
        #Children have fitness equal to the average fitness of their species
        new_population.sort(key=lambda x: x.fitness, reverse=True)

        #Create new population by taking up to the top 100 individuals in the newly generated population
        max_individuals = min(MAX_POPULATION, len(new_population))

        self.individuals = new_population[:max_individuals]
    
    def classify_life(self):
        ''''
        Classifies the species of all networks
        '''
        #goes through all networks in the list. 
        #If it does not have a species classify it and assign it to the appropriate list
        for network in self.individuals:
            #Classify the network if it hasnt been classified yet
            if network.species == -1:
                network.species = self.classify_network(network)
    
    def classify_network(self, network):
        '''
        Finds the species for the network
        '''
        count = 0
        for species_key in Life.species:
            species_genes = species_key.split()

            #Go through the genes and determine the percentage of matches
            for gene in species_genes:
                #If gene is in the network then increase match percentage
                if int(gene) in network.genes:
                    count += 1

                #If over 50% match then the network is of that species
                if count >= len(network.genes) // 2:
                    self.species_list[Life.species[species_key]].append(network)
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
        self.species_list.append([network])

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

    def print_species_info(self):
        print("All Species:")
        for species in self.species_list:
            print("Species ", self.species_list.index(species), "- Population size: ", len(species), " || ", end="")
    
def get_move(active_game, active_network):
    stimuli = []
    
    for entry in active_game.curr_board.matrix:
        if entry == 0:
            stimuli.append(0)
        else:
            stimuli.append(1)

    other_stimuli = find_moves_board(active_game.curr_board)

    stimuli += other_stimuli
    return active_network.feed(stimuli)

def find_moves_board(board):
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


MAX_GENERATIONS = 50
RUNS_PER_IND = 5

all_life = Life()
all_life.individuals = network.create_init_population(30, [
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0,
                0,0,0,0
                ], ["up", "down", "left", "right"])

all_life.run(MAX_GENERATIONS, RUNS_PER_IND)

all_life.run_visualization(1)

all_life.print_top_performers()

print("\nGene Key:", network.Network.innovation_to_gene_key, "\n")

print("Species Key:", Life.species, "\n")

all_life.print_species_info()
