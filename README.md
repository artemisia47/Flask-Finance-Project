# Flask-Finance-Project

A web application that allows users to manage a simulated stock portfolio by buying, selling, and tracking stocks in real time.
This project is part of the CS50 curriculum.

## Features

* User Authentication: Secure login and registration with hashed passwords.
* Stock Trading: Buy and sell stocks with real-time price updates via the Alpha Vantage API.
* Portfolio Management: Track holdings and cash balance.
* Transaction History: View past trades and track portfolio changes over time.
* Responsive UI: Designed with Bootstrap for a clean and user-friendly experience.

### Tech Stack

* Backend: Flask (Python)
* Frontend: HTML, CSS, Jinja, Bootstrap
* Database: SQLite
* APIs: Alpha Vantage for stock data
* Security: Hashed passwords, session-based authentication

### Installation

Clone the repository:

```bash
git clone https://github.com/your-username/unreal-finance.git
cd unreal-finance
```

Create a virtual environment and install dependencies:
```bash 
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -r requirements.txt
```
Get an Alpha Vantage API key and update helpers.py:

Change API KEY on helpers.py script to your actual API key. 

API_KEY = "your_api_key_here" 

Run the application:

```bash
flask run  # Initializes SQLite and starts the server
```


### Usage

* Register and log in to your account.
* Search for stock quotes and view real-time prices.
* Buy stocks if you have enough balance.
* Sell stocks from your portfolio.
* View your transaction history.

### Screenshots



