"""
This script retrieves data from an Azure SQL Database, processes it, and generates a visual representation (a plot) of the data using the matplotlib library. 
The data, consisting of temperature, humidity, and timestamp values, is fetched and plotted to visualize the trends over time. 
The plot is saved as a PNG file on the server (Azure VM), and can be transferred to a local machine for further analysis or reporting purposes.

Key steps:
1. Retrieve the top 20 most recent records from the SensorData table in Azure SQL Database.
2. Process the data to extract temperature, humidity, and timestamp values.
3. Generate a plot using matplotlib, showing the trends of temperature and humidity over time.
4. Save the plot as a PNG image on the Azure VM at '/home/ubuntu/sensor_data_plot.png'.
5. The file can be transferred from the Azure VM to a local machine using the 'scp' command.

Example SCP command for transferring the plot to a local machine:
scp -i ~/.ssh/id_rsa ubuntu@<VM-IP-Address>:/home/ubuntu/sensor_data_plot.png /<local-path>/

Note:
The database connection details (server, database name, user, and password) are now retrieved from environment variables for enhanced security.
"""

import os
import pyodbc
import matplotlib.pyplot as plt

# Retrieve the database connection details from environment variables
DB_SERVER = os.getenv("DB_SERVER")  # Azure SQL Server address
DB_NAME = os.getenv("DB_NAME")  # Azure SQL Database name
DB_USER = os.getenv("DB_USER")  # Azure SQL Database username
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Azure SQL Database password

# Construct the database connection string using environment variables
DB_CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"Server=tcp:{DB_SERVER},1433;"
    f"Database={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Connect to the database and fetch the top 20 records ordered by Timestamp
with pyodbc.connect(DB_CONNECTION_STRING) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 20 Temperature, Humidity, Timestamp FROM SensorData ORDER BY Timestamp DESC")
    rows = cursor.fetchall()

    if rows:
        # Extract temperature, humidity, and timestamp values from the database records
        temperatures = [row[0] for row in rows]
        humidities = [row[1] for row in rows]
        timestamps = [row[2] for row in rows]
        
        # Plot the data using matplotlib
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, temperatures, label='Temperature (°C)', marker='o')
        plt.plot(timestamps, humidities, label='Humidity (%)', marker='x')
        plt.xlabel('Timestamp')
        plt.ylabel('Values')
        plt.title('Temperature and Humidity Trends')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot as a PNG file on the server (Azure VM)
        plt.savefig('/home/ubuntu/sensor_data_plot.png')
        print("Plot saved as sensor_data_plot.png")
    else:
        print("No data found.")
