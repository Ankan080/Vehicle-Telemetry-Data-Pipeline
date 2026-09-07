# Vehicle Telemetry Data Pipeline

A Python-based data engineering pipeline for processing vehicle telemetry data, validating data quality, cleaning and transforming sensor data, detecting abnormal vehicle conditions, and generating analytical reports.

The project focuses on practical Python automation, data quality validation, anomaly detection, logging, configuration management, automated testing, and end-to-end pipeline execution.

---

## Project Overview

Vehicle telemetry data contains measurements collected from different vehicle systems and sensors, such as:

- Engine temperature
- Engine RPM
- Coolant temperature
- Battery voltage
- Battery health
- Brake temperature
- Vehicle speed
- Wheel speed
- Vibration
- GPS information
- ABS fault indicators

Real-world telemetry data can contain data-quality problems such as:

- Missing values
- Duplicate records
- Invalid measurements
- Abnormal sensor values
- Fault indicators
- Inconsistent data

This project builds a Python pipeline that processes telemetry data through multiple stages:

1. Test data generation
2. Data validation
3. Data cleaning and transformation
4. Anomaly detection
5. Anomaly analysis
6. Report generation
7. Logging
8. Automated testing

The original source dataset is kept unchanged. Controlled synthetic issues and anomalies are introduced into a test copy so that the pipeline can be evaluated safely.

---

# Pipeline Architecture

```text
                    Vehicle Telemetry CSV
                             |
                             v
                 +-------------------------+
                 |   Test Data Generation  |
                 |-------------------------|
                 | Missing Values          |
                 | Duplicate Records       |
                 | Synthetic Anomalies     |
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 |    Data Validation      |
                 |-------------------------|
                 | Required Columns        |
                 | Missing Values          |
                 | Duplicates              |
                 | Invalid Values          |
                 | Warning Conditions      |
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 | Cleaning & Transformation|
                 |-------------------------|
                 | Remove Duplicates       |
                 | Convert Timestamps      |
                 | Median Imputation       |
                 | Derived Status Fields   |
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 |    Anomaly Detection    |
                 |-------------------------|
                 | Engine Conditions       |
                 | Battery Conditions      |
                 | Brake Conditions        |
                 | Speed Conditions        |
                 | ABS Faults              |
                 +-----------+-------------+
                             |
                             v
                 +-------------------------+
                 | Analysis & Reporting     |
                 |-------------------------|
                 | Anomaly Report          |
                 | Anomaly Summary         |
                 | Vehicle Analysis        |
                 +-----------+-------------+
                             |
                             v
                    CSV Reports + Logs
