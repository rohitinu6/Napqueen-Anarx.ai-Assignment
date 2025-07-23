from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import asyncio
import time
from ai_agent import AIAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Product Data AI Agent",
    description="AI agent that answers questions about product sales, advertising, and eligibility data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Agent
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")

ai_agent = AIAgent(api_key)

class QuestionRequest(BaseModel):
    question: str
    stream: bool = False

class QuestionResponse(BaseModel):
    question: str
    sql_query: str
    response: str
    results: list
    visualization: Optional[str] = None
    row_count: int

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Product Data AI Agent API",
        "version": "1.0.0",
        "endpoints": {
            "/ask": "POST - Ask a question about the data",
            "/ask/stream": "POST - Ask a question with streaming response",
            "/health": "GET - Health check",
            "/schema": "GET - Database schema information"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/schema")
async def get_schema():
    """Get database schema information"""
    return {
        "schema": ai_agent.schema_info,
        "tables": [
            "ad_sales_metrics",
            "total_sales_metrics", 
            "product_eligibility"
        ]
    }

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get a complete response"""
    try:
        result = ai_agent.process_question(request.question)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return QuestionResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.post("/ask/stream")
async def ask_question_stream(request: QuestionRequest):
    """Ask a question and get a streaming response"""
    
    async def generate_stream():
        try:
            # Step 1: Generate SQL query
            yield f"data: {json.dumps({'step': 'generating_sql', 'message': 'Generating SQL query...'})}\n\n"
            await asyncio.sleep(0.5)
            
            sql_query = ai_agent.get_sql_query(request.question)
            if not sql_query:
                yield f"data: {json.dumps({'step': 'error', 'message': 'Failed to generate SQL query'})}\n\n"
                return
            
            yield f"data: {json.dumps({'step': 'sql_generated', 'sql_query': sql_query})}\n\n"
            await asyncio.sleep(0.5)
            
            # Step 2: Execute query
            yield f"data: {json.dumps({'step': 'executing_query', 'message': 'Executing database query...'})}\n\n"
            await asyncio.sleep(0.5)
            
            results_df = ai_agent.execute_query(sql_query)
            yield f"data: {json.dumps({'step': 'query_executed', 'row_count': len(results_df)})}\n\n"
            await asyncio.sleep(0.5)
            
            # Step 3: Generate response
            yield f"data: {json.dumps({'step': 'generating_response', 'message': 'Generating human-readable response...'})}\n\n"
            await asyncio.sleep(0.5)
            
            response = ai_agent.generate_response(request.question, results_df)
            yield f"data: {json.dumps({'step': 'response_generated', 'response': response})}\n\n"
            await asyncio.sleep(0.5)
            
            # Step 4: Create visualization
            yield f"data: {json.dumps({'step': 'creating_visualization', 'message': 'Creating visualization...'})}\n\n"
            await asyncio.sleep(0.5)
            
            visualization = ai_agent.create_visualization(request.question, results_df)
            
            # Final result
            final_result = {
                "step": "complete",
                "question": request.question,
                "sql_query": sql_query,
                "response": response,
                "results": results_df.to_dict('records') if not results_df.empty else [],
                "visualization": visualization,
                "row_count": len(results_df)
            }
            
            yield f"data: {json.dumps(final_result)}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'step': 'error', 'message': f'Error: {str(e)}'})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.get("/example-questions")
async def get_example_questions():
    """Get example questions for testing"""
    return {
        "example_questions": [
            "What is my total sales?",
            "Calculate the RoAS (Return on Ad Spend).",
            "Which product had the highest CPC (Cost Per Click)?",
            "How many products are eligible for advertising?",
            "What is the total ad spend across all products?",
            "Which products have the highest impressions?",
            "What is the average cost per click?",
            "How many units were sold from advertising?",
            "Which products are not eligible and why?",
            "What is the total revenue from ads vs organic sales?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 