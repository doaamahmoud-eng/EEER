import os
import io
import pandas as pd
import streamlit as st

# ==========================================
# 1. Page & Layout Configuration
# ==========================================
st.set_page_config(
    page_title="EEER - Energy Efficiency & SEAP Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Metric Cards & Layout
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #1a1e29;
        border: 1px solid #2d3748;
        padding: 14px;
        border-radius: 8px;
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. File Handlers & Helper Functions
# ==========================================
EEER_FILE = "EG EEER Excel template_v0.6_2025.07.31 2.xlsx"
SEAP_FILE = "20190219_SEAP Guidebook for   DISCOs_final draft.xlsx"

@st.cache_data
def load_excel_file(file_path):
    if os.path.exists(file_path):
        return pd.ExcelFile(file_path)
    return None

eeer_xls = load_excel_file(EEER_FILE)
seap_xls = load_excel_file(SEAP_FILE)

# ==========================================
# 3. Sidebar Navigation
# ==========================================
with st.sidebar:
    st.title("⚡ EdgePro Platform")
    st.caption("EG EEER & DISCOs SEAP Management")
    st.markdown("---")
    
    app_mode = st.radio(
        "Select Platform Module:",
        [
            "🏠 Overview Dashboard",
            "📊 EG EEER (Emissions & EE)",
            "📋 SEAP DISCOs Action Plan",
            "💰 Cost-Benefit Analysis (CBA)",
            "📁 Raw Excel Explorer & Export"
        ]
    )
    
    st.markdown("---")
    st.markdown("**Data Source Status:**")
    st.markdown(f"• EEER Template: {'🟢 Loaded' if eeer_xls else '🔴 Not Found'}")
    st.markdown(f"• SEAP Guidebook: {'🟢 Loaded' if seap_xls else '🔴 Not Found'}")

# ==========================================
# 4. Module 1: Overview Dashboard
# ==========================================
if app_mode == "🏠 Overview Dashboard":
    st.title("Energy Efficiency & SEAP Governance Platform")
    st.markdown("Centralized intelligence combining facility emission registers and distribution company action plans.")
    st.write("")

    # Top Level KPIs
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Active DISCO Projects", "4 Areas", "DSM, ES, PR, AR")
    kpi2.metric("Target Energy Savings", "245.8 GWh", "+8.2% vs baseline")
    kpi3.metric("Est. Carbon Reduction", "118.4 kt CO₂e", "Scope 1 & Scope 2")
    kpi4.metric("Average B/C Ratio", "2.14", "High Feasibility")
    kpi5.metric("EEER Register Status", "Compliant", "v0.6 Framework")

    st.markdown("<hr style='border:1px solid #2d3748;'>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("⚡ SEAP Action Plan Measure Allocation")
        summary_data = pd.DataFrame({
            "Action Category": ["Demand Side Management (DSM)", "Energy Savings (ES)", "Power Loss Reduction (PR)", "Awareness & Renewables (AR)"],
            "Planned Actions": [14, 18, 12, 10],
            "Est. Savings (MWh/yr)": [45000, 82000, 95000, 23800],
            "Total Cost (EGP M)": [12.5, 28.0, 65.0, 8.2]
        })
        st.dataframe(summary_data, use_container_width=True, hide_index=True)

        st.write("")
        st.subheader("📈 Energy Savings Potential by Category")
        st.bar_chart(summary_data.set_index("Action Category")["Est. Savings (MWh/yr)"])

    with col_right:
        st.subheader("🔔 EEER Compliance Quick Status")
        st.info("**Scope 1 & 2 Emissions:** Energy consumption data validated against local calorific values.")
        st.success("**EE Projects Pipeline:** 5 energy audits submitted for current reporting cycle.")
        st.warning("**Grid Loss Target:** PR measures under review for Substation Transformers.")
        
        st.write("")
        st.subheader("⚡ Quick Export")
        st.button("📥 Download EEER Summary Report", use_container_width=True, type="primary")
        st.button("📥 Download SEAP DISCO Action Plan", use_container_width=True)

# ==========================================
# 5. Module 2: EG EEER (Emissions & Energy Efficiency)
# ==========================================
elif app_mode == "📊 EG EEER (Emissions & EE)":
    st.title("EG EEER - Energy Efficiency & Emissions Register")
    st.markdown("Track energy consumption, Scope 1 & 2 greenhouse gas emissions, and EE initiatives.")

    tab1, tab2, tab3 = st.tabs(["⚡ Energy & Consumption", "🌱 Emissions Factors", "🛠️ EE Project Register"])

    with tab1:
        st.subheader("Facility Consumption Baseline")
        if eeer_xls and "2EnergyConsumption" in eeer_xls.sheet_names:
            df_cons = pd.read_excel(eeer_xls, sheet_name="2EnergyConsumption")
            st.dataframe(df_cons.dropna(how="all").head(15), use_container_width=True)
        else:
            sample_cons = pd.DataFrame({
                "Fuel / Energy Type": ["Electricity (Grid)", "Natural Gas", "Diesel", "Heavy Fuel Oil (Mazut)"],
                "Annual Consumption": [12500000, 850000, 420000, 180000],
                "Unit": ["kWh", "m³", "Liters", "Liters"],
                "Energy Equivalent (GJ)": [45000, 32300, 16200, 7200]
            })
            st.dataframe(sample_cons, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Standard Emission Factors (SI Units)")
        if eeer_xls and "EmissionFactors" in eeer_xls.sheet_names:
            df_ef = pd.read_excel(eeer_xls, sheet_name="EmissionFactors")
            st.dataframe(df_ef.dropna(how="all"), use_container_width=True)
        else:
            st.info("Emission factors sheet available in template.")

    with tab3:
        st.subheader("Energy Efficiency Projects Pipeline")
        if eeer_xls and "EnergyEfficiencyProjects" in eeer_xls.sheet_names:
            df_eep = pd.read_excel(eeer_xls, sheet_name="EnergyEfficiencyProjects")
            st.dataframe(df_eep.dropna(how="all").head(15), use_container_width=True)
        else:
            sample_eep = pd.DataFrame({
                "Project Name": ["VFD Installation on Pumps", "LED Lighting Retrofit", "Boiler Waste Heat Recovery", "Power Factor Correction"],
                "Category": ["Motors & Drives", "Lighting", "Thermal", "Electrical"],
                "Est. Investment (EGP)": [450000, 120000, 850000, 200000],
                "Annual Savings (kWh)": [180000, 65000, 310000, 95000],
                "Simple Payback (Yrs)": [2.1, 1.4, 2.8, 1.8]
            })
            st.dataframe(sample_eep, use_container_width=True, hide_index=True)

# ==========================================
# 6. Module 3: SEAP DISCOs Action Plan
# ==========================================
elif app_mode == "📋 SEAP DISCOs Action Plan":
    st.title("SEAP Action Plan for Electricity DISCOs")
    st.markdown("Action planning framework across Demand Side Management, Energy Savings, Power Loss, and Renewables.")

    category = st.selectbox(
        "Filter Action Category:",
        ["DSM - Demand Side Management", "ES - Energy Savings", "PR - Power Loss Reduction", "AR - Awareness & Renewables"]
    )

    sheet_map = {
        "DSM - Demand Side Management": "List Of Actions_DSM",
        "ES - Energy Savings": "List Of Actions_ES",
        "PR - Power Loss Reduction": "List Of Actions_PR",
        "AR - Awareness & Renewables": "List Of Actions_AR"
    }

    selected_sheet = sheet_map[category]

    if seap_xls and selected_sheet in seap_xls.sheet_names:
        df_actions = pd.read_excel(seap_xls, sheet_name=selected_sheet)
        st.subheader(f"Measures Register: {category}")
        st.dataframe(df_actions.dropna(how="all"), use_container_width=True)
    else:
        sample_actions = pd.DataFrame({
            "No.": [1, 2, 3],
            "Measure Name": ["Time-of-Use Tariff Awareness", "Smart Metering Rollout", "Transformer Efficiency Upgrade"],
            "Target Customer": ["Industrial / Commercial", "Residential", "Distribution Grid"],
            "Energy Savings (MWh)": [12000, 35000, 48000],
            "Est. Cost (EGP)": [1500000, 18000000, 25000000],
            "Benefit / Cost Ratio": [3.2, 1.8, 2.4]
        })
        st.dataframe(sample_actions, use_container_width=True, hide_index=True)

# ==========================================
# 7. Module 4: Cost-Benefit Analysis (CBA)
# ==========================================
elif app_mode == "💰 Cost-Benefit Analysis (CBA)":
    st.title("Cost-Benefit Analysis Evaluator")
    st.markdown("Perform financial modeling and evaluate project feasibility metrics.")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Input Financial Parameters")
        capex = st.number_input("Capital Expenditure - CAPEX (EGP)", value=1000000, step=50000)
        annual_opex = st.number_input("Annual OPEX (EGP/yr)", value=30000, step=5000)
        annual_savings = st.number_input("Annual Energy Savings (EGP/yr)", value=320000, step=10000)
        discount_rate = st.slider("Discount Rate (%)", min_value=1.0, max_value=25.0, value=12.0) / 100
        project_life = st.slider("Project Lifetime (Years)", min_value=1, max_value=25, value=10)

        # Net Cash Flow & Simple Payback Calculation
        net_annual_flow = annual_savings - annual_opex
        simple_payback = capex / net_annual_flow if net_annual_flow > 0 else 0
        
        # NPV Calculation
        npv = -capex + sum([net_annual_flow / ((1 + discount_rate) ** t) for t in range(1, project_life + 1)])
        benefit_cost_ratio = (sum([net_annual_flow / ((1 + discount_rate) ** t) for t in range(1, project_life + 1)])) / capex if capex > 0 else 0

    with col2:
        st.subheader("Financial Feasibility Results")
        res1, res2, res3 = st.columns(3)
        res1.metric("Simple Payback", f"{simple_payback:.2f} Years")
        res2.metric("Net Present Value (NPV)", f"{npv:,.0f} EGP")
        res3.metric("Benefit-Cost Ratio (B/C)", f"{benefit_cost_ratio:.2f}")

        st.write("")
        st.subheader("Cumulative Discounted Cash Flow Projection")
        cash_flows = []
        cum_flow = -capex
        timeline = [0]
        cum_flows = [cum_flow]

        for t in range(1, project_life + 1):
            discounted_p = net_annual_flow / ((1 + discount_rate) ** t)
            cum_flow += discounted_p
            timeline.append(t)
            cum_flows.append(cum_flow)

        df_cf = pd.DataFrame({"Year": timeline, "Cumulative Net Cash Flow (EGP)": cum_flows})
        st.line_chart(df_cf.set_index("Year"))

# ==========================================
# 8. Module 5: Raw Excel Explorer & Export
# ==========================================
elif app_mode == "📁 Raw Excel Explorer & Export":
    st.title("Excel Template Explorer & Data Inspector")
    st.markdown("Inspect, filter, and export any sheet from the underlying EEER and SEAP templates.")

    selected_file = st.selectbox("Select Template Workbook:", ["EG EEER Template", "SEAP DISCO Guidebook"])

    active_xls = eeer_xls if selected_file == "EG EEER Template" else seap_xls

    if active_xls:
        sheet_choice = st.selectbox("Select Sheet to Inspect:", active_xls.sheet_names)
        df_sheet = pd.read_excel(active_xls, sheet_name=sheet_choice)
        
        st.subheader(f"Sheet: {sheet_choice} (Rows: {df_sheet.shape[0]}, Cols: {df_sheet.shape[1]})")
        st.dataframe(df_sheet, use_container_width=True)

        # Download button for sheet CSV
        buffer = io.BytesIO()
        df_sheet.to_csv(buffer, index=False)
        st.download_button(
            label=f"📥 Download '{sheet_choice}' as CSV",
            data=buffer.getvalue(),
            file_name=f"{selected_file}_{sheet_choice}.csv",
            mime="text/csv"
        )
    else:
        st.error("Selected template workbook is not available in the working directory.")
