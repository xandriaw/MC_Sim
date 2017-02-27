# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:02:19 2017

@author: xandr
"""

#simulate the real imagery NIIRS ratings
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

np.random.seed(123)

#NIIRS has a scale of 0-8 
lower, upper = 0, 10
mu, sigma = 4.5, 1.5
#use a truncated normal random variable
[a,b] =(lower - mu) / sigma, (upper - mu) / sigma


from pymc import TruncatedNormal, HalfNormal, Normal, Model

basic_model = Model()
with basic_model:
    mu_dist = TruncatedNormal('mu_dist', mu=mu, tau=sigma, a=a, b=b)
    sigma_dist = HalfNormal('sigma_dist', tau=1) #use a half-normal since sd is always positive, had sd=1, maybe for pymc3
    Y_obs= TruncatedNormal('Y_obs', mu=mu_dist, tau=sigma_dist, a=a, b=b) #, observed=True) this was giving error- must have an initial value if observed=True
    
