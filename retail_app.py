import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from io import BytesIO
from fpdf import FPDF

# App Configuration
st.set_page_config(page_title="Retail AI Insights", layout="wide")

# Branding and Store Information
store_logo_url = "https://via.placeholder.com/150"  # Replace with actual logo URL
store_name = "Retail Insights Pro"

# Mock Data Functions
@st.cache_data
def create_mock_data():
    np.random.seed(42)
    return pd.DataFrame({
        "CustomerID": np.arange(1, 101),
        "DwellTime": np.random.randint(5, 30, 100),  # minutes
        "PurchaseAmount": np.random.randint(10, 200, 100),  # dollars
        "VisitFrequency": np.random.randint(1, 10, 100),  # per month
    })

@st.cache_data
def get_live_data():
    np.random.seed(42)
    return pd.DataFrame({
        "Time": pd.date_range(start="2023-11-15", periods=10, freq="H"),
        "Aisle": np.random.choice(["A1", "A2", "B1", "B2"], 10),
        "Traffic": np.random.randint(50, 200, 10),
        "Sales": np.random.randint(100, 500, 10),
    })

# Load Data
data = create_mock_data()
live_data = get_live_data()

# Sidebar Navigation
st.sidebar.image(store_logo_url, width=150)
st.sidebar.title(store_name)
st.sidebar.markdown("Explore the features below to understand how data-driven insights can transform retail operations:")
view = st.sidebar.radio("Go to", [
    "Executive Summary", 
    "Real-Time Operational Data", 
    "Store Traffic Heatmap", 
    "Sales and Trend Forecasting", 
    "Customer Behavioral Insights", 
    "Actionable Recommendations", 
    "Custom Data Upload"
])

# Executive Summary Section
if view == "Executive Summary":
    st.image(store_logo_url, width=150)  # Replace with actual logo
    st.title(f"{store_name}: Unlocking Retail Potential")
    st.markdown("""
    Welcome to the Retail AI Insights App, your go-to solution for data-driven decision-making in retail.
    
    **Why This Matters**:
    - Real-time insights drive operational efficiency.
    - Actionable analytics improve sales and customer engagement.
    - Tailored recommendations maximize ROI.
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Customers Today", "1,245")
        st.metric("Average Dwell Time", "15.2 minutes")
    with col2:
        st.metric("Checkout Efficiency", "97%")
        st.metric("Total Sales", "$23,450")

# Real-Time Operational Data Section
elif view == "Real-Time Operational Data":
    st.title("Monitor Store Performance in Real Time")
    st.subheader("Understand Key Metrics as They Happen")
    st.write("Simulated real-time data from autonomous checkout systems, including aisle traffic and sales performance.")
    time_filter = st.slider("Select Time Range (in Hours)", min_value=0, max_value=24, value=(8, 18))
    filtered_data = live_data[(live_data["Time"].dt.hour >= time_filter[0]) & 
                              (live_data["Time"].dt.hour <= time_filter[1])]
    st.dataframe(filtered_data)

# Store Traffic Heatmap Section
elif view == "Store Traffic Heatmap":
    st.title("Identify High-Traffic Areas with a Visual Heatmap")
    st.subheader("Optimize Store Layout and Staff Allocation")
    st.write("This heatmap provides insights into customer traffic patterns across the store, helping identify high-priority areas.")
    traffic = np.random.rand(10, 10) * 100  # Simulated traffic data
    fig = px.imshow(
        traffic, 
        color_continuous_scale="Viridis", 
        labels=dict(x="Aisle", y="Section", color="Traffic Level"),
        title="Simulated Store Traffic Heatmap",
    )
    fig.update_traces(hovertemplate="Aisle: %{x}<br>Section: %{y}<br>Traffic: %{z}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

# Sales and Trend Forecasting Section
elif view == "Sales and Trend Forecasting":
    st.title("Predict Future Sales and Trends")
    st.subheader("Plan Inventory and Promotions with Data-Backed Predictions")
    st.write("Leverage historical data to forecast sales trends and plan for future demand.")
    data["RollingAvg"] = data["PurchaseAmount"].rolling(5).mean()
    fig = px.line(
        data, 
        x="CustomerID", 
        y=["PurchaseAmount", "RollingAvg"],
        labels={"value": "Sales ($)", "CustomerID": "Customer ID"},
        title="Customer Purchase Trends and Predictions",
    )
    fig.update_traces(hovertemplate="Customer ID: %{x}<br>Sales Value: %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

# Customer Behavioral Insights Section
elif view == "Customer Behavioral Insights":
    st.title("Discover Customer Behavioral Patterns")
    st.subheader("Segment Customers to Drive Personalized Experiences")
    st.write("Analyze customer behavior to create actionable segments for targeted marketing and engagement.")
    features = data[["DwellTime", "PurchaseAmount", "VisitFrequency"]]
    kmeans = KMeans(n_clusters=3, random_state=42)
    data["Segment"] = kmeans.fit_predict(features)
    fig = px.scatter(
        data, 
        x="DwellTime", 
        y="PurchaseAmount", 
        color="Segment",
        size="VisitFrequency", 
        hover_data=["CustomerID", "VisitFrequency"],
        title="Customer Segments: Spending vs. Dwell Time",
    )
    fig.update_traces(hovertemplate="Customer ID: %{customdata[0]}<br>Dwell Time: %{x} min<br>Purchase Amount: $%{y}<br>Visits: %{customdata[1]} times<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

# Actionable Recommendations Section
elif view == "Actionable Recommendations":
    st.title("Actionable Insights to Drive Results")
    st.subheader("Maximize Efficiency and Customer Engagement")
    st.write("AI-driven recommendations help you make informed decisions about inventory, staffing, and promotions.")
    st.subheader("Inventory Optimization")
    st.write("- **Low-stock alert:** Restock beverages in Aisle A3 (current level: 10 units).")
    st.write("- **High demand prediction:** Increase stock of snacks for Aisle B1 (expected 20% increase).")
    st.subheader("Staff Allocation")
    st.write("- **Peak hours:** Assign additional staff between 4-6 PM in high-traffic areas.")
    st.subheader("Customer Engagement")
    st.write("- **Segment A:** Send 10% discount coupons via email.")
    st.write("- **Segment B:** Offer loyalty program rewards at checkout.")

# Custom Data Upload Section
elif view == "Custom Data Upload":
    st.title("Analyze Your Own Data with Custom Uploads")
    st.subheader("Upload and Visualize Shopper Data")
    st.write("Upload your own CSV file to analyze shopper behavior and generate actionable insights.")
    uploaded_file = st.file_uploader("Choose a CSV File")
    if uploaded_file:
        custom_data = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.write(custom_data.head())

# Downloadable Data
csv = data.to_csv(index=False)
st.sidebar.download_button(
    label="Download Shopper Data",
    data=csv,
    file_name="shopper_data.csv",
    mime="text/csv"
)
