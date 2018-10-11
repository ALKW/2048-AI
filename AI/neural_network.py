import node

class Network():
    def __init__(self):
        #generate inputs
        self.inputs = [node.Node(label) for label in range(16)]
        #generate outputs
        self.outputs = [node.Node(label) f or label in range(4)]

    def breed(self):
        pass

    def create_random(self):
        pass

    def create_population(self, count):
        pop = []