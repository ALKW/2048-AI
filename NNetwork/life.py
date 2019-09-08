import copy
import sys
from NNetwork import neural_network as network

class Life:
    # Dictionary for classifying species. If 50%+ of the genes match the original creator of the species, then that species is the same.
    # The key is the sequence of genes for network with each gene separated by a space
    # If the species doesnt match any then a new species is created 
    species = dict()

    # The next available number to assign to a species
    curr_species_num = 0

    def __init__(self, population=[], species_list=[], top_performers=[]):
        # Array of all networks regardless of species
        self.population = population

        # list of lists. each list has a specific species list. 
        self.species_list = species_list

        # List of top performers from each generation
        self.top_performers = top_performers

    def run(self, game_loop, MAX_GENERATIONS=1, RUNS_PER_IND=1, ):
        '''
        Runs each network in the population a certain number of times

        MAX_GENERATIONS defines the number of times the whole population gets ran

        RUNS_PER_IND defines the number of times each member of the population is ran per generation

        game_loop is a method defined by the user that the game runs. Within the game loop, there should be:
            Something to get the current game state
            Something that serializes the current game state to an array of integers
            Something that calls 'individual.feed' where 
                - individual is a neural network object
                - individual is an argument passed to the game_loop method
                - 'individual.feed' will return one of the strings the user specified earlier
            Something that takes the return value of 'individual.feed' of the move and executes it in the game
            Something that checks for an exit condition of the game and exits the game loop once the condition is met
            Something that returns a score of the game and if the user prefers translates that score to a fitness for the network
        '''
        # Run the simulation for MAX_GENERATIONS iterations with a population size of 20
        for iteration in range(MAX_GENERATIONS):
            # Test each memeber of the population
            for individual in self.population:
                run_total = 0

                #Run the individual through a number of games to get an average fitness
                for _ in range(RUNS_PER_IND):
                    # Give a unique identifier (An index in the list of members in the population) and pass the network object to the game loop
                    run_total += game_loop(self.population.index(individual), individual)
                
                # Assign the average fitness to the network
                individual.fitness = run_total // RUNS_PER_IND

            # Sort the results to get the highest performers ranked at the top
            self.population.sort(key=lambda x: x.fitness, reverse=True)

            print("Finished Generation:", iteration + 1)
            sys.stdout.flush()

            # Classify each new network species
            self.classify_life()

            # Fill in generation numbers
            for individual in self.population:
                if individual.generation == -1:
                    individual.generation = iteration

            # Keep track of top performers from each generation for analytic purposes
            top_performer = "Generation: " + str(iteration + 1) +  " | Max Fitness: " + str(self.population[0].fitness) + " | Species: " + str(self.population[0].species)
            self.top_performers.append(top_performer)

            # IF we reach the last generation, then break
            if iteration == (MAX_GENERATIONS - 1):
                return
            # Otherwise mate and mutate the population by species. Take top 100 to keep population low
            else:
                self.mutate_population()

            # Classify each new network species that was added
            self.classify_life()

    def mutate_population(self):
        '''
        mutates/breeds the appropriate members of the population

        Each species has its own sorted array and all members of the population are 
        sorted through the classify_life() method
       
        Have sorted lists (species) of 20 individuals max. At each stage:
            -Mate top 4 perfomers and keep original: +10
            -Keep next top 5 original: +5
            -Mutate Next top 5: +5
            -Disregard 5 lowest performers
        '''
        MAX_PER_SPECIES = 20
        MAX_POPULATION = 100

        # Perform Breeding/Mutating
        new_population = []

        # Used for classifying species within the current population
        species = [[] for x in range(len(Life.species))]
        total_fitness = [0 for x in range(len(Life.species))]
        avg_fitness = [0 for x in range(len(Life.species))]

        # Sort life based on species, then breed/mutate all the species 
        # Keep track of the average fitness for each species
        for network in self.population:
            # Add the network to the apporpriate species index
            species_key = network.species
            species[species_key].append(network)
            total_fitness[species_key] += network.fitness

        # Get the average fitness for each species
        for species_index in range(len(species)):
            #If there are no individuals of the species, then disregard it
            if len(species[species_index]) == 0:
                continue

            # Compute the average fitness for the species
            avg_fitness[species_index] = total_fitness[species_index] // len(species[species_index])

        # mutate/breed each species
        for species_t in species:
            # Determine if there are enough members in the species to mate
            mate_max = min(4, len(species_t))
            num_made = 0

            # Mate up to top 4 performers (less if the species doesnt have enough) 
            # -> add their children (max 6) plus the parents (max 4) 
            # -> result is up to 10 networks for the species
            for first_index in range(mate_max):
                # Append first parent in the pair. Because each parent is first at some point we append them all
                new_population.append(species_t[first_index])

                # Mate that network with all other networks it hasnt mated with yet within its species
                for second_index in range(first_index + 1, mate_max):
                    # Create and append the child in the pair
                    child = species_t[first_index].breed_with(species_t[second_index])

                    # set the initial fitness to the average fitness for the species
                    child.fitness = avg_fitness[species.index(species_t)]

                    # Add the child to the new population
                    new_population.append(child)
                    num_made += 1
            
            # The last index in species_t to mutate
            mutate_max = min(len(species_t), mate_max + (MAX_PER_SPECIES - num_made))

            # Mutate the rest of the network so that there is up to 20 individuals made for the new population
            for ind_index in range(mate_max, mutate_max):
                species_t[ind_index].mutate()
                new_population.append(species_t[ind_index])
                num_made += 1

            # Disregard The rest of the species so as not to poplute with 1 species

        # Sort the new population by fitness.
        # Children have fitness equal to the average fitness of their species
        new_population.sort(key=lambda x: x.fitness, reverse=True)

        # Create new population by taking up to the top 100 individuals in the newly generated population
        max_individuals = min(MAX_POPULATION, len(new_population))

        self.population = new_population[:max_individuals]
    
    def classify_life(self):
        ''''
        Classifies the species for each network in the population

        The species are kept track in the species dictionary where each is a positive number starting from 1
        '''
        # goes through all networks in the list. 
        # If it does not have a species classify it and assign it to the appropriate list
        for network in self.population:
            # Classify the network if it hasnt been classified yet
            if network.species == -1:
                network.species = self.classify_network(network)
    
    def classify_network(self, network):
        '''
        Finds the species for the network according to its gene array
        '''
        count = 0
        for species_key in Life.species:
            species_genes = species_key.split()

            # Go through the genes and determine the percentage of matches
            for gene in species_genes:
                # If gene is in the network then increase match percentage
                if int(gene) in network.genes:
                    count += 1

                # If over 50% match then the network is of that species
                if count >= len(network.genes) // 2:
                    self.species_list[Life.species[species_key]].append(network)
                    return Life.species[species_key]

            # If we make it through reset
            count = 0

        # If we make it through all species without a classification, then this is a new species
        # Create the key for the new species
        species_key = ""
        for gene in network.genes[:-1]:
            species_key += str(gene) + " "
        species_key += str(network.genes[-1])

        # Create the new key and add it to the dictionary
        Life.species[species_key] = Life.curr_species_num

        # Increment to the next available number
        Life.curr_species_num += 1

        # Append a list with the new species as the only network in the list
        self.species_list.append([network])

        return Life.species[species_key]

    def run_visualization(self, game_loop, amount=1):
        '''
        Run a visualization through a number of networks equivalent to amount
        '''

        # Ensure the number of 
        if amount > len(self.population):
            print("Not Valid, exceeds individual count")
            return
        
        print("--------------------- PRINTING TOP ", amount, "---------------------")
        for individual in self.population[:amount]:
            print("-----------NETWORK ", self.population.index(individual) + 1,"-------------")
            game_loop(self.population.index(individual), individual)
            print()
            print(individual)

    def print_top_performers(self):
        '''
        Print the highest fitness network from each generation
        '''
        print("\nTop performers from each generation:")
        for performer in self.top_performers:
            print(performer)

    def print_population_detail(self):
        '''
        Prints all of the population and the detailed stats for each network
        Topology included
        '''
        print("\nLatest Generation:")
        for individual in self.population:
            individual.print_d()
        print()

    def print_population_simple(self):
        '''
        Prints all of the population and the simple stats for each network
        No topology included
        '''
        print("\nLatest Generation:")
        for individual in self.population:
            individual.print_s()
        print()

    def print_species_info(self):
        '''
        Prints each species identifier and the number of species in the network
        '''
        print("\nAll Species:")
        for species in Life.species.keys():
            print("Species ", Life.species[species], "- Genes: ", species, "- Population size: ", len(self.species_list[int(Life.species[species])]), " || ")

    def print_genes(self):
        '''
        Prints all genes across all networks in a formatted manner
        '''
        print("\nGenes:")
        line_length = 10
        count = 0
        for key in network.Network.innovation_to_gene_key.keys():
            if count == line_length:
                print(key, "\t: ", network.Network.innovation_to_gene_key[key])
                count = 0
            else:
                print(key, "\t:", network.Network.innovation_to_gene_key[key], end="\t| ")
                count += 1
        print()