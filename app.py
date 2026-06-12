import streamlit as st
import numpy as np
import pandas as pd
import joblib
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI-Based LPG Demand Forecasting ",
    page_icon="🔥",
    layout="wide"
)

# ================= LOAD MODEL =================
try:
    model = joblib.load("lpg_model.pkl")
except Exception as e:
    st.error(f"Model Loading Error: {e}")
    st.stop()

# ================= HEADER =================
st.title("AI-Based LPG Demand Forecasting and Inventory Management System Using Machine Learning")
st.markdown("### AI-Based LPG Demand Prediction Dashboard")
st.markdown("---")

# ================= SIDEBAR =================
st.sidebar.header("📌 Input Parameters")

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

# ================= KPI CARDS =================
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

        reorder_qty = max(
            0,
            round(predicted_demand - stock)
        )

        status = (
            "⚠ Reorder Required"
            if stock < predicted_demand
            else "✅ Stock Sufficient"
        )

        # ================= RESULTS =================
        st.subheader("📊 Prediction Results")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Predicted Demand",
                round(predicted_demand, 2)
            )

        with c2:
            st.metric(
                "Inventory Status",
                status
            )

        with c3:
            st.metric(
                "Reorder Quantity",
                reorder_qty
            )

        st.markdown("---")

        # ================= INVENTORY HEALTH =================
        st.subheader("📦 Inventory Health")

        inventory_percentage = min(
            int((stock / max(predicted_demand, 1)) * 100),
            100
        )

        st.progress(inventory_percentage)

        st.write(
            f"Inventory Utilization: {inventory_percentage}%"
        )

        st.markdown("---")

        # ================= BAR CHART =================
        st.subheader("📈 Dashboard Analytics")

        chart_data = pd.DataFrame(
            {
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
            ]
        )

        st.bar_chart(chart_data)

        st.markdown("---")

        # ================= SUMMARY =================
        st.subheader("📄 Summary Report")

        summary = pd.DataFrame({
            "Parameter": [
                "Stock Available",
                "Deliveries",
                "Temperature",
                "Predicted Demand",
                "Inventory Status",
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
        st.error(f"Prediction Error: {e}")

# ================= FOOTER =================
st.markdown("---")
st.caption("🔥 LPG Demand Forecasting Dashboard")
