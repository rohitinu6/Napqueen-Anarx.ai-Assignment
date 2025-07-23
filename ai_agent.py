import google.generativeai as genai
import sqlite3
import pandas as pd
import json
import os
from typing import Dict, Any, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import io

class AIAgent:
    def __init__(self, api_key: str):
        """Initialize the AI agent with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.db_path = 'product_data.db'
        
        # Database schema for context
        self.schema_info = """
        Database Schema:
        
        1. ad_sales_metrics table:
           - date: Date of the metrics
           - item_id: Product identifier
           - ad_sales: Sales generated from advertising
           - impressions: Number of ad impressions
           - ad_spend: Cost of advertising
           - clicks: Number of ad clicks
           - units_sold: Number of units sold from ads
        
        2. total_sales_metrics table:
           - date: Date of the metrics
           - item_id: Product identifier
           - total_sales: Total sales (including organic and ad-driven)
           - total_units_ordered: Total units ordered
        
        3. product_eligibility table:
           - eligibility_datetime_utc: Timestamp of eligibility check
           - item_id: Product identifier
           - eligibility: 1 for eligible, 0 for not eligible
           - message: Reason for ineligibility (if any)
        
        Key relationships:
        - All tables can be joined on item_id
        - date columns can be used for time-based analysis
        """
    
    def get_sql_query(self, question: str) -> str:
        """Convert natural language question to SQL query"""
        
        prompt = f"""
        You are a SQL expert. Given the following database schema and a question, generate the appropriate SQL query.
        
        {self.schema_info}
        
        Question: {question}
        
        Generate a SQLite-compatible SQL query that answers this question. 
        Return ONLY the SQL query, nothing else.
        
        Common calculations:
        - RoAS (Return on Ad Spend) = ad_sales / ad_spend
        - CPC (Cost Per Click) = ad_spend / clicks
        - CTR (Click Through Rate) = clicks / impressions
        """
        
        try:
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            
            # Clean up the response to extract just the SQL
            if sql_query.startswith('```sql'):
                sql_query = sql_query[6:]
            if sql_query.endswith('```'):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
        except Exception as e:
            print(f"Error generating SQL: {e}")
            return None
    
    def execute_query(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(sql_query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()
    
    def generate_response(self, question: str, results_df: pd.DataFrame) -> str:
        """Generate human-readable response from query results"""
        
        prompt = f"""
        You are a data analyst. Given a question and the results from a database query, provide a clear, 
        professional response that answers the question in a human-readable format.
        
        Question: {question}
        
        Query Results:
        {results_df.to_string() if not results_df.empty else 'No results found'}
        
        Provide a comprehensive answer that:
        1. Directly answers the question
        2. Includes relevant numbers and insights
        3. Uses proper formatting for currency, percentages, etc.
        4. Is professional and business-friendly
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error generating response: {e}"
    
    def create_visualization(self, question: str, results_df: pd.DataFrame) -> Optional[str]:
        """Create appropriate visualization based on question and results"""
        
        if results_df.empty:
            return None
        
        try:
            # Determine chart type based on question keywords
            question_lower = question.lower()
            
            if 'roas' in question_lower or 'return on ad spend' in question_lower:
                if 'ad_sales' in results_df.columns and 'ad_spend' in results_df.columns:
                    fig = px.scatter(results_df, x='ad_spend', y='ad_sales', 
                                   title='Ad Spend vs Ad Sales (RoAS Analysis)',
                                   labels={'ad_spend': 'Ad Spend ($)', 'ad_sales': 'Ad Sales ($)'})
                    fig.add_trace(go.Scatter(x=[0, results_df['ad_spend'].max()], 
                                           y=[0, results_df['ad_spend'].max()], 
                                           mode='lines', name='1:1 Line', line=dict(dash='dash')))
            
            elif 'cpc' in question_lower or 'cost per click' in question_lower:
                if 'item_id' in results_df.columns and 'ad_spend' in results_df.columns and 'clicks' in results_df.columns:
                    results_df['cpc'] = results_df['ad_spend'] / results_df['clicks'].replace(0, 1)
                    fig = px.bar(results_df.head(10), x='item_id', y='cpc',
                               title='Top 10 Products by Cost Per Click (CPC)',
                               labels={'item_id': 'Product ID', 'cpc': 'Cost Per Click ($)'})
            
            elif 'sales' in question_lower and 'total' in question_lower:
                if 'total_sales' in results_df.columns:
                    fig = px.line(results_df, x='date', y='total_sales',
                               title='Total Sales Over Time',
                               labels={'date': 'Date', 'total_sales': 'Total Sales ($)'})
            
            elif 'impressions' in question_lower or 'clicks' in question_lower:
                if 'impressions' in results_df.columns and 'clicks' in results_df.columns:
                    fig = make_subplots(rows=2, cols=1, subplot_titles=('Impressions', 'Clicks'))
                    fig.add_trace(go.Scatter(x=results_df['date'], y=results_df['impressions'], name='Impressions'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=results_df['date'], y=results_df['clicks'], name='Clicks'), row=2, col=1)
                    fig.update_layout(title='Ad Performance Metrics Over Time', height=600)
            
            else:
                # Default visualization for numerical data
                numeric_cols = results_df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    fig = px.histogram(results_df, x=numeric_cols[0], title=f'Distribution of {numeric_cols[0]}')
                else:
                    return None
            
            # Convert plot to base64 string
            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode()
            return img_base64
            
        except Exception as e:
            print(f"Error creating visualization: {e}")
            return None
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """Main method to process a question and return comprehensive response"""
        
        # Step 1: Generate SQL query
        sql_query = self.get_sql_query(question)
        if not sql_query:
            return {
                "error": "Failed to generate SQL query",
                "question": question
            }
        
        # Step 2: Execute query
        results_df = self.execute_query(sql_query)
        
        # Step 3: Generate response
        response = self.generate_response(question, results_df)
        
        # Step 4: Create visualization
        visualization = self.create_visualization(question, results_df)
        
        return {
            "question": question,
            "sql_query": sql_query,
            "results": results_df.to_dict('records') if not results_df.empty else [],
            "response": response,
            "visualization": visualization,
            "row_count": len(results_df)
        } 