from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
from plotly.subplots import make_subplots

dt = pd.read_csv('AnalysisData.csv')
flds = dt.columns.tolist()
app = Flask(__name__)

# Define the root route
@app.route('/')
def index():
    return render_template('index3.html',colours=flds)

@app.route('/callback/<endpoint>')
def cb(endpoint):
    if endpoint == "getFields":
        print(request.args.get('field1')) 
        return gm(request.args.get('field1'),request.args.get('field2'),request.args.get('field3'))
    if endpoint == "getCorr":
        print(request.args.get('field1'))
        return gc(request.args.get('field1'))

def gm(Fl1,Fl2,Fl3):
    print(Fl1)
    print(Fl2)
    print(Fl3)
    fig1 = px.line(dt,x="rowID",y=Fl1)
    fig2 = px.line(dt,x="rowID",y=Fl2)
    fig3 = px.line(dt,x="rowID",y=Fl3)
    trace1 = fig1['data'][0]
    trace2 = fig2['data'][0]
    trace3 = fig3['data'][0]
    fig = make_subplots(rows=3, cols=1, shared_xaxes=False)
    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=2, col=1)
    fig.add_trace(trace3, row=3, col=1)
    fig['layout']['xaxis']['title']='rowID'
    fig['layout']['xaxis2']['title']='rowID'
    fig['layout']['xaxis3']['title']='rowID'
    fig['layout']['yaxis']['title']=Fl1
    fig['layout']['yaxis2']['title']=Fl2
    fig['layout']['yaxis3']['title']=Fl3
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def gc(Fl1):
    print(Fl1)
    d1p = dt.corr(method=Fl1)
    fig = px.imshow(d1p)
    corrJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return corrJSON

if __name__ == "__main__":
    app.run()
