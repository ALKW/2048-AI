from neural_network import Network

#species determined by combination of traits; hidden_layer, hidden_width, and act_func

#Have sets of 20 species max. At each stage:
#   Delete 4 lowest performers. : -4 
#   Mate top 4 perfomers. : +6
#   Mutate Next top 4: +4