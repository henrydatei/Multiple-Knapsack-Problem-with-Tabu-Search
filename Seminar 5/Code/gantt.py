import pandas as pd
import numpy
import plotly
import plotly.express as px
from plotly.figure_factory import create_gantt
from datetime import datetime
import os
import sys

# Convert to Dates
def ConvertToDate(x):
        return datetime.fromtimestamp(1609459200 + x*60) #.strftime("%d-%m-%Y")

def GanttChart(sol, graphicsFilePath):
    # prepare x-Axis
    ticks = numpy.linspace(start = 0, stop = sol.End.max(), num = 25, dtype=int)
    tickDate = [ConvertToDate(x) for x in ticks]
    ticksy = numpy.linspace(start = 1, stop = sol.Machine.max(), num = sol.Machine.max(), dtype=int)
    ticksNamey = []
    for i in ticksy:
        ticksNamey.append("M "+str(i))    
    
    # Convert to Dates
    sol["Start_Setup"] = sol["Start_Setup"].apply(lambda x: ConvertToDate(x))
    sol["End_Setup"] = sol["End_Setup"].apply(lambda x: ConvertToDate(x))
    sol["Start"] = sol["Start"].apply(lambda x: ConvertToDate(x))
    sol["End"] = sol["End"].apply(lambda x: ConvertToDate(x))

    # Create Chart
    fig = px.timeline(sol,x_start=sol["Start"],x_end=sol["End"],y=sol["Machine"],text="Job", color="Job")
    fig.layout.xaxis.update({
        'tickvals' : tickDate,
        'ticktext' : ticks})
    fig.layout.yaxis.update({
        'tickvals' : ticksy,
        'ticktext' : ticksNamey})
    fig.show()
    
    # Output
    plotly.offline.plot(fig,filename=graphicsFilePath)

def GanttChartFromCsv(solutionFile, graphicFile):
    # Read Data
    sol = pd.read_csv(solutionFile)

    GanttChart(sol, graphicFile)