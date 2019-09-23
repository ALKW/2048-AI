import random
from nnetwork import node
import copy
import sys
 
class Network:
    # Inputs and Outputs have defined numbers, however internals do not and need to be kept track of.
    # Dictionary to keep track of all internal nodes with the number member as the key and weight as value
    internal_nodes_key = dict()

    # The next available number to assign to an internal node
    internal_nodes_num = 0

    # Dictionary for keeping track of all gene codes. 
    # Key is a gene (2 connected nodes) node1.number + " " + node2.number
    # Value is the innovation number for that gene (first gene discovered is 0, second gene discovered is 1, ...)
    gene_to_innovation_key = dict()

    # Reverse key value pair so key and value switch places for quicker lookup for innovation number
    innovation_to_gene_key = dict()

    # The current innovation number for genes. As the list is empty, the next gene to be created will be assigned 0
    curr_gene_num = 0

    # Used to ensure new networks added have the same input size as other networks
    input_size = 0

    # Used to ensure new networks added have the same outputs as other networks
    outputs = []

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
        # Fitness for the network, initialized to 0
        self.fitness = 0

        # Species for the network, initialized to 0.
        # Species is determined by which move (up, down, left, right) results in the least amount of game endings (a move is selected that doesnt do anything)
        self.species = -1

        # Historical Makrings to improve breeding uniqueness so that higher generations dont become replicas of lower generations
        self.generation = -1

        # Input layer of nodes
        self.inputs = [node.Node(value=inputs[x], num=(-1 * x) - 1) for x in range(len(inputs))]

        # Output layer of nodes
        self.outputs = [node.Node(0, desc=outputs[x], num=(-1 * (x + len(inputs)) - 1)) for x in range(len(outputs))]

        # internal nodes
        self.internal = []

        # Connections (genes) between nodes - a list of lists of length 2
        # Input node as numbered 0 -> len(self.inputs) - 1
        # Output nodes are len(self.inputs) -> len(self.inputs) + len(self.outputs) - 1
        # Internal nodes are kept track of using a dictionary with keys being the weight of the internal node
        self.genes = []

        # Error handling for new networks to ensure new networks have identical input and output parameters as other networks
        if Network.internal_nodes_num == 0:
            Network.internal_nodes_num = len(inputs) + len(outputs)

        if Network.input_size == 0:
            Network.input_size = len(self.inputs)

        if not Network.outputs:
            Network.outputs = [x.desc for x in self.outputs]

        if Network.input_size != Network.input_size:
            print("Invalud input length for new network. Exiting")
            exit(1)

        if Network.outputs != [x.desc for x in self.outputs]:
            print(Network.outputs)
            print(self.outputs)
            print("Invalid outputs for new network. Exiting")
            exit(1)
            

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
        # If stimuli are given then update the input neurons
        if stimuli != None:
            # Assign values to each input nodes based on stimuli passed in
            for input_node in self.inputs:
                input_node.value = stimuli[self.inputs.index(input_node)]

        # For each node, run DFS with it as the source in order to calculate the output node values
        # Output node values will be used to determine the appropriate move
        for input_node in self.inputs:
            # DFS style feed forward
            self.feed_forward(input_node)

            # DFS style reset, dont reset output node values
            self.reset_nodes(input_node, end=False)

        # Find maximum node
        output_info = self.find_max_output()

        # reset internal nodes and outputs
        for input_node in self.inputs:
            # DFS style reset
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
        # Because no loops can exist in this network, we dont have to worry about coloring nodes for DFS
        # Run recursively, so once we get to a node with no connections (this is an output node, or an internal node that doesnt connect to anything)
        # We recurse up and move on to the next node in the layer, similar to DFS
        for curr_node in start_node.connections:
            curr_node.value += start_node.value + start_node.weight
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
        # Use to determine if we want to reset output nodes as well
        outputs_too = end

        # Because no loops can exist in this network, we dont have to worry about coloring nodes
        # For each starting node (a.k.a - input node) run a DFS style search that resets all values in the network to 0
        for curr_node in start_node.connections:
            # If the node's desc is none then it it an internal node
            if curr_node.desc == None:
                curr_node.value = 0
            
            # If we want to reset output node values too
            if outputs_too:
                curr_node.value = 0

            # Recursively call itself
            self.reset_nodes(curr_node, end=outputs_too)
    
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
        # Initialize variables
        max_node = node.Node(float("-inf"))
        max_nodes = [max_node]

        # Find the maximum node(s)
        for output_node in self.outputs:
            # Determine the maximum node
            if output_node.value > max_node.value:
                max_node = output_node
                max_nodes = [max_node]

            # if there are two or more output nodes that share the same value append them all to the list
            elif output_node.value == max_node.value:
                max_nodes.append(output_node)

        # Sort the outputs by value, largest value is highest rank
        ranks = copy.deepcopy(self.outputs)
        ranks.sort(key=lambda x: x.value, reverse=True)

        return max_nodes, len(max_nodes), ranks

    def breed_with(self, other_parent):
        '''
        Breeds two neural networks together using genome markers in the network. The resulting child contains all the genes
        from both parents. If both parents share a gene, the child only gets one of that gene from either the first or second parent.
        Args:
            other_parent (Network object) - Other parent to mutate from
        Returns:
            child (Network object) - Network object contains traits of both parents
        Raises:
            None
        '''

        INTERNAL_START_NUM = len(self.inputs) + len(self.outputs)
        INTERNAL_NODE_OFFSET = len(self.inputs) + len(self.outputs)
        OUTPUT_NODE_OFFSET = len(self.inputs)

        # Create a network object to be the child
        child = Network(inputs=[x.value for x in self.inputs], outputs=[x.desc for x in self.outputs])
        for x in child.outputs:
            if x.desc == None:
                print(child)
                sys.exit("Child has none in output node")
        
        #-----------GENE BREEDING----------#
        # Get the genes from each parent
        calling_parent_genes = self.genes
        arg_parent_genes = other_parent.genes

        # Create the set of genes to be passed to the child
        # Duplicate genes are removed automatically as it is a set
        # Child gets all genes from both parents
        child_genes = set()
        for gene in calling_parent_genes:
            child_genes.add(gene)
        for gene in arg_parent_genes:
            child_genes.add(gene)

        # Go through the set of genes and add them to the childs genes
        for gene in child_genes:
            child.genes.append(gene)

        # Create the childs connections from the genes it was given
        # Each gene is kept track of by an innovation number
        for innovation_num in child.genes:

            # Decode the inovation number from the global dictionary of innovation numbers 
            nodes = Network.innovation_to_gene_key[str(innovation_num)]
            nodes = nodes.split()

            # Get the two genes that are connected. Left node connects to right node
            left_node_index = int(nodes[0])
            right_node_index = int(nodes[1])

            # Right node can only be an internal or output node as two input nodes cannot be connected
            # If right node is an output node
            if right_node_index < INTERNAL_START_NUM:
                output_node_index = right_node_index - OUTPUT_NODE_OFFSET
                right_node = child.outputs[output_node_index]
            # Otherwise the right node is an internal node
            else:
                # adjust for offset as the list of nodes goes 
                internal_node_index = right_node_index - INTERNAL_NODE_OFFSET

                # Create the node if it doesnt exist
                unique = True
                for internal_node in child.internal:
                    # if not unique then dont make a new node
                    if internal_node.number == internal_node_index:
                        unique = False
                        right_node = internal_node

                # If the node innovation number has not been added to the childs internal nodes then create a new node
                if unique:
                    # Get the weight of the internal node to create a new internal node for the new network
                    right_node_weight = Network.internal_nodes_key[str(internal_node_index)]
                    right_node = node.Node(weight=right_node_weight, num=internal_node_index)
                    child.internal.append(right_node)

            ## Left node can only be input or internal node
            # Add the right node to the conection list of the left node
            if left_node_index < INTERNAL_START_NUM:
                # left node is an input node
                child.inputs[left_node_index].connections.append(right_node)
            else:
                # left node is an internal node
                # adjust for offset
                internal_node_index = left_node_index - INTERNAL_NODE_OFFSET

                # create the new internal node if it doesnt exist
                unique = True
                for internal_node in child.internal:
                    if internal_node.number == internal_node_index:
                        unique = False
                        left_node = internal_node

                # If the node innovation number has not been added to the childs internal nodes then create a new node
                if unique:
                    # adjust for offset
                    internal_node_index = left_node_index - INTERNAL_NODE_OFFSET

                    # Create the node
                    left_node_weight = Network.internal_nodes_key[str(internal_node_index)]
                    left_node = node.Node(weight=left_node_weight, num=internal_node_index)
                    child.internal.append(left_node)

                # Add the internal node to the left node's connection list
                left_node.connections.append(right_node)
        
        return child

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
        # If no mutation was passed in, choose a random one
        if mutation == -1:
            mutation = random.randint(0, 3)

        if mutation == 0:
            # Either connects an input -> output or an internal -> output
            # Choose either an internal or an input node; 0 - input, 1 - internal
            # Choose the input/internal node to connect to the output node (both are random)
            self.mutation_add_branch()

        if mutation == 1:
            # Create a new internal node
            # select two nodes to connect to the new internal node
            self.mutation_create_node()

        if mutation == 2:
            # Choose an internal node and modify its weight
            # Determine if there are any nodes to begin with
            self.mutation_modify_internal_weight()

        if mutation == 3:
            # Choose an input node and modify its weight
            self.mutation_modify_input_weight()

        self.update_genes()

    def mutation_add_branch(self):
        # Error checking to make sure there exists internal nodes
        if len(self.internal) > 0:
            choice = random.randint(0, len(self.internal) + len(self.inputs) - 1)
            internal_index = random.randint(0, len(self.internal) - 1)
        # if there are no internal nodes, then the only choice is input -> output
        else:
            choice = 0
            internal_index = 0

        input_index = random.randint(0, len(self.inputs) - 1)
        output_index = random.randint(0, len(self.outputs) - 1)
        count = 0

        # try 1000 times to do a valid mutation, and if its not possible, then do another mutation
        while count < 1000:
            if choice <= len(self.inputs) - 1 and self.outputs[output_index] not in self.inputs[input_index].connections:
                self.inputs[input_index].connections.append(self.outputs[output_index])
                break
            if choice > len(self.inputs) - 1 and self.outputs[output_index] not in self.internal[internal_index].connections:
                self.internal[internal_index].connections.append(self.outputs[output_index])
                break

            # Find new indices for internal
            if len(self.internal) > 0:
                choice = random.randint(0, 1)
                internal_index = random.randint(0, len(self.internal) - 1)

            # Find new indices for input and output
            input_index = random.randint(0, len(self.inputs) - 1)
            output_index = random.randint(0, len(self.outputs) - 1)
            count += 1

        # If nothing was modifided then move on and try another mutation
        if count >= 1000:
            self.mutate(mutation=random.randint(1, 3))

    def mutation_create_node(self):
        # Assign the node the next availble global internal marker
        to_add = node.Node(weight=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]), num=Network.internal_nodes_num)
        # add it to the list of internals with the weight as the value and number as the key
        Network.internal_nodes_key[str(Network.internal_nodes_num)] = to_add.weight
        Network.internal_nodes_num += 1

        # Combinations include:
        # input -> new -> internal
        # input -> new -> output
        # internal -> new -> output
        first_node_index = random.randint(0, len(self.inputs) + len(self.internal) - 2)

        # If the node is an internal then only an output node can be selected
        # internal -> new -> output
        if first_node_index >= len(self.inputs):
            second_node_index = random.randint(0, len(self.outputs) - 1)

            # Adjust the index
            first_node_index -= len(self.inputs)

            # Connect the internal to the new node
            self.internal[first_node_index].connections.append(to_add)

            # and the new node to the output
            to_add.connections.append(self.outputs[second_node_index])
        # otherwise an internal or an output node can be appened to the end of the chain
        else:
            second_node_index = random.randint(0, len(self.internal) + len(self.outputs) - 2)

            # Connect the input to the new node
            self.inputs[first_node_index].connections.append(to_add)

            # Connect the new node to the output
            # input -> new -> output
            if second_node_index >= len(self.internal):
                second_node_index -= len(self.internal)
                to_add.connections.append(self.outputs[second_node_index])
            # connect the new node to the internal
            # input -> new -> internal
            else:
                to_add.connections.append(self.internal[second_node_index])

        # Add the nodes to the list of internals for the network
        self.internal.append(to_add)

    def mutation_modify_internal_weight(self):
        # If there are none, then then choose another mutation that doesnt involve internal nodes
        if len(self.internal) == 0:
            self.mutate(mutation=random.choice([1,3]))
            return

        mutate_index = random.randint(0, len(self.internal) - 1)
        curr_weight = self.internal[mutate_index].weight
        poss_weights = set(range(-5,6))

        # Make sure a change actually happens and a weight of 0 is not achieved
        poss_weights.remove(0)
        poss_weights.remove(curr_weight)

        # Change the weight of the internal node
        self.internal[mutate_index].weight = random.choice(list(poss_weights))

    def mutation_modify_input_weight(self):
        mutate_index = random.randint(0, len(self.inputs) - 1)
        curr_weight = self.inputs[mutate_index].weight
        poss_weights = set(range(-5,5))

        # Make sure a change actually happens and a weight of 0 is not achieved
        poss_weights.remove(0)
        poss_weights.remove(curr_weight)

        # Change the weight of the internal node
        self.inputs[mutate_index].weight = random.choice(list(poss_weights))

    def update_genes(self):
        # Goes through all paths in the network and updates the genes list member for the network
        # Left node can only be input or internal,, so just cycle through all internal/input nodes for the network
        INTERNAL_NODE_OFFSET = len(self.inputs) + len(self.outputs)

        # Keys consist of "leftNode + " " +  rightNode"
        for input_node in self.inputs:
            # Get the first half of the key
            first_half_key = self.inputs.index(input_node)
            self.determine_genes(input_node, first_half_key)

        for internal_node in self.internal:
            # Get the first half of the key
            # If the internal node does not have a number assigned to it, then it needs to be assigned one
            if internal_node.number == None:
                internal_node.number = Network.internal_nodes_num
                Network.internal_nodes_key[str(Network.internal_nodes_num)] = internal_node.weight
                Network.internal_nodes_num += 1
            first_half_key = internal_node.number + INTERNAL_NODE_OFFSET
            self.determine_genes(internal_node, first_half_key)
    
    def determine_genes(self, curr_node, first_half_key):
        INTERNAL_NODE_OFFSET = len(self.inputs) + len(self.outputs)
        OUTPUT_NODE_OFFSET = len(self.inputs)

        for con_node in curr_node.connections:
            # If the connection node is an output node, set the second half of the key
            if con_node.desc != None:
                second_half_key = self.outputs.index(con_node) + OUTPUT_NODE_OFFSET
            # Else the second half of the key is another internal node
            else:
                if con_node.number == None:
                    con_node.number = Network.internal_nodes_num
                    Network.internal_nodes_key[str(Network.internal_nodes_num)] = con_node.weight
                    Network.internal_nodes_num += 1
                second_half_key = con_node.number + INTERNAL_NODE_OFFSET

            # Create the key
            key = str(first_half_key) + " " + str(second_half_key)

            # If the key is not in the dictionary, add it, then take its innovation number
            if key not in Network.gene_to_innovation_key:
                Network.gene_to_innovation_key[key] = Network.curr_gene_num
                Network.innovation_to_gene_key[str(Network.curr_gene_num)] = key
                Network.curr_gene_num += 1

            # Get the gene value
            gene_value = Network.gene_to_innovation_key[key]

            # determine if the gene is already marked in the list and add it if it is not yet
            if gene_value not in self.genes:
                self.genes.append(gene_value)

                       
    def print_s(self):
        print("Fitness: ", self.fitness)
        print("Species: ", self.species)
        print("Generation: ", self.generation)
        print("Genes: ", self.genes, "\n")

    def print_d(self):
        print("Fitness: ", self.fitness)
        print("Species: ", self.species)
        print("Generation: ", self.generation)
        print("Genes: ", self.genes, "\n")
        print("Topology: ")
        self.print_node_paths()

    def __str__(self):
        print("Topology: ")
        self.print_node_paths()
        return "Fitness: " + str(self.fitness) + " Species: "+ str(self.species) + " Generation: " + str(self.generation) + " Genes: " + str(self.genes) + "\n"

    def print_node_paths(self):
        # Start with each internal nodes
        for input_node in self.inputs:
            self.find_paths_to_print(input_node, [])
            print()
            
    def find_paths_to_print(self, curr, path):
        # append the current node to the path
        path.append(curr)

        # if we reach a node with no other connections, then print and return
        if len(curr.connections) == 0:
            print("PATH FOR NODE",  self.inputs.index(path[0]), ":", end="")
            for curr_node in path[:-1]:
                print("[ Weight:", curr_node.weight, "I-Num:", curr_node.number, "] -> ", end="")
                
            if path[-1].desc != None:
                print(path[-1].desc)
            else:
                print("[ Weight:", path[-1].weight, "I-Num:", path[-1].number, "]-> [-None-]")
            return

        # Append the current node to the path and then return
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
    # Create a list of blank network objects
    networks = [Network(inputs, outputs) for x in range(count)]

    # For each network connect all four output nodes to input nodes initially
    for network_index in range(count):
        for output_index in range(len(networks[network_index].outputs)):
            # choose the node from input layer to connect to the output node randomly
            input_index = random.randint(0, len(inputs) - 1)

            # Connect the input node to the output node
            networks[network_index].inputs[input_index].connections.append(networks[network_index].outputs[output_index]) 

        # fill in the genes for the network   
        networks[network_index].update_genes()

    return networks








    
