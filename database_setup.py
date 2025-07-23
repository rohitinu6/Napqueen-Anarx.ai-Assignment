import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
import os

def setup_database():
    """Convert Excel files to SQLite database with proper schema"""
    
    # Create SQLite database
    engine = create_engine('sqlite:///product_data.db')
    
    # Read Excel files
    print("Reading Excel files...")
    
    # Ad Sales and Metrics
    ad_sales_df = pd.read_excel('Product-Level Ad Sales and Metrics (mapped).xlsx')
    print(f"Ad Sales data: {ad_sales_df.shape}")
    
    # Total Sales and Metrics
    total_sales_df = pd.read_excel('Product-Level Total Sales and Metrics (mapped).xlsx')
    print(f"Total Sales data: {total_sales_df.shape}")
    
    # Eligibility Table
    eligibility_df = pd.read_excel('Product-Level Eligibility Table (mapped).xlsx')
    print(f"Eligibility data: {eligibility_df.shape}")
    
    # Clean and prepare data
    # Convert date columns to datetime
    ad_sales_df['date'] = pd.to_datetime(ad_sales_df['date'])
    total_sales_df['date'] = pd.to_datetime(total_sales_df['date'])
    eligibility_df['eligibility_datetime_utc'] = pd.to_datetime(eligibility_df['eligibility_datetime_utc'])
    
    # Ensure item_id is integer
    ad_sales_df['item_id'] = ad_sales_df['item_id'].astype(int)
    total_sales_df['item_id'] = total_sales_df['item_id'].astype(int)
    eligibility_df['item_id'] = eligibility_df['item_id'].astype(int)
    
    # Convert boolean to integer for SQLite compatibility
    eligibility_df['eligibility'] = eligibility_df['eligibility'].astype(int)
    
    # Write to SQLite database
    print("Writing to SQLite database...")
    
    with engine.connect() as conn:
        # Create tables
        ad_sales_df.to_sql('ad_sales_metrics', conn, if_exists='replace', index=False)
        total_sales_df.to_sql('total_sales_metrics', conn, if_exists='replace', index=False)
        eligibility_df.to_sql('product_eligibility', conn, if_exists='replace', index=False)
        
        # Create indexes for better performance
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_ad_sales_item_id ON ad_sales_metrics(item_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_ad_sales_date ON ad_sales_metrics(date)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_total_sales_item_id ON total_sales_metrics(item_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_total_sales_date ON total_sales_metrics(date)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_eligibility_item_id ON product_eligibility(item_id)"))
        
        conn.commit()
    
    print("Database setup completed!")
    print("Tables created:")
    print("- ad_sales_metrics")
    print("- total_sales_metrics") 
    print("- product_eligibility")
    
    # Verify data
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) as count FROM ad_sales_metrics"))
        print(f"Ad sales records: {result.fetchone()[0]}")
        
        result = conn.execute(text("SELECT COUNT(*) as count FROM total_sales_metrics"))
        print(f"Total sales records: {result.fetchone()[0]}")
        
        result = conn.execute(text("SELECT COUNT(*) as count FROM product_eligibility"))
        print(f"Eligibility records: {result.fetchone()[0]}")

if __name__ == "__main__":
    setup_database() 