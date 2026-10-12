import pandas as pd
from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)


# =========================
# Dashboard
# =========================

@app.route("/")
def home():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) "
        "FROM transactions WHERE type = 'income'"
    )

    total_income = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) "
        "FROM transactions WHERE type = 'expense'"
    )

    total_expenses = cursor.fetchone()[0]

    balance = total_income - total_expenses

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance
    )


# =========================
# Add Transaction
# =========================

@app.route("/add-transaction", methods=["GET", "POST"])
def add_transaction():

    if request.method == "POST":

        transaction_type = request.form.get("type")
        category = request.form.get("category")
        amount = request.form.get("amount")
        date = request.form.get("date")
        description = request.form.get("description")

        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO transactions
        (date, type, category, description, amount)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            date,
            transaction_type,
            category,
            description,
            amount
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

        return "Transaction saved successfully!"

    return render_template("add_transaction.html")


# =========================
# View + Search + Filter
# =========================

@app.route("/transactions")
def transactions():

    search = request.args.get("search", "")
    selected_type = request.args.get("type", "")
    selected_category = request.args.get("category", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM transactions
    WHERE 1=1
    """

    values = []

    # Search
    if search:

        query += """
        AND (
            category LIKE %s
            OR description LIKE %s
            OR type LIKE %s
        )
        """

        search_value = "%" + search + "%"

        values.extend([
            search_value,
            search_value,
            search_value
        ])

    # Type filter
    if selected_type:

        query += " AND type = %s"

        values.append(selected_type)

    # Category filter
    if selected_category:

        query += " AND category = %s"

        values.append(selected_category)

    query += " ORDER BY date DESC"

    cursor.execute(query, values)

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "transactions.html",
        transactions=transactions,
        search=search,
        selected_type=selected_type,
        selected_category=selected_category
    )


# =========================
# Edit Transaction
# =========================

@app.route("/edit-transaction/<int:id>", methods=["GET", "POST"])
def edit_transaction(id):

    connection = get_connection()

    if request.method == "POST":

        transaction_type = request.form.get("type")
        category = request.form.get("category")
        amount = request.form.get("amount")
        date = request.form.get("date")
        description = request.form.get("description")

        cursor = connection.cursor()

        query = """
        UPDATE transactions
        SET type = %s,
            category = %s,
            amount = %s,
            date = %s,
            description = %s
        WHERE id = %s
        """

        values = (
            transaction_type,
            category,
            amount,
            date,
            description,
            id
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

        return "Transaction updated successfully!"

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM transactions WHERE id = %s",
        (id,)
    )

    transaction = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_transaction.html",
        transaction=transaction
    )


# =========================
# Delete Transaction
# =========================

@app.route("/delete-transaction/<int:id>")
def delete_transaction(id):

    connection = get_connection()
    cursor = connection.cursor()

    query = "DELETE FROM transactions WHERE id = %s"

    cursor.execute(query, (id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/transactions")


# =========================
# Run Flask
# =========================

# =========================
# Financial Analytics
# =========================

@app.route("/analytics")
def analytics():

    connection = get_connection()

    try:
        df = pd.read_sql(
            "SELECT * FROM transactions",
            connection
        )
    finally:
        connection.close()

    income = df[df["type"] == "income"]["amount"].sum()
    expenses = df[df["type"] == "expense"].copy()

    total_expenses = expenses["amount"].sum()
    balance = income - total_expenses

    if not expenses.empty:
        category_totals = expenses.groupby("category")["amount"].sum()
        highest_category = category_totals.idxmax()
        highest_amount = category_totals.max()
        average_expense = expenses["amount"].mean()

        expenses["date"] = pd.to_datetime(expenses["date"])
        expenses["month"] = expenses["date"].dt.to_period("M").astype(str)

        monthly_expenses = (
            expenses.groupby("month")["amount"]
            .sum()
            .to_dict()
        )

    else:
        highest_category = "No expenses yet"
        highest_amount = 0
        average_expense = 0
        monthly_expenses = {}

    return render_template(
        "analytics.html",
        total_income=round(float(income), 2),
        total_expenses=round(float(total_expenses), 2),
        balance=round(float(balance), 2),
        highest_category=highest_category,
        highest_amount=round(float(highest_amount), 2),
        average_expense=round(float(average_expense), 2),
        monthly_expenses=monthly_expenses
    )

if __name__ == "__main__":
    app.run(debug=True)