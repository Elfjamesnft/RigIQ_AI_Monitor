# RigIQ - AI-Powered Mining Rig Monitor

🚀 **RigIQ** is an AI-powered tool for monitoring GPU mining rigs using anomaly detection. It auto-detects performance issues, alerts you via Telegram, and can take preventive actions like auto-shutdown or profitability alerts.

## ✨ Features
- Smart anomaly detection with Isolation Forest
- Visual performance monitoring
- Telegram alert integration
- Auto-shutdown on overheating
- Profitability alert system

## 📦 Installation

```bash
git clone https://github.com/yourusername/RigIQ_AI_Monitor.git
cd RigIQ_AI_Monitor
pip install -r requirements.txt
```

## 🧠 Usage

Edit your `TELEGRAM_TOKEN` and `CHAT_ID` in `rig_monitor/rigiq_monitor.py`, then:

```bash
python rig_monitor/rigiq_monitor.py
```

## 📬 Telegram Alerts
Create a bot via [@BotFather](https://t.me/BotFather), get your bot token and chat ID, and plug them into the script.

## 🤖 Coming Soon
- Live Streamlit dashboard
- Integration with HiveOS/NiceHash APIs
- Auto-coin switching

Made with ❤️ by Elf & GPT.
