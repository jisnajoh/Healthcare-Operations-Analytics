
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

CSV_PATH = (
    ROOT / "data" / "cleaned"
    / "medical_appointments_cleaned.csv"
)

DB_PATH = ROOT / "database" / "healthcare.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Read cleaned data
df = pd.read_csv(
    CSV_PATH,
    dtype={"patient_id": "string"}
)

print("Loaded records:", len(df))

# Connect to SQLite database
with sqlite3.connect(DB_PATH) as conn:

    # Create appointments table
    df.to_sql(
        "appointments",
        conn,
        if_exists="replace",
        index=False
    )

    # Verify inserted records
    result = conn.execute(
        "SELECT COUNT(*) FROM appointments"
    ).fetchone()[0]

    print("Database records:", result)

    # First healthcare analytics SQL query
    query = """
    SELECT
        COUNT(*) AS total_appointments,
        SUM(no_show) AS missed_appointments,
        ROUND(AVG(no_show) * 100, 2)
            AS no_show_rate_percent,
        ROUND(AVG(waiting_days), 2)
            AS average_waiting_days
    FROM appointments;
    """

    summary = pd.read_sql_query(query, conn)

    print("\n=== HEALTHCARE KPI SUMMARY ===")
    print(summary.to_string(index=False))

print("\nDatabase created successfully!")
print("Location:", DB_PATH)
