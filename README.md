# Vehicle Telemetry Data Pipeline

A Python-based data engineering pipeline for processing vehicle telemetry data, validating data quality, cleaning and transforming sensor data, detecting abnormal vehicle conditions, and generating analytical reports.

The project demonstrates an end-to-end workflow for handling vehicle telemetry data with a focus on **Python automation, data quality, anomaly detection, logging, configuration management, and automated testing**.

---

## Project Overview

Vehicle telemetry systems generate large amounts of sensor data such as engine temperature, engine RPM, coolant temperature, battery voltage, brake temperature, vehicle speed, and fault indicators.

Before this data can be reliably analyzed, it needs to be checked for issues such as:

* Missing sensor values
* Duplicate records
* Invalid timestamps
* Out-of-range sensor readings
* Abnormal vehicle conditions

This project builds a reusable Python pipeline that processes telemetry data from raw input to structured analytical reports.

---

## Pipeline Architecture

```text
                  Raw Vehicle Telemetry
                           │
                           ▼
              ┌────────────────────────┐
              │ Test Data Generation   │
              │                        │
              │ Controlled synthetic   │
              │ data-quality issues    │
              │ and anomalies          │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ Data Validation        │
              │                        │
              │ • Missing values       │
              │ • Duplicate records    │
              │ • Range validation     │
              │ • Required columns     │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ Data Transformation    │
              │                        │
              │ • Remove duplicates    │
              │ • Fill missing values  │
              │ • Convert timestamps   │
              │ • Create status fields │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ Anomaly Detection      │
              │                        │
              │ • Engine conditions    │
              │ • Battery conditions   │
              │ • Brake conditions     │
              │ • Speed conditions     │
              │ • ABS faults           │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ Analysis & Reporting   │
              │                        │
              │ • Anomaly analysis     │
              │ • Severity analysis    │
              │ • Vehicle analysis     │
              │ • Summary reports      │
              └────────────────────────┘

                 Logging + Pytest
```

---

## Key Features

### 1. Data Profiling

The pipeline can inspect the telemetry dataset to understand:

* Dataset dimensions
* Column names
* Data types
* Missing values
* Duplicate records
* Unique vehicles
* Vehicle brands
* Numerical statistics
* Potential fault-related fields

### 2. Test Data Generation

The original source dataset is kept separate from the generated test dataset.

Controlled synthetic data-quality issues are introduced to test the robustness of the pipeline, including:

* Missing sensor values
* Duplicate records
* High engine temperature
* Excessive engine RPM
* Low battery voltage
* High brake temperature
* Excessive vehicle speed

This allows the pipeline to be tested without modifying the original source data.

### 3. Data Validation

The validation stage checks:

* Required columns
* Missing values
* Duplicate records
* Negative telemetry values
* Suspicious sensor ranges
* Vehicle speed limits
* Engine RPM limits
* Engine temperature
* Battery voltage

The validation process generates:

```text
reports/data_quality_report.csv
```

### 4. Data Transformation

The transformation stage:

* Removes duplicate records
* Converts timestamps to datetime
* Handles missing telemetry values using median imputation
* Creates derived vehicle-status fields

Derived fields include:

```text
temperature_status
battery_status
engine_status
speed_status
```

The cleaned dataset is saved as:

```text
data/processed/clean_vehicle_telemetry.csv
```

### 5. Anomaly Detection

Rule-based anomaly detection is applied to important telemetry parameters.

| Parameter           |  Condition | Anomaly                  |
| ------------------- | ---------: | ------------------------ |
| Engine temperature  |    ≥ 110°C | Engine Overheating       |
| Engine RPM          |     > 6000 | Excessive Engine RPM     |
| Coolant temperature |    ≥ 110°C | High Coolant Temperature |
| Battery voltage     |    < 11.5V | Low Battery Voltage      |
| Vehicle speed       | > 180 km/h | Excessive Vehicle Speed  |
| Brake temperature   |    > 350°C | High Brake Temperature   |
| ABS fault indicator |        = 1 | ABS Fault                |

Anomaly severity is classified as:

```text
HIGH
CRITICAL
```

The resulting report is saved as:

```text
reports/anomaly_report.csv
```

### 6. Anomaly Analysis

The pipeline analyzes detected anomalies by:

* Anomaly type
* Severity
* Vehicle
* Affected telemetry parameter

A summarized report is generated at:

```text
reports/anomaly_summary.csv
```

---

## Results

The complete pipeline was executed successfully.

### Test Data

```text
Original records:       1,970
Test records:           1,989
Duplicate records added:   19
```

### Data Validation

```text
Total validation checks: 58
Passed:                  48
Failed:                   6
Warnings:                 4
```

The failed and warning checks are expected because controlled data-quality issues were intentionally introduced during test-data generation.

### Data Transformation

```text
Records before cleaning: 1,989
Duplicates removed:         18
Final processed records:  1,971
Final columns:               45
```

Missing values in five telemetry columns were handled using median imputation.

### Anomaly Detection

```text
Total anomalies detected: 400
Critical anomalies:       237
High-severity anomalies:  163
```

Detected anomaly categories include:

```text
ABS Fault
Low Battery Voltage
High Brake Temperature
Engine Overheating
Excessive Engine RPM
High Coolant Temperature
Excessive Vehicle Speed
```

> Note: The source telemetry dataset already contained some fault indicators. Therefore, not all detected anomalies represent injected test anomalies. Synthetic anomalies were introduced specifically to test the pipeline's data-quality and anomaly-detection capabilities.

---

## Automated Testing

The project includes automated tests using `pytest`.

Current test result:

```text
9 passed in 0.55s
```

The tests verify:

* Processed dataset availability
* Missing-value handling
* Required processed columns
* Anomaly report generation
* Anomaly report structure
* Valid anomaly severity values
* Anomaly summary generation
* Anomaly summary structure
* Valid anomaly counts

Run the tests with:

```bash
pytest
```

---

## Logging

Pipeline execution is recorded using Python's `logging` module.

The logger records:

* Pipeline start
* Pipeline step execution
* Pipeline step completion
* Errors
* Processing events

Log output:

```text
logs/pipeline.log
```

The generated log file is excluded from Git tracking using `.gitignore`.

---

## Configuration Management

Project paths are centralized in:

```text
src/config.py
```

The project uses `pathlib` to construct paths relative to the project root rather than depending on a machine-specific absolute path.

This makes the project easier to run on another system.

---

## Project Structure

```text
vehicle-telemetry-pipeline/
│
├── data/
│   ├── raw/
│   │   ├── synthetic_telemetry_data.csv
│   │   ├── vehicle_logs.csv
│   │   └── vehicle_telemetry_test.csv
│   │
│   └── processed/
│       └── clean_vehicle_telemetry.csv
│
├── reports/
│   ├── anomaly_report.csv
│   ├── anomaly_summary.csv
│   └── data_quality_report.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── generate_data.py
│   ├── profile_data.py
│   ├── validate.py
│   ├── transform.py
│   ├── check_processed_data.py
│   ├── anomaly_detection.py
│   ├── analyze_anomalies.py
│   ├── create_anomaly_summary.py
│   ├── logger_config.py
│   └── test_logger.py
│
├── tests/
│   └── test_pipeline.py
│
├── requirements.txt
├── run_pipeline.py
├── .gitignore
├── LICENSE
└── README.md
```

---

## Technologies Used

### Programming

* Python

### Data Processing

* Pandas
* NumPy

### Testing

* Pytest

### Development Tools

* Git
* GitHub
* VS Code

### Python Concepts Demonstrated

* File handling
* Data processing
* Functions and modules
* Exception handling
* Logging
* Configuration management
* Subprocess execution
* Automated testing

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Ankan080/Vehicle-Telemetry-Data-Pipeline.git
```

Navigate to the project:

```bash
cd Vehicle-Telemetry-Data-Pipeline
```

Create a virtual environment:

```bash
python -m venv vehiclevenv
```

Activate it on Windows:

```powershell
vehiclevenv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Pipeline

Run the complete pipeline from the project root:

```bash
python run_pipeline.py
```

The pipeline executes the processing stages in sequence:

```text
Generate Test Data
        ↓
Validate Data
        ↓
Transform Data
        ↓
Detect Anomalies
        ↓
Analyze Anomalies
        ↓
Create Anomaly Summary
```

Successful execution ends with:

```text
VEHICLE TELEMETRY PIPELINE COMPLETED
PIPELINE STATUS: SUCCESS
```

---

## Future Improvements

Possible extensions include:

* SQL database integration
* Batch and incremental data processing
* Apache Kafka for streaming telemetry
* Apache Spark for large-scale processing
* Docker containerization
* Workflow orchestration using Airflow
* Dashboard development using Power BI
* Integration with automotive communication protocols such as CAN
* UDS-based diagnostic data processing
* More advanced statistical or machine-learning-based anomaly detection
* Cloud-based data storage and processing

These are future extensions; the current implementation focuses on building a reliable Python-based telemetry data pipeline.

---

## What I Learned

Through this project, I practiced how to build a data pipeline from raw data to analytical output.

Key learning areas include:

* Designing an ETL-style workflow
* Identifying and handling data-quality problems
* Building validation rules
* Transforming telemetry data
* Detecting abnormal conditions using business rules
* Generating structured reports
* Implementing application logging
* Managing configuration separately from processing logic
* Creating automated tests
* Running multiple processing stages through a master pipeline
* Using Git and GitHub for version control

---

## Project Goal

The main goal of this project is to demonstrate practical **Python and data engineering fundamentals** using a vehicle telemetry use case.

The project is designed as a learning and portfolio project rather than a production automotive telemetry system.
