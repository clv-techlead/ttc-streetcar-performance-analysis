import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="TTC Operational Intelligence",
    page_icon="🚊",
    layout="wide"
)


# Title
st.title("🚊 TTC Operational Intelligence Dashboard")
st.markdown("*Data-driven insights for streetcar incident management*")


# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/ttc_feature_engineered_2014_2025.csv')
    return df


# Show loading message
with st.spinner('Loading data...'):
    df = load_data()


st.success(f"Loaded {len(df):,} incidents from 2014-2025")


# Sidebar filters
st.sidebar.header("Filters")
st.sidebar.markdown("*Use these to filter the data*")


# Route filter
all_routes = sorted(df['route'].unique().tolist())
selected_routes = st.sidebar.multiselect(
    "📍 Select Routes",
    options=['All'] + all_routes,
    default=['All'],
    help="Choose one or more routes, or 'All' for everything"
)


# Hour filter
selected_hours = st.sidebar.slider(
    "⏰ Hour of Day",
    min_value=0,
    max_value=23,
    value=(0, 23),
    help="Filter by time of day (0 = midnight, 23 = 11 PM)"
)


# Severity filter
severity_order = ['Low', 'Medium', 'High', 'Severe']
selected_severity = st.sidebar.multiselect(
    "🚨 Severity Level",
    options=severity_order,
    default=severity_order,
    help="Filter by incident severity"
)


st.sidebar.markdown("---")
st.sidebar.caption("Filters apply to all visualizations below")


# Apply filters
filtered_df = df.copy()


# Apply route filter
if 'All' not in selected_routes:
    filtered_df = filtered_df[filtered_df['route'].isin(selected_routes)]


# Apply hour filter
filtered_df = filtered_df[
    (filtered_df['hour'] >= selected_hours[0]) & 
    (filtered_df['hour'] <= selected_hours[1])
]


# Apply severity filter
if selected_severity:
    filtered_df = filtered_df[filtered_df['delay_bin'].isin(selected_severity)]


# Show filtered count
st.info(f"Showing **{len(filtered_df):,}** of {len(df):,} total incidents ({len(filtered_df)/len(df)*100:.1f}%)")


# Key metrics
st.markdown("---")
st.subheader("Key Metrics")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        label="Total Incidents",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df):,} from total",
        delta_color="inverse"
    )


with col2:
    avg_delay = filtered_df['min_delay'].mean()
    overall_avg = df['min_delay'].mean()
    st.metric(
        label="Avg Delay (min)",
        value=f"{avg_delay:.1f}",
        delta=f"{avg_delay - overall_avg:.1f}",
        delta_color="inverse"
    )


with col3:
    high_severity = filtered_df['delay_bin'].isin(['High', 'Severe']).sum()
    high_severity_pct = (high_severity / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric(
        label="High Severity %",
        value=f"{high_severity_pct:.1f}%",
        delta=f"{high_severity} incidents"
    )


with col4:
    if len(filtered_df) > 0:
        top_route = filtered_df['route'].value_counts().index[0]
        top_count = filtered_df['route'].value_counts().values[0]
        st.metric(
            label="Most Impacted Route",
            value=f"{top_route}",
            delta=f"{top_count} incidents"
        )
    else:
        st.metric(label="Most Impacted Route", value="N/A")


# Route Analysis
st.markdown("---")
st.subheader("📍 Route Analysis")


top_n = 10
route_counts = filtered_df['route'].value_counts().head(top_n)


if len(route_counts) > 0:
    fig = px.bar(
        x=route_counts.index,
        y=route_counts.values,
        labels={'x': 'Route', 'y': 'Number of Incidents'},
        title=f"Top {top_n} Routes by Incident Count",
        color=route_counts.values,
        color_continuous_scale='Reds',
        text=route_counts.values
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        xaxis_title="Route",
        yaxis_title="Number of Incidents",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data to display with current filters")


# Temporal Patterns
st.markdown("---")
st.subheader("⏰ When Do Incidents Happen?")


# Create pivot table for heatmap
heatmap_data = filtered_df.groupby(['weekday', 'hour']).size().reset_index(name='count')
heatmap_pivot = heatmap_data.pivot(index='weekday', columns='hour', values='count')
heatmap_pivot = heatmap_pivot.fillna(0)


# Create day labels
day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Create heatmap
fig = px.imshow(
    heatmap_pivot,
    labels=dict(x="Hour of Day", y="Day of Week", color="Incidents"),
    x=list(range(24)),
    y=[day_labels[int(i)] for i in heatmap_pivot.index],
    color_continuous_scale="Reds",
    aspect="auto",
    title="Incident Heatmap: Day vs Hour"
)
fig.update_xaxes(side="bottom")
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)


# Find peak time
if len(heatmap_data) > 0:
    peak_hour = heatmap_data.loc[heatmap_data['count'].idxmax()]
    st.info(f"🔥 **Peak incident time:** {day_labels[int(peak_hour['weekday'])]} at {int(peak_hour['hour'])}:00 ({int(peak_hour['count'])} incidents)")


# Route 504 Deep Dive
st.markdown("---")
st.subheader("Deep Dive: Route 504 Morning Hours")


route_504_morning = df[
    (df['route'] == '504') & 
    (df['hour'] >= 5) & 
    (df['hour'] <= 9)
]


if len(route_504_morning) > 0:
    st.write(f"Found **{len(route_504_morning):,} incidents** on Route 504 between 5:00-9:00 AM")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hourly = route_504_morning.groupby('hour').size()
        fig = px.line(
            x=hourly.index,
            y=hourly.values,
            markers=True,
            labels={'x': 'Hour', 'y': 'Incidents'},
            title="Route 504: Incidents by Hour (Morning)"
        )
        fig.update_traces(line_color='#e74c3c', marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        severity = route_504_morning['delay_bin'].value_counts()
        fig = px.pie(
            values=severity.values,
            names=severity.index,
            title="Severity Distribution",
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        st.plotly_chart(fig, use_container_width=True)
    
    high_severity_count = route_504_morning['delay_bin'].isin(['High', 'Severe']).sum()
    
    st.success(f"""
    **💡 Actionable Insights:**
    
    Route 504 experiences **{len(route_504_morning):,} incidents** during morning rush (5-9 AM), 
    with **{high_severity_count} classified as High/Severe** severity.
    
    **Recommendations:**
    - Pre-position maintenance crew by 5:00 AM
    - Deploy backup vehicle during 6-8 AM peak
    - Enhanced pre-service vehicle inspection
    - Real-time monitoring dashboard for operations team
    """)
else:
    st.warning("No Route 504 data found for morning hours (5-9 AM)")


# About section in sidebar
st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info("""
**TTC Operational Intelligence Dashboard**


Analyzing TTC streetcar incidents to provide actionable insights for transit operations.


**Data Coverage:** 2014-2025  
**Total Incidents:** 67,151  
**Routes Covered:** Major TTC streetcar routes


---


**Created by:** [Your Name]  
**Portfolio Project**


*Built with Streamlit & Python*
""")