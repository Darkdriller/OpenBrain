import pandas as pd
import plotly
import plotly.graph_objects as go
import json


def read_swc(filename):
    columns = ['ID', 'Type', 'X', 'Y', 'Z', 'Radius', 'Parent']
    neuron_data = pd.read_csv(filename, sep=' ', names=columns, comment='#')
    return neuron_data

def plot_neuron(neuron_data):
    fig = go.Figure()
    for index, row in neuron_data.iterrows():
        if row['Parent'] == -1:
            continue
        parent_row = neuron_data[neuron_data['ID'] == row['Parent']].iloc[0]
        color = 'red' if row['Type'] == 0 else 'black'
        fig.add_trace(go.Scatter3d(x=[row['X'], parent_row['X']],
                                   y=[row['Y'], parent_row['Y']],
                                   z=[row['Z'], parent_row['Z']],
                                   mode='lines', line=dict(color=color)))
    return fig