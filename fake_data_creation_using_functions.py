# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 12:14:08 2017

@author: xandr
"""

#ROPE is the Region of practical equivalence. 
#This is often [-0.1, 0.1] or something like this.
execfile('C:\\Users\\xandr\\OneDrive\\Documents\\GitHub\\MC_Sim\\functionizing_fake_data.py')

difference= differenceOfmeans(humanMean=4.5, variance=0.2, sampleSize =50)
#HighestDensityInterval: where 95% of the differences are? are they close to 0?
HDI= HDIofMCMC(differenceOfMeans= difference, credMass=0.95)

probInROPE(difference, ROPESize=0.5 )

plotROPEHDI(difference, HDI, ROPESize=0.5, credMass=0.95)
