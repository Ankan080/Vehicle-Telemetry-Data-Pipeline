import subprocess
import sys

from src.logger_config import get_logger

logger = get_logger("vehicle_pipeline")


def run_step(script):
    print("\n" + "=" * 60)
    print(f"RUNNING: {script}")
    print("=" * 60)

    logger.info(f"Pipeline step started: {script}")

    try:
        module = script.replace("/", ".").replace("\\", ".").replace(".py", "")
        result = subprocess.run(
            [sys.executable, "-m", module],
            check=True
        )

        logger.info(f"Pipeline step completed: {script}")

        return result.returncode

    except subprocess.CalledProcessError as error:
        logger.error(
            f"Pipeline step failed: {script} | "
            f"Return code: {error.returncode}"
        )

        print(f"\nERROR: Pipeline step failed: {script}")
        print("Pipeline execution stopped.")

        sys.exit(error.returncode)


def main():
    logger.info("Complete vehicle telemetry pipeline started.")

    steps = [
        "src/generate_data.py",
        "src/validate.py",
        "src/transform.py",
        "src/anomaly_detection.py",
        "src/analyze_anomalies.py",
        "src/create_anomaly_summary.py"
    ]

    for step in steps:
        run_step(step)

    logger.info("Complete vehicle telemetry pipeline completed successfully.")

    print("\n" + "=" * 60)
    print("VEHICLE TELEMETRY PIPELINE COMPLETED")
    print("PIPELINE STATUS: SUCCESS")
    print("=" * 60)


if __name__ == "__main__":
    main()