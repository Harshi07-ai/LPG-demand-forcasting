import streamlit as st
import numpy as np
import joblib
from datetime import datetime
import pandas as pd

# ================= LOAD MODEL =================
model = joblib.load("lpg_model.pkl")

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="LPG Demand Dashboard",
    page_icon="🔥",
    layout="wide"
)

# ================= HEADER =================
st.title("🔥 LPG Demand Forecasting Dashboard")
st.markdown("### AI-Powered Inventory & Demand Analytics System")
st.markdown("---")

# ================= SIDEBAR =================
st.sidebar.header("📌 Input Controls")

stock = st.sidebar.number_input(
    "Stock Available",
    min_value=0,
    value=5000
)

deliveries = st.sidebar.number_input(
    "Deliveries",
    min_value=0,
    value=1000
)

temperature = st.sidebar.number_input(
    "Temperature (°C)",
    value=30
)

st.sidebar.markdown("---")
st.sidebar.info(
    f"🕒 {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

# ================= KPI METRICS =================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📦 Stock Available", stock)

with col2:
    st.metric("🚚 Deliveries", deliveries)

with col3:
    st.metric("🌡 Temperature", f"{temperature} °C")

st.markdown("---")

# ================= PREDICTION =================
if st.button("🚀 Predict Demand"):

    try:
        features = np.array([[stock, deliveries, temperature]])

        prediction = model.predict(features)
        predicted_demand = float(prediction[0])

        reorder_qty = max(0, round(predicted_demand - stock))

        status = (
            "⚠ Reorder Required"
            if stock < predicted_demand
            else "✅ Stock Sufficient"
        )

        # ================= RESULTS =================
        st.subheader("📊 Prediction Results")

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric("Predicted Demand", round(predicted_demand, 2))

        with r2:
            st.metric("Inventory Status", status)

        with r3:
            st.metric("Reorder Quantity", reorder_qty)

        # ================= INVENTORY HEALTH =================
        st.subheader("📦 Inventory Health")

        stock_percentage = min(
            int((stock / max(predicted_demand, 1)) * 100),
            100
        )

        st.progress(stock_percentage)

        st.write(
            f"Inventory Utilization: **{stock_percentage}%**"
        )

        # ================= BAR CHART =================
        st.subheader("📈 Dashboard Analytics View")

        data = pd.DataFrame({
            "Values": [
                stock,
                deliveries,
                predicted_demand
            ]
        },
        index=[
            "Stock",
            "Deliveries",
            "Predicted Demand"
        ])

        st.bar_chart(data)

        # ================= SUMMARY =================
        st.subheader("📄 Summary Report")

        summary = pd.DataFrame({
            "Parameter": [
                "Stock Available",
                "Deliveries",
                "Temperature",
                "Predicted Demand",
                "Status",
                "Reorder Quantity"
            ],
            "Value": [
                stock,
                deliveries,
                f"{temperature} °C",
                round(predicted_demand, 2),
                status,
                reorder_qty
            ]
        })

        st.table(summary)

    except Exception as e:
        st.error(f"Error: {e}")

# ================= FOOTER =================
st.markdown("---")
st.caption(
    "🔥 AI-Based LPG Demand Forecasting & Inventory Management Dashboard"
)
