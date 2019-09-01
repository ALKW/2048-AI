import sys
from NNetwork import life
from NNetwork import neural_network as network

# Single pass parser that builds a life object from a snapshot (.snp) file
class Parser:
    def __init__(self, filename):
        if ".snp" not in filename:
            print("Invalid file type, quitting...")
            sys.exit()

        self.file = open(filename, "r")
        self.ops = {"GG": self.build_gtoi_key, 
                    "GS": self.build_species_key, 
                    "NS": self.build_network}

    def build_world(self):
        line = self.file.readline()
        while line:
            # Ignore comments
            if "#" in line:
                line = self.file.readline()
                continue

            # "$" Indicates a new category
            if "$" in line:
                category = line.split(" ")
                self.ops[category[1]]()

            line = self.file.readline()
        return self.world


    def build_gtoi_key(self):
        KEY = 0
        VALUE = 1

        line = self.file.readline()
        while line:
            # If we see a "$" then we know we are in another section
            if "$" in line:
                return
            elif "#" in line:
                line = self.file.readline()
                continue
            else:
                key_val = line.split(":")
                network.Network.gene_to_innovation_key[key_val[KEY]] =  key_val[VALUE]
                network.Network.innovation_to_gene_key[key_val[VALUE]] =  key_val[KEY]
            
            # Read next line in    
            line = self.file.readline()


    def build_species_key(self):
        KEY = 0
        VALUE = 1

        line = self.file.readline()
        while line:
            # If we see a "$" then we know we are in another section
            if "$" in line:
                return
            elif "#" in line:
                line = self.file.readline()
                continue
            else:
                key_val = line.split(":")
                life.Life.species[key_val[KEY]] = key_val[VALUE]
            
            # Read next line in    
            line = self.file.readline()

    def build_network(self):
        # Initialize the life object with the a number of empty networks equal to the number of networks in the file
        line = self.file.readline()
        world_size = int(line.split(":")[1])
        self.world = life.Life(world_size,                     [
                    0,0,0,0,
                    0,0,0,0,
                    0,0,0,0,
                    0,0,0,0,
                    0,0,0,0,
                    0,0,0,0
                    ], 
                    ["up", "down", "left", "right"])
        pass