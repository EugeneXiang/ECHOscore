import plotly.graph_objects as go
from config import DIMS

def make_radar(max_scores: list[float]) -> go.Figure:
    """Create a 9-dimension radar chart from max_scores"""
    closed = DIMS + [DIMS[0]]
    r = max_scores + [max_scores[0]]
    fig = go.Figure(go.Scatterpolar(r=r, theta=closed, fill='toself', name='Final'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])),
                      showlegend=False,
                      title="Final Scores Radar")
    return fig