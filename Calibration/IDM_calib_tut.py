# -*- coding: utf-8 -*-
"""
Looking only at cancer cases
We have data for the number of cancer cases in Nigeria in 2020 across different age groups
The idea is for optuna to trial out some parameter values, run a simulation with these parameteres from
1980 to 2020 (in this case), and see if we end up with similar results to out actual data.


Each 'worker' represnts a simulation with the randomly chosen, fixed, paramter values
And for each worker, you run n_trials (so if the sim randomly chooses beta = 0.03 to try run 
                                      the sim with, thsi counts as a worker, and for beta =0.03, 
                                     you might run the trial 3 times and take the average value)
If the number of workers is set to 1, you only try out each randomly chosen beta once
The total trials is therefore number workers * number of trials for each worker.
    
ie: Each worker evaluates a different set of hyperparameter combinations.
    
"""


import sciris
print(sciris.__version__)
# In other scripts this you might write print(sc.__version__), if you have done 'import sciris as sc'

# Import HPVsim
import hpvsim as hpv
# Importing hpvsim is just saying import all the folders with all the scripts needed
# This will automatically import the calibration simulation, as well as optuna

# Configure a simulation with some parameters
pars = dict(n_agents=10e3, start=1980, end=2020, dt=0.25, location='nigeria')
sim = hpv.Sim(pars)
# This is calling the Sim function (is there a way to tell where this function is being called from?)

# These paramters are fixed !

# Number of agents is number of people assumed to start with in the sim. pop_scale is the scale factor
# which allows you to scale up to the real total population size.

# Start year is 1980, default burnin is 25 years, saying only show data after the sim has ran for 25 years
# This is because the first 25 years of data is unreliable
# dt = 0.35 is the timestep for the sumulatoin

# Specify some parameters to adjust during calibration.
# The parameters in the calib_pars dictionary don't vary by genotype,
# whereas those in the genotype_pars dictionary do. Both kinds are
# given in the order [best, lower_bound, upper_bound].
calib_pars = dict(
        beta=[0.05, 0.010, 0.20],
    )

genotype_pars = dict(
    hpv16=dict(
        cin_fn=dict(k=[0.5, 0.2, 1.0]),
        dur_cin=dict(par1=[6, 4, 12])
    ),
    hpv18=dict(
        cin_fn=dict(k=[0.5, 0.2, 1.0]),
        dur_cin=dict(par1=[6, 4, 12])
    )
)


"""
Optuna is trying to find the best beta value within 0.010 and 0.20 (you need to supply an upper and 
lower bound, otherwise optuna has too much reign to work with, but you don't want them too tight that you
end up exclusing the actual value

 Note: running a calibration does not guarantee a good fit! You must ensure that
 you run for a sufficient number of iterations, have enough free parameters, and
 that the parameters have wide enough bounds. Please see the tutorial on calibration
 for more information.
"""

# List the datafiles that contain data that we wish to compare the model to:
datafiles=['hpvsim_MINE/docs/tutorials/nigeria_cancer_cases.csv',
           'hpvsim_MINE/docs/tutorials/nigeria_cancer_types.csv']

### The data files contain the ACTUAL data that we are trying to calibrate to !!

# List extra results that we don't have data on, but wish to include in the
# calibration object so we can plot them.
results_to_plot = ['cancer_incidence', 'asr_cancer_incidence']

# Create the calibration object, run it, and plot the results
calib = hpv.Calibration(
    sim,
    calib_pars=calib_pars,
    genotype_pars=genotype_pars,
    extra_sim_result_keys=results_to_plot,
    datafiles=datafiles,
    total_trials=3, n_workers=1
)

"""
Total trials = n_trials * n_workers

n_trials is the number of trials per worker
n_workers is the number of parallel workers 
"""

# The calibartion will run 3 different times when total_trials set to = 3. You can see this in the Console
# 


calib.calibrate(die=True)
calib.plot(res_to_plot=4);