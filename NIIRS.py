# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:02:19 2017

@author: xandr
"""

#simulate the real imagery NIIRS ratings
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib

np.random.seed(123)

#NIIRS has a scale of 0-8 
lower, upper = 0, 10
mu, sigma = 4.5, 1.5
#use a truncated normal random variable
###this normalizes our bounds- but i don't think we want this###
#[a,b] =(lower - mu) / sigma, (upper - mu) / sigma
###this may not be what we actually want to use as upper and lower

from pymc import TruncatedNormal, HalfNormal, Normal, Model, MCMC, Metropolis

mu_dist = TruncatedNormal('mu_dist', mu=mu, tau=sigma, a=lower, b=upper)
sigma_dist = HalfNormal('sigma_dist', tau=1) #use a half-normal since sd is always positive, had sd=1, maybe for pymc3
Y_dist= TruncatedNormal('Y_dist', mu=mu_dist, tau=sigma_dist, a=lower, b=upper) #, observed=True) this was giving error- must have an initial value if observed=True
    
sim=MCMC([mu_dist, sigma_dist, Y_dist])
sim.sample(iter=50000, burn=10000, thin=1)

y_samples = sim.trace("Y_dist")[:]
fig = plt.figure(figsize=(15,10))
axes = fig.add_subplot(111)
axes.hist(y_samples, bins=50, normed=True, color="blue");
fig.show()

mu_samples = sim.trace("mu_dist")[:]
fig = plt.figure(figsize=(15,10))
axes = fig.add_subplot(111)
axes.hist(mu_samples, bins=50, normed=True, color="green");
fig.show()

sig_samples = sim.trace("sigma_dist")[:]
fig = plt.figure(figsize=(15,10))
axes = fig.add_subplot(111)
axes.hist(sig_samples, bins=50, normed=True, color="red");
fig.show()

#Confidence Intervals
#how many human verified samples ('known cases') do I need to ensure.
#analysts averaged is unbiased.iid
#want to lower the number of inspections by analysts. function -->
from scipy.special import erfinv

def bayes_CR_mu(D, sigma, frac=0.95):
    """Compute the credible region on the mean"""
    #D is
    Nsigma = np.sqrt(2) * erfinv(frac)
    mu = D.mean()
    sigma_mu = sigma * D.size ** -0.5
    return mu - Nsigma * sigma_mu, mu + Nsigma * sigma_mu

print("95% Credible Region: [{0:.0f}, {1:.0f}]".format(*bayes_CR_mu(y_samples, 10)))


###This attempts the same but with newer version of pymc3. 
# Doesn't work for bounding distribution
import pymc3 as pm
import numpy as np
# after reading some of the probablistic programming book:
with pm.Model() as my_model:
    mu_dist= pm.Normal('mu_dist', mu=mu,sd=sigma   )
    sigma_dist = pm.HalfNormal('sigma_dist', tau=1)
    Y_obs= pm.Normal('Y_obs', mu=mu_dist, tau=sigma_dist)
    step = pm.Metropolis()
    trace = pm.sample(20000, step=step)
    burned_trace=trace[1000:]
    
mu_samples= burned_trace["mu_dist"]
sigma_samples = burned_trace["sigma_dist"]
Y_samples= burned_trace["Y_obs"]

%matplotlib inline
figsize(12.5, 10)

#histogram of posteriors

ax = plt.subplot(311)

p#lt.xlim(0, .1)
plt.hist(mu_samples, histtype='stepfilled', bins=25, alpha=0.85, label="posterior of mu", color="#A60628", normed=True)
plt.vlines(mu, 0, 0.3, linestyle="--", label="true mu (unknown)")
plt.legend(loc="upper right")
plt.title("Posterior distributions ")

ax = plt.subplot(312)
#this one doesn't work
#plt.xlim(0, .1)
plt.hist(sigma_samples, histtype='stepfilled', bins=25, alpha=0.85, label="posterior of sigma", color="#467821")
plt.vlines(sigma, 0, .3, linestyle="--", label="true sigma (unknown)")
plt.legend(loc="upper right")

ax = plt.subplot(313)
plt.hist(Y_samples, histtype='stepfilled', bins=30, alpha=0.85, label="posterior of Y-obs", color="#7A68A6", normed=True)
#plt.vlines(Y_obs, 0, 60, linestyle="--", label="true delta (unknown)")
#plt.vlines(0, 0, 60, color="black", alpha=0.2)
plt.legend(loc="upper right");

def bayes_CR_mu(D, sigma, frac=0.95):
    """Compute the credible region on the mean"""
    #D is
    Nsigma = np.sqrt(2) * erfinv(frac)
    mu = D.mean()
    sigma_mu = sigma * D.size ** -0.5
    return mu - Nsigma * sigma_mu, mu + Nsigma * sigma_mu

print("95% Credible Region: [{0:.0f}, {1:.0f}]".format(*bayes_CR_mu(D, 10)))
