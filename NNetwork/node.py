class Node:
    def __init__(self, value=0, weight=1, num=None, desc=None):
        self.value = value
        self.weight = weight
        self.desc = desc
        self.number = num
        self.connections = []

    def print(self):
        print("I-Num:", self.number, "| Weight:", self.weight, "| Description:", self.desc, "| Connected to", len(self.connections), "Nodes\n") 

    def to_str(self):
        return self.number + ":" + self.weight + ":" + self.desc + ":" + str([x.number for x in self.connections])

    def to_str_det(self):
        return "I-Num:" + self.number + "|Weight:" + self.weight + "|Description:" + self.desc + "|Connections:" + str([x.number for x in self.connections])