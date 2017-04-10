# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:29:00 2017

@author: xandr
"""

import numpy as np
import pymc
import scipy.optimize as opt
import scipy.stats as stats

sigma = 1.0
tau = 1 / sigma**2

sigma0 = 3.0
tau0 = 1 / sigma0**2
#define the dist of mu's
mu = pymc.Normal("mu", mu=0, tau=tau0)
#define our distribution of distributions
x = pymc.Normal("x", mu=mu, tau=tau)

mcmc = pymc.MCMC([mu, x])
mcmc.sample(50000, 10000, 1)

x_samples = mcmc.trace("x")[:]

# alternative hypothessis is that mu = 0
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(15,15))
axes = fig.add_subplot(111)
axes.hist(x_samples, bins=50, normed=True, color="gray");
x_range = np.arange(-15, 15, 0.1)
x_precision = tau * tau0 / (tau + tau0)
axes.plot(x_range, stats.norm.pdf(x_range, 0, 1 / np.sqrt(x_precision)), color='k', linewidth=2);
fig.show()

x_pdf = stats.kde.gaussian_kde(x_samples)

#simulated bayes factor
def bayes_factor_sim(x_obs):
    return x_pdf.evaluate(x_obs) / stats.norm.pdf(x_obs, 0, sigma)
#actual bayes factor
def bayes_factor_exact(x_obs):
    return np.sqrt(tau0 / (tau + tau0)) * np.exp(0.5 * tau**2 / (tau + tau0) * x_obs**2)

fig = plt.figure(figsize=(10, 10))
axes = fig.add_subplot(111)
x_range = np.arange(0, 2, 0.1)
axes.plot(x_range, bayes_factor_sim(x_range), color="red", label="Simulated Bayes factor", linewidth=2)
axes.plot(x_range, bayes_factor_exact(x_range), color="blue", label="Exact Bayes factor")
axes.legend(loc=2)
fig.show()


def bayes_factor_crit_helper(x):
    return bayes_factor_sim(x) - 1

#brentq finds the roots of an equation. next two numbers are the lower and upper (range) for x
x_crit = opt.brentq(bayes_factor_crit_helper, 0, 2)
x_crit
