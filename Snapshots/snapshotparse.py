class Parser:
    def __init__(self, filename):
        self.file = open(filename, "r")

    def parse(self):
        line = self.file.readline()
        while line:
            print(line)
            line = self.file.readline()


        