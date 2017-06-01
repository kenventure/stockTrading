import plotly.plotly as py
import plotly.graph_objs as go
from Display import Display

class PlotlyDisplay (Display):
    def __init__(self):
        print('Init')
        
    def display(self, arr, anno):
    
        xArr=[]
        for i in range(0, 5000):
            xArr.append(i)
        yArr = arr[0:4999]
        annoArr = anno[0:4999]
        trace1 = go.Scatter(
        x=xArr,
        y=yArr,
        mode='lines+markers+text',
        name='Lines, Markers and Text',
        text=annoArr,
        textposition='top')
        data = [trace1]
        layout = go.Layout(
            showlegend=False
        )
        fig = go.Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename='text-chart-basic')