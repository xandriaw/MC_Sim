# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:02:19 2017

@author: xandr
"""

#simulate the real imagery NIIRS ratings
import scipy.stats as stats
import matplotlib.pyplot as plt

#NIIRS has a scale of 0-8 
lower, upper = 0, 8
mu, sigma = 4.5, 1.25
#use a truncated normal random variable

[a,b] =(lower - mu) / sigma, (upper - mu) / sigma

X = stats.truncnorm(a,b, loc=mu, scale=sigma)

fig, ax
plt.title("NIIRS Ratings for 1000 images")
plt.hist(X.rvs(size=1000))
plt.show()



import pymc

np.random.seed(123)

tr_norm_mod = Model()

human_NIIRS = pymc.TruncatedNormal('human_NIIRS', mu, tau =sigma, a =a, b=b )
        