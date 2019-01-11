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
        self.species = -1
        #Historical Makrings to improve breeding uniqueness so that higher generations dont become replicas of lower generations
        self.generation = -1
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
            Output info (tuple (desc (var), length (list), nodes (list)) 
                - the highest value output node(s)
                - Whether the choice was random or not
                - All the nodes sorted by rank
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
            start_node (Node object) - the node whose connections we are examining
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
            if curr_node.desc == None:
                curr_node.value *= 0
            if outputs_too:
                curr_node.value *= 0
            self.reset_nodes(curr_node)
    
    def find_max_output(self):
        '''
        Finds the maximum value of all output nodes. Defaults to first if they are all the same
        Args:
            None
        Returns:
            tuple - (desc (var), length (list), nodes (list)) 
                - the highest value output node(s)
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

        '''
        #------------------PRINT Moves-----------------
        print("Determine Move:", desc_to_return, end="")
        if len(max_nodes) > 1:
            print(" | Random Choice from:", "".join([str(x.desc) + " " for x in max_nodes]))
        else:
            print()
        '''
        #Sort the outputs by value, highest is highest rank
        ranks = [x for x in self.outputs]
        ranks.sort(key=lambda x: x.value, reverse=True)

        return max_nodes, len(max_nodes), ranks

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
        #Create a network object to be the child
        child = Network(inputs=[x.value for x in self.inputs], outputs=[x.desc for x in self.outputs])

        '''
        #---------INPUT BREEDING------------
        #Create a list of input indexes to choose from
        choices = [x for x in range(len(self.inputs))]
        calling_input_indices = []
        arg_input_indices = []

        #Choose half the inputs that are taken from the calling parent. Other half are reserved for other parent
        for x in range(len(choices) // 2):
            to_append = random.choice(choices)
            calling_input_indices.append(to_append)
            #Remove it so it is not picked again
            choices.remove(to_append)

        #Assign the rest to the inputs from the argument parent
        arg_input_indices = [x for x in choices]

        '''
        '''
        #----------------PRINT---------------------
        print("calling: ", calling_input_indices)
        print("args: ", arg_input_indices)
        '''
        '''        

        #take inputs paths from calling parent and assign them to the child
        for index in calling_input_indices:
            child.inputs[index] = copy.deepcopy(self.inputs[index])

        #take inputs paths from argument parent and assign them to the child
        for index in arg_input_indices:
            child.inputs[index] = copy.deepcopy(other_parent.inputs[index])

        #fill in the internal nodes of the child
        self.fill_in_internals(child)
        
        '''

        #-----------OUTPUT BREEDING----------
        #Create a list of output indexes to choose from
        choices = [x for x in range(len(self.outputs))]
        calling_output_indices = []
        arg_output_indices = []
        paths = []

        #Choose half the outputs that are taken from the calling parent. Other half are reserved for other parent
        for x in range(len(choices) // 2):
            to_append = random.choice(choices)
            calling_output_indices.append(to_append)
            #Remove it so it is not picked again
            choices.remove(to_append)

        #Assign the rest to the outputs from the argument parent
        arg_output_indices = [x for x in choices]

        #Get the outputs and assign them to the appropriate lists
        calling_poss_outputs = [x.desc for x in self.outputs if self.outputs.index(x) in calling_output_indices]
        arg_poss_outputs = [x.desc for x in self.outputs if self.outputs.index(x) in arg_output_indices]

        '''
        #----------------PRINT---------------------
        print("calling: ", calling_poss_outputs)
        print("args: ", arg_poss_outputs)
        '''

        #take paths to output from calling parent and assign them to the child
        for input_node in self.inputs:
            result = self.find_paths(input_node, [], calling_poss_outputs, [])
            if result != None:
                paths += result

        self.append_paths(child, paths, self)
        paths = []

        #take paths to output from argument parent and assign them to the child
        for input_node in other_parent.inputs:
            result = other_parent.find_paths(input_node, [], arg_poss_outputs, [])
            if result != None:
                paths += result

        self.append_paths(child, paths, other_parent)

        self.fill_in_internals(child)

        return child

    def fill_in_internals(self, child):
        for input_node in self.inputs:
            self.find_internals(child, input_node, [])   

    def find_internals(self, child, curr, path):
        #append the current node to the path
        path.append(curr)

        #if we reach an output node and the path has an internal node, 
        # then add all the input nodes to the internals if they arent in there already
        if len(curr.connections) == 0 and len(path) > 2:
            for internal_node in path[1:-1]:
                if internal_node not in child.internal:
                    child.internal.append(internal_node)
            return
        #if we reach an output node and the path has no internal nodes
        #Then do nothing
        if len(curr.connections) == 0 and len(path) <= 2:
            return

        #Append the current node to the path and then return
        for con_node in curr.connections:
            self.find_internals(child, con_node, path.copy())

    #----------------OUTPUT BREEDING-------------------
    def find_paths(self, curr, path, poss_outputs, paths):
        #append the current node to the path
        path.append(curr)

        #if we reach a correct output node, then delete the path up to the point that no other paths are affected
        if curr.desc in poss_outputs:
            paths.append(path)
            return

        #if we reach an output node without encountering the node to terminate, then dont do anything
        if len(curr.connections) == 0:
            return

        #Append the current node to the path and then return
        for con_node in curr.connections:
            self.find_paths(con_node, path.copy(), poss_outputs, paths)

        return paths

    def append_paths(self, child, paths, parent):
        #Go through all the paths and append them to the child network
        #for more efficient storage keep track of nodes added 
        #Key: Old Node | Value: New Node
        nodes = dict()
        OUTPUTS = [x.desc for x in child.outputs]

        for path in paths:
            #Find the corresponding input node
            input_index = parent.inputs.index(path[0])
            curr = child.inputs[input_index]
            #Connect the path
            for node_obj in path[1:]:
                #if we reach an output node, use the child output nodes
                if node_obj.desc != None:
                    output_index = OUTPUTS.index(node_obj.desc)
                    node_obj = child.outputs[output_index]
                    #If the output is already connected then dont append it again
                    if node_obj in curr.connections:
                        break
                #if the node was already replicated use that replicated one
                elif node_obj in nodes:
                    node_obj = nodes[node_obj]
                #Else stoZNre the node for future use and use the replicated one
                else:
                    nodes[node_obj] = node.Node(value=node_obj.value, weight=node_obj.weight)
                    node_obj = nodes[node_obj]
                #Assign the node to the correct connection list
                #Start at the second entry as the first is not in any connection list
                curr.connections.append(node_obj)
                curr = node_obj

    def mutate(self, mutation=-1):
        '''
        Returns a mutation of the network passed in. The mutation will take an input node and along its path either:
            -add an extra branch
            -create a new node that links two nodes together
            -modify an existing weight of internal
            -modify existing weight of an input node
        Only internal nodes can have weights different than 1
        Args:
            network (Network object) - network to mutate from
        Returns:
            None
        Raises:
            None
        '''
        #If no mutation was passed in
        if mutation == -1:
            mutation = random.randint(0, 3)

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
            #select two nodes to connect to the new internal node
            to_add = node.Node(weight=random.choice([-2,-1,1,2]))

            #Combinations include:
            #input -> new -> internal
            #input -> new -> output
            #internal -> new -> output
            first_node_index = random.randint(0, len(self.inputs) + len(self.internal) - 2)

            #If the node is an internal then only an output node can be selected
            if first_node_index >= len(self.inputs):
                second_node_index = random.randint(0, len(self.outputs) - 1)
                #Adjust the index
                first_node_index -= len(self.inputs)
                #Connect the internal to the new node
                self.internal[first_node_index].connections.append(to_add)
                #and the new node to the output
                to_add.connections.append(self.outputs[second_node_index])
            else:
                second_node_index = random.randint(0, len(self.internal) + len(self.outputs) - 2)
                #Connect the input to the new node
                self.inputs[first_node_index].connections.append(to_add)
                #Connect the new node to either the output or the internal
                if second_node_index >= len(self.internal):
                    second_node_index -= len(self.internal)
                    to_add.connections.append(self.outputs[second_node_index])
                else:
                    to_add.connections.append(self.internal[second_node_index])

        if mutation == 2:
            #Choose an internal node and modify its weight
            #Determine if there are any nodes to begin with
            #If there are none, then then choose another mutation that doesnt involve internal nodes
            if len(self.internal) == 0:
                self.mutate(mutation=random.choice([1,3]))
                return

            mutate_index = random.randint(0, len(self.internal) - 1)
            curr_weight = self.internal[mutate_index].weight
            poss_weights = set(range(-5,5))

            #Make sure a change actually happens and a weight of 0 is not achieved
            poss_weights.remove(0)
            poss_weights.remove(curr_weight)

            #Change the weight of the internal node
            self.internal[mutate_index].weight = random.choice(list(poss_weights))

        if mutation == 3:
            #Choose an input node and modify its weight
            mutate_index = random.randint(0, len(self.inputs) - 1)
            curr_weight = self.inputs[mutate_index].weight
            poss_weights = set(range(-5,5))

            #Make sure a change actually happens and a weight of 0 is not achieved
            poss_weights.remove(0)
            poss_weights.remove(curr_weight)

            #Change the weight of the internal node
            self.inputs[mutate_index].weight = random.choice(list(poss_weights))
                       
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
            self.find_paths_to_print(input_node, [])
            print()
            
    def find_paths_to_print(self, curr, path):
        #append the current node to the path
        path.append(curr)

        #if we reach an output node, then print and return
        if len(curr.connections) == 0:
            print("----PATH FOR NODE",  self.inputs.index(path[0]), ":", end="")
            for curr_node in path[:-1]:
                print("| Value:", curr_node.value, "Weight:", curr_node.weight, "| -> ", end="")
                
            if path[-1].desc != None:
                print(path[-1].desc)
            else:
                print("| Value:", path[-1].value, "Weight:", path[-1].weight, "|-> ---None---")
            return

        #Append the current node to the path and then return
        for con_node in curr.connections:
            self.find_paths_to_print(con_node, path.copy())


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
    #Create a list of blank network objects
    networks = [Network(inputs, outputs) for x in range(count)]
    #For each network connect all four output nodes to input nodes initially
    for network_index in range(count):
        for output_index in range(4):
            #choose the node from input layer to connect to the output node randomly
            input_index = random.randint(0, len(inputs) - 1)
            #Connect the input node to the output node
            networks[network_index].inputs[input_index].connections.append(networks[network_index].outputs[output_index])
    return networks

'''
#-----------------BREEDING TEST------------------
test = create_init_population(2, [
                2,2,2,2,
                2,16,50,2,
                16,8,2,32,
                16,4,2,32,
                ], ["up", "down", "left", "right"])


internal1 = node.Node()
internal1.connections.append(test[0].outputs[0])   
print(internal1)
 
internal2 = node.Node() 
internal2.connections.append(test[1].outputs[0])  
print(internal2)  

test[0].inputs[0].connections.append(internal1)
test[0].inputs[1].connections.append(internal1)

test[1].inputs[0].connections.append(internal2)

test[0].mutate(mutation=1)


test[0].print()
test[1].print()
child = test[0].breed_with(test[1])
child.print()
print(len(child.internal))
'''






    
