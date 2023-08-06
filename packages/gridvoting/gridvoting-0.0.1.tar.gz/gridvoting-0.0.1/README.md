# gridvoting

Voting simulations on a 2D grid of feasible outcomes

Helper class and functions for a Markov Chain voting model
based on a series of status quos and random challenges.

**This software is at a pre-release stage and not yet intended for general use.**

Inputs:

* grid size in 2D -glimit <= x,y <= glimit
* utility functions for each voter for each point on the grid
* challenger strategy (zi True/False)

Outputs:
* Markov chain transition matrix
* Existence of core (absorbing) points
* Stationary distributions (no core)
* Diagnostic and distribution plots
