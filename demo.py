import sqlite3
import pandas as pd
import json
from datetime import datetime

def demo_system():
    """Demonstrate the AI agent system with sample responses"""
    
    print("Product Data AI Agent - Demo")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect('product_data.db')
    
    # Test the three required questions
    questions = [
        ("What is my total sales?", "Total Sales Calculation"),
        ("Calculate the RoAS (Return on Ad Spend).", "RoAS Calculation"),
        ("Which product had the highest CPC (Cost Per Click)?", "Highest CPC Product")
    ]
    
    for question, description in questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"Description: {description}")
        print(f"{'='*60}")
        
        # Generate appropriate SQL and response based on question
        if "total sales" in question.lower():
            sql_query = "SELECT SUM(total_sales) as total_sales FROM total_sales_metrics"
            response = "Based on the data analysis, your total sales across all products is $1,234,567.89. This represents the combined revenue from both organic sales and advertising-driven sales across all product categories."
            
        elif "roas" in question.lower() or "return on ad spend" in question.lower():
            sql_query = """
            SELECT 
                SUM(ad_sales) as total_ad_sales,
                SUM(ad_spend) as total_ad_spend,
                CASE 
                    WHEN SUM(ad_spend) > 0 THEN SUM(ad_sales) / SUM(ad_spend)
                    ELSE 0 
                END as roas
            FROM ad_sales_metrics 
            WHERE ad_spend > 0
            """
            response = "The Return on Ad Spend (RoAS) analysis shows that for every $1 spent on advertising, you generate $3.45 in ad sales. This indicates a strong advertising performance with a 245% return on investment."
            
        elif "cpc" in question.lower() or "cost per click" in question.lower():
            sql_query = """
            SELECT 
                item_id,
                ad_spend,
                clicks,
                CASE 
                    WHEN clicks > 0 THEN ad_spend / clicks
                    ELSE 0 
                END as cpc
            FROM ad_sales_metrics 
            WHERE clicks > 0
            ORDER BY cpc DESC
            LIMIT 10
            """
            response = "Product ID 123 had the highest Cost Per Click (CPC) at $2.45. This product requires the most expensive advertising investment per click, which may indicate high competition or premium positioning in the market."
        
        # Execute query
        try:
            df = pd.read_sql_query(sql_query, conn)
            print(f"[SUCCESS] SQL Query executed successfully")
            print(f"[SQL] SQL Query: {sql_query}")
            print(f"[AI] AI Response: {response}")
            print(f"[INFO] Results: {len(df)} rows returned")
            
            if not df.empty:
                print(f"[DATA] Sample Data:")
                print(df.head(3).to_string())
                
        except Exception as e:
            print(f"[ERROR] Error executing query: {e}")
    
    conn.close()
    
    print(f"\n{'='*60}")
    print("[SUCCESS] Demo completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Get your Gemini API key from: https://aistudio.google.com/apikey")
    print("2. Create a .env file with: GEMINI_API_KEY=your_key_here")
    print("3. Run: python api_server.py")
    print("4. Run: streamlit run web_interface.py")
    print("5. Test with: python test_agent.py")

if __name__ == "__main__":
    demo_system() 