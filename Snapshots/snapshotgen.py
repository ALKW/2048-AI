from time import gmtime, strftime

import inspect
import os
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir) 
from nnetwork import neural_network as network

class Cons:
    FILE = 0
    FILENAME = 1

class Snapshot:
    def __init__(self, population, species, gtoi_key):
        self.population = population
        self.species = species
        self.gtoi_key = gtoi_key
    
    def create_snapshot(self, filename=None):
        # Create a file
        filedata = self.create_file(filename)
        file = filedata[Cons.FILE]

        # Print header information
        self.print_header(file)

        # Print the gene to innovation key to the file
        self.print_gtoi_key(file)

        # Print the species key to the file
        self.print_species_key(file)

        # Print the population key to the file
        self.print_networks_key(file)

        # Close the file
        file.close()

        # Return the name of the file
        return filedata[Cons.FILENAME]

    def create_file(self, filename=None):
        if filename == None:
            today = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
            filename = "snapshot" + today + ".snp"
        file = open(filename, "w+")

        return [file, filename]

    def print_header(self, file):
        file.write("# Header\n")

    def dtol(self, dic):
        # Convert dictionary to key and value lists
        keys = list()
        for entry in dic.keys():
            keys.append(entry)

        values = list()
        for entry in dic.values():
            values.append(entry)
        
        return keys, values

    def print_gtoi_key(self, file):
        file.write("# Life Parameters - Gene Composition to Gene Number Key\n")
        file.write("$ GG\n")
        
        keys, values = self.dtol(self.gtoi_key)

        for i in range(len(keys)):
           file.write(str(keys[i]) + ":" + str(values[i]) + "\n") 

    def print_species_key(self, file):
        file.write("# Life Parameters - Genes to Species\n")
        file.write("$ GS\n")

        keys, values = self.dtol(self.species)

        for i in range(len(keys)):
           file.write(str(keys[i]) + ":" + str(values[i]) + "\n")  

    def print_networks_key(self, file):
        # Header information about the shared networks structures
        file.write("\n# Life Parameters - Network Structure\n")
        file.write("$ NS\n")
        file.write("size:" + str(len(self.population)) + "\n")
        file.write("inp-size:" + str(network.Network.input_size) + "\n")
        file.write("int-size:" + str(len(network.Network.internal_nodes_key)) + "\n")
        outputs = str(network.Network.outputs[0])
        for item in network.Network.outputs[1:]:
            outputs += "," + str(item) 
        file.write("outs:" + outputs  + "\n")

        # Go through the population and make a snapshot of each
        for individual in self.population:
            # Signal New Network
            file.write("\n$ Network " + str(self.population.index(individual)) + "\n")

            # Write the input nodes to the file
            file.write("\n$ Inputs " + str(len(individual.inputs)) + "\n")
            for node in individual.inputs:
                file.write(node.to_str() + "\n")

            # Write the internal nodes to the file
            file.write("\n$ Internals " + str(len(individual.internal)) + "\n")
            for node in individual.internal:
                file.write(node.to_str() + "\n")
    
            # Write the output nodes to the file
            file.write("\n$ Outputs " + str(len(individual.outputs)) + "\n")
            for node in individual.outputs:
                file.write(node.to_str() + "\n")

        file.write("$ CS\n")
        
        

