from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
import requests

LATITUDE = '51.5074'
LONGITUDE = '-0.1278'
POSTGRES_CONN_ID = 'books_connection'  # Keeping the same connection ID
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'fetch_and_store_weather_data',  # Changed DAG name to avoid conflict
    default_args=default_args,
    description='A DAG to fetch weather data and store it in PostgreSQL',
    schedule_interval='@daily',
    catchup=False
)

def fetch_book_data(ti):  # Replacing book fetching logic with weather API call
    """Extract weather data from Open-Meteo API."""
    http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')

    endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'
    response = http_hook.run(endpoint)

    if response.status_code == 200:
        weather_data = response.json()
        ti.xcom_push(key='weather_data', value=weather_data)
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code}")

def insert_book_data_into_postgres(ti):  # Replacing book insertion with weather data insertion
    """Transform and load weather data into PostgreSQL."""
    weather_data = ti.xcom_pull(key='weather_data', task_ids='fetch_book_data')

    if not weather_data:
        raise ValueError("No weather data found")

    current_weather = weather_data['current_weather']
    transformed_data = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'temperature': current_weather['temperature'],
        'windspeed': current_weather['windspeed'],
        'winddirection': current_weather['winddirection'],
        'weathercode': current_weather['weathercode']
    }

    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    insert_query = """
    INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    postgres_hook.run(insert_query, parameters=(
        transformed_data['latitude'],
        transformed_data['longitude'],
        transformed_data['temperature'],
        transformed_data['windspeed'],
        transformed_data['winddirection'],
        transformed_data['weathercode']
    ))

create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id=POSTGRES_CONN_ID,
    sql="""
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        latitude FLOAT,
        longitude FLOAT,
        temperature FLOAT,
        windspeed FLOAT,
        winddirection FLOAT,
        weathercode INT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    dag=dag,
)

fetch_book_data_task = PythonOperator(
    task_id='fetch_book_data',  # Keeping the same function name
    python_callable=fetch_book_data,
    dag=dag,
)

insert_book_data_task = PythonOperator(
    task_id='insert_book_data',  # Keeping the same function name
    python_callable=insert_book_data_into_postgres,
    dag=dag,
)

create_table_task >> fetch_book_data_task >> insert_book_data_task
