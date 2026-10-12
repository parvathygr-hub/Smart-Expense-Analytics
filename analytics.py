import pandas as pd
from database import get_connection


def get_transactions_data():
    connection = get_connection()

    try:
        query = "SELECT * FROM transactions"
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()


def get_financial_summary():
    df = get_transactions_data()

    total_income = df.loc[
        df["type"] == "income", "amount"
    ].sum()

    total_expenses = df.loc[
        df["type"] == "expense", "amount"
    ].sum()

    balance = total_income - total_expenses

    print("\n===== FINANCIAL SUMMARY =====")
    print(f"Total Income: ₹{total_income:.2f}")
    print(f"Total Expenses: ₹{total_expenses:.2f}")
    print(f"Balance: ₹{balance:.2f}")

def get_category_expenses():

    df = get_transactions_data()

    expenses = df[df["type"] == "expense"]

    category_totals = expenses.groupby("category")["amount"].sum()

    print("\n===== CATEGORY-WISE EXPENSES =====")

    print(category_totals)

def get_monthly_expenses():

    df = get_transactions_data()

    # Keep only expense transactions
    expenses = df[df["type"] == "expense"].copy()

    # Convert date column to datetime
    expenses["date"] = pd.to_datetime(expenses["date"])

    # Extract month and year
    expenses["month"] = expenses["date"].dt.to_period("M")

    # Calculate monthly spending
    monthly_totals = expenses.groupby("month")["amount"].sum()

    print("\n===== MONTHLY EXPENSES =====")
    print(monthly_totals)

def get_spending_insights():

    df = get_transactions_data()

    expenses = df[df["type"] == "expense"]

    if expenses.empty:
        print("\nNo expenses available for analysis.")
        return

    # Total spending by category
    category_totals = expenses.groupby("category")["amount"].sum()

    # Find the highest spending category
    highest_category = category_totals.idxmax()
    highest_amount = category_totals.max()

    # Calculate average expense transaction
    average_expense = expenses["amount"].mean()

    print("\n===== SPENDING INSIGHTS =====")
    print(f"Highest Spending Category: {highest_category}")
    print(f"Amount Spent in This Category: ₹{highest_amount:.2f}")
    print(f"Average Expense: ₹{average_expense:.2f}")

def create_category_chart():
    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    import os

    df = get_transactions_data()

    expenses = df[df["type"] == "expense"]

    if expenses.empty:
        print("No expenses available to create a chart.")
        return

    category_totals = expenses.groupby("category")["amount"].sum()

    # Create the chart
    plt.figure(figsize=(8, 5))
    category_totals.plot(
        kind="bar",
        color="#2878B5",
        edgecolor="white"
    )

    plt.title("Category-wise Expenses")
    plt.xlabel("Expense Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the chart inside the Flask static folder
    chart_path = os.path.join(
        os.path.dirname(__file__),
        "static",
        "category_expenses.png"
    )

    plt.savefig(chart_path, dpi=150)
    plt.close()

    print("Category expense chart created successfully!")
    print("Saved to:", chart_path)


def create_monthly_chart():
    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    import os
    import pandas as pd

    df = get_transactions_data()
    expenses = df[df["type"] == "expense"].copy()

    if expenses.empty:
        print("No expenses available for a monthly chart.")
        return

    expenses["date"] = pd.to_datetime(expenses["date"])
    expenses["month"] = expenses["date"].dt.to_period("M").astype(str)

    monthly_totals = expenses.groupby("month")["amount"].sum()

    plt.figure(figsize=(8, 5))
    plt.plot(
        monthly_totals.index,
        monthly_totals.values,
        marker="o",
        linewidth=2,
        color="#2878B5"
    )

    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Expenses (₹)")
    plt.xticks(rotation=30)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    chart_path = os.path.join(
        os.path.dirname(__file__),
        "static",
        "monthly_expenses.png"
    )

    plt.savefig(chart_path, dpi=150)
    plt.close()

    print("Monthly expense chart created successfully!")
    print("Saved to:", chart_path)

if __name__ == "__main__":
    get_financial_summary()
    get_category_expenses()
    get_monthly_expenses()
    get_spending_insights()
    create_category_chart()
    create_monthly_chart()