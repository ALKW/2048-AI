from NNetwork import neural_network as network

test = network.create_init_population(2, [
                2,2,2,2,
                2,16,50,2,
                16,8,2,32,
                16,4,2,32,
                ], ["up", "down", "left", "right"])

# Add internal nodes
internal1 = node.Node(weight=2, num=0)
internal1.connections.append(test[0].outputs[0])   
 
internal2 = node.Node(weight=2, num=0) 
internal2.connections.append(test[1].outputs[0])

Network.internal_nodes_key['0'] = 2

#append the internal nodes to the same position
test[0].inputs[0].connections.append(internal1)
test[0].internal.append(internal1)
test[1].inputs[0].connections.append(internal2)

test[0].mutate(mutation=1)

test[0].update_genes()
print()
test[1].update_genes()

#create a child network
child = test[0].breed_with(test[1])

#print data
test[0].print()
test[1].print()
child.print()

print("Internal: ", Network.internal_nodes_key)
print("Gene to innovation", Network.gene_to_innovation_key)
print("Innovation to Gene", Network.innovation_to_gene_key)