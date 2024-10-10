# Script Purpose:
# This Azure Function is triggered whenever a new message is added to an Azure Storage Queue.
# It reads the message from the queue, parses it (assuming the message is in JSON format),
# and inserts the data into an Azure SQL Database. All sensitive information (database details,
# queue name, etc.) is retrieved from environment variables for security.
import azure.functions as func  # Import Azure Functions SDK for Python
import logging  # Import logging module to log messages and errors
import json  # Import JSON module to parse messages from the queue
import pymssql  # Import pymssql module for connecting to SQL Server
import os  # Import os module to read environment variables
from datetime import datetime, timezone  # Import datetime module for timestamp conversion

# Create a Function App instance
app = func.FunctionApp()

# Read database connection settings from environment variables
# These environment variables should be set in Azure (or locally in local.settings.json)
DB_SERVER = os.getenv('DB_SERVER')  # The database server URL (e.g., mydbserver1090.database.windows.net)
DB_USER = os.getenv('DB_USER')  # The username for the SQL Server (e.g., adminuser)
DB_PASSWORD = os.getenv('DB_PASSWORD')  # The password for the SQL Server (ensure it's secure)
DB_NAME = os.getenv('DB_NAME')  # The name of the SQL database (e.g., mydatabase1090)
AZURE_QUEUE_NAME = os.getenv('AZURE_QUEUE_NAME') 


# Define the function triggered by Azure Storage Queue events
@app.queue_trigger(arg_name="azqueue", queue_name=AZURE_QUEUE_NAME, connection="AzureWebJobsStorage")
def queue_trigger(azqueue: func.QueueMessage):
    """
    This function is triggered when a new message is added to the Azure Storage Queue 'AZURE_QUEUE_NAME'.
    The message contains sensor data, which is parsed and inserted into the SQL database.
    """

    # Log the received queue message
    logging.info('Queue trigger function processed a message: %s', azqueue.get_body().decode('utf-8'))
    
    # Parse the JSON message from the queue
    try:
        # Decode the queue message and parse it as JSON
        message = json.loads(azqueue.get_body().decode('utf-8'))
        logging.info("Parsed message: %s", message)

        # Establish a connection to the SQL database using pymssql
        with pymssql.connect(DB_SERVER, DB_USER, DB_PASSWORD, DB_NAME) as conn:
            with conn.cursor() as cursor:
                # Execute the SQL INSERT query to store sensor data into the database
                cursor.execute(
                    """
                    INSERT INTO SensorData (Temperature, Humidity, Timestamp)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        message["temperature"],  # Insert the temperature value from the message
                        message["humidity"],  # Insert the humidity value from the message
                        datetime.utcfromtimestamp(message["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')  # Convert the timestamp to a human-readable format
                    )
                )
                # Commit the transaction to ensure data is saved in the database
                conn.commit()
                logging.info("Data inserted into SQL Database.")  # Log success message

    # Handle JSON parsing errors
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse message: {str(e)}")

    # Handle any other errors that occur while inserting data into the database
    except Exception as e:
        logging.error(f"Error occurred while inserting data into SQL Database: {str(e)}")