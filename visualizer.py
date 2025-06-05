import plotly.express as px
import pandas as pd

def pie_chart(found, missing):
    data = pd.DataFrame({
        'Skill Status': ['Matched', 'Missing'],
        'Count': [len(found), len(missing)]
    })
    fig = px.pie(data, names='Skill Status', values='Count', title='Skill Match Overview')
    return fig
