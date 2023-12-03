## Algorithm Implementation README

# LAB9

Write a local-search algorithm (eg. an EA) able to solve the *Problem* instances 1, 2, 5, and 10 on a 1000-loci genomes, using a minimum number of fitness calls. That's all.

## Overview
This README provides a formal description of the implementation process for an algorithm designed to achieve optimal performances in a black box task, with less fitness evaluations. The problem and the fitness function are defined in [lab9_lib.py](./lab9_lib.py) and the algorithm is implemented in [lab9.ipynb](./lab9.ipynb). The local-search algorithm used to solve this task is a Genetic Algorithm, which can use a generic fitness function and different methods of crossover, mutation and distance, in order to evaluate different strategies and find the best one.

## Implementation
For convenience, the size of the population `µ`, the problems `problems`, the size of the bitstring `l` and . . . are parametrized in order to explore and evaluate easily the performances of the algorithm.

### Methods implementation
* `genetic_algorithm()` : The first method implemented is the scheleton of the `genetic_algorithm()` function. At the beginning this function only had 1 parameter, namely the fitness function. After that, other parameters were introduced to evaluate different mutations, crossovers or parent selections . . .
This function executes the following steps:
  - Initialization of the population
  - Evaluation (fitness) of each individual
  - Loop until the time is over or the stopping criterion (100% returned by fitness) is met:
    - Update of the best individual
    - Initialize a new population (initially empty)
    - Loop for half of the population size:
      - Selection of two parents
      - Crossover of the parents, generating two children (offspring)
      - Mutation of the offspring
      - Add the offspring to the new population
    - Evaluation (fitness) of the new population
    - Update of the population
Than the best individual fitness value, with the count of fitness and the iteration where the best individual is found is returned. This results can be significant in order to reduce the external loops.

* `init_population()`: initializes randomly the population, composed by `µ` individuals, each one with a bitstring of `l` bits and a fitness value of 0 at the beginning.

* `evaluate_population()`: evaluates the population using the fitness function. The fitness value is calculated for each individual and the tuple is updated.

* `select_with_replacement()`: this method initially took two random individuals from the population, but now selects elements based on their mutual diversity. This diversity is computed for each individual and all the other individuals. The diversity is than weitghed with the fitness value and evalutated thought the two individuals with the highest value are selected.

  Remember: the diversity can be evaluated considering
  - Genotype: bit-string of `l` bits
  - Phenotype: bit-string of `l` bits
  - Fitness: function fitness returned by `lab9_lib.make_problem(problem)`

* `compute_diversity()`: in order to evaluate the diversity a xor operation is performed between two individuals. The result of the xor is than used to calculate the pencentage of different bits with respect to the total number of bits (`l` = 1000). It is a genotype diversity.

  *Consideration:*<br> 
  During the `select_with_replacement()` implementation, the diversity matrix was printed in order to understand if the diversity was correctly computed and if the fitness value could influence the selection. Using the colorama library it was possible to hilight the maximum diversity value of the matrix and the value selected weighting with the fitness value. From this test it was possible to understand that usually the selected values are also the most different ones.<br>
  Later on, the diversity matrix of the population that generated the children that gave rise to the best (that matrix which is not weighted with the fitness value) was plotted in order to understand how the diversiry is distributed during the evolution of the algorithm. Those graphs are very nice.

* `diversity_selection()`: is used to select the most different individuals, weighting the difference with the fitness value. Also in this case the `diff_matrix` is modified in order to evaluate the diversity convergence over the generations.
A `study_diversity_selection()` method was used at the beginning to study the evolution.


* `mutation()`: this method takes as input an individual and a probability of mutation (set by default to `O.5`) and computes a bit-flip mutation, returning . The mutation is performed on each bit of the bitstring with the given probability in a for loop. If the random number generated is less than the probability, the bit is flipped.

  Two methods of crossover are implemented and their performance is evaluated in order to understand which one is better:

* `std_crossover()`: this method performs a two-point crossover between two individuals. The two points are randomly generated and the two sections of the bit-string are swapped between the two points.

* `crossover_cyclic_shift()`: this method performs a two-point crossover between two individuals but the two sections of swapping are shifted and the bit-string is treated as a circular array.

  The cyclic shift crossover appears to work better than the standard crossover by increasing the fitness percentage by a few units.


### Island Model :
After the implementation of the genetic algorithms with variants of parent selection and crossover, a non-parallelized island model is implemented, in order to observe how different populations can evolve, passing promising individuals among themselves. In the implemented model, an individual is promising if it has a high fitness value. Since this promising value is passed from one population to another it is likely that it is also different from other individuals in another population. Clearly, if the population is not very large, convergence to very similar individuals is rapid.<br>
In particoular this model iterates `iteration` times and, for each iteration, each island computes a cycle of `evolve()` method, in which two parents are selected thanks to the selection methods implemented above, than crossover and mutation are computed and the new population is evaluated in order to select the best individual to passo to another population.

## Results
The results are evaluated using the percentage of fitness reached. Unfortunately, the professor implementation, which generates 10 random bitstrings, calling only 10 times the fitness function, generates solutions slightly lower than the solutions obtained using the genetic algorithm which calls the fitness many more times.<br>
* **Statistics**:

  - **Professor results (random search):**
    | Problem | Fitness | Fit calls |
    |:-------:|:-------:|:---------:|
    |    1    |  53.90% |     10    |
    |    2    |  48.60% |     10    |
    |    5    |  19.50% |     10    |
    |   10    |   5.29% |     10    |

  - **Standard crossover (two pt) using selection with replacement:**
    | Problem | Fitness | Fit calls |
    |:-------:|:-------:|:--------:|
    |    1    |  54.00% |   2020   |
    |    2    |  52.40% |   2020   |
    |    5    |  20.62% |   2020   |
    |   10    |  16.20% |   2020   |

  - **Cyclic shift crossover using selection based on diversity:**
    | Problem | Fitness | Fit calls |
    |:-------:|:-------:|:--------:|
    |    1    |  54.40% |   2020   |
    |    2    |  52.60% |   2020   |
    |    5    |  22.34% |   2020   |
    |   10    |  17.11% |   2020   |

  - **Island model (using Cyclic shift crossover using selection based on diversity because of the best performances):**
    | Problem | Fitness | Fit calls |
    |:-------:|:-------:|:--------:|
    |    1    |  54.40% |   8000   |
    |    2    |  52.00% |   8000   |
    |    5    |  31.24% |   8000   |
    |   10    |  25.43% |   8000   |


### Deadlines:

* Submission: Sunday, December 3 ([CET](https://www.timeanddate.com/time/zones/cet))
* Reviews: Sunday, December 10 ([CET](https://www.timeanddate.com/time/zones/cet))

Notes:

* Reviews will be assigned  on Monday, December 4
* You need to commit in order to be selected as a reviewer (ie. better to commit an empty work than not to commit)