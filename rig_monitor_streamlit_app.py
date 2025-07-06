import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="RigIQ Dashboard", layout="wide")

st.title("⚙️ RigIQ - AI-Powered Mining Rig Monitor")
st.markdown("Monitor your GPU rig in real-time with anomaly detection and profitability alerts.")

# Sidebar config
st.sidebar.header("Simulation Settings")
n_samples = st.sidebar.slider("Data Points", 50, 500, 200)
anomaly_contamination = st.sidebar.slider("Anomaly Sensitivity", 0.01, 0.2, 0.025)

# Simulate fake mining data
np.random.seed(42)
temperature = np.random.normal(loc=65, scale=5, size=n_samples)
fan_speed = np.random.normal(loc=70, scale=10, size=n_samples)
hash_rate = np.random.normal(loc=50, scale=3, size=n_samples)
for i in np.random.choice(range(n_samples), size=int(n_samples * 0.03), replace=False):
    temperature[i] += np.random.randint(15, 25)
    fan_speed[i] -= np.random.randint(10, 20)
    hash_rate[i] -= np.random.randint(10, 15)

df = pd.DataFrame({
    "Temperature (°C)": temperature,
    "Fan Speed (%)": fan_speed,
    "Hash Rate (MH/s)": hash_rate
})

# Anomaly Detection
model = IsolationForest(contamination=anomaly_contamination, random_state=42)
model.fit(df)
df["Anomaly"] = model.predict(df)

# Layout
col1, col2 = st.columns(2)
with col1:
    st.metric("Avg Temp (°C)", f"{df['Temperature (°C)'].mean():.1f}")
    st.metric("Avg Hash Rate (MH/s)", f"{df['Hash Rate (MH/s)'].mean():.2f}")
with col2:
    st.metric("Detected Anomalies", f"{(df['Anomaly'] == -1).sum()}")

# Display Data
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Plotting
fig, ax = plt.subplots(figsize=(10, 4))
colors = df["Anomaly"].map({1: "green", -1: "red"})
ax.scatter(df.index, df["Hash Rate (MH/s)"], c=colors)
ax.axhline(y=df["Hash Rate (MH/s)"].mean(), color="blue", linestyle="--", label="Average")
ax.set_title("Hash Rate Anomaly Detection")
ax.set_xlabel("Sample")
ax.set_ylabel("Hash Rate (MH/s)")
ax.legend()
st.pyplot(fig)

st.success("This is a simulated preview. Real-time GPU monitoring would require integration with mining software.")
