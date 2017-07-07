# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 12:14:08 2017

@author: xandr
"""
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.charts import Histogram
from bokeh.models import Span
from bokeh.models.widgets import Slider, TextInput
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox

#ROPE is the Region of practical equivalence. 
#This is often [-0.1, 0.1] or something like this.
execfile('C:\\Users\\xandr\\OneDrive\\Documents\\GitHub\\MC_Sim\\functionizing_fake_data.py')

credMass=0.95
ROPESize=0.5 
output_file("diff_means_app.html", "Difference of Means")
difference= differenceOfmeans(humanMean=4.5, variance=0.2, sampleSize =50)
#HighestDensityInterval: where 95% of the differences are? are they close to 0?
HDI= HDIofMCMC(differenceOfMeans= difference, credMass=0.95)

probInROPE(difference, ROPESize=0.5 )
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


#p1 = figure(width=400, height=400, 
#           title = "histogram of difference of means {0:.0f}% HDI" .format(credibleRegionSlider.value*100))
#hist,edges =np.histogram(difference)
#p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
#        fill_color="#7cb5ec", line_color="#033649")
#ROPE1 = Span(location=0-ROPESlider.value, dimension='height', line_color='red', 
#             line_width=3)
#ROPE2 = Span(location=ROPESlider.value, dimension='height', line_color='red', 
#             line_width=3)
#p1.renderers.extend([ROPE1, ROPE2])
#p1.line(x=[HDI[0], HDI[1]], y=[3,3], line_color='black', line_width=4, legend ="HDI")

#difference= differenceOfmeans(humanMean=humanMeanSlider.value, variance=varianceSlider.value, sampleSize =sampleSlider.value)
##HighestDensityInterval: where 95% of the differences are? are they close to 0?
#diffSource= ColumnDataSource(data=dict(difference=difference))
#
#HDI= HDIofMCMC(differenceOfMeans= difference, credMass=credibleRegionSlider.value)
#
#probInROPE(difference, ROPESize=ROPESlider.value )
#
#plotROPEHDI(difference, HDI, ROPESize=ROPESlider.value, credMass=credibleRegionSlider.value)

#show(p1)
sampleSlider = Slider(title="Sample Size", value=50, start=10, end=10000, step=10)
varianceSlider = Slider(title="Variance", value=0.2, start=0.05, end=2, step=0.05)
humanMeanSlider= Slider(title="Human Mean NIIRS", value=4.5, start=1, end=10, step=0.1)
ROPESlider= Slider(title= "ROPE Size (Region of Practical Equivalence)", value = 0.5, start= 0.05, end = 1, step=0.05)
credibleRegionSlider= Slider(title = "Credible Mass", value = 0.95, start = 0.75, end = 0.995, step=0.05)

def update_plot(attr, new,old):
    difference= differenceOfmeans(humanMean=humanMeanSlider.value, variance=varianceSlider.value, sampleSize =sampleSlider)
    diffSource.data['difference']=difference
    return diffSource

for w in [sampleSlider, varianceSlider, humanMeanSlider, ROPESlider, credibleRegionSlider]:
    w.on_change('value', update_plot)
    
inputs = widgetbox(sampleSlider, varianceSlider, humanMeanSlider, ROPESlider, credibleRegionSlider)

curdoc().add_root(row(inputs, p1, width=800))
curdoc().title = "Difference of Means"

####Need to figure out how to round this and put it in annotation
#HDIText="HDI: {}" .format(np.around(HDI, decimals=1))
#ROPEText="ROPE: [-{0}, {1}]" .format(ROPESize, ROPESize)
#ax.annotate(HDIText, (0.4, 0.05), textcoords='axes fraction', size=20, color='black')
#ax.annotate(ROPEText, (.5, .8), textcoords='axes fraction', size = 20, color = 'red')
#    
#    
#    show(p)
