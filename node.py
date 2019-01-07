class Node:
    def __init__(self, value=0, weight=1, desc=None):
        self.value = value
        self.weight = weight
        self.desc = desc
        self.connections = []

    def print(self):
        print("Value:", self.value, "| Weight:", self.weight, "| Description:", self.desc, "| Connected to", len(self.connections), "Nodes\n") 