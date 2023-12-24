# CS311 Artificial Intelligence(H) Capacitied Arc Routing Problems Project
This repository is for SUSTech CS311 Artificial Intelligence(H) CARP Project.
## 1. Overview
In this project you need to design and implement heuristic search algorithms for CARP, a classical NP-hard arc routing problem. An introduction to CARP (including problem formulation and solution representation) can be found in the slides we provide (CARP.pdf). Overall, CARP is a constrained optimization problem, and your algorithm needs to find high-quality feasible solutions to it. The scores you get in this project will be given according to your algorithm’s performance in our test.

## 2. General Rules
After you submit your project, we will run some scripts to test your CARP solver on different CARP problem instances. To make this process as smooth as possible, the package you submit must satisfy the following requirements.

### 2.1. Algorithm description
A solver description (in pdf format) must be submitted to Sakai, in which you should describe the core idea of your design, entail each component of your algorithm, illustrate the algorithm structure and give the pseudo code.

### 2.2. Programming aspects
In order to get rid of the operating system related issues and the execution efficiency issues of different programming languages, your algorithm must be implemented using Python 3.9.7 and the only allowed library is numpy.

The name of your executable CARP solver must be CARP_solver.py

### 2.3. Input and output
Input
In the test, we will repeatedly call your CARP solver through scripts. Specifically, the format of the solver call is as follows (the test environment is Unix-like):

python CARP_solver.py <CARP instance file> -t <termination> -s <random seed>
, CARP_solver.pyis your executable CARP solver, <CARP instance file> -t <termination> -s <random seed>are the arguments passed to your CARP solver, <CARP instance file> is the absolute path of the test CARP instance file specifies the termination condition of your algorithm. Specifically, <termination> is a positive number which indicates how many seconds (in Wall clock time, range: [60s, 600s]) your algorithm can spend on this instance. Once the time budget is consumed, your algorithm should be terminated immediately. <random seed> specifies the random seed used in this run. In case that your solver is stochastic, the random seed controls all the stochastic behaviors of your solver, such that the same random seeds will make your solver produce the same results. If your solver is deterministic, it still needs to accept , but can just ignore them while solving CARPs.

You can use multithread, but the number of thread shall not exceed 8.

In summary, your CARP solver needs to:

handle the arguments passed from our scripts while being called as above

measure the runtime, and terminate after the time budget is consumed. Typically, in python 3.6 you can measure runtime using time.time():

    start = time.time()

    ...solving carp

    un_time = (time.time() - start)
Note here although our tests rely on your solver’s internal time measurement, we will still measure your solver’s runtime from external, so make sure that your solver’s internal time measurement is accurate.

use random seeds to control all the stochastic behaviors
Output
Your solver must print messages to the standard output. These messages will be used to evaluate this solver run. Your solver has to print two lines. Each of them, according to its first char, must belong to one of the categories described below. Lines that do not start with one of the patterns below will be considered a comment and hence ignored.

Solution line begins with a lower case “s” followed by a space (ASCII code 32). Only one such line is allowed and it is mandatory. The best solution your solver has found for the CARP problem instance must be printed in this line. The format of the solution can be found in the slides we provide (CARP.pdf). For example, for the CARP instance given below, the “s” line is:

s 0,(1,2),(2,4),(4,1),0,0,(4,3),(3,1),0
Quality line begins with a lower case “q” followed by a space (ASCII code 32). Only one such line is allowed and it is mandatory. The solution quality (i.e., the total cost) of your best found solution must be printed in this line. The “q” line of the above example is:

q 15
2.4. Format of CARP problem instance
The format of the CARP problem instances can be found in the instruction we provide (CARP_format.txt), and we also provide some CARP instance files as examples (CARP_samples/).

## 3. Evaluation
We divide the solver evaluation into three parts:

### 3.1 Usability test (50%)
In this test we will use some CARP problem instances to check whether your solvers are usable. Here the meanings behind usability are twofold:

a) (25%) Your solvers can satisfy the input and the output requirements (See Section 2). The failure cases include: cannot handle the inputs, the output messages are undesirable (missing ‘s’ line or ‘q’ line, the format of the output solution is incorrect or the total cost of the output solution is not correctly calculated), crash.

b) (25%) The best found solution output by your solver is a feasible solution (since CARP is a constrained problem). Infeasible solutions violate at least one constraints of CARP.

Once your solvers have passed a test, you will get all the corresponding scores. Note only those solvers that have been through test a) will be tested in b).

### 3.2 Efficacy test (30%)
In this test we will focus on how good your solvers are. Specifically, we will select different CARP instances with different sizes from existing CARP benchmarks to test your solvers. For each instance, we will set a common cut-off time for all participant solvers and compare their solution quality.

The scores you get in this test depend on the rankings your solvers obtain. Note only those solvers that have been through usability test will be tested in efficacy test.

### 3.3 Robustness tes (20%)
A robust solver is said to be applicable to a wide range of problem instances. Although your solvers may show good performance in the efficacy test, they may perform badly on unseen instances. In this test, for each participant solver, we will generate a fixed number of instances that are very hard for it. After this we will put all the newly generated instances into a pool, forming a test set. Finally, all the participant solvers will be tested on this set. Like efficacy test, we will set a common cut-off time for all participant solvers and compare their solution quality.

The scores you get in this test depend on the rankings your solvers obtain. Note only those solvers that have been through usability test will be tested in robustness test.

## 4. Test Environment
Operation System: Debian 10

Server CPU：2.2GHz*2, 8-core total

Python version: 3.9.7

Your code will be tested in a container whose image is built by the following dockerfile:

FROM python:3.9.7-buster
RUN pip install --no-cache-dir -U numpy
CMD ["python3"]

## 5. Results
### 5.1 Stage1
![image](https://github.com/0SliverBullet/CS311-Artificial-Intelligence-H-CARP-Project/assets/110400562/6880f0d7-bed8-442b-9410-cd2e971e086b)
### 5.2 Stage2
![image](https://github.com/0SliverBullet/CS311-Artificial-Intelligence-H-CARP-Project/assets/110400562/7a309bc0-cb82-48aa-a1ee-e0c09940a856)


