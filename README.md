# 2048-AI
### Description
Python based AI that learned to play 2048 on its own.  All code written from scratch

#### Version 1.0:  
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
  

### Dependencies
pygame
