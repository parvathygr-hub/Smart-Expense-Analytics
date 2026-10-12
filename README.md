# Smart Expense & Financial Analytics Web Application

A web-based personal finance application built with Python, Flask, and MySQL to record transactions, track income and expenses, and understand spending patterns through data analysis and visualizations.

## Features

- **Financial Dashboard:** View total income, total expenses, and available balance.
- **Transaction Management:** Add, view, edit, and delete financial transactions.
- **Search and Filtering:** Find transactions by keyword, type, and category.
- **Spending Insights:** Identify the highest spending category and average expense.
- **Category-wise Analysis:** Visualize expenses by category using Matplotlib.
- **Monthly Expense Trends:** Understand how expenses change over time.
- **Database Integration:** Store transaction records in MySQL.

## Technologies Used

- Python
- Flask
- MySQL
- Pandas
- Matplotlib
- HTML
- CSS

## Project Structure

```text
Smart-Expense-Analytics/
├── app.py
├── database.py
├── analytics.py
├── requirements.txt
├── .gitignore
├── .env                 # Local credentials; not committed
├── templates/
│   ├── index.html
│   ├── add_transaction.html
│   ├── transactions.html
│   ├── edit_transaction.html
│   └── analytics.html
└── static/
    ├── style.css
    ├── category_expenses.png
    └── monthly_expenses.png
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Smart-Expense-Analytics
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=expense_tracker
```

Replace the password placeholder with your own local MySQL password. Never commit `.env` to GitHub.

### 5. Create the MySQL database and table

Run the following SQL in MySQL Workbench:

```sql
CREATE DATABASE IF NOT EXISTS expense_tracker;

USE expense_tracker;

CREATE TABLE IF NOT EXISTS transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    type VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(100),
    amount DECIMAL(10,2) NOT NULL
);
```

### 6. Run the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Data Analysis

Pandas is used to calculate financial summaries, category-wise spending, monthly expense totals, and spending insights. Matplotlib generates charts that help users understand their financial data.

## Screenshots

Add screenshots of the dashboard, transaction list, and financial analytics page here.

## Future Improvements

- Date-range filters for financial reports
- Export reports to CSV or Excel
- Monthly budgets and spending alerts
- Improved interactive visualizations

## Author

Parvathy GR

B.Tech Computer Science Engineering Graduate | 2026

## Disclaimer

This is an educational portfolio project. Use sample financial data when sharing screenshots publicly.