# 🚊TTC Streetcar Operational Intelligence Dashboard

An interactive dashboard analyzing 11 years of Toronto Transit Commission streetcar incident data (2014-2025) to provide actionable operational insights and strategic resource allocation recommendations.

##  Project Overview

This dashboard transforms 67,000+ historical incident records into strategic recommendations for transit operations, demonstrating how data analysis can drive operational improvements. Built to help transit managers make data-driven decisions about resource allocation, preventive maintenance, and operational planning.

##  Live Demo

**[View Live Dashboard](https://ttc-streetcar-performance-analysis-ngwammt9iwtqkix7bo3vte.streamlit.app/)** 


##  Key Features

### Core Analytics
- **Interactive Filtering**: Filter by routes, time of day, and severity levels
- **Performance Metrics**: Track incidents, delays, and severity patterns in real-time
- **Route Analysis**: Identify highest-impact routes with visual comparisons
- **Temporal Patterns**: Heatmap visualization showing incident patterns across days and hours

### Advanced Planning Tools
- **Dynamic Deep Dives**: Analyze specific routes during morning (5-9 AM) and afternoon (1-6 PM) rush hours
- **What-If Scenario Planning**: Model the impact of operational interventions (maintenance crews, inspections, backup vehicles) with cost-benefit analysis and ROI calculations
- **Resource Allocation Recommendations**: Priority-ranked intervention areas with detailed action plans for top routes and time windows
- **Data-Driven Recommendations**: Smart, context-aware operational recommendations based on actual historical patterns

##  Key Insights Discovered

- **Route 501** has the highest incident volume with 13,483 incidents over 11 years
- **Afternoon rush hours (1-6 PM)** show highest incident concentration based on heatmap analysis
- Severity distribution varies significantly by route and time period
- Peak incident times identified for targeted operational improvements
- **Top 20 priority areas** identified where resource allocation would have maximum impact
- Estimated **20% reduction** in incidents possible with targeted interventions

##  Built With

- **Python** - Data processing and analysis
- **Streamlit** - Interactive web dashboard framework
- **Plotly** - Interactive visualizations and charts
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Background styling for priority tables

##  Run Locally

```bash
1. Clone repository
git clone https://github.com/clv-techlead/ttc-streetcar-performance-analysis.git
cd ttc-streetcar-performance-analysis

2. Install dependencies
pip install -r requirements.txt

3. Run dashboard
streamlit run app.py
```

##  Project Structure

```
ttc-streetcar-performance-analysis/
├── README.md                                     # Project documentation
├── app.py                                        # Main dashboard application
├── check_data.py
├── data
│   └── TTC_Feature_Engineered_2014_2025.csv      # Historical incident data
└── requirements.txt                              # Python dependencies
```

##  Data

- **Source**: Toronto Open Data - TTC Streetcar Delay Data
- **Time Period**: 2014-2025
- **Records**: 67,151 incidents
- **Features**: Timestamp, route, station, incident type, delay duration, severity classification
- **Routes Covered**: Major TTC streetcar routes including 501, 504, 506, and more

##  Use Cases

This dashboard is designed for:
- **Transit Operations Managers**: Identify where to deploy resources for maximum impact
- **Maintenance Planning**: Schedule preventive maintenance during high-risk time windows
- **Budget Planning**: Estimate ROI of operational interventions with scenario planning tool
- **Performance Monitoring**: Track incident patterns and severity trends over time
- **Strategic Planning**: Make data-driven decisions about route improvements

##  Learning Outcomes

This project demonstrates:
- Building interactive data visualization dashboards with Streamlit
- Translating analytical insights into actionable business recommendations
- Creating user-friendly interfaces for non-technical stakeholders
- Strategic thinking about operational optimization
- Cost-benefit analysis and ROI modeling
- Priority scoring algorithms for resource allocation

##  Related Projects

This dashboard visualizes insights from my [TTC Incident Classification](https://github.com/clv-techlead/ML_12/blob/main/README.md) machine learning project, where my team and I built models to predict incident severity and engineered features for operational analysis.

##  Contributing

Feedback and suggestions welcome! Feel free to open an issue or submit a pull request.

##  License

This project is available for portfolio and educational purposes.

**Created by:** @clv-techlead (J.W.)

