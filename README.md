# 2048-AI - Version 2.0
## Description
Python based AI that learned to play 2048 on its own. 

The goal was to make the neural netowrk as generic as possible to make it possible not only to learn how to play 2048, but other games potential using a transition layer that converts the current state of the game to a standard stimuli to feed into the game.

Everything except the visual library (pygame) was created from scratch 

## Version 2.0:  
1. Breeding is done within species and mutating is done within species  
    - Follows the Genetic algorithm: NEAT  
    - Top networks from each species are used
2. Total Population of 100 (Can be made up of multiple species)
    - Each species has a restriction of a max of 20
3. Each network has a group of genes that keep track of which nodes are connected
    - Genes determine the species of a network
4. Network class modified to be easily generalized to multiple types of games
5. Life class can be easily generalized to multiple types of games by using a transition layer defined by the user that converts the current state of a game to stimuli (a list of items) that are then read in by the AI.

## Version 1.0:  
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
  
## Dependencies
pygame

## Usage
Run AI_Script.py from the command line using:
  ```
  python AI_Script.py
  ```
