import pandas as pd
from pathlib import Path
from src.logger_config import get_logger
from src.config import TEST_DATA, PROCESSED_DATA

logger = get_logger()


# ============================================================
# Configuration
# ============================================================

INPUT_FILE = TEST_DATA
OUTPUT_FILE = PROCESSED_DATA


# ============================================================
# Load Data
# ============================================================

def load_dataset(file_path):

    print("Loading telemetry data...")

    df = pd.read_csv(file_path)

    print(f"Records loaded: {len(df)}")
    
    logger.info(
        f"Transformation started: {len(df)} records loaded"
    )

    return df


# ============================================================
# Remove Duplicates
# ============================================================

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    removed = before - after

    print(f"Duplicate records removed: {removed}")
    
    logger.info(
        f"Transformation: {removed} duplicate records removed"
    )

    return df


# ============================================================
# Convert Timestamp
# ============================================================

def convert_timestamp(df):

    if "timestamp" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

        print("Timestamp converted to datetime.")

    return df


# ============================================================
# Handle Missing Values
# ============================================================

def handle_missing_values(df):

    numeric_columns = [
        "engine_temp_c",
        "engine_rpm",
        "coolant_temp_c",
        "battery_voltage_v",
        "vehicle_speed_kph"
    ]

    for column in numeric_columns:

        if column not in df.columns:
            continue

        missing_before = df[column].isna().sum()

        if missing_before > 0:

            median_value = df[column].median()

            df[column] = df[column].fillna(
                median_value
            )

            print(
                f"{column}: "
                f"{missing_before} missing values "
                f"filled using median ({median_value:.2f})"
            )
            logger.info(
                f"Transformation: {column} - "
                f"{missing_before} missing values filled"
            )

    return df


# ============================================================
# Create Temperature Status
# ============================================================

def create_temperature_status(df):

    if "engine_temp_c" not in df.columns:
        return df

    def classify_temperature(temp):

        if temp >= 110:
            return "CRITICAL"

        elif temp >= 100:
            return "WARNING"

        else:
            return "NORMAL"

    df["temperature_status"] = (
        df["engine_temp_c"]
        .apply(classify_temperature)
    )

    return df


# ============================================================
# Create Battery Status
# ============================================================

def create_battery_status(df):

    if "battery_voltage_v" not in df.columns:
        return df

    def classify_battery(voltage):

        if voltage < 11.5:
            return "CRITICAL"

        elif voltage < 12.0:
            return "WARNING"

        else:
            return "NORMAL"

    df["battery_status"] = (
        df["battery_voltage_v"]
        .apply(classify_battery)
    )

    return df


# ============================================================
# Create Engine Status
# ============================================================

def create_engine_status(df):

    if "engine_rpm" not in df.columns:
        return df

    def classify_engine(rpm):

        if rpm > 6000:
            return "CRITICAL"

        elif rpm > 4500:
            return "WARNING"

        else:
            return "NORMAL"

    df["engine_status"] = (
        df["engine_rpm"]
        .apply(classify_engine)
    )

    return df


# ============================================================
# Create Speed Status
# ============================================================

def create_speed_status(df):

    if "vehicle_speed_kph" not in df.columns:
        return df

    def classify_speed(speed):

        if speed > 180:
            return "CRITICAL"

        elif speed > 150:
            return "WARNING"

        else:
            return "NORMAL"

    df["speed_status"] = (
        df["vehicle_speed_kph"]
        .apply(classify_speed)
    )

    return df


# ============================================================
# Save Processed Dataset
# ============================================================

def save_dataset(df, file_path):

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        file_path,
        index=False
    )

    print("\nProcessed dataset saved to:")

    print(file_path)

    print(
        f"Final records: {len(df)}"
    )

    print(
        f"Final columns: {len(df.columns)}"
    )
    
    logger.info(
        f"Processed dataset saved: "
        f"{file_path} | "
        f"records={len(df)} | "
        f"columns={len(df.columns)}"
    )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("VEHICLE TELEMETRY TRANSFORMATION")
    print("=" * 60)

    df = load_dataset(INPUT_FILE)

    # 1. Remove duplicate records
    df = remove_duplicates(df)

    # 2. Convert timestamp
    df = convert_timestamp(df)

    # 3. Handle missing values
    df = handle_missing_values(df)

    # 4. Create derived fields
    df = create_temperature_status(df)

    df = create_battery_status(df)

    df = create_engine_status(df)

    df = create_speed_status(df)

    # 5. Save processed data
    save_dataset(
        df,
        OUTPUT_FILE
    )

    print("\n" + "=" * 60)
    print("TRANSFORMATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()