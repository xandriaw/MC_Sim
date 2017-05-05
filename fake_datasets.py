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
import math

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
df['difference']= df.botMean-df.humanMean
    
differenceOfMeans=np.array(df['difference'])

df.difference.plot(kind="hist",bins=40)

ROPE= df[(df['difference'] < .01) & (df['difference'] > -0.01)]
interval = np.round(ROPE.shape[0]*1.0/df.shape[0]*1.0, decimals=2)
print  "{:0.0f}".format(interval*100) + "% of our robot outputs are less than 0.01 away from human output" 

ROPE= df[(df['difference'] < .1) & (df['difference'] > -0.1)]
interval = np.round(ROPE.shape[0]*1.0/df.shape[0]*1.0, decimals=2)
print  "{:0.0f}".format(interval*100) + "% of our robot outputs are less than 0.1 away from human output" 



#"Given our observed data, there is a 95% probability that the true 
# value of μμ falls within CRμCRμ" - Bayesians

    
###################### translated from R code for BEST HDI calculation

    # Computes highest density interval from a sample of representative values,
    #   estimated as shortest credible interval.
    # Arguments:
    #   sampleVec
    #     is a vector of representative values from a probability distribution.
    #   credMass
    #     is a scalar between 0 and 1, indicating the mass within the credible
    #     interval that is to be estimated.
    # Value:
    #   HDIlim is a vector containing the limits of the HDI
credMass=0.95 #95% CDI
sortedPts = sorted(differenceOfMeans)
ciLength = int(math.floor( credMass * len( sortedPts) ))
outsideCIlength = len(sortedPts)-ciLength
ciWidth = np.zeros(outsideCIlength)

for i in np.arange(outsideCIlength):
    ciWidth[i]=sortedPts[i+ciLength]-sortedPts[i]
    
HDImin=sortedPts[ciWidth.argmin()]
HDImax=sortedPts[ciWidth.argmin()+ciLength]
HDIlim = [HDImin, HDImax]

differenceOfMeans=np.genfromtxt('C:\\Users\\xandr\\OneDrive\\Documents\\GitHub\\quality_data_science\\sampleVec.csv', delimiter=',')
    
