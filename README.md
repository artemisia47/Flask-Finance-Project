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

![Screenshot 2025-03-08 230418](https://github.com/user-attachments/assets/8381ae88-1480-4bd3-8e8e-2d6f4c16a6f0)
![Screenshot 2025-03-08 230430](https://github.com/user-attachments/assets/a594f3bc-237a-4536-97a4-dd930ea1f946)
![Screenshot 2025-03-08 230436](https://github.com/user-attachments/assets/faa6c705-3a40-42e3-aa78-ccb4e398ed3f)
![Screenshot 2025-03-08 230441](https://github.com/user-attachments/assets/9b6bd6fc-8671-4a75-b3c3-42ddf9abdc1d)
![Screenshot 2025-03-08 230511](https://github.com/user-attachments/assets/f9e3b2d7-e874-421a-b992-45dd23333a58)
