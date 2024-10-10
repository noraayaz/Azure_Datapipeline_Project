import os  # Import os module to read environment variables
import time  # Import time module to handle sleep and timestamp
import random  # Import random module to generate random sensor data
import json  # Import json module to convert Python objects to JSON format
from azure.storage.queue import QueueServiceClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy  # Import Azure Queue SDK

# Retrieve the connection string and queue name from environment variables
# These environment variables must be set in your local environment or in Azure

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")  # Get the connection string from environment variables
queue_name = os.getenv("AZURE_QUEUE_NAME")  # Get the queue name from environment variables

# Check if the required environment variables are set
if not connection_string or not queue_name:
    raise ValueError("Environment variables AZURE_STORAGE_CONNECTION_STRING and AZURE_QUEUE_NAME must be set.")

# Connect to Azure Queue service using the connection string
queue_service = QueueServiceClient.from_connection_string(conn_str=connection_string)

# Get a reference to the queue (queue_client will allow us to send messages to this queue)
queue_client = queue_service.get_queue_client(queue_name)

# Set encoding and decoding policies (messages will be encoded in Base64 for secure transfer)
queue_client._message_encode_policy = BinaryBase64EncodePolicy()
queue_client._message_decode_policy = BinaryBase64DecodePolicy()

# Function to generate and send random sensor data to the Azure Queue
def generate_data():
    while True:  # Infinite loop to continuously generate and send data
        # Generate random values for temperature (between 20.0 and 30.0) and humidity (between 40.0 and 60.0)
        temperature = random.uniform(20.0, 30.0)
        humidity = random.uniform(40.0, 60.0)
        timestamp = time.time()  # Get the current timestamp (in Unix time format)

        # Create a Python dictionary with the generated data
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": timestamp
        }

        # Convert the Python dictionary to a JSON-formatted string
        message = json.dumps(data)
        # Convert the JSON string to bytes (since Azure Queue expects messages in bytes format)
        message_bytes = message.encode('utf-8')

        # Send the message to the Azure Queue
        queue_client.send_message(message_bytes)
        print(f"Sent message: {data}")  # Print the data that was sent for debugging/verification

        # Sleep for 2 seconds before generating the next data point
        time.sleep(2)

# Call the generate_data function to start producing and sending data
generate_data()