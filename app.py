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


# Define consistent color scheme for severity
SEVERITY_COLORS = {
    'Severe': '#c0392b',   # Dark red (hottest)
    'High': '#e67e22',     # Orange (hot)
    'Medium': '#f39c12',   # Gold/yellow (warm)
    'Low': '#27ae60'       # Green (cool/calm)
}


# Title
st.title("🚊 TTC Streetcar Performance Analysis ")
st.markdown("*Strategic data-driven insights for streetcar operations management*")


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
st.subheader("📈 Key Metrics")


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
    # Create bar chart with professional colors
    fig = px.bar(
        x=route_counts.index,
        y=route_counts.values,
        labels={'x': 'Route', 'y': 'Number of Incidents'},
        title=f"Top {top_n} Routes by Incident Count",
        text=route_counts.values
    )
    
    # Use professional color palette
    colors = ['#c0392b', '#e67e22', '#f39c12', '#27ae60', '#3498db', 
              '#9b59b6', '#1abc9c', '#34495e', '#e74c3c', '#16a085']
    fig.update_traces(
        marker_color=colors[:len(route_counts)],
        textposition='outside'
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title="Route",
        yaxis_title="Number of Incidents",
        height=500,  # Increased height so numbers don't cut off
        xaxis=dict(
            tickmode='array',
            tickvals=list(route_counts.index),
            ticktext=list(route_counts.index),
        ),
        margin=dict(t=80)  # Extra top margin for numbers
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


# Create heatmap with warmer color scheme to match severity theme
fig = px.imshow(
    heatmap_pivot,
    labels=dict(x="Hour of Day", y="Day of Week", color="Incidents"),
    x=list(range(24)),
    y=[day_labels[int(i)] for i in heatmap_pivot.index],
    color_continuous_scale="OrRd",  # Orange to Red (matches severity theme)
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


# Route Deep Dive with Tabs
st.markdown("---")
st.subheader("🔍 Route Deep Dive Analysis")


# Route selector (applies to all tabs)
top_routes = df['route'].value_counts().head(5).index.tolist()
selected_deep_dive_route = st.selectbox(
    "Select Route to Analyze",
    options=top_routes,
    index=1 if '504' in top_routes else 0
)


# Create tabs for different time periods
tab1, tab2 = st.tabs(["🌅 Morning Rush (5-9 AM)", "☀️ Afternoon Rush (1-6 PM)"])


# Helper function to generate smart recommendations
def generate_recommendations(route_data, route_name, time_period, start_hour, end_hour):
    """Generate data-driven recommendations based on incident patterns"""
    
    total_incidents = len(route_data)
    high_severity = route_data['delay_bin'].isin(['High', 'Severe']).sum()
    high_severity_pct = (high_severity / total_incidents * 100) if total_incidents > 0 else 0
    
    # Find peak hour in this window
    hourly_counts = route_data.groupby('hour').size()
    peak_hour = hourly_counts.idxmax() if len(hourly_counts) > 0 else start_hour
    peak_count = hourly_counts.max() if len(hourly_counts) > 0 else 0
    
    # Build smart recommendations
    recommendations = []
    
    # Recommendation 1: Based on incident volume
    if total_incidents > 100:
        recommendations.append(f"**High incident volume:** Pre-position maintenance crew by {start_hour}:00")
    elif total_incidents > 50:
        recommendations.append(f"**Moderate incidents:** On-call maintenance crew during {time_period}")
    else:
        recommendations.append(f"**Low incident volume:** Standard maintenance protocols sufficient")
    
    # Recommendation 2: Based on severity
    if high_severity_pct > 40:
        recommendations.append(f"**High severity rate ({high_severity_pct:.0f}%):** Deploy backup vehicle throughout window")
    elif high_severity_pct > 25:
        recommendations.append(f"**Elevated severity ({high_severity_pct:.0f}%):** Backup vehicle on standby")
    else:
        recommendations.append(f"**Manageable severity ({high_severity_pct:.0f}%):** Standard backup protocols")
    
    # Recommendation 3: Based on peak hour
    if peak_count > (total_incidents * 0.3):  # If one hour has >30% of incidents
        recommendations.append(f"**Concentrated peak at {peak_hour}:00:** Enhanced monitoring {peak_hour-1}:30-{peak_hour+1}:30")
    else:
        recommendations.append(f"**Distributed pattern:** Maintain consistent staffing throughout window")
    
    # Recommendation 4: Proactive measures
    if total_incidents > 75:
        recommendations.append(f"**Preventive action:** Enhanced pre-service inspection before {start_hour}:00")
    else:
        recommendations.append(f"**Standard protocol:** Regular pre-service inspection")
    
    return recommendations


# TAB 1: Morning Rush
with tab1:
    st.markdown(f"**Analyzing Route {selected_deep_dive_route}** during morning rush hours (5:00-9:00 AM)")
    
    route_morning = df[
        (df['route'] == selected_deep_dive_route) & 
        (df['hour'] >= 5) & 
        (df['hour'] <= 9)
    ]
    
    if len(route_morning) > 0:
        st.write(f"Found **{len(route_morning):,} incidents** during this period")
        
        col1, col2 = st.columns(2)
        
        with col1:
            hourly = route_morning.groupby('hour').size()
            fig = px.line(
                x=hourly.index,
                y=hourly.values,
                markers=True,
                labels={'x': 'Hour', 'y': 'Incidents'},
                title=f"Route {selected_deep_dive_route}: Hourly Pattern"
            )
            fig.update_traces(line_color='#c0392b', marker=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            severity = route_morning['delay_bin'].value_counts()
            severity_ordered = ['Severe', 'High', 'Medium', 'Low']
            severity_data = [severity.get(s, 0) for s in severity_ordered]
            
            fig = px.pie(
                values=severity_data,
                names=severity_ordered,
                title="Severity Distribution",
                color=severity_ordered,
                color_discrete_map=SEVERITY_COLORS,
                category_orders={'names': severity_ordered}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Generate smart recommendations
        recommendations = generate_recommendations(
            route_morning, 
            selected_deep_dive_route, 
            "morning rush",
            5, 9
        )
        
        st.success(f"""
### 💡 Data-Driven Recommendations for Route {selected_deep_dive_route} (Morning):


{chr(10).join(f"- {rec}" for rec in recommendations)}
        """)
    else:
        st.warning(f"No Route {selected_deep_dive_route} data found for morning hours")


# TAB 2: Afternoon Rush
with tab2:
    st.markdown(f"**Analyzing Route {selected_deep_dive_route}** during afternoon rush hours (1:00-6:00 PM)")
    
    route_afternoon = df[
        (df['route'] == selected_deep_dive_route) & 
        (df['hour'] >= 13) &  # 1 PM
        (df['hour'] <= 18)     # 6 PM
    ]
    
    if len(route_afternoon) > 0:
        st.write(f"Found **{len(route_afternoon):,} incidents** during this period")
        
        col1, col2 = st.columns(2)
        
        with col1:
            hourly = route_afternoon.groupby('hour').size()
            # Convert 24hr to 12hr for display
            hour_labels = {13: '1 PM', 14: '2 PM', 15: '3 PM', 16: '4 PM', 17: '5 PM', 18: '6 PM'}
            
            fig = px.line(
                x=[hour_labels.get(h, h) for h in hourly.index],
                y=hourly.values,
                markers=True,
                labels={'x': 'Hour', 'y': 'Incidents'},
                title=f"Route {selected_deep_dive_route}: Hourly Pattern"
            )
            fig.update_traces(line_color='#c0392b', marker=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            severity = route_afternoon['delay_bin'].value_counts()
            severity_ordered = ['Severe', 'High', 'Medium', 'Low']
            severity_data = [severity.get(s, 0) for s in severity_ordered]
            
            fig = px.pie(
                values=severity_data,
                names=severity_ordered,
                title="Severity Distribution",
                color=severity_ordered,
                color_discrete_map=SEVERITY_COLORS,
                category_orders={'names': severity_ordered}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Generate smart recommendations
        recommendations = generate_recommendations(
            route_afternoon, 
            selected_deep_dive_route, 
            "afternoon rush",
            13, 18
        )
        
        st.success(f"""
### 💡 Data-Driven Recommendations for Route {selected_deep_dive_route} (Afternoon):

{chr(10).join(f"- {rec}" for rec in recommendations)}
        """)
    else:
        st.warning(f"No Route {selected_deep_dive_route} data found for afternoon hours")

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


**Created by:** clv-lead (J.W.)  
**Portfolio Project**


*Built with Streamlit & Python*
""")