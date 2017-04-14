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
sampleSize= [10, 50, 100, 1000, 2000, 3000,4000, 5000]
variances = np.array([1, .75, .5, .25, .1])
#note that tau is not sigm! 
#sigma^2=1/\tau
taus = 1/variances

df=pd.DataFrame(columns = ["variance", "sampleSize", "Matches"])

i=1
for t in taus:

    #make a tight distribution for both the bot and the human output
    botOutput = TruncatedNormal('botOutput', mu=4.5, tau=t, a=1, b=10)
    humanOutput = TruncatedNormal('humanOutput', mu=4.5, tau=t, a=1, b=10)
    
    sim=MCMC([botOutput, humanOutput])


    for s in sampleSize:
        sim.sample(s, 0, 1)
        
        botOutput = round_to_half(sim.trace("botOutput")[:])
        humanOutput = round_to_half(sim.trace("humanOutput")[:])
#        fig = plt.figure(figsize=(10,10))
#        axes = fig.add_subplot(111)
#        axes.hist(botOutput, bins=20, normed=True, color="blue");
#        axes.hist(humanOutput, bins=20, normed=True, color="red")
#        fig.show()
    
        #find where they are the same..?
        print()
        print "variance:", 1/t, "sample size: " , s 
        print( )
        print "number of times human and bot are the same:", sum(botOutput ==humanOutput)
        df.append({"variance": 1/t, "sampleSize": s,"Matches:": sum(botOutput ==humanOutput)}, 
                   ignore_index=True)
        df.loc[i]=[1/t, s, sum(botOutput==humanOutput)]
        i=i+1
print(df)

