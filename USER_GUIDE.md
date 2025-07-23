# 🚀 Complete User Guide - Product Data AI Agent

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.8 or higher** installed
- **Windows, Mac, or Linux** operating system
- **Internet connection** (for API key and dependencies)

## 🎯 Quick Start (3 Steps)

### Step 1: Setup the System
```bash
# Open terminal/command prompt in the project folder
cd "C:\Users\User\Desktop\Anarx Assignment"

# Run the automated setup
python setup.py
```

### Step 2: Get Your API Key
1. Visit: **https://aistudio.google.com/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key (looks like: `AIzaSyC...`)

### Step 3: Configure and Run
```bash
# Edit the .env file with your API key
# Replace 'your_gemini_api_key_here' with your actual key

# Start the API server
python api_server.py

# Open a NEW terminal and start the web interface
streamlit run web_interface.py
```

## 📖 Detailed Step-by-Step Instructions

### **Phase 1: Initial Setup**

#### 1.1 Check Python Installation
```bash
python --version
```
You should see Python 3.8 or higher.

#### 1.2 Navigate to Project Folder
```bash
cd "C:\Users\User\Desktop\Anarx Assignment"
```

#### 1.3 Run Automated Setup
```bash
python setup.py
```
This will:
- Install all required packages
- Convert Excel files to database
- Create environment file
- Test the database

**Expected Output:**
```
Product Data AI Agent - Setup
============================================================
[OK] Python 3.13 detected
[SETUP] Installing dependencies...
[OK] fastapi installed
[OK] uvicorn installed
...
[DATABASE] Setting up database...
[OK] Found Product-Level Ad Sales and Metrics (mapped).xlsx
[OK] Found Product-Level Total Sales and Metrics (mapped).xlsx
[OK] Found Product-Level Eligibility Table (mapped).xlsx
[OK] Database setup completed
[ENV] Setting up environment variables...
[OK] Created .env file template
[TEST] Testing database...
[OK] ad_sales_metrics: 3696 records
[OK] total_sales_metrics: 702 records
[OK] product_eligibility: 4381 records
[SUCCESS] Setup completed successfully!
```

### **Phase 2: Get API Key**

#### 2.1 Visit Google AI Studio
- Go to: **https://aistudio.google.com/apikey**
- Sign in with your Google account

#### 2.2 Create API Key
- Click **"Create API Key"**
- Choose **"Create API Key in new project"**
- Give your project a name (e.g., "Product Data AI Agent")
- Copy the generated key

#### 2.3 Configure API Key
Edit the `.env` file in your project folder:
```
# Gemini API Key
# Get your API key from: https://aistudio.google.com/apikey
GEMINI_API_KEY=AIzaSyC...your_actual_key_here...
```

**Example:**
```
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvwxyz
```

### **Phase 3: Start the System**

#### 3.1 Start API Server
Open a terminal and run:
```bash
python api_server.py
```

**Expected Output:**
```
INFO:     Started server process [10752]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### 3.2 Start Web Interface
Open a **NEW terminal** and run:
```bash
streamlit run web_interface.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.0.101:8501
```

### **Phase 4: Test the System**

#### 4.1 Test via Web Interface
1. Open your browser
2. Go to: **http://localhost:8501**
3. You'll see the web interface
4. Try asking: "What is my total sales?"

#### 4.2 Test via Command Line
Open a **third terminal** and run:
```bash
python test_agent.py
```

#### 4.3 Test Individual Questions
```bash
# Test the three required questions
python -c "
import requests
questions = [
    'What is my total sales?',
    'Calculate the RoAS (Return on Ad Spend).',
    'Which product had the highest CPC (Cost Per Click)?'
]
for q in questions:
    response = requests.post('http://localhost:8000/ask', json={'question': q})
    print(f'Q: {q}')
    print(f'A: {response.json()[\"response\"]}')
    print('---')
"
```

## 🌐 Access Points

Once running, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **Web Interface** | http://localhost:8501 | Main user interface |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs |
| **Health Check** | http://localhost:8000/health | System status |
| **API Root** | http://localhost:8000 | API information |

## 🧪 Example Questions to Test

### Required Questions (for assignment):
1. **"What is my total sales?"**
2. **"Calculate the RoAS (Return on Ad Spend)."**
3. **"Which product had the highest CPC (Cost Per Click)?"**

### Additional Questions:
- "How many products are eligible for advertising?"
- "What is the total ad spend across all products?"
- "Which products have the highest impressions?"
- "What is the average cost per click?"
- "How many units were sold from advertising?"

## 🔧 Troubleshooting

### Common Issues:

#### 1. "ModuleNotFoundError: No module named 'plotly'"
```bash
pip install plotly kaleido streamlit
```

#### 2. "Cannot connect to API server"
- Make sure the API server is running: `python api_server.py`
- Check if port 8000 is available

#### 3. "UnicodeEncodeError"
- The system now uses text-based indicators instead of emojis
- Should work on all systems

#### 4. "API Key Error"
- Make sure you've added your API key to the `.env` file
- Verify the key is correct and complete

#### 5. "Database Error"
```bash
python database_setup.py
```

### Port Conflicts:
If ports 8000 or 8501 are in use:
- Change ports in `api_server.py` (line with `uvicorn.run`)
- Change ports in `web_interface.py` (line with `streamlit run`)

## 📱 Windows Users - Easy Start

### Using Batch Files:
1. **Double-click** `start_system.bat` to start API server
2. **Double-click** `start_web_interface.bat` to start web interface
3. Open browser to **http://localhost:8501**

### Using PowerShell:
```powershell
# Start API server
.\start_system.bat

# Start web interface (new window)
.\start_web_interface.bat
```

## 🎯 Demo Mode (No API Key Required)

If you want to test without getting an API key:
```bash
python demo.py
```

This shows how the system works with sample responses.

## 📊 What You'll See

### Web Interface Features:
- **Question Input**: Type your questions in natural language
- **Real-time Responses**: See the AI processing your questions
- **SQL Queries**: View the generated SQL code
- **Data Tables**: See the raw results
- **Visualizations**: Charts and graphs for relevant questions
- **Example Questions**: Pre-loaded questions to try

### API Features:
- **Natural Language Processing**: Convert questions to SQL
- **Streaming Responses**: Real-time progress updates
- **Data Visualization**: Automatic chart generation
- **Error Handling**: Graceful error management

## ✅ Success Indicators

You'll know everything is working when:

1. **API Server**: Shows "Uvicorn running on http://0.0.0.0:8000"
2. **Web Interface**: Opens in browser at http://localhost:8501
3. **Test Script**: Runs without errors and shows responses
4. **Questions**: Get intelligent, data-driven answers

## 🎉 Congratulations!

Once you see the web interface and can ask questions, your AI agent is fully operational! You can now:

- Ask questions about your product data
- Get insights about sales, advertising, and eligibility
- View visualizations and charts
- Export results and share findings

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Ensure the API key is correctly configured
4. Check that both servers are running

The system is designed to be user-friendly and should work out of the box once properly configured! 