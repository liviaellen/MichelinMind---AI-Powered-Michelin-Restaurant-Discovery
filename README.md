# MichelinMind - AI-Powered Michelin Restaurant Discovery

A cutting-edge restaurant intelligence platform that combines the power of AI, MongoDB Atlas, and Google Cloud to revolutionize how we discover and understand Michelin-starred restaurants worldwide.

## 🏆 Hackathon Submission
This project is submitted for the Google Cloud Hackathon, focusing on the MongoDB Challenge track. It demonstrates the power of AI-driven analysis and generation using MongoDB's powerful search capabilities and Google Cloud's advanced services.

## 🌟 Key Features

- **AI-Powered Restaurant Discovery**
  - Smart restaurant recommendations using vector search
  - Sentiment analysis on restaurant reviews
  - Price prediction based on location and cuisine
  - Cuisine trend analysis

- **Real-Time Data Pipeline**
  - Automated data collection and processing
  - MongoDB Atlas Search integration
  - Google Cloud BigQuery analytics
  - Real-time updates via MongoDB Change Streams

- **Interactive Dashboard**
  - Live restaurant data visualization
  - Dynamic filtering and search
  - Trend analysis and insights
  - User-friendly interface

## 🛠 Tech Stack

- **Backend & API**
  - FastAPI for RESTful API
  - MongoDB Atlas for primary database
  - MongoDB Atlas Search for advanced search
  - Vector Search for semantic similarity

- **Data Pipeline**
  - Apache Airflow for ETL
  - Google Cloud Storage
  - Google BigQuery for analytics
  - Real-time data processing

- **AI/ML Components**
  - TensorFlow for deep learning
  - Scikit-learn for machine learning
  - Natural Language Processing for review analysis
  - Vector embeddings for semantic search

- **Cloud Infrastructure**
  - Google Cloud Platform
  - MongoDB Atlas
  - Cloud Run for API hosting
  - Looker Studio for visualization

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/liviaellen/michelinmind.git
   cd michelinmind
   ```

2. **Environment Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment variables
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Start Services**
   ```bash
   # Start the API
   make start-api

   # Start Airflow
   make start-airflow
   ```

4. **Access the Dashboard**
   Visit [MichelinMind Dashboard](https://liviaellen.com/michelin) to explore the interactive visualization.

## 📊 Data Pipeline

1. **Data Collection**
   - Automated scraping of Michelin restaurant data
   - Google Places API integration
   - Review data collection

2. **Processing**
   - Data cleaning and normalization
   - Feature engineering
   - ML model training

3. **Storage**
   - MongoDB Atlas for primary storage
   - Google BigQuery for analytics
   - Vector embeddings for search

4. **Analysis**
   - Real-time analytics
   - Trend detection
   - Price prediction
   - Sentiment analysis

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Cloud Platform
- MongoDB Atlas
- Apache Airflow
- FastAPI
- TensorFlow
- Scikit-learn

## 📞 Contact

For questions or support, please open an issue in this repository or contact the maintainers.

## Dashboard
View our interactive dashboard: [Michelin Star Explorer Dashboard](https://liviaellen.com/michelin)

## Data Pipeline & Visualization

- Data is collected and processed through our ETL pipeline
- Results are stored in both Google BigQuery and MongoDB
- Interactive visualizations are created using Google Looker Studio
- Dashboard pulls data from both Google BigQuery and MongoDB for comprehensive analysis

## Overview
This project is an Apache Airflow DAG that orchestrates tasks related to fetching, processing, and storing restaurant data in a MongoDB database.

## Summary of the Process

1. **Environment Setup**:
   - Loads environment variables using `dotenv`, specifically fetching the `GOOGLE_PLACES_API_KEY` required for Google Places API calls.

2. **Function Definitions**:
   - **`get_place_rating(name, address)`**: Fetches the Google Places rating and user ratings total for a given restaurant name and address.
   - **`json_to_mongo(json_data)`**: Inserts or updates restaurant data in a MongoDB collection.
   - **`csv_to_json(csv_data)`**: Converts CSV data into JSON format.
   - **`call_api()`**: Fetches CSV data from a specified GitHub URL containing restaurant information.
   - **`task_dag()`**: Calls the API, converts the CSV data to JSON, and uploads it to MongoDB.
   - **`google_dag()`**: Processes the CSV data to fetch Google ratings for each restaurant, updates the DataFrame, and uploads the results to MongoDB.
   - **`aggregate_michelin_data()`**: Aggregates restaurant data from MongoDB, calculating average ratings and counts of Michelin stars, and stores the results in a new collection.

3. **DAG Definition**:
   - The DAG is defined with default arguments, including the owner, start date, and retry settings.
   - Scheduled to run daily.

4. **Task Definitions**:
   - Several tasks are defined using `PythonOperator`:
     - `api_call_task`: Executes the `task_dag` function.
     - `google_dag_task`: Executes the `google_dag` function.
     - `aggregation_task`: Executes the `aggregate_michelin_data` function.
     - `aggregation_cuisine_task`: Executes the `aggregate_top_cuisines_by_rating` function (imported from another script).

5. **Task Dependencies**:
   - The tasks are set to run in a specific order: `api_call_task` runs first, followed by `google_dag_task`, and then both `aggregation_task` and `aggregation_cuisine_task` run in parallel.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:yourusername/michelin_star_explorer.git
   cd michelin_star_explorer
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory of the project and add your Google Places API key:
     ```
     GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
     ```

5. **Set Up MongoDB**:
   - Ensure you have MongoDB installed and running on your local machine or use a cloud MongoDB service.
   - Update the `MONGO_URI` in the code if necessary.

## How to Run the DAG

1. **Start Apache Airflow**:
   - Initialize the database:
     ```bash
     airflow db init
     ```
   - Start the web server:
     ```bash
     airflow webserver --port 8080
     ```
   - In a new terminal, start the scheduler:
     ```bash
     airflow scheduler
     ```

2. **Access the Airflow UI**:
   - Open your web browser and go to `http://localhost:8080`.
   - You should see the `daily_api_call` DAG listed.

3. **Trigger the DAG**:
   - Click on the DAG name to view its details.
   - You can manually trigger the DAG by clicking the "Trigger DAG" button.

4. **Monitor the Tasks**:
   - You can monitor the progress of each task in the Airflow UI.
