# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:02:19 2017

@author: xandr
"""

#simulate the real imagery NIIRS ratings
import scipy.stats as stats
import matplotlib.pyplot as plt
np.random.seed(123)

#NIIRS has a scale of 0-8 
lower, upper = 0, 10
mu, sigma = 4.5, 1.5
#use a truncated normal random variable
[a,b] =(lower - mu) / sigma, (upper - mu) / sigma


X = stats.truncnorm(a,b, loc=mu, scale=sigma)
fig, ax
plt.title("NIIRS Ratings for 1000 images")
plt.hist(X.rvs(size=1000))
plt.show()


# not sure if this chunk even worked
import pymc
human_NIIRS = pymc.TruncatedNormal('human_NIIRS', mu, tau =sigma, a =a, b=b )

human_NIIRS_model = pymc.Model([human_NIIRS])
human_NIIRS_mcmc = pymc.MCMC(human_NIIRS_model)
human_NIIRS_mcmc.sample(iter=11000)
, burn=10000)

plt.hist(human_NIIRS.trace(), 15, histtype='step', normed=True, label='post');
# try again
from pymc3 import *
basic_model = Model()
with basic_model:
    mu_dist = TruncatedNormal('mu_dist', mu=mu, tau=sigma, a=a, b=b)
    sigma_dist = HalfNormal('sigma_dist', sd=1) #use a half-normal since sd is always positive
    Y_obs= TruncatedNormal('Y_obs', mu=mu_dist, tau=sigma_dist, a=a, b=b, observed=True)