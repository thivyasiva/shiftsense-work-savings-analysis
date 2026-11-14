"""ShiftSense — Work & Savings Analysis.

Solo project. Reads a CSV of shifts (date, start_time, end_time,
hourly_rate, expenses), calculates hours, income and estimated
savings per shift with pandas, and summarises weekday and
shift-length trends.

Usage:
    python3 shiftsense.py [--input shifts.csv] [--output summary.csv]
"""
import argparse
from datetime import datetime, timedelta

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="ShiftSense — work and savings analysis")
    parser.add_argument("--input", default="shifts.csv", help="Input shifts CSV (default: shifts.csv)")
    parser.add_argument("--output", default="summary.csv", help="Output summary CSV (default: summary.csv)")
    return parser.parse_args()


def load_shifts(path):
    df = pd.read_csv(path)
    required = {"date", "start_time", "end_time", "hourly_rate", "expenses"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in {path}: {sorted(missing)}")
    df["date"] = pd.to_datetime(df["date"])
    df["hourly_rate"] = pd.to_numeric(df["hourly_rate"])
    df["expenses"] = pd.to_numeric(df["expenses"]).fillna(0)

    def shift_hours(row):
        start = datetime.combine(row["date"].date(), datetime.strptime(str(row["start_time"]), "%H:%M").time())
        end = datetime.combine(row["date"].date(), datetime.strptime(str(row["end_time"]), "%H:%M").time())
        if end <= start:  # overnight shift
            end += timedelta(days=1)
        return (end - start).total_seconds() / 3600

    df["hours"] = df.apply(shift_hours, axis=1)
    df["income"] = (df["hours"] * df["hourly_rate"]).round(2)
    df["savings"] = (df["income"] - df["expenses"]).round(2)
    df["weekday"] = df["date"].dt.day_name()
    df["shift_length"] = pd.cut(
        df["hours"], bins=[0, 4, 8, 24], labels=["Short (<=4h)", "Standard (4-8h)", "Long (>8h)"]
    )
    return df


def main():
    args = parse_args()
    df = load_shifts(args.input)

    total_hours = df["hours"].sum()
    total_income = df["income"].sum()
    total_expenses = df["expenses"].sum()
    total_savings = df["savings"].sum()

    print("ShiftSense — Work & Savings Summary")
    print(f"Shifts analysed: {len(df)}")
    print(f"Total hours: {total_hours:.2f}")
    print(f"Total income: ${total_income:,.2f}")
    print(f"Total expenses: ${total_expenses:,.2f}")
    print(f"Estimated savings: ${total_savings:,.2f}")
    print(f"Average income per shift: ${df['income'].mean():,.2f}")
    print()
    print("Average income by weekday:")
    print(df.groupby("weekday")["income"].mean().round(2).to_string())
    print()
    print("Average hours and income by shift length:")
    print(df.groupby("shift_length", observed=True).agg(
        shifts=("hours", "size"),
        avg_hours=("hours", "mean"),
        avg_income=("income", "mean"),
    ).round(2).to_string())

    summary = df.groupby("weekday", as_index=False).agg(
        shifts=("hours", "size"),
        total_hours=("hours", "sum"),
        total_income=("income", "sum"),
        total_expenses=("expenses", "sum"),
        total_savings=("savings", "sum"),
    )
    summary.to_csv(args.output, index=False)
    print(f"\nWeekday summary written to {args.output}")


if __name__ == "__main__":
    main()
