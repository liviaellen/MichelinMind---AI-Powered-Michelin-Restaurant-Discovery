# Makefile for setting up and running Apache Airflow DAG

# Variables
PYTHON_VERSION=3.10.6
VENV_NAME=michelin_af
REQUIREMENTS_FILE=requirements.txt
# AIRFLOW_HOME=$(shell pwd)
AIRFLOW_HOME=~/airflow
DAG_FILE=$(AIRFLOW_HOME)/dags/airflow_dag.py
VENV_DIR=$(AIRFLOW_HOME)/$(VENV_NAME)  # Directory for the virtual environment
MONGO_URI='mongodb://localhost:27017'

# Default target
.PHONY: all
all: setup venv install init start

# Setup Airflow environment
.PHONY: setup
setup:
	@echo "Setting up Airflow environment..."
	mkdir -p $(AIRFLOW_HOME)/dags
	mkdir -p $(AIRFLOW_HOME)/logs
	mkdir -p $(AIRFLOW_HOME)/plugins
	@echo "Airflow environment set up at $(AIRFLOW_HOME)."

# Create Python virtual environment using pyenv
.PHONY: venv
venv:
	@echo "Creating Python virtual environment with pyenv..."
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	@echo "Virtual environment created at $(VENV_DIR)."

# Install dependencies
.PHONY: install
install: venv
	@echo "Installing Apache Airflow and required packages from $(REQUIREMENTS_FILE)..."
	@pyenv activate $VENV_NAME && \
	pip install -r $(REQUIREMENTS_FILE)

# Initialize Airflow database
.PHONY: init
init:
	@echo "Initializing Airflow database..."
	# @pyenv activate $(VENV_NAME)
	airflow db init

# Start Airflow web server and scheduler
.PHONY: start
start:
	echo $(AIRFLOW_HOME)
	@export AIRFLOW_HOME=$(AIRFLOW_HOME)
	@echo "Starting Airflow web server..."
	airflow webserver --port 8080 &
	@echo "Starting Airflow scheduler..."
	airflow scheduler &

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	killall airflow || true

# Run the DAG
.PHONY: run
run:
	@echo "Triggering the DAG..."
	airflow dags trigger daily_api_call

.PHONY: setup start-api start-airflow test lint clean docs

# Development setup
setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cp .env.example .env

# Start services
start-api:
	uvicorn api.main:app --reload --host $(API_HOST) --port $(API_PORT)

start-airflow:
	airflow db init
	airflow users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com \
		--password admin
	airflow webserver --port 8080 & airflow scheduler

# Testing
test:
	pytest tests/ -v

# Linting
lint:
	black .
	isort .
	flake8 .
	mypy .

# Documentation
docs:
	mkdocs serve

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# ML model training
train-models:
	python -m ml.train_models

# Data pipeline
run-pipeline:
	airflow dags trigger michelinmind_pipeline

# Help
help:
	@echo "Available commands:"
	@echo "  setup          - Set up development environment"
	@echo "  start-api      - Start the FastAPI server"
	@echo "  start-airflow  - Start Airflow services"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linters"
	@echo "  docs          - Start documentation server"
	@echo "  clean         - Clean up cache files"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-up     - Start Docker containers"
	@echo "  docker-down   - Stop Docker containers"
	@echo "  train-models  - Train ML models"
	@echo "  run-pipeline  - Run the data pipeline"
