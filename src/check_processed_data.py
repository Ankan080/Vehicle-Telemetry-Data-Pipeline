import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data/processed/clean_vehicle_telemetry.csv")


def check_processed_data(file_path):

    print("=" * 60)
    print("PROCESSED DATA VERIFICATION")
    print("=" * 60)

    # Load processed dataset
    df = pd.read_csv(file_path)

    print(f"\nRecords: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    # --------------------------------------------------
    # 1. Check missing values
    # --------------------------------------------------

    print("\n1. Missing Values")

    missing_values = df.isnull().sum()

    missing_values = missing_values[missing_values > 0]

    if len(missing_values) == 0:
        print("PASS - No missing values found.")
    else:
        print("WARNING - Missing values still exist:")
        print(missing_values)

    # --------------------------------------------------
    # 2. Check duplicates
    # --------------------------------------------------

    print("\n2. Duplicate Records")

    duplicate_count = df.duplicated().sum()

    if duplicate_count == 0:
        print("PASS - No duplicate records found.")
    else:
        print(f"WARNING - {duplicate_count} duplicate records found.")

    # --------------------------------------------------
    # 3. Check timestamp
    # --------------------------------------------------

    print("\n3. Timestamp Validation")

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    invalid_timestamp = df["timestamp"].isnull().sum()

    if invalid_timestamp == 0:
        print("PASS - All timestamps are valid.")
    else:
        print(
            f"FAIL - {invalid_timestamp} invalid timestamps found."
        )

    # --------------------------------------------------
    # 4. Check derived columns
    # --------------------------------------------------

    print("\n4. Derived Columns")

    required_columns = [
        "temperature_status",
        "battery_status",
        "engine_status",
        "speed_status"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if len(missing_columns) == 0:
        print("PASS - All derived columns are present.")
    else:
        print("FAIL - Missing derived columns:")
        print(missing_columns)

    # --------------------------------------------------
    # 5. Display status distribution
    # --------------------------------------------------

    print("\n5. Temperature Status")

    if "temperature_status" in df.columns:
        print(
            df["temperature_status"]
            .value_counts()
        )

    print("\n6. Battery Status")

    if "battery_status" in df.columns:
        print(
            df["battery_status"]
            .value_counts()
        )

    print("\n7. Engine Status")

    if "engine_status" in df.columns:
        print(
            df["engine_status"]
            .value_counts()
        )

    print("\n8. Speed Status")

    if "speed_status" in df.columns:
        print(
            df["speed_status"]
            .value_counts()
        )

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    check_processed_data(INPUT_FILE)