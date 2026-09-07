import pandas as pd
from pathlib import Path
from src.config import TEST_DATA, DATA_QUALITY_REPORT


# ============================================================
# Configuration
# ============================================================

INPUT_FILE = TEST_DATA
REPORT_FILE = DATA_QUALITY_REPORT


# ============================================================
# Load Dataset
# ============================================================

def load_dataset(file_path):
    """Load telemetry data from CSV."""

    print("Loading telemetry dataset...")

    df = pd.read_csv(file_path)

    print(f"Records loaded: {len(df)}")

    return df


# ============================================================
# Check Required Columns
# ============================================================

def check_required_columns(df):

    required_columns = [
        "vehicle_id",
        "timestamp",
        "engine_temp_c",
        "engine_rpm",
        "coolant_temp_c",
        "battery_voltage_v",
        "vehicle_speed_kph"
    ]

    results = []

    for column in required_columns:

        if column in df.columns:

            results.append({
                "check": "Required Column",
                "column": column,
                "issue": "None",
                "status": "PASS"
            })

        else:

            results.append({
                "check": "Required Column",
                "column": column,
                "issue": "Column missing",
                "status": "FAIL"
            })

    return results


# ============================================================
# Check Missing Values
# ============================================================

def check_missing_values(df):

    results = []

    for column in df.columns:

        missing_count = df[column].isna().sum()

        if missing_count > 0:

            results.append({
                "check": "Missing Values",
                "column": column,
                "issue": f"{missing_count} missing values",
                "status": "FAIL"
            })

        else:

            results.append({
                "check": "Missing Values",
                "column": column,
                "issue": "None",
                "status": "PASS"
            })

    return results


# ============================================================
# Check Duplicate Records
# ============================================================

def check_duplicates(df):

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        return [{
            "check": "Duplicate Records",
            "column": "ALL",
            "issue": f"{duplicate_count} duplicate records",
            "status": "FAIL"
        }]

    return [{
        "check": "Duplicate Records",
        "column": "ALL",
        "issue": "None",
        "status": "PASS"
    }]


# ============================================================
# Check Negative Values
# ============================================================

def check_negative_values(df):

    results = []

    numeric_columns = [
        "engine_rpm",
        "engine_temp_c",
        "coolant_temp_c",
        "battery_voltage_v",
        "vehicle_speed_kph"
    ]

    for column in numeric_columns:

        if column not in df.columns:
            continue

        negative_count = (df[column] < 0).sum()

        if negative_count > 0:

            results.append({
                "check": "Negative Values",
                "column": column,
                "issue": f"{negative_count} negative values",
                "status": "FAIL"
            })

        else:

            results.append({
                "check": "Negative Values",
                "column": column,
                "issue": "None",
                "status": "PASS"
            })

    return results


# ============================================================
# Check Vehicle Speed
# ============================================================

def check_vehicle_speed(df):

    results = []

    column = "vehicle_speed_kph"

    if column not in df.columns:
        return results

    invalid_count = (df[column] > 180).sum()

    if invalid_count > 0:

        results.append({
            "check": "Vehicle Speed",
            "column": column,
            "issue": f"{invalid_count} readings above 180 km/h",
            "status": "WARNING"
        })

    else:

        results.append({
            "check": "Vehicle Speed",
            "column": column,
            "issue": "None",
            "status": "PASS"
        })

    return results


# ============================================================
# Check Engine RPM
# ============================================================

def check_engine_rpm(df):

    results = []

    column = "engine_rpm"

    if column not in df.columns:
        return results

    invalid_count = (df[column] > 6000).sum()

    if invalid_count > 0:

        results.append({
            "check": "Engine RPM",
            "column": column,
            "issue": f"{invalid_count} readings above 6000 RPM",
            "status": "WARNING"
        })

    else:

        results.append({
            "check": "Engine RPM",
            "column": column,
            "issue": "None",
            "status": "PASS"
        })

    return results


# ============================================================
# Check Engine Temperature
# ============================================================

def check_engine_temperature(df):

    results = []

    column = "engine_temp_c"

    if column not in df.columns:
        return results

    invalid_count = (df[column] > 110).sum()

    if invalid_count > 0:

        results.append({
            "check": "Engine Temperature",
            "column": column,
            "issue": f"{invalid_count} readings above 110°C",
            "status": "WARNING"
        })

    else:

        results.append({
            "check": "Engine Temperature",
            "column": column,
            "issue": "None",
            "status": "PASS"
        })

    return results


# ============================================================
# Check Battery Voltage
# ============================================================

def check_battery_voltage(df):

    results = []

    column = "battery_voltage_v"

    if column not in df.columns:
        return results

    invalid_count = (df[column] < 11.5).sum()

    if invalid_count > 0:

        results.append({
            "check": "Battery Voltage",
            "column": column,
            "issue": f"{invalid_count} readings below 11.5V",
            "status": "WARNING"
        })

    else:

        results.append({
            "check": "Battery Voltage",
            "column": column,
            "issue": "None",
            "status": "PASS"
        })

    return results


# ============================================================
# Generate Validation Report
# ============================================================

def generate_report(results):

    report = pd.DataFrame(results)

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report.to_csv(
        REPORT_FILE,
        index=False
    )

    print("\nValidation report saved to:")
    print(REPORT_FILE)

    return report


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("VEHICLE TELEMETRY DATA VALIDATION")
    print("=" * 60)

    df = load_dataset(INPUT_FILE)

    results = []

    results.extend(
        check_required_columns(df)
    )

    results.extend(
        check_missing_values(df)
    )

    results.extend(
        check_duplicates(df)
    )

    results.extend(
        check_negative_values(df)
    )

    results.extend(
        check_vehicle_speed(df)
    )

    results.extend(
        check_engine_rpm(df)
    )

    results.extend(
        check_engine_temperature(df)
    )

    results.extend(
        check_battery_voltage(df)
    )

    report = generate_report(results)

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    status_counts = report["status"].value_counts()

    print("\nValidation Results:")

    for status, count in status_counts.items():
        print(f"{status}: {count}")

    print("\nTotal validation checks:", len(report))

    print(
    "Failed checks:",
    (report["status"] == "FAIL").sum()
)

    print(
        "Warnings:",
        (report["status"] == "WARNING").sum()
    )

    print(
        "Passed checks:",
        (report["status"] == "PASS").sum()
    )

    print("\nValidation completed.")


if __name__ == "__main__":
    main()