import numpy as py

class Network:
    def __init__(self, hidden_count):
        #generate inputs
        self.inputs = [1 for x in range(16)]
        #generate hidden layers
        self.hidden_layers = [[1 for x in range(8)] for x in range(hidden_count)]
        #generate outputs
        self.outputs = [0 for x in range(4)]

    def run(self, stimuli):
        #fill in the inputs layer with numbers based on game board
        for i in range(0, len(stimuli)):
            #equation for determining results from input. result is between 0 and 1
            self.inputs[i] = self.sigmoid(stimuli[i])
        
    def breed(self):
        pass

    def create_random(self):
        pass

    def create_population(self, count):
        pop = []

    def sigmoid(self, x):
        return 1 / (1 + py.exp(-x))

    def print_layers(self):
        print("inputs: ") 
        print(self.inputs)
        print("Hidden: ")
        for i in range(0, len(self.hidden_layers)):
            print(self.hidden_layers[i])
        print("Outputs: ")
        print(self.outputs)

    

    