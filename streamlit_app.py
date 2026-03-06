import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Bengaluru Gig Worker Fairness Simulator")

st.write("Simulate how fairness adjustments affect gig worker income and platform performance.")

# Sidebar controls
st.sidebar.header("Simulation Controls")

fairness_weight = st.sidebar.slider(
    "Fairness Weight",
    min_value=0.0,
    max_value=0.5,
    value=0.1,
    step=0.01
)

uploaded_file = st.sidebar.file_uploader("Upload Order Dataset (CSV)")

zones = ["Indiranagar","Koramangala","Whitefield","Electronic City","BTM Layout"]
selected_zone = st.sidebar.selectbox("Select Zone", zones)

run_simulation = st.sidebar.button("Run Simulation")

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(data.head())

    if run_simulation:

        st.subheader("Running Simulation...")

        # Simulated fairness adjustment
        data["equity_score"] = 1 / (data["driver_earnings"] + 1)

        data["dispatch_score"] = (
            (1 - fairness_weight) * data["delivery_time"]
            + fairness_weight * data["equity_score"]
        )

        avg_income = data["driver_earnings"].mean()
        income_variance = data["driver_earnings"].var()

        avg_delivery_time = data["delivery_time"].mean()

        revenue = data["order_value"].sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("Average Driver Income", round(avg_income,2))
        col2.metric("Income Variance", round(income_variance,2))
        col3.metric("Avg Delivery Time", round(avg_delivery_time,2))

        st.metric("Total Platform Revenue", round(revenue,2))

        st.subheader("Income Distribution")

        fig, ax = plt.subplots()
        ax.hist(data["driver_earnings"], bins=20)
        ax.set_xlabel("Driver Earnings")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

        st.subheader("Delivery Time Distribution")

        fig2, ax2 = plt.subplots()
        ax2.hist(data["delivery_time"], bins=20)

        st.pyplot(fig2)
