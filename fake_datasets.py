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

sampleSize= np.arange(10,1000,1)
variances = np.array([ 1, .75, .5, .3, .2, .1])
#note that tau is not sigm! 
#sigma^2=1/tau
taus = 1/variances

df=pd.DataFrame(columns = ["variance", "sampleSize","botMean", "humanMean", 
                           "bias","matches"])

#what is the probability that an analyst would give this image the same rating?


i=1

for t in taus:
    # the bot will always give the same output for a given image
    #tau = 1/variance - this is varying for each iteration of the loop
    placeHolder = TruncatedNormal('placeHolder', mu=4.5, tau=t, a=1, b=10)
    humanOutput = TruncatedNormal('humanOutput', mu=4.5, tau=t, a=1, b=10)
    
    sim=MCMC([placeHolder, humanOutput])


    for s in sampleSize:
        #get s number of samples, no burn in for this- not optimizing anything
        sim.sample(s, 0, 1)
        #assume no bias at this point but we can add bias later
        b=0
        #computer is always going to get the same value for an image
        botOutput = np.full(s,4.5+b)
        #vary the human output for this image
        humanOutput = round_to_half(sim.trace("humanOutput")[:])
        #fill the dataframe
        df.loc[i]=[1/t, s, botOutput.mean(), humanOutput.mean(), b, 
              sum(botOutput==humanOutput)]
        i=i+1
    #plot for each variance/tau
    
df['probability'] = df.matches/df.sampleSize
df['difference']= np.abs(df.botMean-df.humanMean)
    
print(df)
#"Given our observed data, there is a 95% probability that the true 
# value of μμ falls within CRμCRμ" - Bayesians
fig, axes = plt.subplots(nrows=1, ncols=len(taus))
fig.canvas.set_window_title('probability that an analyst would give this image the same NIIRS')

for t in taus:
    df=df.loc[(df.variance ==1/t)]
    whichplace = int(np.argwhere(taus==t))
    tdf.plot.scatter(x='sampleSize', y='probability', ax=axes[whichplace])
    axes[whichplace].set_title('variance:' + str( 1/t))



