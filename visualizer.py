import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_skills_chart(analysis_result):
    # Bar chart showing matched vs missing skills counts
    matched = len(analysis_result.get('matched_skills', []))
    missing = len(analysis_result.get('missing_skills', []))
    labels = ['Matched Skills', 'Missing Skills']
    values = [matched, missing]

    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=['green', 'red'])])
    fig.update_layout(title='Matched vs Missing Skills Count',
                      yaxis=dict(title='Number of Skills'),
                      xaxis=dict(title='Skill Status'))
    return fig

def create_match_visualization(analysis_result):
    # Pie chart showing matched vs missing skills proportion
    matched = len(analysis_result.get('matched_skills', []))
    missing = len(analysis_result.get('missing_skills', []))
    labels = ['Matched Skills', 'Missing Skills']
    values = [matched, missing]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title='Skill Match Proportion')
    return fig

def create_skills_distribution_bar(analysis_result):
    # Bar chart showing number of skills required and found per skill category if available
    # For simplicity, using job skills categories if present in analysis_result['skills_categories']
    # If not available, fallback to a dummy bar chart
    categories = analysis_result.get('skills_categories', {})
    if categories:
        categories_names = list(categories.keys())
        required_counts = [len(skills['required']) for skills in categories.values()]
        matched_counts = [len(skills['matched']) for skills in categories.values()]

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Required', x=categories_names, y=required_counts))
        fig.add_trace(go.Bar(name='Matched', x=categories_names, y=matched_counts))
        fig.update_layout(barmode='group', title='Skills Distribution by Category', yaxis_title='Count')
    else:
        # Simple placeholder bar chart
        fig = go.Figure(data=[go.Bar(x=['Skills'], y=[len(analysis_result.get('matched_skills', []))])])
        fig.update_layout(title='Skills Found Count')

    return fig

def create_match_gauge(analysis_result):
    # Gauge chart to show overall match percentage
    match_pct = analysis_result.get('match_percentage', 0)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=match_pct,
        title={'text': "Overall Match Percentage"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 50], 'color': "red"},
                   {'range': [50, 80], 'color': "yellow"},
                   {'range': [80, 100], 'color': "green"}]}
    ))
    return fig

def create_skills_radar(analysis_result):
    # Radar chart comparing required vs matched skills count by category if categories exist
    categories = analysis_result.get('skills_categories', {})
    if categories:
        categories_names = list(categories.keys())
        required_counts = [len(skills['required']) for skills in categories.values()]
        matched_counts = [len(skills['matched']) for skills in categories.values()]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=required_counts,
            theta=categories_names,
            fill='toself',
            name='Required Skills'
        ))
        fig.add_trace(go.Scatterpolar(
            r=matched_counts,
            theta=categories_names,
            fill='toself',
            name='Matched Skills'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(required_counts + matched_counts) + 1]
                )),
            showlegend=True,
            title="Skills Coverage Radar Chart"
        )
    else:
        # Fallback radar with dummy data if no categories
        categories_names = ['All Skills']
        required_counts = [len(analysis_result.get('job_skills', []))]
        matched_counts = [len(analysis_result.get('matched_skills', []))]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=required_counts,
            theta=categories_names,
            fill='toself',
            name='Required Skills'
        ))
        fig.add_trace(go.Scatterpolar(
            r=matched_counts,
            theta=categories_names,
            fill='toself',
            name='Matched Skills'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(required_counts + matched_counts) + 1]
                )),
            showlegend=True,
            title="Skills Coverage Radar Chart"
        )
    return fig
