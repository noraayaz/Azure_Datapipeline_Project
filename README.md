# Azure Data Pipeline Project
## Introduction

This project demonstrates a serverless cloud-based data pipeline implemented using Azure services. The goal of the project was to simulate an IoT-like system where sensor data is generated, queued, processed, and stored in the cloud for visualization and analysis. The pipeline is designed for scalability and cost-efficiency, leveraging serverless components and cloud-native services.

## Architecture Overview

The data pipeline consists of the following components:
- Data Producer: A Python script generates random sensor data (temperature, humidity, timestamp) and sends it to an Azure Storage Queue.
- Azure Storage Queue: Serves as a buffer for the sensor data, allowing decoupling between the producer and consumer components.
- Azure Function: Automatically triggered when new data arrives in the queue, the function processes the data and inserts it into the Azure SQL Database.
- Azure SQL Database: Stores the processed sensor data, providing a scalable and reliable storage solution.
- Data Consumers:
- Grafana: Connects to the Azure SQL Database to visualize real-time data in dashboards.
- Power BI: Retrieves and visualizes the stored data in detailed reports.
- Python Data Consumer: A custom Python script fetches data from the SQL Database and visualizes it using matplotlib.

## Project Structure
```bash
├── send_to_queue.py          # Python script for generating and sending sensor data to Azure Queue
├── function_app.py           # Azure Function script for processing and storing data in SQL Database
├── python_data_consumer.py   # Python script to retrieve data from the SQL Database and visualize it
├── .env                      # Environment variables for secure connection details
├── requirements.txt          # Python dependencies for the project
└── README.md                 # Project documentation (this file)
```

## Prerequisites

- Azure Account: Sign up for a free Azure account to access the Azure services.
- Python 3.11: Ensure Python is installed on your local machine.
- Azure CLI: Install the Azure CLI for managing Azure resources from your terminal.

## Installation and Setup

**Clone the Repository**
```bash
git clone https://github.com/noraayaz/Azure_Datapipeline_Project.git
cd azure_datapipeline_project
```

**Install Dependencies Install the required Python packages using pip:**
```bash
pip install -r requirements.txt
```

**Configure Environment Variables Create a .env file and add the following variables:**
```
bash
AZURE_STORAGE_CONNECTION_STRING="<storage_connection_string>"
AZURE_QUEUE_NAME="<queue_name>"
DB_SERVER="<sql_server>"
DB_USER="<sql_user>"
DB_PASSWORD="<sql_password>"
DB_NAME="<sql_database>"
```
**Run the Data Producer Use the Python script to generate and send data to the Azure Queue:**
```
bash
python send_to_queue.py
```
**Deploy Azure Function Use the Azure CLI to deploy the Azure Function:**
```
bash
az functionapp deployment source config-zip --resource-group <resource_group> --name <function_app_name> --src function_app.zip
```
**Run the Python Data Consumer Fetch data from the Azure SQL Database and visualize it using matplotlib:**
```
bash
python python_data_consumer.py
```
## Data Flow

- Data Generation: The send_to_queue.py script generates random sensor data and sends it to the Azure Queue.
Queue to Database: The Azure Function (function_app.py) processes the queued messages and inserts the sensor data into the SQL Database.
- Data Consumption: The data stored in the SQL Database can be consumed and visualized by Grafana, Power BI, or the custom Python data consumer.
## Challenges

**During the implementation, I encountered a few challenges, such as:**
- Managing environment variables securely for Azure services.
- Solving data encoding issues while sending data to the Azure Queue.
- Handling compatibility issues with ODBC drivers and switching to pymssql for database connectivity.

