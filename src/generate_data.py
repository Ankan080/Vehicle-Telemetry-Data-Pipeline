import pandas as pd
import numpy as np

from src.config import RAW_DATA, TEST_DATA
from src.logger_config import get_logger

logger = get_logger()

INPUT_FILE = RAW_DATA
OUTPUT_FILE = TEST_DATA



# ============================================================
# Configuration
# ============================================================

RANDOM_SEED = 42


# ============================================================
# Load Dataset
# ============================================================

def load_dataset(file_path):
    """Load the vehicle telemetry dataset."""

    print("Loading vehicle telemetry dataset...")

    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} records.")
    print(f"Columns available: {len(df.columns)}")
    
    logger.info(
        f"Dataset loaded: {len(df)} records, "
        f"{len(df.columns)} columns"
    )

    return df


# ============================================================
# Introduce Missing Values
# ============================================================

def introduce_missing_values(df, percentage=0.01):
    """
    Randomly introduce missing values into selected telemetry columns.
    """

    columns = [
        "engine_temp_c",
        "engine_rpm",
        "coolant_temp_c",
        "battery_voltage_v",
        "vehicle_speed_kph"
    ]

    number_of_values = int(len(df) * percentage)

    for column in columns:

        indexes = np.random.choice(
            df.index,
            size=number_of_values,
            replace=False
        )

        df.loc[indexes, column] = np.nan

    print(
    f"Introduced missing values into "
    f"{len(columns)} telemetry columns."
    )

    logger.info(
        f"Test data generation: missing values "
        f"introduced into {len(columns)} columns"
    ) 

    return df


# ============================================================
# Introduce Duplicate Records
# ============================================================

def introduce_duplicates(df, percentage=0.01):
    """
    Duplicate a small percentage of existing records.
    """

    number_of_duplicates = int(len(df) * percentage)

    duplicate_rows = df.sample(
        number_of_duplicates,
        random_state=RANDOM_SEED
    )

    df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    print(f"Added {number_of_duplicates} duplicate records.")
    
    logger.info(
    f"Test data generation: "
    f"{number_of_duplicates} duplicate records added"
    )

    return df


# ============================================================
# Introduce Engine Anomalies
# ============================================================

def introduce_engine_anomalies(df, percentage=0.01):
    """
    Introduce abnormal engine telemetry values.
    """

    number_of_anomalies = int(len(df) * percentage)

    indexes = np.random.choice(
        df.index,
        size=number_of_anomalies,
        replace=False
    )

    # High engine temperature
    df.loc[indexes, "engine_temp_c"] = np.random.uniform(
        115,
        135,
        number_of_anomalies
    )

    # High RPM
    df.loc[indexes, "engine_rpm"] = np.random.uniform(
        6000,
        8000,
        number_of_anomalies
    )

    # High coolant temperature
    df.loc[indexes, "coolant_temp_c"] = np.random.uniform(
        110,
        130,
        number_of_anomalies
    )

    print(f"Introduced {number_of_anomalies} engine anomalies.")
    
    logger.info(
        f"Test data generation: "
        f"{number_of_anomalies} engine anomalies added"
    )

    return df


# ============================================================
# Introduce Battery Anomalies
# ============================================================

def introduce_battery_anomalies(df, percentage=0.01):
    """
    Introduce abnormal battery readings.
    """

    number_of_anomalies = int(len(df) * percentage)

    indexes = np.random.choice(
        df.index,
        size=number_of_anomalies,
        replace=False
    )

    # Low battery voltage
    df.loc[indexes, "battery_voltage_v"] = np.random.uniform(
        9.5,
        11.0,
        number_of_anomalies
    )

    # Low battery health
    df.loc[indexes, "battery_health_percent"] = np.random.uniform(
        20,
        40,
        number_of_anomalies
    )

    print(f"Introduced {number_of_anomalies} battery anomalies.")
    
    logger.info(
        f"Test data generation: "
        f"{number_of_anomalies} engine anomalies added"
    )

    return df


# ============================================================
# Introduce Brake Anomalies
# ============================================================

def introduce_brake_anomalies(df, percentage=0.01):
    """
    Introduce abnormal brake-related readings.
    """

    number_of_anomalies = int(len(df) * percentage)

    indexes = np.random.choice(
        df.index,
        size=number_of_anomalies,
        replace=False
    )

    # High brake temperature
    df.loc[indexes, "brake_temp_c"] = np.random.uniform(
        350,
        500,
        number_of_anomalies
    )

    # Simulated ABS fault
    df.loc[indexes, "abs_fault_indicator"] = 1

    print(f"Introduced {number_of_anomalies} brake anomalies.")
    
    logger.info(
        f"Test data generation: "
        f"{number_of_anomalies} engine anomalies added"
    )

    return df


# ============================================================
# Introduce Speed Anomalies
# ============================================================

def introduce_speed_anomalies(df, percentage=0.01):
    """
    Introduce abnormal vehicle speed readings.
    """

    number_of_anomalies = int(len(df) * percentage)

    indexes = np.random.choice(
        df.index,
        size=number_of_anomalies,
        replace=False
    )

    df.loc[indexes, "vehicle_speed_kph"] = np.random.uniform(
        180,
        250,
        number_of_anomalies
    )

    print(f"Introduced {number_of_anomalies} speed anomalies.")
    
    logger.info(
        f"Test data generation: "
        f"{number_of_anomalies} engine anomalies added"
    )

    return df


# ============================================================
# Save Dataset
# ============================================================

def save_dataset(df, file_path):
    """Save the modified telemetry dataset."""

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        file_path,
        index=False
    )

    print()
    print("Dataset saved successfully.")
    print(f"Output file: {file_path}")
    print(f"Total records: {len(df)}")
    
    logger.info(
        f"Test dataset saved: {file_path} "
        f"with {len(df)} records"
    )


# ============================================================
# Main Pipeline
# ============================================================

def main():

    print("=" * 60)
    print("VEHICLE TELEMETRY TEST DATA GENERATOR")
    print("=" * 60)

    # Make random results reproducible
    np.random.seed(RANDOM_SEED)

    # 1. Load original dataset
    df = load_dataset(INPUT_FILE)

    # 2. Introduce data-quality problems
    df = introduce_missing_values(df)

    df = introduce_duplicates(df)

    # 3. Introduce vehicle anomalies
    df = introduce_engine_anomalies(df)

    df = introduce_battery_anomalies(df)

    df = introduce_brake_anomalies(df)

    df = introduce_speed_anomalies(df)

    # 4. Save test dataset
    save_dataset(df, OUTPUT_FILE)

    print("=" * 60)
    print("TEST DATA GENERATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()