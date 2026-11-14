# ShiftSense — Work & Savings Analysis

Solo project by Thivya Siva — Toronto Metropolitan University, Bachelor of Commerce, Business Technology Management (minor in Computer Science), expected April 2027.

A Python / pandas application that analyses working hours, income, expenses and estimated savings from shift records, and calculates weekday and shift-length trends.

## What it does

Given a CSV of shifts — date, start time, end time, hourly rate and expenses — ShiftSense:

- calculates hours worked, income and savings per shift
- summarises total hours, income, expenses and estimated savings
- calculates average income by weekday
- calculates average hours and income by shift length (short / standard / long)
- prints a clear text summary and writes a summary CSV

## Skills

Python, pandas, data cleaning, grouping and aggregation, CSV input/output.

## Input format

`shifts.csv` — one row per shift:

| Column | Example | Description |
| --- | --- | --- |
| `date` | `2026-10-05` | Shift date (YYYY-MM-DD) |
| `start_time` | `09:00` | Shift start (HH:MM, 24-hour) |
| `end_time` | `17:00` | Shift end (HH:MM, 24-hour; overnight shifts ending after midnight are supported) |
| `hourly_rate` | `18.50` | Pay per hour |
| `expenses` | `12.00` | Expenses for that shift (e.g. transport, food); use `0` if none |

A sample file is included at `shifts.csv`. It is synthetic sample data, provided so the script can be run as-is.

## How to run

```bash
pip install -r requirements.txt
python3 shiftsense.py
```

By default it reads `shifts.csv` in the same folder and writes `summary.csv`.

To analyse your own file:

```bash
python3 shiftsense.py --input my_shifts.csv --output my_summary.csv
```

## Example output

```
ShiftSense — Work & Savings Summary
Shifts analysed: 10
Total hours: 70.50
Total income: $1,322.25
Total expenses: $98.00
Estimated savings: $1,224.25
Average income per shift: $132.22
...
```

## Files

| File | Description |
| --- | --- |
| `shiftsense.py` | The analysis application |
| `shifts.csv` | Synthetic sample shift data |
| `requirements.txt` | Python dependencies (pandas) |
