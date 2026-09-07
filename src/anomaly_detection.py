import pandas as pd
from pathlib import Path
from src.logger_config import get_logger
from src.config import PROCESSED_DATA, ANOMALY_REPORT
logger = get_logger()

INPUT_FILE = PROCESSED_DATA
OUTPUT_FILE = ANOMALY_REPORT


def load_dataset(file_path):
    print("Loading processed telemetry data...")

    df = pd.read_csv(file_path)

    print(f"Records loaded: {len(df)}")
    
    logger.info(
        f"Anomaly detection started: "
        f"{len(df)} records loaded"
    )

    return df


def detect_anomalies(df):

    anomalies = []

    # --------------------------------------------------
    # 1. Engine Temperature
    # --------------------------------------------------

    if "engine_temp_c" in df.columns:

        condition = df["engine_temp_c"] >= 110

        for _, row in df[condition].iterrows():

            anomalies.append({
                "vehicle_id": row["vehicle_id"],
                "timestamp": row["timestamp"],
                "parameter": "engine_temp_c",
                "value": row["engine_temp_c"],
                "anomaly_type": "Engine Overheating",
                "severity": "HIGH"
            })

    # --------------------------------------------------
    # 2. Engine RPM
    # --------------------------------------------------

    if "engine_rpm" in df.columns:

        condition = df["engine_rpm"] > 6000

        for _, row in df[condition].iterrows():

            anomalies.append({
                "vehicle_id": row["vehicle_id"],
                "timestamp": row["timestamp"],
                "parameter": "engine_rpm",
                "value": row["engine_rpm"],
                "anomaly_type": "Excessive Engine RPM",
                "severity": "HIGH"
            })

    # --------------------------------------------------
    # 3. Coolant Temperature
    # --------------------------------------------------

    if "coolant_temp_c" in df.columns:

        condition = df["coolant_temp_c"] >= 110

        for _, row in df[condition].iterrows():

            anomalies.append({
                "vehicle_id": row["vehicle_id"],
                "timestamp": row["timestamp"],
                "parameter": "coolant_temp_c",
                "value": row["coolant_temp_c"],
                "anomaly_type": "High Coolant Temperature",
                "severity": "HIGH"
            })

    # --------------------------------------------------
    # 4. Battery Voltage
    # --------------------------------------------------

    if "battery_voltage_v" in df.columns:

        condition = df["battery_voltage_v"] < 11.5

        for _, row in df[condition].iterrows():

            anomalies.append({
                "vehicle_id": row["vehicle_id"],
                "timestamp": row["timestamp"],
                "parameter": "battery_voltage_v",
                "value": row["battery_voltage_v"],
                "anomaly_type": "Low Battery Voltage",
                "severity": "HIGH"
            })

    # --------------------------------------------------
    # 5. Vehicle Speed
    # --------------------------------------------------

    if "vehicle_speed_kph" in df.columns:

        condition = df["vehicle_speed_kph"] > 180

        for _, row in df[condition].iterrows():

            anomalies.append({
                "vehicle_id": row["vehicle_id"],
                "timestamp": row["timestamp"],
                "parameter": "vehicle_speed_kph",
                "value": row["vehicle_speed_kph"],
                "anomaly_type": "Excessive Vehicle Speed",
                "severity": "HIGH"
            })

    # --------------------------------------------------
    # 6. Brake Temperature
    # --------------------------------------------------

    if "brake_temp_c" in df.columns:

        condition = df["brake_temp_c"] > 350

        for _, row in df[condition].iterrows():

            anomalies.append({
                "vehicle_id": row["vehicle_id"],
                "timestamp": row["timestamp"],
                "parameter": "brake_temp_c",
                "value": row["brake_temp_c"],
                "anomaly_type": "High Brake Temperature",
                "severity": "HIGH"
            })

    # --------------------------------------------------
    # 7. ABS Fault
    # --------------------------------------------------

    if "abs_fault_indicator" in df.columns:

        condition = df["abs_fault_indicator"] == 1

        for _, row in df[condition].iterrows():

            anomalies.append({
                "vehicle_id": row["vehicle_id"],
                "timestamp": row["timestamp"],
                "parameter": "abs_fault_indicator",
                "value": row["abs_fault_indicator"],
                "anomaly_type": "ABS Fault",
                "severity": "CRITICAL"
            })

    return pd.DataFrame(anomalies)


def save_report(anomaly_df, file_path):

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    anomaly_df.to_csv(
        file_path,
        index=False
    )

    print("\nAnomaly report saved to:")
    print(file_path)

    print(
        f"Total anomalies detected: "
        f"{len(anomaly_df)}"
    )
    
    logger.info(
        f"Anomaly report saved: "
        f"{file_path} | "
        f"anomalies={len(anomaly_df)}"
    )


def main():

    print("=" * 60)
    print("VEHICLE TELEMETRY ANOMALY DETECTION")
    print("=" * 60)

    df = load_dataset(INPUT_FILE)

    anomaly_df = detect_anomalies(df)

    save_report(
        anomaly_df,
        OUTPUT_FILE
    )

    print("\n" + "=" * 60)
    print("ANOMALY DETECTION COMPLETED")
    print("=" * 60)
    
    logger.info(
        f"Anomaly detection completed: "
        f"{len(anomaly_df)} anomalies detected"
    )


if __name__ == "__main__":
    main()