import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os

TELEGRAM_TOKEN = "your_bot_token_here"
CHAT_ID = "your_chat_id_here"

def simulate_mining_data(samples=1000):
    np.random.seed(42)
    temperature = np.random.normal(loc=65, scale=5, size=samples)
    fan_speed = np.random.normal(loc=70, scale=10, size=samples)
    hash_rate = np.random.normal(loc=50, scale=3, size=samples)
    for i in np.random.choice(range(samples), size=int(samples * 0.01), replace=False):
        temperature[i] += np.random.randint(15, 25)
        fan_speed[i] -= np.random.randint(10, 20)
        hash_rate[i] -= np.random.randint(10, 15)
    return pd.DataFrame({
        "temperature": temperature,
        "fan_speed": fan_speed,
        "hash_rate": hash_rate
    })

def train_model(data):
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(data)
    return model

def detect_anomalies(model, data):
    data = data.copy()
    data["anomaly"] = model.predict(data)
    return data

def visualize_data(data):
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=range(len(data)), y="hash_rate", hue="anomaly", data=data, palette={1: 'green', -1: 'red'})
    plt.title("AI-Powered Anomaly Detection in Hash Rate")
    plt.xlabel("Sample Index")
    plt.ylabel("Hash Rate (MH/s)")
    plt.axhline(y=data['hash_rate'].mean(), color='blue', linestyle='--', label='Average Hash Rate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("📩 Telegram alert sent!")
        else:
            print("⚠️ Failed to send Telegram alert.")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def alert_anomalies(data):
    anomalies = data[data["anomaly"] == -1]
    if not anomalies.empty:
        print("⚠️ ALERT: Anomalous mining behavior detected!")
        print(anomalies.tail())
        send_telegram_alert("⚠️ AI Monitor: Mining anomaly detected!")
    else:
        print("✅ All systems operating normally.")

def check_auto_shutdown(data, temp_thresh=90, hash_thresh=30):
    recent = data.iloc[-1]
    if recent["temperature"] > temp_thresh and recent["hash_rate"] < hash_thresh:
        print("🔥 CRITICAL: Overheating + Low hash rate. Initiating shutdown...")
        # Uncomment below for production
        # os.system("shutdown /s /t 1")  # Windows
        # os.system("sudo shutdown now")  # Linux
    else:
        print("✅ Temperature and hash rate within safe limits.")

def check_profitability(current_profit_usd, threshold=1.5):
    if current_profit_usd < threshold:
        print(f"📉 ALERT: Profitability = ${current_profit_usd:.2f}. Suggest switching coin.")
        send_telegram_alert(f"💸 Profit Alert: Rig making only ${current_profit_usd:.2f}/day. Time to switch?")
    else:
        print(f"💰 Profitability OK: ${current_profit_usd:.2f}/day")

def main():
    print("🚀 Starting AI Rig Monitor with Auto Actions...")
    df = simulate_mining_data()
    model = train_model(df[["temperature", "fan_speed", "hash_rate"]])
    result_df = detect_anomalies(model, df)
    visualize_data(result_df)
    alert_anomalies(result_df)
    check_auto_shutdown(result_df)
    simulated_profit = np.random.uniform(0.5, 3.0)
    check_profitability(simulated_profit)

if __name__ == "__main__":
    main()
