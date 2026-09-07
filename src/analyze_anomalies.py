import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "reports/anomaly_report.csv"
)


def load_anomaly_report(file_path):

    print("Loading anomaly report...")

    df = pd.read_csv(file_path)

    print(f"Anomalies loaded: {len(df)}")

    return df


def analyze_anomaly_types(df):

    print("\n" + "=" * 60)
    print("ANOMALIES BY TYPE")
    print("=" * 60)

    result = (
        df["anomaly_type"]
        .value_counts()
    )

    print(result)

    return result


def analyze_severity(df):

    print("\n" + "=" * 60)
    print("ANOMALIES BY SEVERITY")
    print("=" * 60)

    result = (
        df["severity"]
        .value_counts()
    )

    print(result)

    return result


def analyze_vehicles(df):

    print("\n" + "=" * 60)
    print("TOP VEHICLES WITH ANOMALIES")
    print("=" * 60)

    result = (
        df["vehicle_id"]
        .value_counts()
        .head(10)
    )

    print(result)

    return result


def analyze_parameters(df):

    print("\n" + "=" * 60)
    print("ANOMALIES BY PARAMETER")
    print("=" * 60)

    result = (
        df["parameter"]
        .value_counts()
    )

    print(result)

    return result


def main():

    print("=" * 60)
    print("ANOMALY REPORT ANALYSIS")
    print("=" * 60)

    df = load_anomaly_report(
        INPUT_FILE
    )

    if df.empty:

        print("\nNo anomalies found.")

        return

    analyze_anomaly_types(df)

    analyze_severity(df)

    analyze_vehicles(df)

    analyze_parameters(df)

    print("\n" + "=" * 60)
    print("ANOMALY ANALYSIS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()