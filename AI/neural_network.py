import numpy as np
import random 
 
class Network:
    def __init__(self, hidden_count, hidden_width, act_func):
        '''
        Parameters of Neural Network:
            -Number of hidden layers
            -Size of hidden layers
            -Activation function
                Sigmoid - 0
                Tanh - 1
                Linear - 2
        '''
        #generate inputs
        self.inputs = np.array([])
        #generate hidden layer
        self.hidden = np.array([list(range(hidden_width)) for x in range(hidden_count)])
        #generate outputs
        self.outputs = np.array([0 for x in range(4)])
        #choose activation function
        self.act = act_func
        #network parameters
        self.param = [hidden_count, hidden_width, act_func]
        #fitness
        self.fitness = 0

    def feed(self, stimuli):
        stimuli = np.array(stimuli)
        outputs = np.array([])
        first_layer = self.hidden[1]

        #feed input layer into first hidden layer
        for i in range(len(first_layer)):
            outputs.append(self.act_function(np.sum(stimuli * first_layer[i]), self.param[2]))
        inputs = outputs
        outputs = np.array([])

        #Feed inputs into the remaining hidden layers
        for layer in range(1, len(self.hidden)):
            for i in range(len(layer)):
                outputs.append(self.act_function(np.sum(inputs * first_layer[i]), self.param[2]))
            inputs = outputs
            outputs = np.array([])

        #Feeds inputs into the output layer
        for i in range(len(self.outputs)):
            outputs.append(self.act_function(np.sum(inputs), self.param[2]))

        #Determines best move and returns index; 0 - 3 (left, right, down, up)
        return outputs.index(max(outputs))
        
    def act_function(self, input, func):  
        if(func == 0):
            return self.sigmoid(input)
        elif(func == 1):
            return np.tanh(input)
        elif(func == 2):
            return input
        return input

    def breed(self, other_parent):
        #Child has traits from both parents, weights are updated using a optimizer from the most successful parent
        pass

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def print_layers(self):
        print("inputs: ") 
        print(self.inputs)
        print("Hidden: ")
        for i in range(0, len(self.hidden)):
            print(self.hidden[i])
        print("Outputs: ")
        print(self.outputs)

    

def create_random(hidden=4, width=256, act_start=0, act_stop=2):
    '''
    Creates a network using random parameters with limits
    Args:
        hidden (int) Number of hidden layers. Default: 4
        width (int) Number of nodes in layer. Default: 256
        act_start (int) Starting number for limiting size of activation function. Default: 0
        act_stop (int) Ending number for limiting size of activatino funciton. Default: 2
    Returns:
        Network (Network object) Network object with random parameters
    Raises:
        None
    '''
    hidden_count = random.randint(1, hidden)
    hidden_width = random.randint(4, width)
    act_func = random.randint(act_start, act_stop)
    return Network(hidden_count, hidden_width, act_func)

def create_init_population_species(count, hidden=4, width=256, act_start=0, act_stop=2):
    '''
    Returns a list of neural networks that has length count
    Args:
        Count (int) number of memembers of species population
    Returns:
        Population (list of neural network objects)
    Raises:
        None
    '''
    pop = []
    for i in range(count):
        pop.append(create_random(hidden, width, act_start, act_stop))
    return pop