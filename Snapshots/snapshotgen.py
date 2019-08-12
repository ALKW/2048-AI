from time import gmtime, strftime

class snapshot:
    def __init__(self, population, species, gtoi_key):
        self.population = population
        self.species = species
        self.gtoi_key = gtoi_key
    
    def create_snapshot(self):
        # Create a file
        file = self.create_file()

        # Print header information
        self.print_header(file)

        # Print the gene to innovation key to the file
        self.print_gtoi_key(file)

        # Print the species key to the file
        self.print_species_key(file)

        # Print the population key to the file
        self.print_networks_key(file)

    def create_file(self):
        today = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
        file = open("Snapshots/snapshot" + today + ".snp", "w+")

        return file

    def print_header(self, file):
        file.write("# Header\n")

    def dtol(self, dic):
        #Convert dictionary to key and value lists
        keys = list()
        for entry in dic.keys():
            keys.append(entry)

        values = list()
        for entry in dic.values():
            values.append(entry)
        
        return keys, values

    def print_gtoi_key(self, file):
        file.write("# Life Parameters - Gene to Innovation Key\n")
        
        keys, values = self.dtol(self.gtoi_key)

        for i in range(len(keys)):
           file.write(str(keys[i]) + ":" + str(values[i]) + "\n") 

    def print_species_key(self, file):
        file.write("# Life Parameters - Species\n")

        keys, values = self.dtol(self.species)

        for i in range(len(keys)):
           file.write(str(keys[i]) + ":" + str(values[i]) + "\n")  

    def print_networks_key(self, file):
        file.write("# Life Parameters - Networks\n")
        for network in self.population:
            #Write the input nodes to the file
            file.write("# Inputs")
            for node in network.inputs:
                file.write("[" + node.to_str() + "]\n")

            file.write("# Internals")
            for node in network.internal:
                file.write("[" + node.to_str() + "]\n")

            file.write("# Outputs")
            for node in network.outputs:
                file.write("[" + node.to_str() + "]\n")
        
        

