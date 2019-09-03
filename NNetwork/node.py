class Node:
    def __init__(self, value=0, weight=1, desc=None, num=None):
        self.value = value
        self.weight = weight
        self.desc = desc
        self.number = num
        self.connections = []

    def __str__(self):
        print("I-Num:", self.number, "| Weight:", self.weight, "| Description:", self.desc, "| Connected to", len(self.connections), "Nodes\n") 

    def to_str(self):
        toRtrn = str(self.weight) + ":"

        if self.desc == None:
            toRtrn += "-1:"
        else:
            toRtrn += str(self.desc) + ":"

        if self.number == None:
            toRtrn += "-1:"
        else:
            toRtrn += str(self.number) + ":"

        rem = 0
        for x in self.connections:
            if self.number != None:
                toRtrn += str(x.number) + ","
                rem = 1
        if rem == 1:
            toRtrn = toRtrn[:-1]
        
        return toRtrn

    def to_str_det(self):
        toRtrn = "Weight: " + str(self.weight) + "|Description: "

        if self.desc == None:
            toRtrn += "-1|Number: "
        else:
            toRtrn += "|Number: " + self.desc

        if self.number == None:
            toRtrn += "-1|Connections: "
        else:
            toRtrn += self.number + "|Connections: "

        toRtrn += "{"
        rem = 0
        for x in self.connections:
            if self.number != None:
                toRtrn += str(x.number) + ","
            rem = 1
        if rem == 1:
            toRtrn = toRtrn[:-1]
        toRtrn += "}"
        
        return toRtrn