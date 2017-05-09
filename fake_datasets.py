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

#set our variables here
sampleSize= np.arange(10,1000,1)
variances = np.array([ 1, .75, .5, .3, .2, .1])
ROPESize= 0.5 #make this positive
strictly= True #should our rope be strictly less than or less than or equal to the limits
credibleMass=0.95
#note that tau is not sigm! 
#sigma^2=1/tau
taus = 1/variances

df=pd.DataFrame(columns = ["variance", "sampleSize","botMean", "humanMean", 
                           "bias","HDI", "probabilityInROPE"])

#what is the probability that an analyst would give this image the same rating?


i=1

for t in taus:
    # the bot will always give the same output for a given image
    #tau = 1/variance - this is varying for each iteration of the loop
    placeHolder = TruncatedNormal('placeHolder', mu=4.5, tau=t, a=1, b=10)
    humanOutput = TruncatedNormal('humanOutput', mu=4.5, tau=t, a=1, b=10)
    #mu = TruncatedNormal('mu', mu=4.5, tau = t, a=1, b=10)
    #humanOutput = TruncatedNormal('humanOutput', mu=mu, tau=t, a=1, b=10)
    #maybe use this in the future. not sure
    
    sim=MCMC([placeHolder, humanOutput])


    for s in sampleSize:
        #get s number of samples, no burn in for this- not optimizing anything
        sim.sample(s, 0, 1)
        #assume no bias at this point but we can add bias later
        b=0
        #computer is always going to get the same value for an image
        botOutput = np.full(s,4.5+b)
        #vary the human output for this image
        #humans probably only give ratings at the 0.5 interval, not smaller
        humanOutput = round_to_half(sim.trace("humanOutput")[:]) 
        #difference of the means
        difference = botOutput-humanOutput
        #HighestDensityInterval: where 95% of the differences are? are they close to 0?
        HDI= HDIofMCMC(differenceOfMeans= difference, credMass=credibleMass)
        #ROPE
        if strictly == True:
            ROPE=difference[(difference<=ROPESize)&(difference>=(0-ROPESize))]
            probabilityInROPE = np.round(len(ROPE)*1.0/len(difference)*1.0, decimals=2)
            print  "{:0.0f}".format(probabilityInROPE*100) + "% of our robot outputs are less than or equal to 0.5 away from human output" 
        else:
            ROPE=difference[(difference<ROPESize)&(difference>(0-ROPESize))]
            probabilityInROPE = np.round(len(ROPE)*1.0/len(difference)*1.0, decimals=2)
            print  "{:0.0f}".format(probabilityInROPE*100) + "% of our robot outputs are strictly less than .5 away from human output" 
        
        #fill the dataframe
        df.loc[i]=[1/t, s, botOutput.mean(), humanOutput.mean(),b, 
              HDI, probabilityInROPE]
        i=i+1


#"Given our observed data, there is a 95% probability that the true 
# value of μμ falls within CRμCRμ" - Bayesians

    
###################### translated from R code for BEST HDI calculation
def HDIofMCMC(differenceOfMeans, credMass=0.95):
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
    #credMass=0.95 #95% CDI
    sortedPts = sorted(differenceOfMeans)
    ciLength = int(math.floor( credMass * len( sortedPts) ))
    outsideCIlength = len(sortedPts)-ciLength
    ciWidth = np.zeros(outsideCIlength)
    
    for i in np.arange(outsideCIlength):
        ciWidth[i]=sortedPts[i+ciLength]-sortedPts[i]
        
    HDImin=sortedPts[ciWidth.argmin()]
    HDImax=sortedPts[ciWidth.argmin()+ciLength]
    HDIlim = [HDImin, HDImax]
    return HDIlim
##for testing R and python code
#differenceOfMeans=np.genfromtxt('C:\\Users\\xandr\\OneDrive\\Documents\\GitHub\\quality_data_science\\sampleVec.csv', delimiter=',')
    
