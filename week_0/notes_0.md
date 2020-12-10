# **Lecture Notes 1**

## **Artificial Intelligence (AI)**

* We will explore ideas of AI: problems where computers try to solve some general problems

## **Lectures**

* Search: AI will be able to solve a search problem
* Knowledge: AI will be able to "know" and draw conclussions based on info.
* Uncertainty: AI is not 100% sure that some asnwer **is** the answere
* Optimization: find not only the answer but the best answer
* Machine Learning (ML): AI is able to "learn" from data
* Neural Networks
* Language: Natural Language Processing (NLP)

## **Today: Search Problem**

* Ex: find a solution of a maze or a puzzle, find the best way to go from point A to point B.

### **Terminology**

* **agent**: entity that perceives its environment and acts upon that environment.
* **state**: some configuration of the agent and its environment.
* **initial State**: starting point of the search problem.
* **actions**: choices that can be made in a state. ``ACTIONS(s)`` ``s`` is a state and ``ACTIONS`` return the set of actions that can be executed to some state.
* **transition model** a description of what state results from performing any applicable action in any state. ``RESULT(s, a)`` returns the state resulting from action ``a`` in state ``s``.
* **state space**: set of all possible states resulting from a the initiel state. Can be thought as the graph representing the states and possible transitions.
* **goal test**: way to determine whether a given state is a goal state.
* **path cost**: numerical cost associated with a given path. We usually want to find the path that minimizes the cost.
* **search problem**: a search problem is a tuple of
  * initial state
  * actions
  * transition model
  * goal test
  * path cost function
* **solution**: swquence of actions taking us from the initial state to the goal state
* **optimal solution**: solution that has the lowest path cost.
* **node**: data structure that keeps track of:
  * a state
  * a parent (node that  generated this node)
  * an action (action applied to parent to get node)
  * a path cost (from initial state to node)

### **Approach to a search algorithm**

* start with a forntier that contains the initial state.
* repeat:
  * if the frontier is empty, then no solution
  * remove a node from the frontier
  * if the node we removed contains goal state, return solution
  * expand node, add resulting nodes to the frontier.

### **Drawbacks of the previous approach**

* When there graph has double-way arrows i.e. when there is reveribility in some transition models, we can get into an infinite loop.
  * solution: keep track of the states we have already visited

### **Approach revisited**

* start with a forntier that contains the initial state.
* start with an empty explored set
* repeat:
  * if the frontier is empty, then no solution
  * remove a node from the frontier
  * if the node we removed contains goal state, return solution
  * add the removed node to the explored set
  * expand node, add resulting nodes to the frontier only if they are not already in the frontier or the explred set.

### **Depth-first search (DFS)**

* **stack**: last-in first-out data structure.

When we use a stack in the frontier this is called **depth-first search (DFS)** algorithm. This strategy will search each branch at a time.

### **Breath-first search (BFS)**

* **queue**: first-in first-out data structure.

When we choose the frontier to behave as a queue this is called a **breath-first search (BFS)** algorithm. This will explore all the branches of the tree simultaneously.

### **Uninformed search**

Search strategy that uses no problem-specific knowledge.

### **Informed search**

Search strategy that uses problem-specific knowledge to find solutions more efficiently.

### **Greedy best-first search**

Search algorithm that expands the node that is closest to the goal, as estimated by a heuristic function ``h(n)``.

### **A* search**

This search algorithm not only takes into consideration the heuristic function ``h(n)`` but also how far did the algorithm "had to travel in order to get here."

This algorithm expands the node with lowest value of ``g(n) + h(n)`` where
  
* ``g(n)`` = cost to reach node
* ``h(n)`` = estimated cost to goal

This helps to find more optimal solutions under some circumstances:

* ``h(n)`` is admissible (never overestimates the true cost), and
* ``h(n)`` is consistent (for every node n and successor ``n'`` with step cost ``c``, ``h(n) <= h(n') + c``)

### **Adverse Search**

In each step there is "someone" trying to block or stop us from winning (this is the case of a game).

### **Minimax algorithm**

We choose two players: ``MIN`` and ``MAX``. We also set some numbers to different outcomes.

eg. in tic-tac-toe if:
  
* O wins: we assign a value of -1
* Not O nor X wins: we assign a value of 0
* X wins: we assign a value of +1

This way, ``MIN`` will be O and will try to minimize the outcome and ``MAX`` will be X and will try to maximise the outcome.

Minimax will consider all possible moves.

Given a state s:

* ``MAX`` picks action a in ACTIONS(s) that produces highest vallue of MIN-VALUE(RESULT(s, a))
* ``MIN`` picks action a in ACTIONS(s) that produces smallest value of MAX-VALUE(RESULT(s, a))

```bash
function MAX-VALUE(state):
  if TERMINAL(state):
    return UTILITY(state)
  v = - infinity
  for action in ACTIONS(state):
    v = MAX(V, MIN-VALUE(RESULT(state, action)))
  return v

function MIN-VALUE(state):
  if TERMINAL(state):
    return UTILITY(state)
  v = infinity
  for action in ACTIONS(state):
    v = MIN(V, MAX-VALUE(RESULT(state, action)))
  return v
```

A **game** is a set of

* ``S0``: initial state
* ``PLAYER(s)``: returns whoch player to move in state ``s``
* ``ACTION(s)``: returns legal moves in state ``s``
* ``RESULT(s, a)``: returns state after action ``a`` taken in state ``s``
* ``TERMINAL(s)``: checks if state ``s`` is a terminal state
* ``UTILITY(s)``: final numerical value of terminal state ``s``

Alpha-Beta pruning is an optimization of this algorithm: just looking for the branches with the best solution

### **Depth-Limited minimax**

We will need an **evaluation function** that given a state gives us a number stating how good (or bad) is the game for ``MAX`` or ``MIN``. The better this function, the better the AI.
