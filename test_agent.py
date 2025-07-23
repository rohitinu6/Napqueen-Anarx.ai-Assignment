import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
API_BASE_URL = "http://localhost:8000"

def test_question(question, description):
    """Test a specific question and display results"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Question: {question}")
    print(f"{'='*60}")
    
    try:
        # Make API call
        print("Making API call...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json={"question": question}
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ API call successful (took {end_time - start_time:.2f} seconds)")
            print(f"\n📊 SQL Query:")
            print(result['sql_query'])
            
            print(f"\n🤖 AI Response:")
            print(result['response'])
            
            print(f"\n📈 Results Summary:")
            print(f"- Rows returned: {result['row_count']}")
            print(f"- Has visualization: {'Yes' if result.get('visualization') else 'No'}")
            
            if result['results']:
                print(f"\n📋 Sample Data (first 3 rows):")
                for i, row in enumerate(result['results'][:3]):
                    print(f"  Row {i+1}: {row}")
            
        else:
            print(f"❌ API call failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_streaming_question(question, description):
    """Test a question with streaming response"""
    print(f"\n{'='*60}")
    print(f"Testing Streaming: {description}")
    print(f"Question: {question}")
    print(f"{'='*60}")
    
    try:
        print("Making streaming API call...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/ask/stream",
            json={"question": question, "stream": True},
            stream=True
        )
        
        if response.status_code == 200:
            print("✅ Streaming started...")
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = json.loads(line[6:])
                        
                        if data['step'] == 'generating_sql':
                            print("🔄 Generating SQL query...")
                        elif data['step'] == 'sql_generated':
                            print("✅ SQL generated")
                        elif data['step'] == 'executing_query':
                            print("🔄 Executing database query...")
                        elif data['step'] == 'query_executed':
                            print(f"✅ Query executed, found {data['row_count']} results")
                        elif data['step'] == 'generating_response':
                            print("🔄 Generating response...")
                        elif data['step'] == 'response_generated':
                            print("✅ Response generated")
                        elif data['step'] == 'creating_visualization':
                            print("🔄 Creating visualization...")
                        elif data['step'] == 'complete':
                            end_time = time.time()
                            print(f"✅ Complete! (took {end_time - start_time:.2f} seconds)")
                            print(f"\n🤖 Final Response:")
                            print(data['response'])
                            break
                        elif data['step'] == 'error':
                            print(f"❌ Error: {data['message']}")
                            break
        else:
            print(f"❌ API call failed with status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function"""
    print("🤖 Product Data AI Agent - Test Suite")
    print("=" * 60)
    
    # Check if API is running
    try:
        health_response = requests.get(f"{API_BASE_URL}/health")
        if health_response.status_code == 200:
            print("✅ API server is running")
        else:
            print("❌ API server is not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API server: {str(e)}")
        print("Please make sure the API server is running on http://localhost:8000")
        return
    
    # Test the three required questions
    test_questions = [
        ("What is my total sales?", "Total Sales Calculation"),
        ("Calculate the RoAS (Return on Ad Spend).", "RoAS Calculation"),
        ("Which product had the highest CPC (Cost Per Click)?", "Highest CPC Product")
    ]
    
    print(f"\n🧪 Running {len(test_questions)} required tests...")
    
    for question, description in test_questions:
        test_question(question, description)
        time.sleep(1)  # Small delay between tests
    
    # Test streaming response
    print(f"\n🌊 Testing streaming response...")
    test_streaming_question("What is my total sales?", "Streaming Total Sales")
    
    # Additional test questions
    additional_questions = [
        ("How many products are eligible for advertising?", "Eligibility Count"),
        ("What is the total ad spend across all products?", "Total Ad Spend"),
        ("Which products have the highest impressions?", "Highest Impressions")
    ]
    
    print(f"\n🧪 Running {len(additional_questions)} additional tests...")
    
    for question, description in additional_questions:
        test_question(question, description)
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print("🎉 All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 