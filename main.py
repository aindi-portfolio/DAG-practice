import os
import psycopg2
import requests
from dotenv import load_dotenv
load_dotenv()

# Load environment variables from .env file
api_url = os.getenv("API_URL")
database_host = os.getenv("DATABASE_HOST")
database_port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")

# Make a GET request to the API with a timeout of 30 seconds
response = requests.get(api_url, timeout=30)
response.raise_for_status()

# Convert the response to JSON format
response = response.json()

print(f"Database Name: {database_name}\nDatabase Host: {database_host}\nDatabase Port: {database_port}\nDatabase User: {database_user}")
print("/-----------------------------------/")
print(f"API Response: {response}")

# Insert the API response into the PostgreSQL database
# Use "with" statement to ensure the connection is closed after use
with psycopg2.connect(
    host=database_host,
    port=database_port,
    dbname=database_name,
    user=database_user,
    password=database_password
) as db_conn:
    # Use "cursor" to execute SQL commands within the context of the database connection"
    with db_conn.cursor() as cur:
        # Execute your queries here
        cur.execute(
            """
            INSERT INTO raw_api_data (source, payload)
            VALUES (%s, %s)
            """,
            (api_url, response)
        )
        print("API data inserted into PostgreSQL database successfully.")