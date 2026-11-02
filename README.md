
# Healthcare Operations Analytics

## Project Overview
This project analyzes 110,521 medical appointment records to identify patterns in missed appointments, scheduling lead times, and patient attendance.

The project demonstrates an end-to-end data analytics workflow using Python, SQL, SQLite, and Power BI.

## Tools and Technologies
- Python
- Pandas
- SQL and SQLite
- Power BI
- DAX
- Visual Studio Code

## Project Workflow
1. Inspect the raw healthcare appointment dataset.
2. Clean and validate records using Python and Pandas.
3. Store the cleaned dataset in SQLite.
4. Analyze appointment trends using SQL.
5. Build an interactive Power BI dashboard.
6. Document findings and operational recommendations.

## Key Performance Indicators

| KPI | Result |
|---|---|
| Total Appointments | 110,521 |
| Missed Appointments | 22,314 |
| No-Show Rate | 20.19% |
| Average Scheduling Lead Time | 10.18 days |

## Dashboard Features
- Appointment volume by neighbourhood
- Missed appointments by neighbourhood
- No-show rates by neighbourhood
- No-show rates by scheduling lead time
- No-show rates by SMS reminder status
- Interactive neighbourhood and SMS status filters

## Power BI Dashboard
![Healthcare Operations Dashboard](images/healthcare_dashboard.png)

## Key Findings
- Approximately one in five appointments was missed.
- Longer scheduling lead times were associated with higher no-show rates.
- No-show rates differed across neighbourhoods.
- Appointments with recorded SMS reminders had a higher observed no-show rate than appointments without recorded reminders. This is an association, not evidence that reminders cause missed appointments.

## Recommendations
- Review appointments scheduled far in advance.
- Investigate differences in reminder delivery and patient populations.
- Prioritize follow-up analysis in neighbourhoods with higher no-show rates.
- Evaluate potential interventions before making causal claims.

## Project Structure
- `data/` — Raw and cleaned datasets
- `scripts/` — Python processing and database scripts
- `sql/` — SQL analysis queries
- `database/` — SQLite database
- `dashboards/` — Power BI dashboard
- `reports/` — Data quality and analytical CSV reports

## Data Source
Medical Appointment No Shows dataset (Kaggle).

## Limitations
The analysis is observational. Relationships between scheduling lead time, SMS reminders, neighbourhood, and no-show rates should not be interpreted as causal effects.
  