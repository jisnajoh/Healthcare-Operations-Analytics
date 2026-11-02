
from pathlib import Path
import pandas as pd

# Project paths
ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = ROOT / "data" / "raw" / "medical_appointments.csv"
CLEAN_DIR = ROOT / "data" / "cleaned"
REPORT_DIR = ROOT / "reports"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load original dataset
df = pd.read_csv(RAW_FILE)
print("Original rows:", len(df))

# Standardize column names
df = df.rename(columns={
    "PatientId": "patient_id",
    "AppointmentID": "appointment_id",
    "Gender": "gender",
    "ScheduledDay": "scheduled_day",
    "AppointmentDay": "appointment_day",
    "Age": "age",
    "Neighbourhood": "neighbourhood",
    "Scholarship": "scholarship",
    "Hipertension": "hypertension",
    "Diabetes": "diabetes",
    "Alcoholism": "alcoholism",
    "Handcap": "handicap",
    "SMS_received": "sms_received",
    "No-show": "no_show"
})

# Convert dates to datetime
df["scheduled_day"] = pd.to_datetime(
    df["scheduled_day"], errors="coerce", utc=True
)
df["appointment_day"] = pd.to_datetime(
    df["appointment_day"], errors="coerce", utc=True
)

# Convert Yes/No into numeric values
outcomes = (
    df["no_show"]
    .astype("string")
    .str.strip()
    .str.lower()
)

df["no_show"] = outcomes.map({
    "yes": 1,
    "no": 0
})

# Calculate scheduling lead time in calendar days
df["waiting_days"] = (
    df["appointment_day"].dt.normalize()
    - df["scheduled_day"].dt.normalize()
).dt.days

# Identify invalid records before cleaning
invalid_age = df["age"] < 0
invalid_dates = (
    df["scheduled_day"].isna()
    | df["appointment_day"].isna()
    | (df["waiting_days"] < 0)
)
invalid_outcome = df["no_show"].isna()

duplicate_appointments = df["appointment_id"].duplicated(
    keep=False
)

print("\n=== DATA VALIDATION ===")
print("Negative ages:", invalid_age.sum())
print("Invalid dates:", invalid_dates.sum())
print("Invalid no-show values:", invalid_outcome.sum())
print("Rows with duplicate appointment IDs:",
      duplicate_appointments.sum())

print("\n=== AGE STATISTICS ===")
print(df["age"].describe())

print("\n=== WAITING DAYS STATISTICS ===")
print(df["waiting_days"].describe())

# Save invalid records separately for review
invalid = (
    invalid_age
    | invalid_dates
    | invalid_outcome
    | duplicate_appointments
)

df.loc[invalid].to_csv(
    REPORT_DIR / "invalid_records.csv",
    index=False
)

# Create cleaned dataset without invalid records
clean_df = df.loc[~invalid].copy()

# Convert outcome to integer
clean_df["no_show"] = clean_df["no_show"].astype(int)

# Save cleaned dataset
output_path = CLEAN_DIR / "medical_appointments_cleaned.csv"
clean_df.to_csv(output_path, index=False)

print("\n=== CLEANING SUMMARY ===")
print("Original rows:", len(df))
print("Flagged rows:", invalid.sum())
print("Cleaned rows:", len(clean_df))
print("No-show rate:",
      round(clean_df["no_show"].mean() * 100, 2), "%")
print("Cleaned file:", output_path)

print("\nDAY 2 CLEANING COMPLETED!")
