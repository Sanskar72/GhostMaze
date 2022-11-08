# GhostMaze
Make multiple agents who can traverse through a multitude of probabilistic environments of varying sizes. 
<br>The agent has to reach a goal node from a start node in a maze that is filled with ghosts and needs to do it to maximise its safety all while going closer to the goal.
<br>The agents use graph theory and graph traversal techniques to make a AI model to traverse throuhg the graph.
<br> The agent is capable of using basic BFS, A star to find shortest path to the goal.
<br> To avoid ghosts, we are using Monte Carlo simulations to find which path is the safest.
<br> To make the agent invincible, we have also added sensing capabilities to the agent, such that he can sense presence of ghosts nearby ad move away from it if his "senses" kick in.
