# Global Sustainable Energy & SDG 7 Progress Dashboard
### Part of the Data Mining & Analytics Portfolio

[![Streamlit App]([https://static.streamlit.io/badge_streamlit.svg)](ADD_YOUR_STREAMLIT_LINK_HERE](https://life-expectancy-dashboard-lzo8leacaaruw42k5kfbkn.streamlit.app/))

## 🧭 Project Context & Problem Statement
The global energy sector is at a critical juncture. While the United Nations Sustainable Development Goal 7 (SDG 7) calls for affordable, reliable, and sustainable energy for all by 2030, progress remains unevenly distributed. 

This dashboard serves as a **prescriptive analytics tool** designed to monitor energy transition patterns across 152 nations from 2000 to 2020. It specifically addresses the **"Decarbonization Paradox"**: the phenomenon where the world’s highest-emitting industrial powers often show the slowest relative adoption of renewable energy compared to emerging economies.

## 👥 Team Members
* **Ebenezer Danila**
* **Fara Lorraine Jaboneta**
* **Erden Jhed Teope**

## 📊 Key Analytical Insights
The dashboard is built to visualize four interconnected pillars of energy analytics identified in our research[cite: 3]:

1.  **The Decarbonization Gap:** Nations in the "Very High" emission category average significantly lower renewable energy shares (~22-26%) compared to lower-tier emitters.
2.  **The Final Mile of Equity:** Geographic analysis reveals persistent energy poverty clusters, particularly in Sub-Saharan Africa, where electricity access remains below the critical 60% threshold.
3.  **Efficiency Decoupling:** Global energy intensity has improved by approximately 12.3% over the study period, suggesting that economic growth is beginning to decouple from raw energy consumption.
4.  **Transition Velocity:** Renewable electricity generation has grown by 56% since 2000, outstripping fossil fuel growth (23%), yet fossil fuels still dominate the global baseload.

## 🛠️ Technical Implementation
*   **Language:** Python 3.x
*   **Framework:** Streamlit (SaaS-style "Deep Forest" UI)
*   **Visualizations:** 
    *   **Folium Choropleth Maps:** For geographic equity gap analysis.
    *   **Plotly Sunburst Charts:** For hierarchical energy mix breakdown.
    *   **Tornado Charts:** For Fossil vs. Renewable capacity comparison among top emitters.
    *   **Correlation Heatmaps:** To identify structural paradoxes between GDP and green adoption.
*   **Deployment:** Streamlit Community Cloud.

## 📂 Repository Structure
* `MiniProjectDashboard_2.py`: The primary Streamlit application code.
* `cleaned_energy_data.csv`: The cleaned and pre-processed dataset (2000–2020).
* `requirements.txt`: List of necessary Python libraries for deployment.
* `URL.txt`: Direct link to the hosted web application.

## 📜 Data Attribution & Ethics
**Data Source:** [Global Data on Sustainable Energy (2000-2020)](https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy) via Kaggle.
*   **Provenance:** This dataset is Open Data (Public Domain/Apache 2.0).
*   **Ethics:** No proprietary or copyrighted data was used without permission. All country-level data is used for educational and analytical purposes.

## ⚖️ License
This project is licensed under the **GNU General Public License v3.0 (GPLv3)** - see the LICENSE file for details.
