import os  # For accessing environment variables
import pymssql  # For connecting to SQL Server
import matplotlib.pyplot as plt  # For visualizing data
import logging
from datetime import datetime

# Load environment variables for database connection
DB_SERVER = os.getenv('DB_SERVER')  # Database server (e.g., mydbserver.database.windows.net)
DB_USER = os.getenv('DB_USER')  # Database user (e.g., adminuser)
DB_PASSWORD = os.getenv('DB_PASSWORD')  # Database password
DB_NAME = os.getenv('DB_NAME')  # Database name (e.g., mydatabase1090)

# Ensure all required environment variables are set
if not DB_SERVER or not DB_USER or not DB_PASSWORD or not DB_NAME:
    raise ValueError("Environment variables for database connection (DB_SERVER, DB_USER, DB_PASSWORD, DB_NAME) must be set.")

# Function to fetch sensor data from the database
def fetch_sensor_data():
    try:
        # Establish a connection to the Azure SQL Database
        with pymssql.connect(DB_SERVER, DB_USER, DB_PASSWORD, DB_NAME) as conn:
            with conn.cursor(as_dict=True) as cursor:
                # Query to fetch temperature, humidity, and timestamp data from the SensorData table
                cursor.execute("SELECT Temperature, Humidity, Timestamp FROM SensorData ORDER BY Timestamp DESC")
                
                # Fetch all rows from the result
                rows = cursor.fetchall()

                if rows:
                    logging.info(f"Fetched {len(rows)} records from the database.")
                    return rows
                else:
                    logging.info("No data found in the database.")
                    return None
    except Exception as e:
        logging.error(f"Error occurred while fetching data from the database: {e}")
        return None

# Function to visualize sensor data using matplotlib
def visualize_data(data):
    if not data:
        print("No data available to visualize.")
        return

    # Prepare lists for plotting
    temperatures = [row['Temperature'] for row in data]
    humidity = [row['Humidity'] for row in data]
    
    # Since row['Timestamp'] is already a datetime object, we don't need to convert it
    timestamps = [row['Timestamp'] for row in data]

    # Create two subplots: one for temperature and one for humidity
    plt.figure(figsize=(10, 6))

    # Plot temperature data
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='b')
    plt.title("Temperature Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)

    # Plot humidity data
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, humidity, marker='o', linestyle='-', color='g')
    plt.title("Humidity Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Humidity (%)")
    plt.grid(True)

    # Automatically adjust layout
    plt.tight_layout()

    # Show the plots
    plt.show()

# Main function to fetch and visualize data
def main():
    print("Fetching data from the database...")
    sensor_data = fetch_sensor_data()

    if sensor_data:
        print("Visualizing data...")
        visualize_data(sensor_data)
    else:
        print("No data to display.")

# Entry point of the script
if __name__ == "__main__":
    main()
