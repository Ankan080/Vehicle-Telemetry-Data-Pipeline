import pandas as pd


def test_processed_file_exists():
    file_path = "data/processed/clean_vehicle_telemetry.csv"

    df = pd.read_csv(file_path)

    assert len(df) > 0


def test_no_missing_values():
    file_path = "data/processed/clean_vehicle_telemetry.csv"

    df = pd.read_csv(file_path)

    assert df.isnull().sum().sum() == 0


def test_required_columns_exist():
    file_path = "data/processed/clean_vehicle_telemetry.csv"

    df = pd.read_csv(file_path)

    required_columns = [
        "vehicle_id",
        "timestamp",
        "engine_temp_c",
        "engine_rpm",
        "coolant_temp_c",
        "battery_voltage_v",
        "vehicle_speed_kph",
        "temperature_status",
        "battery_status",
        "engine_status",
        "speed_status"
    ]

    for column in required_columns:
        assert column in df.columns
        

def test_anomaly_report_exists():
    file_path = "reports/anomaly_report.csv"

    df = pd.read_csv(file_path)

    assert len(df) > 0


def test_anomaly_report_has_required_columns():
    file_path = "reports/anomaly_report.csv"

    df = pd.read_csv(file_path)

    required_columns = [
        "vehicle_id",
        "timestamp",
        "parameter",
        "anomaly_type",
        "severity"
    ]

    for column in required_columns:
        assert column in df.columns


def test_anomaly_severity_is_valid():
    file_path = "reports/anomaly_report.csv"

    df = pd.read_csv(file_path)

    valid_severities = ["HIGH", "CRITICAL"]

    assert df["severity"].isin(valid_severities).all()
    
def test_anomaly_summary_exists():
    file_path = "reports/anomaly_summary.csv"

    df = pd.read_csv(file_path)

    assert len(df) > 0


def test_anomaly_summary_has_required_columns():
    file_path = "reports/anomaly_summary.csv"

    df = pd.read_csv(file_path)

    required_columns = [
        "parameter",
        "anomaly_type",
        "severity",
        "anomaly_count"
    ]

    for column in required_columns:
        assert column in df.columns


def test_anomaly_count_is_positive():
    file_path = "reports/anomaly_summary.csv"

    df = pd.read_csv(file_path)

    assert (df["anomaly_count"] > 0).all()