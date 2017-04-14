# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:16:52 2017

@author: xandr
"""
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib
from pymc import TruncatedNormal, HalfNormal, Normal, Model, MCMC, Metropolis, Uniform
import pandas as pd

def round_to_half(number):
    """Round a number to the closest half integer."""
    return np.around(number * 2) / 2

from scipy.special import erfinv

def bayes_CR_mu(D, sigma, frac=0.95):
    """Compute the credible region on the mean"""
    Nsigma = np.sqrt(2) * erfinv(frac)
    mu = D.mean()
    sigma_mu = sigma * D.size ** -0.5
    return mu - Nsigma * sigma_mu, mu + Nsigma * sigma_mu

sampleSize= np.arange(1,100,1)
variances = np.array([1, .75, .5, .25, .1])
#note that tau is not sigm! 
#sigma^2=1/\tau
taus = 1/variances

df=pd.DataFrame(columns = ["variance", "sampleSize","botMean", "humanMean", 
                           "bias","matches"])

#what is the probability that an analyst would give this image the same rating?


i=1
for t in taus:
    # the bot will always give the same output for a given image
    botOutput = TruncatedNormal('botOutput', mu=4.5, tau=t, a=1, b=10)
    humanOutput = TruncatedNormal('humanOutput', mu=4.5, tau=t, a=1, b=10)
    
    sim=MCMC([botOutput, humanOutput])


    for s in sampleSize:
        #get s number of samples, no burn in for this- not optimizing anything
        sim.sample(s, 0, 1)
        #assume no bias at this point
        b=0
        #computer is always going to get the same value for an image
        botOutput = np.full(s,4.5+b)
        #vary the human output for this image
        humanOutput = round_to_half(sim.trace("humanOutput")[:])
#        
#        fig = plt.figure(figsize=(10,10))
#        axes = fig.add_subplot(111)
#        axes.hist(botOutput, bins=20, normed=True, color="blue");
#        axes.hist(humanOutput, bins=20, normed=True, color="red")
#        fig.show()

        df.loc[i]=[1/t, s, botOutput.mean(), humanOutput.mean(), b, 
              sum(botOutput==humanOutput)]
        i=i+1
print(df)
df['probability'] = df.matches/df.sampleSize
#"Given our observed data, there is a 95% probability that the true 
# value of μμ falls within CRμCRμ" - Bayesians

matplotlib.style.use('ggplot')
plt.plot( df.sampleSize, df.probability , legend=True )

df.plot(x=sampleSize)

ax = df.plot.scatter(x='sampleSize', y='probability', s=df['variance']*50)



