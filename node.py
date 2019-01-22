class Node:
    def __init__(self, value=0, weight=1, num=None, desc=None):
        self.value = value
        self.weight = weight
        self.desc = desc
        self.number = num
        self.connections = []

    def print(self):
        print("I-Num:", self.number, "| Weight:", self.weight, "| Description:", self.desc, "| Connected to", len(self.connections), "Nodes\n") 
