
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

DB_PATH = ROOT / "database" / "healthcare.db"
SQL_PATH = ROOT / "sql" / "01_healthcare_analysis.sql"
REPORTS_DIR = ROOT / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

# Read SQL statements from the file
sql_text = SQL_PATH.read_text(encoding="utf-8")

# Split the four SQL statements
queries = [
    q.strip()
    for q in sql_text.split(";")
    if q.strip()
]

print(f"SQL file: {SQL_PATH}")
print(f"SQL file size: {len(sql_text)} characters")
print(f"Number of SQL queries found: {len(queries)}")

if len(queries) != 4:
    raise ValueError(
        f"Expected 4 SQL queries, but found {len(queries)}. "
        "Check and save sql/01_healthcare_analysis.sql."
    )

report_names = [
    "no_show_by_gender",
    "no_show_by_age_group",
    "no_show_by_neighbourhood",
    "no_show_by_waiting_group"
]

with sqlite3.connect(DB_PATH) as conn:
    for i, query in enumerate(queries):
        result = pd.read_sql_query(query, conn)

        print(f"\n=== ANALYSIS {i + 1} ===")
        print(result.to_string(index=False))

        output = REPORTS_DIR / f"{report_names[i]}.csv"
        result.to_csv(output, index=False)

        print(f"Saved: {output.name}")

print("\nALL SQL ANALYSES COMPLETED!")
