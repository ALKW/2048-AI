import random 
import node
 
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
        #Historical Makrings to improve breeding uniqueness so that higher generations dont become replicas of lower generations
        self.generation = 0
        #Input layer of nodes
        self.inputs = [node.Node(inputs[x]) for x in range(len(inputs))]
        #Output layer of nodes
        self.outputs = [node.Node(0, desc=outputs[x]) for x in range(len(outputs))]

    def feed(self, stimuli=0):
        '''
        Can run with or without stumli, if no stimuli then previous inputs are kept. 
        Runs through neural network and the output is determined by which has the highest value.
        Args:
            stimuli (list (length: 16)) - list of stimuli for each input neuron
        Returns:
            None
        Raises:
            None
        '''
        #If stimuli are given then update the input neurons
        if stimuli != 0:
            for node in self.inputs:
                node.value = stimuli[self.inputs.index(node)]

        #For each node, run DFS with it as the source
        for node in self.inputs:
            #DFS style feed forward
            self.feed_forward(node)

        #Find maximum node
        fired_node = self.find_max_output()

        #reset internal nodes and outputs
        for node in self.inputs:
            #DFS style reset
            self.reset_nodes(node)

        return fired_node

    def feed_forward(self, start_node):
        '''
        Runs through the network to determine the next neuron to fire
        Args:
            start_node
        Returns:
            None
        Raises:
            None
        '''
        #Because no loops can exist in this network, we dont have to worry about coloring nodes
        for node in start_node.connections:
            node.value += start_node.value * start_node.weight
            self.feed_forward(node)
    
    def reset_nodes(self, start_node):
        '''
        Resets all nodes except for inputs back to 0
        Args:
            start_node (Node object) - the starting input node to destroy all other nodes
        Returns:
            None
        Raises:
            None
        '''
        #Because no loops can exist in this network, we dont have to worry about coloring nodes
        for node in start_node.connections:
            node.value *= 0
            self.feed_forward(node)
    
    def find_max_output(self):
        '''
        Finds the maximum value of all output nodes. Defaults to first if they are all the same
        Args:
            None
        Returns:
            desc (var) - the desc member of the maximum ouput node
        Raises:
            None
        '''
        m = node.Node(float("-inf"))
        for output_node in self.outputs:
            if output_node.value > m.value:
                m = output_node
        m.print()
        return m.desc

    def breed(self, other_parent):
        '''
        Breeds two neural networks together using previous generation markers to preserve innovation. Goes through each node
        and randomly chooses which parent to take it from. Each node is has a path to one or multiple output nodes
        Args:
            other_parent (Network object) - Other parent to mutate from
        Returns:
            child (Network object) - Child that has topology parts from both parents
        Raises:
            None
        '''
        pass

    def mutate(self):
        '''
        Returns a mutation of the network passed in. The mutation will take an input node and along its path either add an extra branch,
        create a new node that two nodes link to, or remove a branch. Only internal nodes can have weights different than 1
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
        print("Generation: ", self.generation, "\n")

def create_init_population(count, inputs, outputs):
    '''
    Returns a list of neural networks that has length count
    Args:
        count (int) number of members of species population
    Returns:
        Population (list of neural network objects)
    Raises:
        None
    '''
    networks = [Network(inputs, outputs) for x in range(count)]
    #Choose random nodes in the input layer and randomly connect them to an output node.
    #Do this x amount of times where 0 < x < number of outputs
    reps = random.randint(1, len(outputs))
    print(reps, "Networks Mutated")
    for x in range(reps):
        #Choose the network then choose the node from input layer to connect to node in output layer randomly
        network_index = random.randint(0, count - 1)
        input_index = random.randint(0, len(inputs) - 1)
        output_index = random.randint(0, len(outputs) - 1)

        #Connect the input node to the output node
        networks[network_index].inputs[input_index].connections.append(networks[network_index].outputs[output_index])
    return networks

'''
test = create_init_population(20, [
                2,2,2,2,
                2,16,0,2,
                16,8,2,32,
                16,4,2,32,
                ], ["up", "down", "left", "right"])


for network in test:
    network.print()
    network.feed()
'''

test = Network(
    [2,2,0,0,
    0,0,0,0,
    0,0,0,0,
    0,0,0,0],
    ["up", "down", "left", "right"])


