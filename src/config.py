from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Data paths
RAW_DATA = BASE_DIR / "data" / "raw" / "synthetic_telemetry_data.csv"
TEST_DATA = BASE_DIR / "data" / "raw" / "vehicle_telemetry_test.csv"
PROCESSED_DATA = BASE_DIR / "data" / "processed" / "clean_vehicle_telemetry.csv"


# Report paths
DATA_QUALITY_REPORT = BASE_DIR / "reports" / "data_quality_report.csv"
ANOMALY_REPORT = BASE_DIR / "reports" / "anomaly_report.csv"
ANOMALY_SUMMARY = BASE_DIR / "reports" / "anomaly_summary.csv"


# Log path
LOG_FILE = BASE_DIR / "logs" / "pipeline.log"