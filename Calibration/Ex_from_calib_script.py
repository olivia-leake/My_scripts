#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 12:29:23 2025

@author: olivialeake
"""

import hpvsim as hpv

sim = hpv.Sim(pars, genotypes=[16, 18])
calib_pars = dict(beta=[0.05, 0.010, 0.20],hpv_control_prob=[.9, 0.5, 1])
calib = hpv.Calibration(sim, calib_pars=calib_pars,
                        datafiles=['hpvsim_MINE/tests/test_data/south_africa_hpv_data.csv',
                                   'hpvsim_MINE/tests/test_data/south_africa_cancer_data_2020.csv'],
                        total_trials=10, n_workers=4)
calib.calibrate()
calib.plot()


# %%

# This is an example of an output you might get
# Notice how the simulation keeps resetting the people, this is due to pruning !
# If the simulation notices that the estimates that it tried to run with will results in cancer cases
# too far from the objective (the data supplied) it will end the simulation and try run with 
# new estimates

'''
%runcell -i 0 '/Users/olivialeake/Documents/Structured Project/HPV Project/My fork/My_scripts/Calibration/Ex_from_calib_script.py'
Loading location-specific demographic data for "nigeria"
Initializing sim with 10000 agents
Loading location-specific data for "nigeria"
[I 2025-01-26 12:57:00,383] A new study created in RDB with name: hpvsim_calibration
Deleted study hpvsim_calibration in sqlite:///hpvsim_calibration.db
Removed existing calibration hpvsim_calibration.db
Initializing sim (resetting people) with 10000 agents
Loading location-specific data for "nigeria"
  Running 1980.0 ( 0/164) (0.00 s)  ———————————————————— 1%
Initializing sim (resetting people) with 10000 agents

  Running 1980.0 ( 0/164) (0.00 s)  ———————————————————— 1%
  Running 1982.5 (10/164) (0.09 s)  •——————————————————— 7%
Initializing sim (resetting people) with 10000 agents
Loading location-specific data for "nigeria"
  Running 1982.5 (10/164) (0.11 s)  •——————————————————— 7%
  Running 1985.0 (20/164) (0.20 s)  ••—————————————————— 13%
  Running 1980.0 ( 0/164) (0.00 s)  ———————————————————— 1%
 ''' 

# %%

# The following shows the parameters decided on at the end of the trail, and what the values of the
# simulation were depending on these parameters

'''
Simulation summary:
     102,038,657 total HPV infections
         127,854 total cancers
          89,067 total cancer deaths
            1.94 mean HPV prevalence (%)
            4.73 mean cancer incidence (per 100k)
           41.48 mean age of infection (years)
           59.50 mean age of cancer (years)

  Running 2017.5 (150/164) (1.54 s)  ••••••••••••••••••—— 92%
[I 2025-01-26 12:57:02,325] Trial 0 finished with value: 7.229771370367558 and parameters: {'beta': 0.07395907807848599, 'hpv_control_prob': 0.7410160358648797}. Best is trial 0 with value: 7.229771370367558.
'''

# %%

# Is total_trials = n_workers * n_trials ? YES ! The simulation rounds
# Because n_trials cannot = 2.5 ...?
" Processed 12 trials; 0 failed " # Recall trials start indexed at 0
# So it rounded n_trials up to 3 and said let's run 12 trials

# %%

# At the end of the running of the trials you get message 
'''
[I 2025-01-26 12:57:06,041] Trial 11 finished with value: 6.676583696831221 and 
parameters: {'beta': 0.12188941997438581, 'hpv_control_prob': 0.8099543439731456}. 
Best is trial 3 with value: 3.672377974243134.
'''

# Recall Optuna is an optimisation library / function
# It works by trying to minimise a problem. My assumption is that we have set this problem up to be 
# weighted least squares between calibration values and actual data points.

# So whne it says 'Best is trial 3 with value: 3.67...', it is trying to get the value as close
# to zero as possible, and this value doesn't actually tell us anything about out model. 
# It is essentially a measure of fit, although doesn't give us any information really!

''' The information that is useful to us is
Says best is trial 3, so go to trial 3 and extract values

Trial 3 was based off of 
Beta = 0.0663
hpv_control_prob = 0.649

'''

# %%





# The following code which is a later example in the calibration script doesn't work due to 
# the parameter 'prog_time' not being a parameter for the genotype hpv16.
# Don't think it is very essential I get this to work if the previous example works
"""

sim = hpv.Sim(genotypes=[16, 18])
calib_pars = dict(beta=[0.05, 0.010, 0.20],hpv_control_prob=[.9, 0.5, 1])
genotype_pars = dict(hpv16=dict(prog_time=[3, 3, 10]))


calib = hpv.Calibration(sim, calib_pars=calib_pars, genotype_pars=genotype_pars,
                    
                     total_trials=10, n_workers=4)

'''
calib = hpv.Calibration(sim, calib_pars=calib_pars, genotype_pars=genotype_pars,
                     datafiles=['test_data/south_africa_hpv_data.xlsx',
                                'test_data/south_africa_cancer_data.xlsx'],
                     total_trials=10, n_workers=4)
'''


 # Is total_trials = n_workers * n_trials ?
 # Because n_trials cannot = 2.5 ...?
 
calib.calibrate()
new_pars = calib.trial_pars_to_sim_pars() # Returns best parameters from calibration in a format ready for sim running
sim.update_pars(new_pars)
sim.run()

"""