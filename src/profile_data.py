import pandas as pd
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

INPUT_FILE = Path("data/raw/vehicle_telemetry_test.csv")


# ============================================================
# Load Dataset
# ============================================================

def load_dataset(file_path):
    """Load the vehicle telemetry dataset."""

    print("\nLoading dataset...")

    df = pd.read_csv(file_path)

    print("Dataset loaded successfully.")

    return df


# ============================================================
# Basic Dataset Information
# ============================================================

def show_basic_information(df):

    print("\n" + "=" * 60)
    print("BASIC DATASET INFORMATION")
    print("=" * 60)

    print(f"Number of records : {len(df)}")
    print(f"Number of columns : {len(df.columns)}")

    print("\nColumn names:")

    for column in df.columns:
        print(f"  - {column}")


# ============================================================
# Data Types
# ============================================================

def show_data_types(df):

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)

    print(df.dtypes)


# ============================================================
# Missing Values
# ============================================================

def show_missing_values(df):

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:
        print("No missing values found.")

    else:
        print(missing)


# ============================================================
# Duplicate Records
# ============================================================

def show_duplicates(df):

    print("\n" + "=" * 60)
    print("DUPLICATE RECORDS")
    print("=" * 60)

    duplicate_count = df.duplicated().sum()

    print(f"Duplicate records: {duplicate_count}")


# ============================================================
# Vehicle Information
# ============================================================

def show_vehicle_information(df):

    print("\n" + "=" * 60)
    print("VEHICLE INFORMATION")
    print("=" * 60)

    if "vehicle_id" in df.columns:

        print(f"Unique vehicles: {df['vehicle_id'].nunique()}")

    if "brand" in df.columns:

        print("\nVehicle brands:")

        print(df["brand"].value_counts())


# ============================================================
# Numerical Statistics
# ============================================================

def show_statistics(df):

    print("\n" + "=" * 60)
    print("NUMERICAL STATISTICS")
    print("=" * 60)

    numerical_data = df.select_dtypes(
        include="number"
    )

    print(
        numerical_data.describe().T
    )


# ============================================================
# Failure Information
# ============================================================

def show_failure_information(df):

    print("\n" + "=" * 60)
    print("FAILURE INFORMATION")
    print("=" * 60)

    possible_columns = [
        "failure",
        "failure_indicator",
        "failure_type"
    ]

    for column in possible_columns:

        if column in df.columns:

            print(f"\n{column}:")

            print(df[column].value_counts(dropna=False))


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 60)
    print("VEHICLE TELEMETRY DATA PROFILER")
    print("=" * 60)

    df = load_dataset(INPUT_FILE)

    show_basic_information(df)

    show_data_types(df)

    show_missing_values(df)

    show_duplicates(df)

    show_vehicle_information(df)

    show_statistics(df)

    show_failure_information(df)

    print("\n" + "=" * 60)
    print("DATA PROFILING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()