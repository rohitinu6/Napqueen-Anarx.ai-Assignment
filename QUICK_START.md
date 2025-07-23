# ⚡ Quick Start Guide

## 🚀 3-Step Setup

### 1. Setup System
```bash
cd "C:\Users\User\Desktop\Anarx Assignment"
python setup.py
```

### 2. Get API Key
- Visit: https://aistudio.google.com/apikey
- Sign in → Create API Key → Copy key
- Edit `.env` file: `GEMINI_API_KEY=your_actual_key_here`

### 3. Start System
```bash
# Terminal 1: API Server
python api_server.py

# Terminal 2: Web Interface  
streamlit run web_interface.py
```

## 🌐 Access Points
- **Web Interface**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## 🧪 Test Questions
1. "What is my total sales?"
2. "Calculate the RoAS (Return on Ad Spend)."
3. "Which product had the highest CPC (Cost Per Click)?"

## 🎯 Demo (No API Key)
```bash
python demo.py
```

## 📱 Windows Easy Start
- Double-click `start_system.bat`
- Double-click `start_web_interface.bat`

## 🔧 Quick Fixes
- **Missing modules**: `pip install plotly kaleido streamlit`
- **API errors**: Check `.env` file has correct API key
- **Port conflicts**: Change ports in the respective files 