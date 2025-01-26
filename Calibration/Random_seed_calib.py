#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 13:26:51 2025

Objective - Trying to calibrate using a random seed 
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