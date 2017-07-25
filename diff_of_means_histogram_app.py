# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 12:14:08 2017

@author: xandr
"""
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import Span, ColumnDataSource
from bokeh.models.widgets import Slider, Button
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox

#ROPE is the Region of practical equivalence. 
#This is often [-0.1, 0.1] or something like this.
execfile('C:\\Users\\xandr\\OneDrive\\Documents\\GitHub\\MC_Sim\\functionizing_fake_data.py')

credMass=0.95
ROPESize=0.5 
output_file("diff_means_app.html", "Difference of Means")

diffSource= ColumnDataSource(data=dict(difference= differenceOfmeans(humanMean=4.5, variance=0.2, sampleSize =50)))

#HighestDensityInterval: where 95% of the differences are? are they close to 0?
p1 = figure(width=400, height=400, 
           title = "histogram of difference of means {0:.0f}% HDI" .format(credMass*100))
probInROPE(diffSource.data['difference'], ROPESize=0.5 )
HDI= HDIofMCMC(differenceOfMeans= diffSource.data['difference'], credMass=0.95)
print("The HDI is {}" .format(HDI))
hist,edges =np.histogram(diffSource.data['difference'])

p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#7cb5ec", line_color="#033649")

df= ColumnDataSource(data=dict(ROPE=[0-ROPESize, ROPESize], HDI=HDI))
ROPE1 = Span(location=df.data['ROPE'][0], dimension='height', line_color='red', 
             line_width=3)
ROPE2 = Span(location=df.data['ROPE'][1], dimension='height', line_color='red', 
             line_width=3)
p1.renderers.extend([ROPE1, ROPE2])

p1.line(x=[df.data['HDI'][0], df.data['HDI'][1]], y=[3,3], line_color='black', 
        line_width=4, legend ="HDI")

sampleSlider = Slider(title="Sample Size", value=50, start=10, end=10000, step=10)
varianceSlider = Slider(title="Variance", value=0.2, start=0.05, end=2, step=0.05)
humanMeanSlider= Slider(title="Human Mean NIIRS", value=4.5, start=1, end=10, step=0.1)
ROPESlider= Slider(title= "ROPE Size (Region of Practical Equivalence)", value = 0.5, start= 0.05, end = 1, step=0.05)
credibleRegionSlider= Slider(title = "Credible Mass", value = 0.95, start = 0.75, end = 0.995, step=0.05)
#button = Button(label='press me') 

def update_title(attr,new, old):
    p1.title.text = "histogram of difference of means {0:.0f}% HDI" .format(credibleRegionSlider.value*100)

credibleRegionSlider.on_change('value', update_title)

#update the ROPE and the credible region
def update_df(attr, new, old):
    HDI= HDIofMCMC(differenceOfMeans= diffSource.data['difference'], credMass=credibleRegionSlider.value)
    df.data=dict(ROPE=[0-ROPESlider.value, ROPESlider.value], HDI=HDI)
    
for v in [credibleRegionSlider, ROPESlider]:
    v.on_change('value', update_df)

#update the difference of means array
def update_data(attr, new,old):
    difference= differenceOfmeans(humanMean=4.5, variance=varianceSlider.value, sampleSize =sampleSlider.value)
    diffSource.data=dict(difference=difference)
    hist,edges =np.histogram(diffSource.data['difference'])
    p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="#7cb5ec", line_color="#033649")    

for w in [sampleSlider, varianceSlider]:
    w.on_change('value', update_data)

    
inputs = widgetbox( sampleSlider, varianceSlider, credibleRegionSlider, ROPESlider)
show(row(p1,inputs))


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
