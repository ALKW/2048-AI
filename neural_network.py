import random
import node
import copy
 
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
        #Species for the network, initialized to 0.
        #Species is determined by which move (up, down, left, right) results in the least amount of game endings (a move is selected that doesnt do anything)
        self.species = 0
        #Historical Makrings to improve breeding uniqueness so that higher generations dont become replicas of lower generations
        self.generation = 0
        #Input layer of nodes
        self.inputs = [node.Node(value=inputs[x]) for x in range(len(inputs))]
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
            for input_node in self.inputs:
                input_node.value = stimuli[self.inputs.index(input_node)]

        #For each node, run DFS with it as the source
        for input_node in self.inputs:
            #DFS style feed forward
            self.feed_forward(input_node)
            #DFS style reset
            self.reset_nodes(input_node, end=False)

        #Find maximum node
        output_info = self.find_max_output()

        #reset internal nodes and outputs
        for input_node in self.inputs:
            #DFS style reset
            self.reset_nodes(input_node, end=True)

        return output_info

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
        #Because no loops can exist in this network, we dont have to worry about coloring nodes for DFS
        for curr_node in start_node.connections:
            curr_node.value += start_node.value * start_node.weight
            self.feed_forward(curr_node)
    
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
        for curr_node in start_node.connections:
            if curr_node.desc != None:
                curr_node.value *= 0
            if outputs_too:
                curr_node.value *= 0
            self.feed_forward(curr_node)
    
    def find_max_output(self):
        '''
        Finds the maximum value of all output nodes. Defaults to first if they are all the same
        Args:
            None
        Returns:
            tuple - (desc (var), length (list), nodes (list)) 
                - the desc member of the maximum ouput node
                - Whether the choice was random or not
                - All the nodes sorted by rank
        Raises:
            None
        '''
        #Initialize variables
        max_node = node.Node(float("-inf"))
        max_nodes = [max_node]

        #Find the maximum node(s)
        for output_node in self.outputs:
            if output_node.value > max_node.value:
                max_node = output_node
                max_nodes = [max_node]
            elif output_node.value == max_node.value:
                max_nodes.append(output_node)

        #Determine the move to do
        index = random.randint(0,len(max_nodes) - 1)
        desc_to_return = max_nodes[index].desc
        '''
        #------------------PRINT-----------------
        print("Determine Move:", desc_to_return, end="")
        if len(max_nodes) > 1:
            print(" | Random Choice from:", "".join([str(x.desc) + " " for x in max_nodes]))
        else:
            print()
        '''
        #Sort the outputs by value, highest is highest rank
        ranks = [x for x in self.outputs]
        ranks.sort(key=lambda x: x.value, reverse=True)

        return desc_to_return, len(max_nodes), ranks

    def breed_with(self, other_parent):
        '''
        Breeds two neural networks together using previous generation markers to preserve innovation. Goes through each networks outputs
        and randomly chooses which parent to take it from. Goes through the list of output nodes and and determines whether to
        take all paths into that output node from the first of second parent. That output node is marked with a unique identifier
        that tells what generation it came from and from what rank in that generation, so that innovation is kept. Cannot use input nodes
        as this disrupts paths and causes networks to perform much worse
        Args:
            other_parent (Network object) - Other parent to mutate from
        Returns:
            child (Network object) - Network object contains traits of both parents
        Raises:
            None
        '''
        #Create a list of input indexes to choose from
        choices = [x.desc for x in self.outputs]
        calling_output_desc = []
        arg_output_desc = []

        #Choose half the outputs that are taken from the calling parent. Other half are reserved for other parent
        for x in range(len(choices) // 2):
            to_append = random.choice(choices)
            calling_output_indices.append(to_append)
            #Remove it so it is not picked again
            choices.remove(to_append)

        #Assign the rest to the outputs from the argument parent
        arg_output_indices = [x for x in choices]

        '''
        #----------------PRINT---------------------
        print("calling: ", calling_input_indices)
        print("args: ", arg_input_indices)
        '''

        #Create a network object to be the child
        child = Network(inputs=[0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0], outputs=["up", "down", "left", "right"])

        #take inputs paths from calling parent and assign them to the child
        for index in calling_input_indices:
            child.inputs[index] = copy.deepcopy(self.inputs[index])

        #take inputs paths from argument parent and assign them to the child
        for index in arg_input_indices:
            child.inputs[index] = copy.deepcopy(other_parent.inputs[index])

        return child

    def find_paths_to_append(self, curr, path, outputs, child):
        #if we reach an output node, then delete the path up to the point that no other paths are affected
        if curr == end:
            self.append_path(path, child)
            return

        #if we reach an output node without encountering the node to terminate, then dont do anything
        if len(curr.connections) == 0:
            return

        #Append the current node to the path and then return
        for con_node in curr.connections:
            new_path.append(con_node)
            self.find_paths_to_delete(con_node, path.copy(), outputs, child)

    def append_path(self, path, child):
        #Go through the path starting at the input node and write network
        count = len(path) - 1
        START = path[0]
        SECOND = path[1]

    def mutate(self, mutation=-1):
        '''
        Returns a mutation of the network passed in. The mutation will take an input node and along its path either:
            -add an extra branch
            -create a new node that two nodes link to 
            -modify an existing weight
            -delete an existing branch
        Only internal nodes can have weights different than 1
        Args:
            network (Network object) - network to mutate from
        Returns:
            mutation (Network object) - mutated network
        Raises:
            None
        '''
        #If no mutation was passed in
        if mutation == -1:
            mutation = random.randint(0, 2)

        if mutation == 0:
            #Either connects an input to an outut or an internal to an output
            #Choose either an internal or an input node; 0 - input, 1 - internal
            #Choose the input/internal node to connect to the output node (both are random)
            #Error checking to make sure there exists internal nodes
            if len(self.internal) > 0:
                choice = random.randint(0, len(self.internal) + len(self.inputs) - 1)
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
            #If there are none, then the only mutation that can happen is the second one
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
        
        if mutation == 3:
            #choose a node to delete one of its paths out. If the node is internal and has only
            #one path out delete all paths to that node
            node_choice = random.randint(0, len(self.inputs) + len(self.internal) - 1)

            #Choosen an input node
            if node_choice < len(self.inputs):
                #choose an input node that has at least 1 output
                while len(self.inputs[node_choice].connections) < 1:
                    node_choice = random.randint(0, len(self.inputs) - 1)
                #Choose the outgoing branch to delete
                del_choice = random.randint(0, len(self.inputs[node_choice].connections) - 1)
                #delete the branch
                self.inputs[node_choice].connections.pop(del_choice)
            #else choose an internal node
            else:
                #if the node has multiple paths leaving it, then just delete the path without deleting the node
                node_choice -= len(self.inputs)
                if len(self.internal[node_choice].connections) > 1:
                    del_choice = random.randint(0, len(self.internal[node_choice].connections) - 1)
                    self.internal[node_choice].connections.pop(del_choice)
                    
                #if the node has only one connection out, delete that node and all paths to it
                #Go through all paths to find paths that include the internal node. Delete all paths to that node
                else:
                    #For each node, run modified DFS with it as the source
                    for input_node in self.inputs:
                        #DFS style feed forward
                        self.find_paths_to_delete(input_node, [input_node], self.internal[node_choice].connections[0])

    def find_paths_to_delete(self, curr, path, end):
        #if we reach an output node, then delete the path up to the point that no other paths are affected
        if curr == end:
            self.del_path(path)
            return
        #if we reach an output node without encountering the node to terminate, then dont do anything
        if len(curr.connections) == 0:
            return

        #Create a duplicate path object
        new_path = [x for x in path]

        #Append the current node to the path and then return
        for con_node in curr.connections:
            new_path.append(con_node)
            self.find_paths_to_delete(con_node, new_path.copy(), end)

    def del_path(self, path):
        #Go through the path starting at the node to delete and look at the number of connections of each node
        count = len(path) - 1
        START = path[0]
        SECOND = path[1]

        for curr_node in path[::-1]:
            #If we reach an input node, delete the path going from that node
            if count == 0:
                self.inputs[self.inputs.index(START)].connections.remove(SECOND)
            #Keep deleting nodes until you encounter one with more than 1 connection
            if len(curr_node.connections) == 1:
                self.internal.remove(curr_node)
            else:
                return
            count -= 1
                       
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
        for input_node in self.inputs:
            self.find_paths(input_node, [input_node])
            print()
            
    def find_paths(self, curr, path):
        #if we reach an output node, then print and return
        if len(curr.connections) == 0:
            print("----PATH FOR NODE",  self.inputs.index(path[0]), ":", end="")
            for curr_node in path[:-1]:
                print("Value:", curr_node.value, "Weight:", curr_node.weight, "-> ", end="")
                
            if path[-1].desc != None:
                print(path[-1].desc)
            else:
                print("Value:", path[-1].value, "Weight:", path[-1].weight, "-> None---")
            return

        #Create a duplicate path object
        new_path = [x for x in path]

        #Append the current node to the path and then return
        for con_node in curr.connections:
            new_path.append(con_node)
            self.find_paths(con_node, new_path.copy())


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
#-----------------BREEDING TEST------------------
test = create_init_population(2, [
                2,2,2,2,
                2,16,0,2,
                16,8,2,32,
                16,4,2,32,
                ], ["up", "down", "left", "right"])
    
test[0].print()
test[1].print()
test[0].breed_with(test[1]).print()
'''

    
