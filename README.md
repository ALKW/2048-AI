# 2048-AI - Version 2.0
### Description
Python based AI that learned to play 2048 on its own. 

The goal was to make the neuron network inputs and outputs as easy as possible to modify in order to find the optimal combination of inputs and outputs.  

The game was created by hand using pygame and mimics the game 2048

### Version 1.0:  
1. No breeding only mutating
    - Top 5 mutated and original networks kept (+10)
    - Next top 5 networks kept the same (+5)
    - Mutate next top 5 (+5)
2. Each generation has a population of 20
3. Runs through 50 Generations
4. Visual Display of top 5 networks of 50th generations
5. Top member score from each generation is displayed at the end in the console
6. Topology of top 5 networks are displayed at the end in the console
7. Score is calculated through normal 2048 moves. Random moves produce a score of 0
8. The only inputs are the individual blocks on the board
9. The top networks develop a strategy of going back and forth either horizontally or vertically
    - Max Score levels out because of this
    - Can be seen in visualization at the end


### Version 2.0:  
1. Breeding is done within species and mutating is done within species  
    - Follows the Genetic algorithm: NEAT  
    - Top networks from each species are used
2. Total Population of 100 (variable)
    - Each species has a population of up to 20  
3. Each network has a group of genes that keep track of which nodes connect to which
    - Genes determine the species of a network
4. Network class can be easily generalized to multiple types of games
5. Life class can be easily generalized to multiple types of games
  
### Dependencies
pygame

### Usage
Run life.py from the command line using:
  ```
  python life.py
  ```
