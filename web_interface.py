import streamlit as st
import requests
import json
import base64
import io
from PIL import Image
import time

# Configure page
st.set_page_config(
    page_title="Product Data AI Agent",
    page_icon="🤖",
    layout="wide"
)

# API configuration
API_BASE_URL = "http://localhost:8000"

def main():
    st.title("🤖 Product Data AI Agent")
    st.markdown("Ask questions about your product sales, advertising, and eligibility data!")
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Ask Questions", "Example Questions", "API Documentation"]
    )
    
    if page == "Ask Questions":
        ask_questions_page()
    elif page == "Example Questions":
        example_questions_page()
    elif page == "API Documentation":
        api_docs_page()

def ask_questions_page():
    st.header("Ask Questions")
    
    # Question input
    question = st.text_area(
        "Enter your question:",
        placeholder="e.g., What is my total sales?",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        stream_response = st.checkbox("Stream Response", value=True)
    
    with col2:
        if st.button("Ask Question", type="primary"):
            if question.strip():
                ask_question(question, stream_response)
            else:
                st.error("Please enter a question!")

def ask_question(question, stream=False):
    """Ask a question and display the response"""
    
    if stream:
        # Streaming response
        st.subheader("Processing your question...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/ask/stream",
                json={"question": question, "stream": True},
                stream=True
            )
            
            if response.status_code == 200:
                step = 0
                final_result = None
                
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = json.loads(line[6:])
                            
                            if data['step'] == 'generating_sql':
                                status_text.text("Generating SQL query...")
                                progress_bar.progress(25)
                            elif data['step'] == 'sql_generated':
                                st.code(data['sql_query'], language='sql')
                                progress_bar.progress(50)
                            elif data['step'] == 'executing_query':
                                status_text.text("Executing database query...")
                                progress_bar.progress(75)
                            elif data['step'] == 'query_executed':
                                status_text.text(f"Found {data['row_count']} results")
                                progress_bar.progress(90)
                            elif data['step'] == 'generating_response':
                                status_text.text("Generating response...")
                                progress_bar.progress(95)
                            elif data['step'] == 'response_generated':
                                progress_bar.progress(100)
                                status_text.text("Complete!")
                                time.sleep(0.5)
                            elif data['step'] == 'creating_visualization':
                                status_text.text("Creating visualization...")
                            elif data['step'] == 'complete':
                                final_result = data
                                break
                            elif data['step'] == 'error':
                                st.error(f"Error: {data['message']}")
                                return
                
                # Display final results
                if final_result:
                    display_results(final_result)
            else:
                st.error(f"API Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")
    
    else:
        # Regular response
        with st.spinner("Processing your question..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={"question": question}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    display_results(result)
                else:
                    st.error(f"API Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error connecting to API: {str(e)}")

def display_results(result):
    """Display the results from the AI agent"""
    
    st.subheader("Results")
    
    # Question
    st.markdown(f"**Question:** {result['question']}")
    
    # SQL Query
    with st.expander("View SQL Query"):
        st.code(result['sql_query'], language='sql')
    
    # Response
    st.markdown("### Answer")
    st.markdown(result['response'])
    
    # Results table
    if result['results']:
        st.markdown("### Data")
        st.dataframe(result['results'], use_container_width=True)
    
    # Visualization
    if result.get('visualization'):
        st.markdown("### Visualization")
        try:
            # Decode base64 image
            img_data = base64.b64decode(result['visualization'])
            img = Image.open(io.BytesIO(img_data))
            st.image(img, use_column_width=True)
        except Exception as e:
            st.error(f"Error displaying visualization: {str(e)}")
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows Returned", result['row_count'])
    with col2:
        st.metric("Has Visualization", "Yes" if result.get('visualization') else "No")
    with col3:
        st.metric("Response Type", "Streaming" if result.get('stream') else "Regular")

def example_questions_page():
    st.header("Example Questions")
    
    try:
        response = requests.get(f"{API_BASE_URL}/example-questions")
        if response.status_code == 200:
            examples = response.json()['example_questions']
            
            st.markdown("Here are some example questions you can ask:")
            
            for i, example in enumerate(examples, 1):
                if st.button(f"{i}. {example}", key=f"example_{i}"):
                    st.session_state.question = example
                    st.rerun()
            
            # Auto-fill question if selected
            if 'question' in st.session_state:
                st.text_area(
                    "Selected Question:",
                    value=st.session_state.question,
                    height=100,
                    key="selected_question"
                )
                if st.button("Ask This Question", type="primary"):
                    ask_question(st.session_state.question, stream=True)
                    del st.session_state.question
        else:
            st.error("Could not load example questions")
            
    except Exception as e:
        st.error(f"Error loading examples: {str(e)}")

def api_docs_page():
    st.header("API Documentation")
    
    st.markdown("""
    ## API Endpoints
    
    ### Base URL
    ```
    http://localhost:8000
    ```
    
    ### Endpoints
    
    #### 1. GET /
    Root endpoint with API information
    
    #### 2. GET /health
    Health check endpoint
    
    #### 3. GET /schema
    Get database schema information
    
    #### 4. POST /ask
    Ask a question and get a complete response
    
    **Request Body:**
    ```json
    {
        "question": "What is my total sales?",
        "stream": false
    }
    ```
    
    #### 5. POST /ask/stream
    Ask a question and get a streaming response
    
    **Request Body:**
    ```json
    {
        "question": "What is my total sales?",
        "stream": true
    }
    ```
    
    #### 6. GET /example-questions
    Get example questions for testing
    
    ## Database Schema
    
    The system works with three main tables:
    
    1. **ad_sales_metrics** - Advertising performance data
    2. **total_sales_metrics** - Total sales data
    3. **product_eligibility** - Product eligibility information
    
    ## Common Calculations
    
    - **RoAS (Return on Ad Spend)** = ad_sales / ad_spend
    - **CPC (Cost Per Click)** = ad_spend / clicks
    - **CTR (Click Through Rate)** = clicks / impressions
    """)

if __name__ == "__main__":
    main() 