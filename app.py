import streamlit as st
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI-Based LPG Demand Forecasting ",
    page_icon="🔥",
    layout="wide"
)

# ================= LOAD MODEL =================
model = joblib.load("lpg_model.pkl")

# ================= HEADER =================
st.title("🔥 AI-Based LPG Demand Forecasting and Inventory Management System Using Machine Learning")
st.markdown("### Smart Inventory Analytics & Demand Prediction Dashboard")
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
            st.metric(
                "Predicted Demand",
                round(predicted_demand, 2)
            )

        with r2:
            st.metric(
                "Inventory Status",
                status
            )

        with r3:
            st.metric(
                "Reorder Quantity",
                reorder_qty
            )

        st.markdown("---")

        # ================= INVENTORY HEALTH =================
        st.subheader("📦 Inventory Health")

        stock_percentage = min(
            int((stock / max(predicted_demand, 1)) * 100),
            100
        )

        st.progress(stock_percentage)

        st.write(
            f"Inventory Utilization: {stock_percentage}%"
        )

        # ================= DATA =================
        chart_data = pd.DataFrame({
            "Category": [
                "Stock",
                "Deliveries",
                "Predicted Demand"
            ],
            "Value": [
                stock,
                deliveries,
                predicted_demand
            ]
        })

        # ================= BAR CHART =================
        st.subheader("📊 Bar Chart")

        bar_data = chart_data.set_index("Category")
        st.bar_chart(bar_data)

        # ================= LINE CHART =================
        st.subheader("📈 Line Chart")

        line_data = pd.DataFrame({
            "Values": [
                stock,
                deliveries,
                predicted_demand
            ]
        },
        index=[
            "Stock",
            "Deliveries",
            "Demand"
        ])

        st.line_chart(line_data)

        # ================= PIE CHART =================
        st.subheader("🥧 Pie Chart")

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            chart_data["Value"],
            labels=chart_data["Category"],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            "Stock vs Deliveries vs Predicted Demand"
        )

        st.pyplot(fig)

        # ================= SUMMARY REPORT =================
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
        st.error(f"Error: {e}")

# ================= FOOTER =================
st.markdown("---")
st.caption(
    "AI-Based LPG Demand Forecasting and Inventory Management System Using Machine Learning"
)
