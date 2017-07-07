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


import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
import matplotlib.lines as mpllines
import matplotlib.ticker as mticker
from pymc.distributions import noncentral_t_like


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

def differenceOfmeans(humanMean=4.5, sampleSize=50, variance=0.2):
    #note that tau is not sigma
    #sigma^2=1/tau
    t = 1/variance
    #what is the probability that an analyst would give this image the same rating?
    mu = TruncatedNormal('mu', mu=humanMean, tau = t, a=1, b=10) #hypothetical ground truth
    botOutput = TruncatedNormal('botOutput', mu=mu, tau=t, a=1, b=10)
    humanOutput = TruncatedNormal('humanOutput', mu=mu, tau=t, a=1, b=10)
    #when we have data from the model we can use this here
    #like this d = pymc.Binomial(‘d’, n=n, p=theta, value=np.array([0.,1.,3.,5.]), observed=True)
    
    sim=MCMC([mu, botOutput, humanOutput])
    
    sim.sample(sampleSize, 0, 1)
    botOutput = sim.trace("botOutput")[:]
    #if humans only give ratings at the 0.5 interval, not smaller
    #        humanOutput = round_to_half(sim.trace("humanOutput")[:]) 
    humanOutput = sim.trace("humanOutput")[:]
    #difference of the means
    #but what we care about is the mean of the human output for each image.
    difference = botOutput-humanOutput.mean()
    return difference

#ROPE
def probInROPE(difference, ROPESize=0.5 ):
    ROPE=difference[(difference<=ROPESize)&(difference>=(0-ROPESize))]
    probabilityInROPE = np.round(len(ROPE)*1.0/len(difference)*1.0, decimals=2)
    print  " \n{:0.0f}".format(probabilityInROPE*100) + "% of our robot outputs are inside the ROPE" 
    return probabilityInROPE

#"Given our observed data, there is a 95% probability that the true 
# value of μμ falls within CRμCRμ" - Bayesians

def plotROPEHDI(difference, HDI, ROPESize=0.5, credibleMass=0.95):
    fig, ax = plt.subplots()
    fig.canvas.set_window_title("histogram of difference of means {0:.0f}% HDI" .format(credibleMass*100))
    plt.hist(difference, rwidth=0.8,
                     facecolor='#7cb5ec', edgecolor='none')
    ax.set_title('Difference of bot mean and human mean')
    ax.axvline(x=(0-ROPESize), color='red' )
    ax.axvline(x=(ROPESize), color='red' )
    #plot the HDI as well
    ax.hlines(y=.1,  linewidth=6, color = 'black' , xmin = HDI[0], xmax= HDI[1] )
    ax.set_xlim(round(min(difference))-1 )
    
    ####Need to figure out how to round this and put it in annotation
    HDIText="HDI: {}" .format(np.around(HDI, decimals=1))
    ROPEText="ROPE: [-{0}, {1}]" .format(ROPESize, ROPESize)
    ax.annotate(HDIText, (0.4, 0.05), textcoords='axes fraction', size=20, color='black')
    ax.annotate(ROPEText, (.5, .8), textcoords='axes fraction', size = 20, color = 'red')
    return fig