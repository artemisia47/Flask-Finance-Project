import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

app = Flask(__name__)
app.jinja_env.filters["usd"] = usd
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Enhanced security
# Uncomment the next line if using HTTPS
# app.config["SESSION_COOKIE_SECURE"] = True
Session(app)

# Create a function to get a connection to the SQLite database
def get_db():
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row  # Allows us to access columns by name
    return conn

# Initialize tables if they don't exist
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL,
            cash NUMERIC DEFAULT 10000.00
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL,
            price NUMERIC NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    # Use the get_db function to connect to the database
    with get_db() as conn:
        user_cash = conn.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchone()["cash"]
        holdings = conn.execute("""
            SELECT symbol, SUM(shares) as total_shares
            FROM history
            WHERE user_id = ?
            GROUP BY symbol
            HAVING total_shares > 0
        """, (session["user_id"],)).fetchall()

    total_portfolio_value = user_cash
    # Convert the sqlite3.Row objects to dictionaries for item assignment
    holdings_list = []
    for holding in holdings:
        holding_dict = dict(holding)  # Convert the Row object to a dictionary
        quote_result = lookup(holding_dict["symbol"])
        if quote_result:  # Check if the quote_result is not None
            holding_dict["name"] = quote_result["name"]
            holding_dict["price"] = quote_result["price"]
            holding_dict["total_value"] = holding_dict["total_shares"] * quote_result["price"]
            total_portfolio_value += holding_dict["total_value"]
        holdings_list.append(holding_dict)

    return render_template("index.html", user_cash=user_cash, holdings=holdings_list, total_portfolio_value=total_portfolio_value)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("must provide username and password", 403)

        with get_db() as conn:
            rows = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        flash('Logged in successfully!', 'success')  # Provide user feedback
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must confirm password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        hashed_password = generate_password_hash(password)

        try:
            with get_db() as conn:
                conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed_password))
                session["user_id"] = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()["id"]
            flash('Registered successfully!', 'success')
            return redirect("/")
        except sqlite3.IntegrityError:
            return apology("username already exists", 400)
    else:
        return render_template("register.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide stock symbol", 400)

        quote_result = lookup(symbol)
        if not quote_result:
            return apology("stock symbol not found", 400)

        return render_template("quoted.html", quote=quote_result)
    else:
        return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_str = request.form.get("shares")

        if not symbol:
            return apology("must provide stock symbol", 400)
        if not shares_str:
            return apology("must provide number of shares", 400)

        try:
            shares = int(shares_str)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("number of shares must be a positive integer", 400)

        quote_result = lookup(symbol)
        if not quote_result:
            return apology("stock symbol not found", 400)

        total_cost = shares * quote_result["price"]

        with get_db() as conn:
            user_cash = conn.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],)).fetchone()["cash"]

        if total_cost > user_cash:
            return apology("insufficient funds", 400)

        with get_db() as conn:
            conn.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (total_cost, session["user_id"]))
            conn.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                        (session["user_id"], quote_result["symbol"], shares, quote_result["price"]))
        flash('Purchased successfully!', 'success')  # Provide user feedback
        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_str = request.form.get("shares")

        if not symbol:
            return apology("must provide stock symbol", 400)
        if not shares_str:
            return apology("must provide number of shares", 400)

        try:
            shares = int(shares_str)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("number of shares must be a positive integer", 400)

        quote_result = lookup(symbol)
        if not quote_result:
            return apology("stock symbol not found", 400)

        with get_db() as conn:
            user_holdings = conn.execute("""
                SELECT SUM(shares) as total_shares
                FROM history
                WHERE user_id = ? AND symbol = ?
                GROUP BY symbol
            """, (session["user_id"], quote_result["symbol"])).fetchone()

        if not user_holdings or user_holdings["total_shares"] < shares:
            return apology("insufficient shares to sell", 400)

        total_sale_value = shares * quote_result["price"]

        with get_db() as conn:
            conn.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (total_sale_value, session["user_id"]))
            conn.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                        (session["user_id"], quote_result["symbol"], -shares, quote_result["price"]))
        flash('Sold successfully!', 'success')  # Provide user feedback
        return redirect("/")
    else:
        with get_db() as conn:
            symbols = conn.execute("""
                SELECT symbol
                FROM history
                WHERE user_id = ?
                GROUP BY symbol
                HAVING SUM(shares) > 0
            """, (session["user_id"],)).fetchall()
        return render_template("sell.html", holdings=symbols)

@app.route("/history")
@login_required
def history():
    # Fetch the transactions from the database
    with get_db() as conn:
        transactions = conn.execute("""
            SELECT symbol, shares, price, timestamp
            FROM history
            WHERE user_id = ?
        """, (session["user_id"],)).fetchall()

    # Convert sqlite3.Row to a dictionary for each transaction
    for transaction in transactions:
        transaction_dict = dict(transaction)  # Convert Row object to dictionary
        quote_result = lookup(transaction_dict["symbol"])
        transaction_dict["name"] = quote_result["name"] if quote_result else "Unknown"
        # Replace the original transaction with the updated dictionary
        transaction = transaction_dict

    return render_template("history.html", transactions=transactions)


@app.route("/logout")
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')  # Provide user feedback
    return redirect("/login")
