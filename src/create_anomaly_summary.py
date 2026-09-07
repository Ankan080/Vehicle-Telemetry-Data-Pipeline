import pandas as pd
from pathlib import Path
from src.logger_config import get_logger
from src.config import ANOMALY_REPORT, ANOMALY_SUMMARY

logger = get_logger()


INPUT_FILE = ANOMALY_REPORT
OUTPUT_FILE = ANOMALY_SUMMARY


def main():

    print("=" * 60)
    print("CREATING ANOMALY SUMMARY")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)
    
    logger.info(
        f"Anomaly summary started: "
        f"{len(df)} anomaly records loaded"
    )

    if df.empty:
        print("No anomalies available.")
        return

    # Count anomalies by parameter and severity
    summary = (
        df.groupby(
            ["parameter", "anomaly_type", "severity"]
        )
        .size()
        .reset_index(name="anomaly_count")
    )

    # Sort from highest to lowest
    summary = summary.sort_values(
        by="anomaly_count",
        ascending=False
    )

    # Save report
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    summary.to_csv(
        OUTPUT_FILE,
        index=False
    )
    
    logger.info(
        f"Anomaly summary saved: "
        f"{OUTPUT_FILE} | "
        f"{len(summary)} anomaly categories"
    )

    print("\nAnomaly summary:")

    print(summary.to_string(index=False))

    print("\nSummary saved to:")
    print(OUTPUT_FILE)

    print("\n" + "=" * 60)
    print("ANOMALY SUMMARY CREATED")
    print("=" * 60)


if __name__ == "__main__":
    main()