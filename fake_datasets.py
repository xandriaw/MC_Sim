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
    

#set our variables here
sampleSize= np.arange(5,500,2)
#sampleSize= np.array([5,10, 20, 50,100,150,200,250])
#variances = np.array([ 1, .75, .5, .3, .2, .1])
variances= np.array([1,.5,.1])
ROPESize= 0.5 #make this positive
#Region of practical equivalence. This is often [-0.1, 0.1] or something like this.
strictly= True #should our rope be strictly less than or less than or equal to the limits
credibleMass=0.9
#note that tau is not sigm! 
#sigma^2=1/tau
taus = 1/variances

df=pd.DataFrame(columns = ["variance", "sampleSize","botMean", "humanMean", 
                           "bias","lowerHDI", "upperHDI","probabilityInROPE"])

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
    #when we have data from the model we can use this here
    #like this d = pymc.Binomial(‘d’, n=n, p=theta, value=np.array([0.,1.,3.,5.]), observed=True)
    
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
#        humanOutput = round_to_half(sim.trace("humanOutput")[:]) 
        humanOutput = sim.trace("humanOutput")[:]
        #difference of the means
        difference = botOutput-humanOutput
        #HighestDensityInterval: where 95% of the differences are? are they close to 0?
        HDI= HDIofMCMC(differenceOfMeans= difference, credMass=credibleMass)
        #ROPE
        if strictly == True:
            #ROPE=difference[(difference<=ROPESize)&(difference>=(0-ROPESize))]
            ROPE=difference[(difference<=ROPESize)]
            probabilityInROPE = np.round(len(ROPE)*1.0/len(difference)*1.0, decimals=2)
            print  "{:0.0f}".format(probabilityInROPE*100) + "% of our robot outputs are less than or equal to 0.5 away from human output" 
        else:
           # ROPE=difference[(difference<ROPESize)&(difference>(0-ROPESize))]
            ROPE=difference[(difference<ROPESize)] #how many differences are within the ROPE
            probabilityInROPE = np.round(len(ROPE)*1.0/len(difference)*1.0, decimals=2)
            print  "{:0.0f}".format(probabilityInROPE*100) + "% of our robot outputs are strictly less than .5 away from human output" 
        
        #fill the dataframe
        df.loc[i]=[1/t, s, botOutput.mean(), humanOutput.mean(),b, 
              HDI[0], HDI[1], probabilityInROPE]
        i=i+1

df['meanDifference']= df.botMean-df.humanMean

#"Given our observed data, there is a 95% probability that the true 
# value of μμ falls within CRμCRμ" - Bayesians

fig, axes = plt.subplots(nrows=1, ncols=len(taus))
fig.canvas.set_window_title('%s highest density interval'%credibleMass)
for t in taus:
    tdf=df.loc[(df.variance ==1/t)]
    whichplace = int(np.argwhere(taus==t))
    #not sure if it even makes sense to plot the mean difference-
#    tdf.plot.scatter(x='sampleSize', y='meanDifference', ax=axes[whichplace], s=3, c = 'red')
    axes[whichplace].fill_between(x=tdf.sampleSize, y1=tdf.lowerHDI, y2=tdf.upperHDI)
    axes[whichplace].set_title('variance:' + str( 1/t))
    axes[whichplace].set_ylim(df.lowerHDI.min(), df.upperHDI.max())
    
fig, axes = plt.subplots(nrows=1, ncols=len(taus))
fig.canvas.set_window_title('proportion of images inside the ROPE (region of practical equivalence) - set to %s'%ROPESize)
for t in taus:
    tdf=df.loc[(df.variance ==1/t)]
    whichplace = int(np.argwhere(taus==t))
    tdf.plot.scatter(x='sampleSize', y='probabilityInROPE', ax=axes[whichplace], s=3)
    axes[whichplace].set_title('variance:' + str( 1/t))
    axes[whichplace].set_ylim(df.probabilityInROPE.min(), df.probabilityInROPE.max())


    