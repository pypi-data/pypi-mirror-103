import numpy as np
import plotly.graph_objects as go 
    
def create_timeseries_with_annotations_plot(x: np.ndarray, y: np.ndarray, x_a: np.ndarray, y_a: np.ndarray, marker_size: int=6):
    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=x, y=y,
                    mode='lines+markers',
                    name='signal',
                    marker = dict(color='rgba(0, 0, 255, .5)', size=marker_size),
                    selected_marker = dict(color='rgba(0, 0, 255, .5)', size=marker_size),
                    unselected_marker = dict(color='rgba(0, 0, 255, .5)', size=marker_size)))
    fig.add_trace(go.Scattergl(x=x_a, y=y_a,
                    mode='markers',
                    name='annotation', marker_color='rgba(255, 0, 0, .9)', marker_size=marker_size+2,
                    selected_marker = dict(color='rgba(255, 0, 0, .9)', size=marker_size+2),
                    unselected_marker = dict(color='rgba(255, 0, 0, .9)', size=marker_size+2)))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(clickmode='event+select')

    return fig

def create_timeseries_with_support_signal_and_annotations_plot(x: np.ndarray, y: np.ndarray, x_support: np.ndarray,y_support: np.ndarray, x_a: np.ndarray, y_a: np.ndarray, marker_size: int=6):
    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=x, y=y,
                    mode='lines+markers',
                    name='signal',
                    marker = dict(color='rgba(0, 0, 255, .5)', size=marker_size),
                    selected_marker = dict(color='rgba(0, 0, 255, .5)', size=marker_size),
                    unselected_marker = dict(color='rgba(0, 0, 255, .5)', size=marker_size)))
    fig.add_trace(go.Scattergl(x=x_support, y=y_support,
                    mode='lines',
                    name='support signal',
                    marker = dict(color='rgba(0, 255, 0, .5)', size=marker_size)))
    fig.add_trace(go.Scattergl(x=x_a, y=y_a,
                    mode='markers',
                    name='annotation', marker_color='rgba(255, 0, 0, .9)', marker_size=marker_size+2,
                    selected_marker = dict(color='rgba(255, 0, 0, .9)', size=marker_size+2),
                    unselected_marker = dict(color='rgba(255, 0, 0, .9)', size=marker_size+2)))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(clickmode='event+select')

    return fig
