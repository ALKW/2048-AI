class Node:
    def __init__(self, value, desc=None):
        self.value = value
        self.desc = desc
        self.next = [Node(None)]