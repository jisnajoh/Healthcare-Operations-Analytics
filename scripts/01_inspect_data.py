
from pathlib import Path
import pandas as pd

# Find the project root from the location of this script.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define input and output paths.
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "medical_appointments.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}\n"
        "Download the Kaggle CSV and rename it to medical_appointments.csv"
    )

# 1. Load the dataset.
df = pd.read_csv(DATA_PATH)

# 2. Inspect the dataset.
print("\n=== HEALTHCARE APPOINTMENT DATA ===")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\n=== FIRST FIVE ROWS ===")
print(df.head().to_string(index=False))

print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

print("\n=== DATA TYPES ===")
print(df.dtypes.to_string())

# 3. Check missing values and duplicates.
missing = df.isna().sum().sort_values(ascending=False)
duplicate_rows = df.duplicated().sum()

print("\n=== MISSING VALUES ===")
print(missing.to_string())

print(f"\nExact duplicate rows: {duplicate_rows:,}")

# 4. Check the no-show outcome, if available.
if "No-show" in df.columns:
    print("\n=== NO-SHOW DISTRIBUTION ===")
    print(df["No-show"].value_counts(dropna=False).to_string())

    valid = df["No-show"].astype("string").str.strip().str.lower()
    known = valid.isin(["yes", "no"])

    if known.any():
        no_show_rate = (valid[known] == "yes").mean() * 100
        print(f"\nNo-show rate among valid Yes/No rows: {no_show_rate:.2f}%")

# 5. Save a basic data-quality report.
quality = pd.DataFrame({
    "column": df.columns,
    "data_type": df.dtypes.astype(str).values,
    "missing_count": df.isna().sum().values,
    "missing_percent": (
        df.isna().mean().values * 100
    ).round(2),
    "unique_values": df.nunique(dropna=True).values
})

report_path = REPORTS_DIR / "data_quality_report.csv"
quality.to_csv(report_path, index=False)

print(f"\nData-quality report saved to: {report_path}")
print("\nDAY 1 INSPECTION COMPLETED!")
