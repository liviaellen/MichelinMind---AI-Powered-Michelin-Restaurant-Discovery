# 🌟 MichelinMind - AI-Powered Michelin Restaurant Discovery

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)](https://www.mongodb.com/cloud/atlas)
[![Google Cloud](https://img.shields.io/badge/Google-Cloud-orange)](https://cloud.google.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A cutting-edge restaurant intelligence platform that combines MongoDB Atlas, Google Cloud, and AI to revolutionize how we discover and understand Michelin-starred restaurants worldwide.

## 🔍 Features

- **Real-time Data Pipeline**

  - Apache Airflow ETL process
  - Automated data collection
  - Real-time updates
- **Intelligent Search**

  - MongoDB Atlas Search
  - Vector search for semantic similarity
  - Hybrid search capabilities
- **AI/ML Components**

  - Restaurant recommendations
  - Sentiment analysis
  - Price prediction
  - Cuisine trend analysis
- **Interactive Dashboard**

  - Google Looker Studio integration
  - Real-time data visualization
  - Dynamic filtering

## 🛠 Tech Stack

- **Backend & API**

  - FastAPI
  - MongoDB Atlas
  - Motor (async MongoDB driver)
- **Data Pipeline**

  - Apache Airflow
  - Google Cloud Storage
  - Google BigQuery
- **ML/AI**

  - TensorFlow
  - scikit-learn
  - sentence-transformers
- **Cloud Infrastructure**

  - Google Cloud Platform
  - MongoDB Atlas
  - Cloud Run

## 📁 Project Structure

```
michelinmind/
├── api/                    # FastAPI application
│   ├── app/
│   │   ├── routes/        # API endpoints
│   │   ├── models/        # Data models
│   │   └── services/      # Business logic
├── ml/                    # Machine learning
│   ├── models/           # ML models
│   └── notebooks/        # Jupyter notebooks
├── pipeline/             # Airflow DAGs
│   ├── dags/            # DAG definitions
│   └── operators/       # Custom operators
├── notebooks/           # Analysis notebooks
├── data/               # Data files
└── docs/              # Documentation
```

## 🚀 Quick Start

1. **Clone the Repository**

   ```bash
   git clone https://github.com/liviaellen/michelinmind.git
   cd michelinmind
   ```
2. **Set Up Environment**

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
   Visit [MichelinMind Dashboard](https://liviaellen.com/michelin)

## 🔑 Environment Variables

Required environment variables:

```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net
MONGODB_DATABASE=michelinmind
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
GOOGLE_PLACES_API_KEY=your-google-places-api-key
AIRFLOW_HOME=/opt/airflow
```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Setup Guide](docs/setup.md)
- [Architecture Overview](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)

## 👥 Contributors

- [@liviaellen](https://github.com/liviaellen) - Project Lead & Full Stack Developer

  - Data Pipeline Architecture
  - API Development
  - Dashboard Implementation

## 🏆 Hackathon Submission

This project is submitted for the Google Cloud Hackathon 2025, focusing on:

- **MongoDB Challenge Track**

  - AI-driven analysis and generation
  - Vector search capabilities
  - Real-time data processing
- **Google Cloud Integration**

  - Cloud Run for API hosting
  - BigQuery for analytics
  - Cloud Storage for data management

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

---

#michelin #restaurant-discovery #mongodb #google-cloud #ai #data-pipeline #fastapi #airflow #vector-search #hackathon
