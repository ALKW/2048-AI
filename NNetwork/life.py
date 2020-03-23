"""Builds an ecosystem of networks using Network objects"""
import sys

from NNetwork import neural_network as network

class Life:
    '''
    Dictionary for classifying species. If 50%+ of the genes match the original creator of the
    species, then that species is the same. The key is the sequence of genes for network with
    each gene separated by a space If the species doesnt match any then a new species is created

    Constructor Args:
        population - (list(Network)) - The initial population of networks that will be used as a
                                       starting point for training
        species_list - (list(list(Network))) - A list of lists where each list is a list of
                                               Network objects that belong to the same species
        top_performers - list(Network) - A list of Network objects that were the top performers
    Raises:
        None
    '''
    # Dictionary for classifying species. If 50%+ of the genes match the original creator of the
    # species, then that species is the same. The key is the sequence of genes for network with
    # each gene separated by a space If the species doesnt match any then a new species is created
    species = dict()

    # The next available number to assign to a species
    curr_species_num = 0

    def __init__(self, population=None, species_list=None, top_performers=None):
        # Array of all networks regardless of species
        if population is None:
            self.population = []
        self.population = population

        # list of lists. each list has a specific list of species
        if species_list is None:
            self.species_list = []
        self.species_list = species_list

        # List of top performers from each generation
        if top_performers is None:
            self.top_performers = []
        self.top_performers = top_performers

    def run(self, game_loop, life_params=(1, 1, 20, 5)):
        '''
        Runs each network in the population a certain number of times and keeps the top performers
        to breed and re run against children. tuple in the arguments tells how the "ecosystem"
        should evolve.

        Args:
            game_loop - (function) - a function defined by the user that the game runs. The game
                                     loop itself is called each time a network is selected for
                                     fitness measurements. The gameloop should be able to be
                                     analyzed at different points by the users custom defined
                                     fitness function.
            life_params - (tuple(ints)) - A tuple that has the parameters for how the ecosystem
                                          should be run (like environment varibales). the values
                                          in the tuple correspond to: (max number of generations,
                                          runs per individual, max population size, max population
                                          per species)
        Returns:
            None
        Raises:
            None
        '''

        # Get the parameters that define the limits on the networks and the ecosystem
        max_generations = life_params[0]
        runs_per_indiv = life_params[1]
        max_population = life_params[2]
        max_per_species = life_params[3]

        # Run the simulation for MAX_GENERATIONS iterations with a population size of 20
        for iteration in range(max_generations):
            # Test each memeber of the population
            for individual in self.population:
                run_total = 0

                #Run the individual through a number of games to get an average fitness
                for _ in range(runs_per_indiv):
                    # Give a unique identifier (An index in the list of members in the population)
                    # and pass the network object to the game loop
                    game_loop(self.population.index(individual), individual)
                    run_total += individual.fitness

                # Assign the average fitness to the network
                individual.fitness = run_total // runs_per_indiv

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
            top_performer = "Generation: " + str(iteration + 1) +  " | Max Fitness: "\
                            + str(self.population[0].fitness) + " | Species: "\
                            + str(self.population[0].species)
            self.top_performers.append(top_performer)

            # IF we reach the last generation, then break
            if iteration == (max_generations - 1):
                return
            # Otherwise mate and mutate the population by species. Take top 100 to keep
            # population low or whatever custom value the user defines
            self.mutate_population(max_population=max_population, max_per_species=max_per_species)

            # Classify each new network species that was added
            self.classify_life()

    def mutate_population(self, max_population, max_per_species):
        '''
        mutates/breeds the appropriate members of the population to create a new population

        Each species has its own sorted array and all members of the population are classified
        through the classify_life() method

        Args:
            max_population - (int) - maximum amount of members in the total population
            max_per_species - (int) - maximum amount of members per species in the population
        Returns:
            None
        Raises:
            None
        '''

        # Perform Breeding/Mutating
        new_population = []

        # Compute the fitness for each species in the population

        species, avg_fitness = self.compute_fitness()

        # mutate/breed each species
        for species_t in species:
            # Determine if there are enough members in the species to mate
            mate_max = min(4, len(species_t))
            num_made = 0

            # Mate up to top 4 performers (less if the species doesnt have enough)
            # -> add their children (max 6) plus the parents (max 4)
            # -> result is up to 10 networks for the species
            for first_index in range(mate_max):
                # Append first parent in the pair. Because each parent is first at some point we
                # append them all
                new_population.append(species_t[first_index])

                # Mate that network with all other networks it hasnt mated with yet within its
                # species
                for second_index in range(first_index + 1, mate_max):
                    # Create and append the child in the pair
                    child = species_t[first_index].breed_with(species_t[second_index])

                    # set the initial fitness to the average fitness for the species
                    child.fitness = avg_fitness[species.index(species_t)]

                    # Add the child to the new population
                    new_population.append(child)
                    num_made += 1

            # The last index in species_t to mutate
            mutate_max = min(len(species_t), mate_max + (max_per_species - num_made))

            # Mutate the rest of the network so that there is up to 20 individuals made for the
            # new population
            for ind_index in range(mate_max, mutate_max):
                species_t[ind_index].mutate()
                new_population.append(species_t[ind_index])
                num_made += 1

            # Disregard The rest of the species so as not to poplute with 1 species

        # Sort the new population by fitness.
        # Children have fitness equal to the average fitness of their species
        new_population.sort(key=lambda x: x.fitness, reverse=True)

        # Create new population by taking up to the top 100 individuals in the newly generated
        # population
        max_individuals = min(max_population, len(new_population))

        self.population = new_population[:max_individuals]

    def compute_fitness(self):
        '''
        Computes the average fitness of the population based on species and sorts them into lists

        Args:
            None
        Returns:
            (list(list(Network))) - A list of lists of species to organize the population
            (list(int)) - Average fitness for each species related by index
        Raises:
            exception_name
        '''
        # Used for classifying species within the current population
        species = [[] for x in range(len(Life.species))]
        total_fitness = [0 for x in range(len(Life.species))]
        avg_fitness = [0 for x in range(len(Life.species))]

        # Sort life based on species, then breed/mutate all the species
        # Keep track of the average fitness for each species
        for nnetwork in self.population:
            # Add the network to the apporpriate species index
            species_key = nnetwork.species
            species[species_key].append(nnetwork)
            total_fitness[species_key] += nnetwork.fitness

        # Get the average fitness for each species
        for species_index in enumerate(species):
            #If there are no individuals of the species, then disregard it
            if len(species[species_index]) == 0:
                continue

            # Compute the average fitness for the species
            avg_fitness[species_index] = total_fitness[species_index] // len(species[species_index])

        return species, avg_fitness

    def classify_life(self):
        '''
        Classifies the species for each network in the population. The species are kept track in
        the species dictionary where each is a positive number starting from 1

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''

        # goes through all networks in the list.
        # If it does not have a species classify it and assign it to the appropriate list
        for nnetwork in self.population:
            # Classify the network if it hasnt been classified yet
            if nnetwork.species == -1:
                nnetwork.species = self.classify_network(nnetwork)

    def classify_network(self, nnetwork):
        '''
        Finds the species for the network according to its gene array

        Args:
            nnetwork - (Network) - current network we are trying to find a species for
        Returns:
            (int) - the species of the network
        Raises:
            None
        '''
        count = 0
        for species_key in Life.species:
            species_genes = species_key.split()

            # Go through the genes and determine the percentage of matches
            for gene in species_genes:
                # If gene is in the network then increase match percentage
                if int(gene) in nnetwork.genes:
                    count += 1

                # If over 50% match then the network is of that species
                if count >= len(nnetwork.genes) // 2:
                    self.species_list[Life.species[species_key]].append(nnetwork)
                    return Life.species[species_key]

            # If we make it through reset
            count = 0

        # If we make it through all species without a classification, then this is a new species
        # Create the key for the new species
        species_key = ""
        for gene in nnetwork.genes[:-1]:
            species_key += str(gene) + " "
        species_key += str(nnetwork.genes[-1])

        # Create the new key and add it to the dictionary
        Life.species[species_key] = Life.curr_species_num

        # Increment to the next available number
        Life.curr_species_num += 1

        # Append a list with the new species as the only network in the list
        self.species_list.append([nnetwork])

        return Life.species[species_key]

    def run_visualization(self, game_loop, amount=1):
        '''
        Run a visualization through a number of networks equivalent to amount

        Args:
            game_loop - (function) - similar to the other game loop except this one displays
                                     the game and analytics are not required
            amount - (int) - The number of networks to run with the visualized game loop. Will run
                             the top networks in the population
        Returns:
            None
        Raises:
            None
        '''

        # Ensure the number of visuals the user is asking to run is less than or
        # equal to the size of the population
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

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        print("\nTop performers from each generation:")
        for performer in self.top_performers:
            print(performer)

    def print_population_detail(self):
        '''
        Prints all of the population and the detailed stats for each network
        Topology included

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        print("\nLatest Generation:")
        for individual in self.population:
            individual.print_d()
        print()

    def print_population_simple(self):
        '''
        Prints all of the population and the simple stats for each network
        No topology included

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        print("\nLatest Generation:")
        for individual in self.population:
            individual.print_s()
        print()

    def print_species_info(self):
        '''
        Prints each species identifier and the number of species in the network

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        print("\nAll Species:")
        for species in Life.species.keys():
            print("Species ", Life.species[species], "\tGenes: ", species, "\tPopulation size: ",
                  len(self.species_list[int(Life.species[species])]))

    @classmethod
    def print_genes(cls):
        '''
        Prints all genes across all networks in a formatted manner

        Args:
            None
        Returns:
            None
        Raises:
            None
        '''
        print("\nGenes:")
        line_length = 3
        count = 0
        for key in network.Network.innovation_to_gene_key:
            if count == line_length:
                print("[ {0:4} : {1:8} ]".format(key, network.Network.innovation_to_gene_key[key]))
                count = 0
            else:
                print("[ {0:4} : {1:8} ]".format(key, network.Network.innovation_to_gene_key[key]), 
                      end="\t")
                count += 1
        print()
