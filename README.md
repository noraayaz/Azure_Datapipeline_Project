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
