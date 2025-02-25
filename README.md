# -Weather-Data-ETL-Pipeline-with-Apache-Airflow-PostgreSQL
📌 Project Overview
This project implements an ETL (Extract, Transform, Load) pipeline using Apache Airflow, PostgreSQL, and Docker to fetch, process, and store real-time weather data from the Open-Meteo API. The system automatically updates daily and maintains historical weather records for analysis.

🛠️ Tech Stack
✅ Apache Airflow – Orchestrates the ETL workflow
✅ PostgreSQL – Stores transformed weather data
✅ Docker & Docker Compose – Containerized deployment
✅ Open-Meteo API – Provides live weather data

📌 Workflow
1️⃣ Extract – Fetches current weather data (temperature, wind speed, direction, etc.) for a specific location using the Open-Meteo API.
2️⃣ Transform – Parses and structures the weather data.
3️⃣ Load – Inserts data into a PostgreSQL database for storage and analysis.

📄 README Content
md
Copy
Edit
# 🌦️ Weather Data ETL Pipeline with Apache Airflow & PostgreSQL

## 📌 Overview  
This ETL pipeline automates weather data collection, processing, and storage using **Apache Airflow, PostgreSQL, and Docker**. It fetches live weather data daily and stores it in a structured database.

## 🏗 Features  
✅ **Automated Data Pipeline** – Runs daily via Apache Airflow  
✅ **Live Weather Data** – Fetches real-time weather updates  
✅ **PostgreSQL Integration** – Stores structured weather records  
✅ **Dockerized Deployment** – Runs seamlessly in containers  

## 📂 Project Structure  
├── dags/
│ ├── weather_etl.py # Airflow DAG for ETL process
├── docker-compose.yml # Manages PostgreSQL and Airflow
├── airflow/ # Airflow configuration
