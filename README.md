Chartify API - Analytics as a Service

Chartify API is a "Database-to-Dashboard" microservice. It allows developers to connect their existing databases (MySQL, PostgreSQL) and dynamically generate chart-ready JSON data without writing complex SQL aggregations or data-processing code.

This is the perfect backend engine for building SaaS dashboards, internal BI tools, or embedding analytics into existing products.

Features

Database Agnostic: Connects seamlessly to PostgreSQL and MySQL databases.

Smart Aggregation: Converts raw table rows into aggregated metrics (sum, count, avg).

Memory Efficient: Generates and executes optimized SQL queries on the target database rather than loading entire tables into memory.

Universal JSON Output: Returns data pre-formatted for popular charting libraries like Chart.js, Recharts, and ApexCharts.

Secure Vault: Encrypts and securely stores customer database credentials locally using cryptography (Fernet).

Fully Dockerized: Runs anywhere without Python environment headaches. Includes Linux-compatible networking for local database testing.

🛠️ Tech Stack

Framework: FastAPI (Python)

Data Engine: Pandas & SQLAlchemy

Database (Internal): SQLite (For storing encrypted API configurations)

Deployment: Docker & Docker Compose

Getting Started (Local Development)

Prerequisites

Docker and Docker Compose installed on your machine.

1. Start the Server

Clone the repository and run the Docker container:

docker-compose up --build


The API will start running at http://localhost:8000.

2. View Interactive Documentation

FastAPI automatically generates interactive Swagger documentation.
Go to: 👉 http://localhost:8000/docs

How to Use the API (The Developer Workflow)

Using Chartify takes just two API calls.

Step 1: Register a Data Source

Register the target database credentials. The API encrypts the password and returns a source_id.

POST /sources/add

{
  "name": "Production Database",
  "db_type": "mysql",
  "host": "host.docker.internal", 
  "port": "3306",
  "user": "db_user",
  "password": "super_secret_password",
  "database_name": "my_app_db"
}


(Note: Use host.docker.internal if connecting to a database running on your local machine outside of Docker).

Step 2: Generate Analytics

Request aggregated data from a specific table.

POST /analytics/generate

{
  "source_id": 1,
  "table_name": "customers",
  "group_by_column": "country",
  "measure_column": "id",
  "operation": "count"
}


Response:

{
  "chart_title": "Count of id by country",
  "data": [
    { "label": "France", "value": 12 },
    { "label": "USA", "value": 36 },
    { "label": "Australia", "value": 5 }
  ]
}


This array can now be plugged directly into any frontend charting library!

Testing with the Demo Dashboard

This project includes a built-in frontend demo (dashboard.html) to visualize the data.

Ensure the Docker container is running.

Double-click dashboard.html to open it in your web browser.

Enter your source_id, target table, and metrics.

Click Generate Chart to see Chart.js render your data instantly!

(Note: The API is configured with generous CORS middleware to allow local HTML files to communicate with it during development).

Project Structure

chartify_api/
│
├── main.py              # FastAPI application and endpoints
├── engine.py            # Core logic: SQL generation and Pandas data formatting
├── models.py            # SQLAlchemy database models & Pydantic schemas
├── security.py          # Fernet encryption for secure credential storage
├── dashboard.html       # Frontend demo using Chart.js
├── Dockerfile           # Docker image build instructions
├── docker-compose.yml   # Multi-container orchestration & volumes
└── requirements.txt     # Python dependencies


Security Note

By default, the security.py file generates a new encryption key every time the server restarts (if a persistent key isn't provided). In a production environment, you must set a static FERNET_KEY environment variable so that previously encrypted passwords can be decrypted after a server restart.
