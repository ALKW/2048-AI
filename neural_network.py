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
        #internal nodes
        self.internal = []

    def feed(self, stimuli=None):
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
        if stimuli != None:
            for node in self.inputs:
                node.value = stimuli[self.inputs.index(node)]

        #For each node, run DFS with it as the source
        for node in self.inputs:
            #DFS style feed forward
            self.feed_forward(node)
            #DFS style reset
            self.reset_nodes(node, end=False)

        #Find maximum node
        fired_node = self.find_max_output()

        #reset internal nodes and outputs
        for node in self.inputs:
            #DFS style reset
            self.reset_nodes(node, end=True)

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
    
    def reset_nodes(self, start_node, end=True):
        '''
        Resets all nodes except for inputs back to 0
        Args:
            start_node (Node object) - the starting input node to destroy all other nodes
            end (Boolean) - determine whether to include the output nodes or not; True - include, False - dont include 
        Returns:
            None
        Raises:
            None
        '''
        #Because no loops can exist in this network, we dont have to worry about coloring nodes
        outputs_too = end
        for node in start_node.connections:
            if node.desc != None:
                node.value *= 0
            if outputs_too:
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
        max_node = node.Node(float("-inf"))
        max_nodes = [max_node]
        for output_node in self.outputs:
            if output_node.value > max_node.value:
                max_node = output_node
                max_nodes = [max_node]
            elif output_node.value == max_node.value:
                max_nodes.append(output_node)

        index = random.randint(0,len(max_nodes) - 1)
        desc_to_return = max_nodes[index].desc
        '''
        ------------------
        print("Determine Move:", desc_to_return, end="")
        if len(max_nodes) > 1:
            print(" | Random Choice from:", "".join([str(x.desc) + " " for x in max_nodes]))
        else:
            print()
        -------------------
        '''
        return desc_to_return, len(max_nodes)

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

    def mutate(self, mutation=-1):
        '''
        Returns a mutation of the network passed in. The mutation will take an input node and along its path either:
            -add an extra branch
            -create a new node that two nodes link to 
            -modify an existing weight
        Only internal nodes can have weights different than 1
        Args:
            network (Network object) - network to mutate from
        Returns:
            mutation (Network object) - mutated network
        Raises:
            None
        '''
        if mutation == -1:
            mutation = random.randint(0, 2)
        if mutation == 0:
            #Either connects an input to an outut or an internal to an output
            #Choose either an internal or an input node; 0 - input, 1 - internal
            #Choose the input/internal node to connect to the output node (both are random)
            #Error checking to make sure there exists internal nodes
            if len(self.internal) > 0:
                choice = random.randint(0, len(self.internal) + len(self.inputs) - 2)
                internal_index = random.randint(0, len(self.internal) - 1)
            else:
                choice = 0
                internal_index = 0

            input_index = random.randint(0, len(self.inputs) - 1)
            output_index = random.randint(0, len(self.outputs) - 1)
            count = 0

            while count < 1000:
                if choice <= len(self.inputs) - 1 and self.outputs[output_index] not in self.inputs[input_index].connections:
                    self.inputs[input_index].connections.append(self.outputs[output_index])
                    break
                if choice > len(self.inputs) - 1 and self.outputs[output_index] not in self.internal[internal_index].connections:
                    self.internal[internal_index].connections.append(self.outputs[output_index])
                    break

                #Find new indices
                if len(self.internal) > 0:
                    choice = random.randint(0, 1)
                    internal_index = random.randint(0, len(self.internal) - 1)
                else:
                    choice = 0
                    internal_index = 0
                input_index = random.randint(0, len(self.inputs) - 1)
                output_index = random.randint(0, len(self.outputs) - 1)
                count += 1
            #If nothing was modifided then move on and try another mutation
            if count >= 1000:
                mutation = random.randint(1, 2)

        if mutation == 1:
            #Create a new internal node
            #select two input nodes to connect to the internal node
            #select an output node to connect to the internal node
            to_add = node.Node(weight=random.choice([-2,-1,1,2]))
            self.internal.append(to_add)
            output_index = random.randint(0, len(self.outputs) - 1)
            left_input_index = random.randint(0, len(self.inputs) - 1)
            right_input_index = random.randint(0, len(self.inputs) - 1)

            #Prevent the inputs from being the same
            while left_input_index == right_input_index:
                left_input_index = random.randint(0, len(self.inputs) - 1)
                right_input_index = random.randint(0, len(self.inputs) - 1)
            
            #Connect the nodes together
            self.inputs[left_input_index].connections.append(to_add)
            self.inputs[right_input_index].connections.append(to_add)
            to_add.connections.append(self.outputs[output_index])

        if mutation == 2:
            #Choose an internal node and modify its weight
            #Determine if there are any nodes to begin with
            if len(self.internal) == 0:
                self.mutate(mutation=1)

            mutate_index = random.randint(0, len(self.internal) - 1)
            curr_weight = self.internal[mutate_index].weight
            poss_weights = set(range(-5,5))

            #Make sure a change actually happens and a weight of 0 is not achieved
            poss_weights.remove(0)
            poss_weights.remove(curr_weight)

            #Change the weight of the internal node
            self.internal[mutate_index].weight = random.choice(list(poss_weights))
    
    def print_s(self):
        print("Fitness: ", self.fitness)

    def print(self):
        print("Fitness: ", self.fitness)
        print("Species: ", self.species)
        print("Generation: ", self.generation, "\n")
        print("Topology: ")
        self.print_node_paths()
    
    def print_node_paths(self):
        #Start with each internal nodes
        for node in self.inputs:
            self.find_paths(node, [node])
            print()
            
    def find_paths(self, curr, path):
        #if we reach an output node, then print and return
        if len(curr.connections) == 0:
            print("----PATH FOR NODE",  self.inputs.index(path[0]), ":", end="")
            for node in path[:-1]:
                print("Value:", node.value, "Weight:", node.weight, "-> ", end="")
            if path[-1].desc != None:
                print(path[-1].desc)
            else:
                print("Value:", path[-1].value, "Weight:", path[-1].weight, "-> None---")
            return

        #Create a duplicate path object
        new_path = [x for x in path]

        #Append the current node to the path and then return
        for node in curr.connections:
            new_path.append(node)
            self.find_paths(node, new_path.copy())


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
    for network_index in range(count):
        #For each network connect all four output nodes to input nodes initially
        for output_index in range(4):
            #choose the node from input layer to connect to node in output layer randomly
            input_index = random.randint(0, len(inputs) - 1)
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
    


