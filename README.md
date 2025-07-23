# Product Data AI Agent

An intelligent AI agent that can answer questions about product sales, advertising, and eligibility data using natural language processing and SQL query generation.

## Features

- 🤖 **Natural Language Processing**: Ask questions in plain English
- 🗄️ **SQL Query Generation**: Automatically converts questions to SQL queries
- 📊 **Data Visualization**: Automatic chart generation for relevant queries
- 🌊 **Streaming Responses**: Real-time response streaming with progress updates
- 🎯 **Multiple Data Sources**: Handles ad sales, total sales, and eligibility data
- 🔌 **RESTful API**: Full API with FastAPI backend
- 🌐 **Web Interface**: Beautiful Streamlit web interface
- 📈 **Business Metrics**: Built-in calculations for RoAS, CPC, CTR, etc.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   FastAPI       │    │   AI Agent      │
│   (Streamlit)   │◄──►│   Server        │◄──►│   (Gemini)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   SQLite        │
                       │   Database      │
                       └─────────────────┘
```

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd anarx-assignment

# Install dependencies
pip install -r requirements.txt

# Set up your Gemini API key
# Copy env_example.txt to .env and add your API key
cp env_example.txt .env
# Edit .env and add your Gemini API key
```

### 2. Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Add it to your `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### 3. Setup Database

```bash
# Convert Excel files to SQLite database
python database_setup.py
```

### 4. Start the API Server

```bash
# Start the FastAPI server
python api_server.py
```

The API will be available at `http://localhost:8000`

### 5. Use the Web Interface

```bash
# Start the Streamlit web interface
streamlit run web_interface.py
```

The web interface will be available at `http://localhost:8501`

## API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /schema` - Database schema information
- `POST /ask` - Ask a question (regular response)
- `POST /ask/stream` - Ask a question (streaming response)
- `GET /example-questions` - Get example questions

### Example API Usage

```python
import requests

# Ask a question
response = requests.post("http://localhost:8000/ask", json={
    "question": "What is my total sales?"
})

result = response.json()
print(result['response'])
```

## Database Schema

### Tables

1. **ad_sales_metrics**
   - `date`: Date of metrics
   - `item_id`: Product identifier
   - `ad_sales`: Sales from advertising
   - `impressions`: Ad impressions
   - `ad_spend`: Advertising cost
   - `clicks`: Ad clicks
   - `units_sold`: Units sold from ads

2. **total_sales_metrics**
   - `date`: Date of metrics
   - `item_id`: Product identifier
   - `total_sales`: Total sales (organic + ad-driven)
   - `total_units_ordered`: Total units ordered

3. **product_eligibility**
   - `eligibility_datetime_utc`: Eligibility check timestamp
   - `item_id`: Product identifier
   - `eligibility`: 1 for eligible, 0 for not eligible
   - `message`: Ineligibility reason

### Common Calculations

- **RoAS (Return on Ad Spend)** = `ad_sales / ad_spend`
- **CPC (Cost Per Click)** = `ad_spend / clicks`
- **CTR (Click Through Rate)** = `clicks / impressions`

## Example Questions

The AI agent can answer questions like:

1. "What is my total sales?"
2. "Calculate the RoAS (Return on Ad Spend)."
3. "Which product had the highest CPC (Cost Per Click)?"
4. "How many products are eligible for advertising?"
5. "What is the total ad spend across all products?"
6. "Which products have the highest impressions?"
7. "What is the average cost per click?"
8. "How many units were sold from advertising?"
9. "Which products are not eligible and why?"
10. "What is the total revenue from ads vs organic sales?"

## Testing

Run the test suite to verify everything works:

```bash
python test_agent.py
```

This will test the three required questions:
1. "What is my total sales?"
2. "Calculate the RoAS (Return on Ad Spend)."
3. "Which product had the highest CPC (Cost Per Click)?"

## Project Structure

```
├── database_setup.py      # Database initialization
├── ai_agent.py           # Core AI agent logic
├── api_server.py         # FastAPI server
├── web_interface.py      # Streamlit web interface
├── test_agent.py         # Test suite
├── requirements.txt      # Python dependencies
├── env_example.txt       # Environment variables example
├── README.md            # This file
└── *.xlsx              # Excel data files
```

## Features Breakdown

### 1. Natural Language to SQL
- Uses Google's Gemini 1.5 Flash model
- Converts questions to optimized SQL queries
- Handles complex business logic and calculations

### 2. Data Visualization
- Automatic chart generation based on question type
- Supports scatter plots, bar charts, line charts, histograms
- Base64 encoded images for easy display

### 3. Streaming Responses
- Real-time progress updates
- Step-by-step processing feedback
- Enhanced user experience

### 4. Error Handling
- Comprehensive error handling
- Graceful degradation
- Informative error messages

## Performance

- **Response Time**: Typically 2-5 seconds per question
- **Database**: SQLite with optimized indexes
- **Caching**: No caching implemented (can be added for production)
- **Scalability**: Can handle thousands of records efficiently

## Security

- API key stored in environment variables
- CORS enabled for web interface
- Input validation and sanitization
- SQL injection protection through parameterized queries

## Future Enhancements

- [ ] Add authentication and authorization
- [ ] Implement response caching
- [ ] Add more visualization types
- [ ] Support for additional data sources
- [ ] Export functionality for results
- [ ] Scheduled report generation
- [ ] Multi-language support

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Gemini API key is correctly set in `.env`
2. **Database Error**: Run `python database_setup.py` to recreate the database
3. **Port Conflicts**: Change ports in the respective files if needed
4. **Dependencies**: Make sure all packages are installed with `pip install -r requirements.txt`

### Logs

Check the terminal output for detailed error messages and processing steps.

## License

This project is created for the Anarx Assignment.

## Support

For issues and questions, please refer to the project documentation or create an issue in the repository. 