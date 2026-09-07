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


```
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

The profiling stage helps understand the structure and quality of the input dataset before further processing.

---

### 2. Test Data Generation

The original source dataset is kept separate from the generated test dataset.

Controlled synthetic data-quality issues are introduced to test the robustness of the pipeline, including:

* Missing sensor values
* Duplicate records
* High engine temperature
* Excessive engine RPM
* High coolant temperature
* Low battery voltage
* High brake temperature
* Excessive vehicle speed

This allows the pipeline to be tested without modifying the original source data.

The generated test dataset is used as the input for the validation and transformation stages.

---

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

The validation process classifies checks into:

* `PASS`
* `FAIL`
* `WARNING`

The validation report is generated at:

```text
reports/data_quality_report.csv
```
## 6. Anomaly Detection

After cleaning and transforming the telemetry data, the next stage of the pipeline identifies abnormal vehicle conditions.

The anomaly detection module checks important vehicle parameters against predefined threshold values.

The purpose is to identify conditions that may indicate:

- Engine overheating
- Excessive engine RPM
- High coolant temperature
- Low battery voltage
- Excessive vehicle speed
- High brake temperature
- ABS faults

### Detection Rules

| Parameter | Condition | Anomaly Type | Severity |
|---|---|---|---|
| `engine_temp_c` | >= 110°C | Engine Overheating | HIGH |
| `engine_rpm` | > 6000 RPM | Excessive Engine RPM | HIGH |
| `coolant_temp_c` | >= 110°C | High Coolant Temperature | HIGH |
| `battery_voltage_v` | < 11.5 V | Low Battery Voltage | HIGH |
| `vehicle_speed_kph` | > 180 km/h | Excessive Vehicle Speed | HIGH |
| `brake_temp_c` | > 350°C | High Brake Temperature | HIGH |
| `abs_fault_indicator` | == 1 | ABS Fault | CRITICAL |

The anomaly detection process generates a structured anomaly report containing information such as:

- Vehicle ID
- Timestamp
- Parameter
- Observed value
- Anomaly type
- Severity

### Important Note About Anomalies

The source dataset already contained some fault indicators, including ABS fault records.

In addition, controlled synthetic anomalies were intentionally introduced during the test-data generation stage.

This allowed the pipeline to be tested against both existing abnormal records and newly injected test cases.

The project does **not** claim that all detected anomalies were originally present in the source dataset or that they represent real vehicle failures.

---

## 7. Anomaly Analysis

After detecting anomalies, the pipeline performs an analysis of the generated anomaly report.

The analysis identifies:

- Frequency of each anomaly type
- Severity distribution
- Vehicles with the highest number of anomalies
- Parameters responsible for detected anomalies

### Anomalies by Type

The current pipeline detected:

| Anomaly Type | Count |
|---|---:|
| ABS Fault | 237 |
| Low Battery Voltage | 55 |
| High Brake Temperature | 26 |
| Engine Overheating | 25 |
| Excessive Engine RPM | 19 |
| High Coolant Temperature | 19 |
| Excessive Vehicle Speed | 19 |
| **Total** | **400** |

### Severity Distribution

| Severity | Count |
|---|---:|
| CRITICAL | 237 |
| HIGH | 163 |
| **Total** | **400** |

The large number of `CRITICAL` anomalies is mainly associated with the existing `ABS Fault` records in the source/test dataset.

### Top Vehicles by Anomaly Count

The vehicles with the highest number of detected anomalies include:

| Vehicle ID | Anomaly Count |
|---|---:|
| VEH0026 | 20 |
| VEH0046 | 14 |
| VEH0020 | 13 |
| VEH0019 | 12 |
| VEH0048 | 12 |
| VEH0004 | 11 |
| VEH0022 | 11 |
| VEH0035 | 11 |
| VEH0043 | 11 |
| VEH0006 | 10 |

### Anomalies by Parameter

| Parameter | Anomaly Count |
|---|---:|
| `abs_fault_indicator` | 237 |
| `battery_voltage_v` | 55 |
| `brake_temp_c` | 26 |
| `engine_temp_c` | 25 |
| `engine_rpm` | 19 |
| `coolant_temp_c` | 19 |
| `vehicle_speed_kph` | 19 |

This analysis provides a simple way to understand which vehicle parameters are contributing most frequently to abnormal conditions.

---

## 8. Anomaly Summary

The pipeline also generates a summarized anomaly report.

The summary groups detected anomalies by:

- Parameter
- Anomaly type
- Severity

The output is stored in:

```text
reports/anomaly_summary.csv
```
# 9. Logging

The pipeline uses Python's built-in `logging` module to maintain execution logs.

Logging is used to record important pipeline events such as:

- Pipeline start
- Pipeline step start
- Data loading
- Records processed
- Data validation results
- Duplicate removal
- Missing-value handling
- Anomaly detection
- Report generation
- Pipeline completion
- Pipeline errors

The logging configuration is centralized in:

```text
src/logger_config.py
```
# 10. Configuration Management

Project paths are centralized in:

```text
src/config.py
```

Instead of hardcoding absolute Windows paths throughout the project, the pipeline uses `pathlib.Path` to construct paths relative to the project root.

The configuration includes paths for:

- Raw source data
- Generated test data
- Processed data
- Data-quality report
- Anomaly report
- Anomaly summary
- Pipeline log

Example structure:

```text
BASE_DIR
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│
└── logs/
```

This makes the project easier to move between machines and environments.

---

# 11. Master Pipeline

The complete pipeline can be executed using:

```bash
python run_pipeline.py
```

The master pipeline executes the processing stages in sequence:

```text
Generate Test Data
       ↓
Validate Data
       ↓
Transform & Clean Data
       ↓
Detect Anomalies
       ↓
Analyze Anomalies
       ↓
Create Anomaly Summary
       ↓
Pipeline Completed
```

The master script uses Python's `subprocess` module to execute each pipeline stage.

It also handles pipeline errors.

If a step fails, the pipeline:

1. Logs the failure.
2. Displays an error message.
3. Stops further execution.
4. Returns the corresponding error code.

If all stages complete successfully, the terminal displays:

```text
============================================================
VEHICLE TELEMETRY PIPELINE COMPLETED
PIPELINE STATUS: SUCCESS
============================================================
```

---

# 12. Automated Testing

The project includes automated tests using `pytest`.

Test file:

```text
tests/test_pipeline.py
```

The tests verify important pipeline outputs and data-quality conditions.

## Current Test Coverage

The test suite checks:

1. Processed data file exists.
2. Processed data contains no missing values.
3. Required processed columns exist.
4. Anomaly report exists.
5. Anomaly report contains required columns.
6. Anomaly severity values are valid.
7. Anomaly summary exists.
8. Anomaly summary contains required columns.
9. Anomaly counts are positive.

Run the tests using:

```bash
pytest
```

Expected result:

```text
======================== test session starts ========================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\vehicle-telemetry-pipeline
collected 9 items

tests\test_pipeline.py .........                         [100%]

========================= 9 passed in 0.55s =========================
```

The tests provide a basic automated verification layer to ensure that important pipeline outputs remain valid after changes.

---

# 13. Pipeline Results

The current execution produced the following results:

| Metric | Result |
|---|---:|
| Original records | 1,970 |
| Test records | 1,989 |
| Processed records | 1,971 |
| Validation checks | 58 |
| Passed validation checks | 48 |
| Failed validation checks | 6 |
| Warning checks | 4 |
| Detected anomalies | 400 |
| Automated tests | 9/9 passed |

## Data Processing Summary

The source dataset contained:

```text
1,970 records
41 columns
```

The test-data generation stage produced:

```text
1,989 records
```

The increase occurred because duplicate records and controlled test anomalies were introduced.

During transformation:

```text
18 duplicate records removed
```

After cleaning:

```text
1,971 processed records
45 columns
```

Five telemetry columns had missing values filled using their median values:

```text
engine_temp_c
engine_rpm
coolant_temp_c
battery_voltage_v
vehicle_speed_kph
```

Four derived status columns were added:

```text
temperature_status
battery_status
engine_status
speed_status
```

---

# 14. Output Files

The pipeline generates several output files.

## Processed Data

```text
data/processed/clean_vehicle_telemetry.csv
```

Contains the cleaned and transformed telemetry dataset.

It includes the original telemetry fields along with derived status fields.

---

## Data Quality Report

```text
reports/data_quality_report.csv
```

Contains validation results for checks such as:

- Required columns
- Missing values
- Duplicate records
- Negative telemetry values
- Temperature thresholds
- RPM thresholds
- Battery voltage thresholds
- Vehicle speed thresholds

---

## Anomaly Report

```text
reports/anomaly_report.csv
```

Contains individual detected anomaly records.

The report includes information such as:

```text
vehicle_id
timestamp
parameter
value
anomaly_type
severity
```

---

## Anomaly Summary

```text
reports/anomaly_summary.csv
```

Contains grouped anomaly statistics based on:

```text
parameter
anomaly_type
severity
anomaly_count
```

---

## Pipeline Log

```text
logs/pipeline.log
```

Contains execution logs generated by the Python logging system.

This file is generated locally and excluded from Git tracking.

---

# 15. Project Structure

The final project structure is:

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
├── reports/
│   ├── data_quality_report.csv
│   ├── anomaly_report.csv
│   └── anomaly_summary.csv
│
├── tests/
│   └── test_pipeline.py
│
├── logs/
│   └── pipeline.log
│
├── requirements.txt
├── run_pipeline.py
├── README.md
├── LICENSE
└── .gitignore
```

---

# 16. How to Run the Project

## Step 1: Clone the Repository

```bash
git clone https://github.com/Ankan080/Vehicle-Telemetry-Data-Pipeline.git
```

Move into the project directory:

```bash
cd Vehicle-Telemetry-Data-Pipeline
```

---

## Step 2: Create a Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The project primarily uses:

```text
pandas
numpy
pytest
```

---

## Step 4: Run the Complete Pipeline

From the project root:

```bash
python run_pipeline.py
```

The master pipeline will execute all processing stages automatically.

---

## Step 5: Run Automated Tests

After the pipeline finishes:

```bash
pytest
```

Expected result:

```text
9 passed
```

---

# 17. Git and Version Control

The project uses Git for version control.

The repository is hosted on GitHub:

```text
https://github.com/Ankan080/Vehicle-Telemetry-Data-Pipeline
```

The `.gitignore` file prevents unnecessary files from being committed, including:

```text
venv/
vehiclevenv/
__pycache__/
*.py[cod]
.pytest_cache/
.vscode/
logs/*.log
.DS_Store
Thumbs.db
```

This keeps generated environments, Python cache files, local logs, and operating-system files out of the repository.

---

# 18. Design Decisions

Several design decisions were made to keep the project realistic while remaining honest about the dataset and project scope.

## 18.1 Original Source Data Is Preserved

The original dataset is not directly modified.

Instead, it is used as the source input for generating a separate test dataset.

This allows the original data to remain available for comparison.

---

## 18.2 Controlled Synthetic Anomalies

Synthetic anomalies are deliberately introduced into the test dataset.

This provides known abnormal cases that can be used to evaluate whether the validation and anomaly-detection logic behaves as expected.

Examples include:

```text
High engine temperature
Excessive RPM
Low battery voltage
High brake temperature
Excessive vehicle speed
```

---

## 18.3 Rule-Based Anomaly Detection

The current anomaly detection system uses predefined threshold rules.

For example:

```text
engine_temp_c >= 110
```

is treated as an engine-overheating event.

This approach was selected because it is:

- Simple
- Explainable
- Easy to test
- Easy to debug
- Suitable for demonstrating data-pipeline logic

The project does not currently claim to use machine-learning-based anomaly detection.

---

## 18.4 Centralized Configuration

File paths are maintained in:

```text
src/config.py
```

This avoids repeatedly writing hardcoded file paths throughout the project.

---

## 18.5 Modular Pipeline

Each major task is separated into its own Python module.

For example:

```text
generate_data.py
validate.py
transform.py
anomaly_detection.py
analyze_anomalies.py
create_anomaly_summary.py
```

This makes individual stages easier to understand, test, maintain, and extend.

---

# 19. Future Improvements

The current project provides a foundation for a more advanced vehicle telemetry data-engineering system.

Possible future improvements include:

## 19.1 Real-Time Data Ingestion

Extend the batch pipeline to process streaming telemetry data.

Potential technologies:

```text
Apache Kafka
MQTT
Apache Spark Streaming
```

---

## 19.2 Automotive Protocol Integration

The pipeline could be extended to work with automotive communication protocols such as:

```text
CAN Bus
UDS
```

The current project does not implement CAN or UDS communication.

These would be future extensions to connect the data pipeline more closely with actual automotive systems.

---

## 19.3 Database Integration

Processed telemetry could be stored in a relational database such as:

```text
PostgreSQL
MySQL
```

A database layer would allow:

- Historical telemetry storage
- SQL-based analysis
- Vehicle-level reporting
- Faster querying
- Data retention

---

## 19.4 Data Visualization

A dashboard could be added using tools such as:

```text
Power BI
Tableau
Streamlit
```

Possible dashboard metrics:

- Vehicle speed
- Engine temperature
- Battery voltage
- Brake temperature
- Fault frequency
- Anomaly trends
- Vehicle-level health indicators

---

## 19.5 Machine Learning Anomaly Detection

The rule-based anomaly detection system could eventually be extended with machine learning techniques.

Possible approaches include:

```text
Isolation Forest
One-Class SVM
Autoencoders
Clustering
```

This could help identify unusual patterns that are difficult to capture using fixed thresholds.

---

## 19.6 Automated Data Quality Monitoring

The validation system could be extended to continuously monitor:

- Schema changes
- Unexpected null rates
- Sensor range violations
- Duplicate rates
- Timestamp problems
- New telemetry fields

Alerts could be generated when data quality falls below predefined thresholds.

---

## 19.7 Linux-Based Execution

The project can be further adapted for Linux-based execution and deployment.

Potential improvements include:

- Shell scripts
- Cron-based scheduling
- Linux log management
- Docker-based execution
- CI/CD pipeline integration

This would strengthen the project's data-engineering and automation capabilities.

---

# 20. Key Takeaways

This project demonstrates an end-to-end approach to processing vehicle telemetry data using Python.

The main concepts demonstrated are:

```text
Data Ingestion
      ↓
Data Profiling
      ↓
Data Validation
      ↓
Test Data Generation
      ↓
Data Cleaning
      ↓
Data Transformation
      ↓
Anomaly Detection
      ↓
Anomaly Analysis
      ↓
Summary Generation
      ↓
Logging
      ↓
Automated Testing
```

The project focuses on practical data-engineering concepts rather than claiming production-level automotive expertise.

It demonstrates the ability to:

- Work with structured telemetry data
- Build modular Python scripts
- Perform data validation
- Handle missing values
- Remove duplicate records
- Transform raw data
- Create derived features
- Detect abnormal conditions
- Generate structured reports
- Implement logging
- Centralize configuration
- Automate pipeline execution
- Write automated tests
- Use Git and GitHub for version control

The project can serve as a foundation for extending the system toward real-time automotive telemetry, database storage, Linux automation, streaming systems, and machine-learning-based anomaly detection.

---

## Author

~ **Ankan Majumdar**

