#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 11:28:42 2025

@author: olivialeake
"""

"""
A simple optimization problem:
Define objective function to be optimized. Let's minimize (x - 2)^2
Suggest hyperparameter values using trial object. Here, a float value of x is suggested from -10 to 10
Create a study object and invoke the optimize method over 100 trials

Clearly soution is x=2 , resulting in a minimalisation of 0
How does optuna know the goal is to minimise ??
"""

import optuna

def objective(trial):
    x = trial.suggest_float('x', -10, 10)
    return (x - 2) ** 2

study = optuna.create_study()
study.optimize(objective, n_trials=10)

study.best_params  # E.g. {'x': 2.002108042}


"""
Trials start indexed at 0
Each time a new trial is ran, optuna compares the value of the trial with the best value so far 
(NOT the value of x of course, but the value of the problem we wish to optimise)
,and decides whether the new value is closer to the objective or not

Clearly this problem is best optimised as (x-2)^2 gets closer to 0 (idea is to minimise this function)

[I 2025-01-26 11:29:12,100] A new study created in memory with name: no-name-fdb8b839-77ae-4af7-b5bc-82eef611e40d
[I 2025-01-26 11:29:12,101] Trial 0 finished with value: 11.704525131917665 and parameters: {'x': 5.421187678558086}. Best is trial 0 with value: 11.704525131917665.
[I 2025-01-26 11:29:12,102] Trial 1 finished with value: 79.86264700501356 and parameters: {'x': -6.936590345596779}. Best is trial 0 with value: 11.704525131917665.
[I 2025-01-26 11:29:12,102] Trial 2 finished with value: 12.545320118432235 and parameters: {'x': -1.54193733971004}. Best is trial 0 with value: 11.704525131917665.
[I 2025-01-26 11:29:12,103] Trial 3 finished with value: 22.042697254248854 and parameters: {'x': -2.6949650961693905}. Best is trial 0 with value: 11.704525131917665.
[I 2025-01-26 11:29:12,103] Trial 4 finished with value: 108.67270044122945 and parameters: {'x': -8.424619918310185}. Best is trial 0 with value: 11.704525131917665.
[I 2025-01-26 11:29:12,104] Trial 5 finished with value: 5.159453283306165 and parameters: {'x': -0.27144299583022}. Best is trial 5 with value: 5.159453283306165.
[I 2025-01-26 11:29:12,105] Trial 6 finished with value: 34.815897864636995 and parameters: {'x': 7.900499797867719}. Best is trial 5 with value: 5.159453283306165.
[I 2025-01-26 11:29:12,105] Trial 7 finished with value: 1.7948014047947085 and parameters: {'x': 3.3397019835749697}. Best is trial 7 with value: 1.7948014047947085.
[I 2025-01-26 11:29:12,106] Trial 8 finished with value: 20.043240221610162 and parameters: {'x': -2.476967748555954}. Best is trial 7 with value: 1.7948014047947085.
[I 2025-01-26 11:29:12,106] Trial 9 finished with value: 81.49148167584083 and parameters: {'x': -7.027263243964963}. Best is trial 7 with value: 1.7948014047947085.

Out[7]: {'x': 3.3397019835749697}

"""