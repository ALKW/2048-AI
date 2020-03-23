# NEAT Version 2.1

## Description
AI that learned to play 2048 on its own. 

The goal was to make a neural netowork that learned to play 2048, while also making a lirbary that would allow people to build neural networks that follow the N.E.A.T Genertic algorithms. Originally the project was a library that only worked with 2048, hence the old name 2048-AI, however a new goal of mine was to abstract out the game and eventually the library became known NEAT-AI with 2048 as one of the examples.

The networks take as input a serialized version of the users choosing, whether it be the screen pixels or the numbers on the board and outputs a string corresponding to what the user specifies. The user can then take this and update the corrresponding game.

The library as of now features the N.E.A.T algorithm and automatically handles ranking and updating neural networks. It also supports snapshot generation and snapshot parsing to allow users to pick up from where they left off last as well as share snapshots.

## NEAT-AI Version 2.1:
1. Added snapshot generation to allow a group of networks to be saved after the simulation is complete.
2. Added snapshot parsing to allow the user to start where they left off in a network using a previously generated snapshot.
3. Added a tests folder to add tests to verify integrity of N.E.A.T Library

## NEAT-AI Version 2.0:  
1. Breeding is done within species and mutating is done within species  
    - Follows the Genetic algorithm: NEAT  
    - Top networks from each species are used
2. Total Population of 100 (Can be made up of multiple species)
    - Each species has a restriction of a max of 20
3. Each network has a group of genes that keep track of which nodes are connected
    - Genes determine the species of a network
4. Network class modified to be easily generalized to multiple types of games
5. Life class can be easily generalized to multiple types of games by using a transition layer defined by the user that converts the current state of a game to stimuli (a list of items) that are then read in by the AI.

## NEAT-AI Version 1:  
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
The 2048 example uses the pygame[https://www.pygame.org/contribute.html] package for rendering the game
