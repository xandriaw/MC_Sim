# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 12:14:08 2017

@author: xandr
"""

#ROPE is the Region of practical equivalence. 
#This is often [-0.1, 0.1] or something like this.
execfile('C:\\Users\\xandr\\OneDrive\\Documents\\GitHub\\MC_Sim\\functionizing_fake_data.py')
credMass=0.95
ROPESize=0.5 
difference= differenceOfmeans(humanMean=4.5, variance=0.2, sampleSize =50)
#HighestDensityInterval: where 95% of the differences are? are they close to 0?
HDI= HDIofMCMC(differenceOfMeans= difference, credMass=0.95)

probInROPE(difference, ROPESize=0.5 )

plotROPEHDI(difference, HDI, ROPESize=0.5, credMass=0.95)

import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.charts import Histogram
from bokeh.models import Span


sampleSize = Slider(title="Sample Size", value=50, start=10, end=10000, step=10)
sampleSize = Slider(title="Sample Size", value=50, start=10, end=10000, step=10)



p1 = figure(width=400, height=400, 
           title = "histogram of difference of means {0:.0f}% HDI" .format(credMass*100))
hist,edges =np.histogram(difference)
p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#7cb5ec", line_color="#033649")
ROPE1 = Span(location=0-ROPESize, dimension='height', line_color='red', 
             line_width=3)
ROPE2 = Span(location=ROPESize, dimension='height', line_color='red', 
             line_width=3)
p1.renderers.extend([ROPE1, ROPE2])
p1.line(x=[HDI[0], HDI[1]], y=[3,3], line_color='black', line_width=4, legend ="HDI")
show(p1)



####Need to figure out how to round this and put it in annotation
HDIText="HDI: {}" .format(np.around(HDI, decimals=1))
ROPEText="ROPE: [-{0}, {1}]" .format(ROPESize, ROPESize)
ax.annotate(HDIText, (0.4, 0.05), textcoords='axes fraction', size=20, color='black')
ax.annotate(ROPEText, (.5, .8), textcoords='axes fraction', size = 20, color = 'red')
    
    
    show(p)
