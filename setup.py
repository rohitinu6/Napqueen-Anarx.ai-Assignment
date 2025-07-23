#!/usr/bin/env python3
"""
Product Data AI Agent - Setup Script
This script guides you through setting up the AI agent system.
"""

import os
import sys
import subprocess
import sqlite3
import pandas as pd

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8 or higher is required")
        return False
    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n[SETUP] Installing dependencies...")
    
    packages = [
        "fastapi",
        "uvicorn", 
        "sqlalchemy",
        "python-multipart",
        "requests",
        "python-dotenv",
        "google-generativeai"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"[OK] {package} installed")
        except subprocess.CalledProcessError:
            print(f"[ERROR] Failed to install {package}")
            return False
    
    return True

def setup_database():
    """Set up the SQLite database from Excel files"""
    print("\n[DATABASE] Setting up database...")
    
    try:
        # Check if Excel files exist
        excel_files = [
            "Product-Level Ad Sales and Metrics (mapped).xlsx",
            "Product-Level Total Sales and Metrics (mapped).xlsx", 
            "Product-Level Eligibility Table (mapped).xlsx"
        ]
        
        for file in excel_files:
            if not os.path.exists(file):
                print(f"[ERROR] Missing file: {file}")
                return False
            print(f"[OK] Found {file}")
        
        # Run database setup
        subprocess.check_call([sys.executable, "database_setup.py"])
        print("[OK] Database setup completed")
        return True
        
    except subprocess.CalledProcessError:
        print("[ERROR] Database setup failed")
        return False

def create_env_file():
    """Create .env file template"""
    print("\n[ENV] Setting up environment variables...")
    
    env_content = """# Gemini API Key
# Get your API key from: https://aistudio.google.com/apikey
GEMINI_API_KEY=your_gemini_api_key_here
"""
    
    if os.path.exists('.env'):
        print("[OK] .env file already exists")
    else:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("[OK] Created .env file template")
        print("[INFO] Please edit .env and add your Gemini API key")
    
    return True

def test_database():
    """Test database connectivity and data"""
    print("\n[TEST] Testing database...")
    
    try:
        conn = sqlite3.connect('product_data.db')
        
        # Check tables
        tables = ['ad_sales_metrics', 'total_sales_metrics', 'product_eligibility']
        for table in tables:
            result = conn.execute(f"SELECT COUNT(*) FROM {table}")
            count = result.fetchone()[0]
            print(f"[OK] {table}: {count} records")
        
        # Test sample queries
        queries = [
            ("Total Sales", "SELECT SUM(total_sales) FROM total_sales_metrics"),
            ("Ad Sales", "SELECT SUM(ad_sales) FROM ad_sales_metrics"),
            ("Eligible Products", "SELECT COUNT(*) FROM product_eligibility WHERE eligibility = 1")
        ]
        
        for name, query in queries:
            result = conn.execute(query)
            value = result.fetchone()[0]
            print(f"[OK] {name}: {value}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Database test failed: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n" + "="*60)
    print("[SUCCESS] Setup completed successfully!")
    print("="*60)
    
    print("\n[NEXT] Next Steps:")
    print("1. Get your Gemini API key:")
    print("   - Visit: https://aistudio.google.com/apikey")
    print("   - Create a new API key")
    print("   - Edit .env file and replace 'your_gemini_api_key_here' with your actual key")
    
    print("\n2. Start the API server:")
    print("   python api_server.py")
    
    print("\n3. Start the web interface (in a new terminal):")
    print("   streamlit run web_interface.py")
    
    print("\n4. Test the system:")
    print("   python test_agent.py")
    
    print("\n[ACCESS] Access points:")
    print("   - API Documentation: http://localhost:8000/docs")
    print("   - Web Interface: http://localhost:8501")
    
    print("\n[EXAMPLES] Example questions to test:")
    print("   - 'What is my total sales?'")
    print("   - 'Calculate the RoAS (Return on Ad Spend).'")
    print("   - 'Which product had the highest CPC (Cost Per Click)?'")

def main():
    """Main setup function"""
    print("Product Data AI Agent - Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup database
    if not setup_database():
        return False
    
    # Create env file
    if not create_env_file():
        return False
    
    # Test database
    if not test_database():
        return False
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n[ERROR] Setup failed. Please check the errors above.")
        sys.exit(1) 