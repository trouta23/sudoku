## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In the naked twins problem we are faced with the situation where we have two spaces that are in the same row, column, or block that both have the same possible choices. We then look around at the other spaces in the same row, column, and/or block as our naked twins, and observe their possible choices; this is where constraint propagation comes in. For example, lets say we have the possibilities analyzed for the top three rows and find multiple naked twins. We can continually apply naked twins to deduce what other spaces cannot be and even infer possible solutions. Say we have a naked twin pair of 1 and 3, and a third space where its possibilities are a 1, 4, or 7. We know that the naked twin pair must be either a 1 or a 3, so we can then remove the 1 from the third space. Using this method and others over and over allows us to, hopefully, get one step closer to a solution.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Student should provide answer here*

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

### Code

* `solution.py`
* `solution_test.py` - You can test your solution by running `python solution_test.py`.
