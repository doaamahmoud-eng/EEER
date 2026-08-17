import datetime
import io
import os
import pandas as pd
import streamlit as st

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="EEER - Energy & Energy Efficiency Register",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #111827;
        border: 1px solid #374151;
        padding: 15px;
        border-radius: 8px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. File Loading & Caching
# ==========================================
EEER_FILE = "EG EEER Excel template_v0.6_2025.07.31 2.xlsx"

@st.cache_data
def get_eeer_excel():
    if os.path.exists(EEER_FILE):
        return pd.ExcelFile(EEER_FILE)
    return None

eeer_xls = get_eeer_excel()

# ==========================================
# 3. Sidebar Navigation
# ==========================================
with st.sidebar:
    st.title("⚡ EEER Platform")
    st.caption("Energy & Energy Efficiency Register (v0.6)")
    st.markdown("---")
    
    navigation = st.radio(
        "EEER Modules:",
        [
            "🏠 EEER Executive Dashboard",
            "🏢 Company Profile & Audits",
            "🏭 Production & Energy Consumption",
            "🌱 GHG Emissions & Reference Factors",
            "💡 Energy Efficiency Projects & Plan",
            "📊 Self-Assessment & Benchmarking",
            "📁 Raw EEER Register Inspector"
        ]
    )
    
    st.markdown("---")
    st.markdown(f"**Register File:** {'🟢 Connected' if eeer_xls else '⚠️ Using Demo Baseline'}")

# ==========================================
# 4. Module 1: Executive Dashboard
# ==========================================
if navigation == "🏠 EEER Executive Dashboard":
    st.title("EEER Executive Overview Dashboard")
    st.markdown("National Energy & Energy Efficiency Reporting & Compliance Summary.")
    st.write("")

    # Top Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Reporting Entity", "Fictive Company 2", "EEER Registered")
    col2.metric("Total Consumption", "93,700 GJ", "-3.8% YoY")
    col3.metric("Specific Energy (SEC)", "3.80 GJ/ton", "Target: 3.50")
    col4.metric("Scope 1 & 2 Emissions", "8,420 tCO₂e", "Validated")
    col5.metric("Active EE Projects", "4 Projects", "EGP 1.62M Investment")

    st.markdown("<hr style='border:1px solid #374151;'>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("⚡ Annual Energy Consumption Breakdown (GJ)")
        energy_data = pd.DataFrame({
            "Energy Stream": ["Grid Electricity", "Natural Gas", "Diesel Fuel", "Heavy Fuel Oil (Mazut)"],
            "Consumption (GJ)": [45000, 32300, 11200, 5200],
            "Share (%)": ["48.0%", "34.5%", "12.0%", "5.5%"]
        })
        st.dataframe(energy_data, use_container_width=True, hide_index=True)
        st.bar_chart(energy_data.set_index("Energy Stream")["Consumption (GJ)"])

    with col_right:
        st.subheader("📋 EEER Submission Checklist")
        st.success("✅ **Company Profile:** Complete")
        st.success("✅ **Production Details:** 2023 Validated")
        st.success("✅ **Energy Consumption:** Verified")
        st.warning("⚡ **Other Emissions:** Refrigerants update pending")
        st.info("ℹ️ **Submit Report:** Ready for final filing")

# ==========================================
# 5. Module 2: Company Profile & Audits
# ==========================================
elif navigation == "🏢 Company Profile & Audits":
    st.title("Company Profile & Energy Audits")
    st.markdown("General facility information, ISIC sector classification, and audit log.")

    if eeer_xls and "Company" in eeer_xls.sheet_names:
        df_comp = pd.read_excel(eeer_xls, sheet_name="Company")
        st.subheader("Registered Entity Information")
        st.dataframe(df_comp.dropna(how="all"), use_container_width=True)
    else:
        st.info("Company profile details loaded.")

    st.write("")
    st.subheader("Energy Audit History")
    if eeer_xls and "Audits" in eeer_xls.sheet_names:
        df_audits = pd.read_excel(eeer_xls, sheet_name="Audits")
        st.dataframe(df_audits.dropna(how="all"), use_container_width=True)

# ==========================================
# 6. Module 3: Production & Energy Consumption
# ==========================================
elif navigation == "🏭 Production & Energy Consumption":
    st.title("Production Details & Energy Consumption")
    st.markdown("Track yearly production output, energy purchases, and specific energy consumption per product.")

    tab1, tab2 = st.tabs(["1 Production Details", "2 Energy Consumption"])

    with tab1:
        st.subheader("Main Production Output")
        if eeer_xls and "1ProductionDetails" in eeer_xls.sheet_names:
            df_prod = pd.read_excel(eeer_xls, sheet_name="1ProductionDetails")
            st.dataframe(df_prod.dropna(how="all"), use_container_width=True)

    with tab2:
        st.subheader("Purchased Energy & Fuel Sources")
        if eeer_xls and "2EnergyConsumption" in eeer_xls.sheet_names:
            df_cons = pd.read_excel(eeer_xls, sheet_name="2EnergyConsumption")
            st.dataframe(df_cons.dropna(how="all"), use_container_width=True)

# ==========================================
# 7. Module 4: GHG Emissions & Reference Factors
# ==========================================
elif navigation == "🌱 GHG Emissions & Reference Factors":
    st.title("GHG Emissions & Reference Tables")
    st.markdown("Scope 1 & 2 emissions tracking alongside official national emission factors and calorific values.")

    tab1, tab2, tab3 = st.tabs(["3 Other Emissions", "Emission Factors", "Calorific Values"])

    with tab1:
        st.subheader("Fugitive & Other Emissions (Refrigerants)")
        if eeer_xls and "3OtherEmissions" in eeer_xls.sheet_names:
            df_oth = pd.read_excel(eeer_xls, sheet_name="3OtherEmissions")
            st.dataframe(df_oth.dropna(how="all"), use_container_width=True)

    with tab2:
        st.subheader("National Carbon Emission Factors")
        if eeer_xls and "EmissionFactors" in eeer_xls.sheet_names:
            df_ef = pd.read_excel(eeer_xls, sheet_name="EmissionFactors")
            st.dataframe(df_ef.dropna(how="all"), use_container_width=True)

    with tab3:
        st.subheader("Local & Global Calorific Values")
        if eeer_xls and "LocalCalorificValues " in eeer_xls.sheet_names:
            df_lcv = pd.read_excel(eeer_xls, sheet_name="LocalCalorificValues ")
            st.dataframe(df_lcv.dropna(how="all"), use_container_width=True)

# ==========================================
# 8. Module 5: Energy Efficiency Projects & Plan
# ==========================================
elif navigation == "💡 Energy Efficiency Projects & Plan":
    st.title("Energy Efficiency Projects & Action Plan")
    st.markdown("Manage energy saving projects, investment requirements, simple payback, and future KPI goals.")

    tab1, tab2 = st.tabs(["Energy Efficiency Projects", "Energy Efficiency Plan"])

    with tab1:
        st.subheader("Registered EE Projects")
        if eeer_xls and "EnergyEfficiencyProjects" in eeer_xls.sheet_names:
            df_eep = pd.read_excel(eeer_xls, sheet_name="EnergyEfficiencyProjects")
            st.dataframe(df_eep.dropna(how="all"), use_container_width=True)

    with tab2:
        st.subheader("Specific Energy Consumption Target Goals (SEC)")
        if eeer_xls and "EnergyEfficiencyPlan" in eeer_xls.sheet_names:
            df_plan = pd.read_excel(eeer_xls, sheet_name="EnergyEfficiencyPlan")
            st.dataframe(df_plan.dropna(how="all"), use_container_width=True)

# ==========================================
# 9. Module 6: Self-Assessment & Benchmarking
# ==========================================
elif navigation == "📊 Self-Assessment & Benchmarking":
    st.title("Self-Assessment & Sector Benchmarking")
    st.markdown("Compare energy performance indicators against national, regional, or global industry benchmarks.")

    if eeer_xls and "SelfAssessment" in eeer_xls.sheet_names:
        df_sa = pd.read_excel(eeer_xls, sheet_name="SelfAssessment")
        st.dataframe(df_sa.dropna(how="all"), use_container_width=True)

# ==========================================
# 10. Module 7: Raw EEER Register Inspector
# ==========================================
elif navigation == "📁 Raw EEER Register Inspector":
    st.title("EEER Template Sheet Inspector & Data Exporter")
    st.markdown("Inspect or export any individual worksheet directly from the `EG EEER` template.")

    if eeer_xls:
        selected_sheet = st.selectbox("Select EEER Sheet:", eeer_xls.sheet_names)
        df_selected = pd.read_excel(eeer_xls, sheet_name=selected_sheet)
        
        st.subheader(f"Sheet: {selected_sheet}")
        st.dataframe(df_selected, use_container_width=True)

        buffer = io.BytesIO()
        df_selected.to_csv(buffer, index=False)
        st.download_button(
            label=f"📥 Download '{selected_sheet}' CSV",
            data=buffer.getvalue(),
            file_name=f"EEER_{selected_sheet}.csv",
            mime="text/csv"
        )
    else:
        st.error(f"Template file '{EEER_FILE}' was not found in the root directory.")
