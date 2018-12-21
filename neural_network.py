import numpy as np
import random 
 
class Network:
    def __init__(self, inputs, outputs):
        '''
        Neural network that breeds through taking unique sup-topologies from others within its species
        Args:
            inputs (list (ints)) - list of inputs to be converted into a list of nodes
            outputs (list (str)) - list of outputs' actions
        Returns:
            None
        Raises:
            None
        '''
        #fitness for the network, initialized to 0
        self.fitness = 0
        #Species for the network, initialized to 0
        self.species = 0
        #Historical Makrings to improve breeding uniqueness
        self.generation = 0
        #Input layer of nodes
        self.inputs = [Node(inputs[x]) for x in range(len(inputs))]
        #Output layer of nodes
        self.outputs = [Node(0, desc=outputs[x]) for x in range(len(outputs)))]

    def feed(self):
        #Perform a bfs type run with each input node as the source
        #Find way to feed network that is efficient and resets values along the way

        for node in self.inputs:
            for toNode in node.next:
                while(node.next.value != None):
                    toPass = node.value
                    node.value = 0
                    node.next.value += toPass


    
    def find_max(self):
        max = Node(float("-inf"))
        for node in outputs:
            if node.value > max.value:
                max = node
        return max.desc

    def breed(self, other_parent):
        pass

    def mutate(self):
        '''
        Returns a mutation of the network passed in. The mutation will have 1 or 2 traits from the
        network passed in and is guarenteed to have 1 randomly created trait.
        Args:
            network (Network object) - network to mutate from
        Returns:
            mutation (Network object) - mutated network
        Raises:
            None
        '''
        pass
    
    def print(self):
        print("Fitness: ", self.fitness)
        print("Species: ", self.species)
        print("Generation: ", self.generation)

def create_init_population_species(count, inputs, outputs):
    '''
    Returns a list of neural networks that has length count
    Args:
        count (int) number of members of species population
    Returns:
        Population (list of neural network objects)
    Raises:
        None
    '''
    toReturn = [Network(inputs, outputs) for x in range(count)]
    #Choose random nodes in the input layer and randomly connect them to an output node.
    #Do this x amount of times where 0 < x < number of outputs
    reps = random.randint(0, len(outputs))
    for x in range(reps)
        #Choose the network then choose the node from input layer to connect to node in output layer randomly
        network_index = random.randint(0, count - 1)
        input_index = random.randint(0, len(inputs) - 1)
        output_index = random.randint(0, len(outputs) - 1)

        #Connect the input node to the output node
        toReturn[network_index].inputs[input_index].next[0].append(toReturn[network_index].outputs[output_index])

