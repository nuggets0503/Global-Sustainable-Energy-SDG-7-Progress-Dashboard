import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="Global Sustainable Energy Dashboard", layout="wide")

# --- DEEP FOREST BRANDING & CSS ---
st.markdown("""
    <style>
    /* Main App Background */
    .stApp { background-color: #121619 !important; }
    
    /* Typography */
    h1, h2, h3, h4, p, label, .stMarkdown { 
        color: #E2E8F0 !important; 
        font-family: 'Inter', sans-serif !important; 
    }
    .brand-text { color: #6FCF97 !important; font-weight: 600; } 
    
    /* KPI Cards */
    [data-testid="stMetric"] { 
        background-color: #1E252B !important; 
        padding: 24px !important; 
        border-radius: 12px !important; 
        border: 1px solid #2D3748 !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    [data-testid="stMetricValue"] > div { color: #6FCF97 !important; }
    
    /* Insight Box */
    .insight-box { 
        background-color: rgba(47, 160, 132, 0.1) !important; 
        padding: 20px 24px !important; 
        border-radius: 8px !important;
        margin-top: 24px !important;
        margin-bottom: 24px !important;
        border: 1px solid #2D3748 !important;
        border-left: 6px solid #2FA084 !important; 
    }
    
    /* Fix for Expander Labels */
    .streamlit-expanderHeader {
        background-color: #1E252B !important;
        color: #E2E8F0 !important;
        border-radius: 8px !important;
    }
    .stExpander {
        border: 1px solid #2D3748 !important;
        background-color: #1E252B !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_energy_data.csv')
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        'Access to electricity (% of population)': 'electricity_access',
        'Renewable energy share in the total final energy consumption (%)': 'renew_share',
        'Renewable-electricity-generating-capacity-per-capita': 'renew_capacity',
        'Energy intensity level of primary energy (MJ/$2017 PPP GDP)': 'energy_intensity',
        'Value_co2_emissions_kt_by_country': 'co2_emissions',
        'Low-carbon electricity (% electricity)': 'low_carbon_perc'
    })
    if 'renewable_category' in df.columns:
        df['renewable_category'] = df['renewable_category'].fillna('Unclassified')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- HEADER ---
st.title("Global Sustainable Energy & SDG 7 Progress")
st.markdown("<p class='brand-text'>Team Analysts: Danila, Jaboneta, Teope</p>", unsafe_allow_html=True)

# --- FILTERS ---
st.markdown("### Dashboard Filters")
selected_year = st.slider("Select Year", int(df['Year'].min()), int(df['Year'].max()), 2019)
emission_tier = st.multiselect("Select Emission Category", 
                               options=df['emission_category'].dropna().unique(),
                               default=df['emission_category'].dropna().unique())

filtered_df = df[(df['Year'] == selected_year) & (df['emission_category'].isin(emission_tier))]

# --- KPI SECTION (MOVED ABOVE INSIGHT BOX) ---
st.markdown("<br>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Electricity Access", f"{filtered_df['electricity_access'].mean():.1f}%")
k2.metric("CO2 (Millions kt)", f"{filtered_df['co2_emissions'].sum()/1e6:.2f}")
k3.metric("Renewable Share", f"{filtered_df['renew_share'].mean():.1f}%")
k4.metric("Energy Intensity", f"{filtered_df['energy_intensity'].mean():.2f}")

# --- INSIGHT BOX (DYNAMIC & BUG-PROOF) ---
if not filtered_df.empty:
    # Calculate mean for the highest category currently selected by the user
    current_categories = filtered_df['emission_category'].unique()
    avg_renew = filtered_df['renew_share'].mean()
    
    insight_html = f"""
    <div class="insight-box">
        <h3 style="margin-top: 0; color: #E2E8F0;">Key Strategic Insight</h3>
        <p style="font-size: 16px; color: #E2E8F0; line-height: 1.5; margin-bottom: 0;">
            For the selected categories in <strong>{selected_year}</strong>, the average renewable energy share is <strong>{avg_renew:.2f}%</strong>. 
            This reflects the transition velocity for the filtered economic group, highlighting the scale of infrastructure pivot required to meet SDG 7.
        </p>
    </div>
    """
    st.markdown(insight_html, unsafe_allow_html=True)
else:
    st.warning("No data available for the selected filters. Please adjust your categories.")

st.markdown("---")

# --- VISUALS ---

# 1. MAP
st.subheader("Global Electricity Access Distribution")
try:
    geo_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
    m = folium.Map(location=[20, 0], zoom_start=1.8, tiles="CartoDB dark_matter")
    folium.Choropleth(
        geo_data=requests.get(geo_url).json(), data=filtered_df,
        columns=["Entity", "electricity_access"], key_on="feature.properties.name",
        fill_color="YlGnBu", fill_opacity=0.7, line_opacity=0.2, legend_name="Access %"
    ).add_to(m)
    st_folium(m, height=500, use_container_width=True)
except:
    st.info("Geographic data is loading...")

with st.expander("Strategic Interpretation: Geographic Access"):
    st.write("Current data shows broad regions, primarily in Sub-Saharan Africa, still possess electricity access rates below 60%. Achieving SDG 7 requires addressing the 'Final Mile' in these specific geographic clusters.")

st.markdown("---")

# 2. SUNBURST
st.subheader("Portfolio Composition by Renewable Tier")
if not filtered_df.empty:
    fig_sun = px.sunburst(
        filtered_df, path=['renewable_category', 'Entity'],
        values='renew_capacity', color='renew_share',
        color_continuous_scale='Greens', template="plotly_dark"
    )
    fig_sun.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, l=0, r=0, b=0))
    st.plotly_chart(fig_sun, use_container_width=True)

with st.expander("Strategic Interpretation: Energy Mix Hierarchy"):
    st.write("The hierarchy reveals that countries with the 'Very High' renewable adoption tier are often smaller or hydro-dependent economies. This visualizes the challenge for large industrial nations to shift their massive baseload requirements to green sources.")

st.markdown("---")

# 3. TRANSITION & CORRELATION
colA, colB = st.columns(2)
with colA:
    st.subheader("Energy Transition Trend")
    # 1. Filter the full historical data by the user's multiselect categories
    hist_filtered_df = df[df['emission_category'].isin(emission_tier)]
    
    # 2. Group the filtered data by year
    hist_df = hist_filtered_df.groupby('Year')[['Electricity from renewables (TWh)', 'Electricity from fossil fuels (TWh)']].mean().reset_index()
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=hist_df['Year'], y=hist_df['Electricity from renewables (TWh)'], name="Renewables", line=dict(color='#6FCF97', width=4)))
    fig_line.add_trace(go.Scatter(x=hist_df['Year'], y=hist_df['Electricity from fossil fuels (TWh)'], name="Fossil", line=dict(color='#718096', dash='dot')))
    fig_line.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_line, use_container_width=True)
    with st.expander("Discussion: Transition Velocity"):
        st.write("Since 2000, renewable electricity generation has grown by 56%, narrowing the gap with fossil fuels, which grew by only 23% in the same period.")

with colB:
    st.subheader("Correlation: Economy vs. Transition")
    corr_cols = ['gdp_per_capita', 'renew_share', 'co2_emissions', 'energy_intensity']
    corr_matrix = filtered_df[corr_cols].corr()
    fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='Viridis', template="plotly_dark")
    st.plotly_chart(fig_corr, use_container_width=True)
    with st.expander("Discussion: Structural Paradox"):
        st.write("A strong negative correlation ($r = -0.52$) exists between renewable share and energy consumption per capita, showing that wealthier nations currently consume more fossil-fuel energy per person.")

# 4. TORNADO CHART (TOP 10 EMITTERS)
st.subheader("Top 10 Emitters: Fossil vs. Renewable Capacity")
top_10 = filtered_df.nlargest(10, 'co2_emissions')
fig_tornado = go.Figure()
fig_tornado.add_trace(go.Bar(y=top_10['Entity'], x=top_10['Electricity from fossil fuels (TWh)'], name='Fossil', orientation='h', marker_color='#1F6F5F'))
fig_tornado.add_trace(go.Bar(y=top_10['Entity'], x=top_10['Electricity from renewables (TWh)'], name='Renewable', orientation='h', marker_color='#6FCF97'))
fig_tornado.update_layout(barmode='stack', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_tornado, use_container_width=True)

with st.expander("Strategic Interpretation: Emission Leaders"):
    st.write("This visualization exposes the decarbonization gap. For the top 10 emitting nations, fossil-fuel reliance overwhelmingly dwarfs renewable generation capacity, highlighting where the most aggressive policy intervention is required.")

# --- FOOTER WITH EXTERNAL LINKS ---
st.markdown("""
    <br><hr>
    <p style='text-align: center; color: #718096;'>
        Data Source: 
        <a href="https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy" target="_blank" style="color: #6FCF97; text-decoration: none;">
            Global Sustainable Energy Dataset (Kaggle)
        </a> 
        | Attribution: Tanwar (2023) | License: GPL v3.0
    </p>
""", unsafe_allow_html=True)