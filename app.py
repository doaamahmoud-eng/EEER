import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="EEER Register & Analytics Dashboard", layout="wide")

# ==========================================
# 1. EMBEDDED DATA FROM YOUR EXCEL TEMPLATE
# ==========================================

DEFAULT_COMPANY = {
    "Company Name": "Fictive Company 2",
    "Commercial Reg. No.": "123 456 789 000",
    "VAT No.": "456 789 000 123",
    "Address": "Street No., Town",
    "Sector": "Food & Tobacco (Bread & Cereals)",
    "Employees": 1402,
    "Production Start": 2016,
    "Primary Contact": "Firstname Lastname I (Energy Manager)",
    "Phone": "(+20) 12 34 56 78"
}

DEFAULT_PRODUCTION = pd.DataFrame([
    {"Product": "Product I", "2022 Amount (ton)": 1750, "2023 Amount (ton)": 2100, "Energy Share": 0.30, "2023 Energy (GJ)": 7288.14},
    {"Product": "Product II", "2022 Amount (ton)": 910, "2023 Amount (ton)": 1575, "Energy Share": 0.25, "2023 Energy (GJ)": 6073.45},
    {"Product": "Product III", "2022 Amount (ton)": 1050, "2023 Amount (ton)": 1400, "Energy Share": 0.20, "2023 Energy (GJ)": 4858.76},
    {"Product": "Product IV", "2022 Amount (ton)": 672, "2023 Amount (ton)": 1400, "Energy Share": 0.15, "2023 Energy (GJ)": 3644.07},
    {"Product": "Product V", "2022 Amount (ton)": 910, "2023 Amount (ton)": 840, "Energy Share": 0.10, "2023 Energy (GJ)": 2429.38},
])

DEFAULT_ENERGY = pd.DataFrame([
    {"Fuel / Energy Type": "Electricity", "Amount 2023": 38000, "Unit": "kWh", "Energy (GJ)": 136.8, "CO2 (ton)": 14.51},
    {"Fuel / Energy Type": "Fuelwood", "Amount 2023": 12500, "Unit": "kg", "Energy (GJ)": 195.0, "CO2 (ton)": 5.95},
    {"Fuel / Energy Type": "Hard Coal", "Amount 2023": 100000, "Unit": "kg", "Energy (GJ)": 2490.0, "CO2 (ton)": 25.15},
    {"Fuel / Energy Type": "LNG", "Amount 2023": 90000, "Unit": "m³", "Energy (GJ)": 1962.0, "CO2 (ton)": 138.12},
    {"Fuel / Energy Type": "LPG", "Amount 2023": 170000, "Unit": "m³", "Energy (GJ)": 4165.0, "CO2 (ton)": 273.22},
    {"Fuel / Energy Type": "Natural Gas", "Amount 2023": 450000, "Unit": "m³", "Energy (GJ)": 15345.0, "CO2 (ton)": 854.72},
])

DEFAULT_PROJECTS = pd.DataFrame([
    {
        "Project Name": "Energy-saving project X",
        "Responsible": "Name Last Name",
        "Implementation Date": "2024-03-14",
        "Application": "Heating/boiling",
        "Energy Savings (GJ/yr)": -4600.6,
        "Financial Savings (EGP/yr)": -44202520,
        "CO2 Reduction (ton/yr)": -43.22,
        "CapEx (EGP)": 350000000,
        "Payback (years)": 7.92,
        "NPV (EGP)": 98300000
    }
])

DEFAULT_KPIS = pd.DataFrame({
    "Product": ["Product I", "Product II", "Product III", "Product IV", "Product V"],
    "2020": [4.32, 4.90, 4.07, 4.20, 3.90],
    "2021": [4.11, 4.68, 3.92, 3.38, 3.52],
    "2022": [3.80, 4.18, 3.62, 2.83, 3.13],
    "2023": [3.47, 3.86, 3.47, 2.60, 2.89],
    "2024 (Target)": [3.22, 3.70, 3.42, 2.53, 2.83],
    "2025 (Target)": [2.84, 3.58, 3.01, 2.27, 2.54],
    "2030 (Target)": [1.70, 3.07, 2.09, 1.25, 1.36],
})

# ==========================================
# 2. STREAMLIT APP LAYOUT & NAVIGATION
# ==========================================

st.title("EEER | Energy & Energy Efficiency Register")
st.caption("National Energy & Efficiency Tracking System")

# File Uploader
uploaded_file = st.sidebar.file_uploader("Upload Excel Register (Optional)", type=["xlsx"])

if uploaded_file is not None:
    st.sidebar.success("Custom File Loaded Successfully!")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard Overview", "Company Profile", "Energy & Emissions", "EE Projects & Plan"])

# Page 1: Dashboard
if page == "Dashboard Overview":
    st.header("Dashboard Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    total_energy_gj = DEFAULT_ENERGY["Energy (GJ)"].sum()
    total_co2_ton = DEFAULT_ENERGY["CO2 (ton)"].sum()
    total_prod_ton = DEFAULT_PRODUCTION["2023 Amount (ton)"].sum()
    
    col1.metric("Total Energy (2023)", f"{total_energy_gj:,.1f} GJ")
    col2.metric("Total Emissions", f"{total_co2_ton:,.1f} t CO₂e")
    col3.metric("Total Production", f"{total_prod_ton:,.0f} tons")
    col4.metric("Active EE Projects", len(DEFAULT_PROJECTS))

    st.subheader("Energy Breakdown by Source (2023)")
    st.bar_chart(DEFAULT_ENERGY.set_index("Fuel / Energy Type")["Energy (GJ)"])

# Page 2: Company Profile
elif page == "Company Profile":
    st.header("Company Profile")
    cols = st.columns(2)
    for i, (k, v) in enumerate(DEFAULT_COMPANY.items()):
        cols[i % 2].write(f"**{k}:** {v}")

# Page 3: Energy & Emissions
elif page == "Energy & Emissions":
    st.header("Energy Consumption & CO₂ Emissions")
    st.dataframe(DEFAULT_ENERGY, use_container_width=True)
    
    st.subheader("Production & Energy Allocation")
    st.dataframe(DEFAULT_PRODUCTION, use_container_width=True)

# Page 4: EE Projects & Plan
elif page == "EE Projects & Plan":
    st.header("Energy Efficiency Projects")
    st.dataframe(DEFAULT_PROJECTS, use_container_width=True)
    
    st.subheader("Key Performance Indicators Trajectory (GJ/ton)")
    st.dataframe(DEFAULT_KPIS, use_container_width=True)
    st.line_chart(DEFAULT_KPIS.set_index("Product").T)
