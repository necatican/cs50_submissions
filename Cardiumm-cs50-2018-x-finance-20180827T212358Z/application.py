import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    rowlist = []
    cash = db.execute("SELECT cash FROM users WHERE id = :usrid", usrid=user_id)
    cash = float(cash[0]["cash"])
    networth = cash
    rows = db.execute("""SELECT stocks.symbol, stocks.name, sum(portfolio.shares) AS shares
    FROM users JOIN portfolio ON portfolio.user_id = users.id JOIN stocks
    ON portfolio.stock_id = stocks.id WHERE users.id = :usrid GROUP BY stocks.symbol""", usrid=user_id)
    for row in rows:
        symbol = row["symbol"]
        stockname = row["name"]
        sharecount = row["shares"]
        lookup_result = lookup(symbol.upper())
        price = float(lookup_result["price"])
        totalprice = price * int(sharecount)
        networth += totalprice

        if sharecount != 0:
            rowlist.append([symbol, stockname, sharecount, usd(price), usd(totalprice)])
    rowlist.append(["CASH", "", "", "", usd(cash)])

    return render_template("index.html", rows=rowlist, networth=usd(networth))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol") or not request.form.get("shares") or not request.form.get("shares").isdigit():
            return apology("Missing fields", 400)
        elif float(request.form.get("shares")) % 1 != 0 or int(request.form.get("shares")) < 1:
            return apology("Wrong share count", 400)
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        if len(symbol) > 5:
            return apology("Invalid ticker symbol")
        if not lookup(symbol.upper()):
            return apology("Invalid ticker")
        lookup_result = lookup(symbol.upper())
        if len(lookup_result) != 3:
            return apology("Invalid ticker")
        lookup_result = lookup(symbol)
        price = float(lookup_result["price"])
        name = lookup_result["name"]
        user_id = usrid = session["user_id"]

        user_row = db.execute("SELECT * FROM users WHERE id = :usrid", usrid=user_id)
        user_cash = int(user_row[0]["cash"])
        if user_cash < price * shares:
            return apology("Not enough cash", 400)
        else:
            user_cash -= price * shares
        stock_row = db.execute("SELECT * FROM stocks WHERE symbol = :symbol", symbol=symbol)
        if len(stock_row) == 0:
            db.execute("INSERT INTO stocks(id, symbol, name) VALUES (NULL, :symbol, :name)", symbol=symbol, name=name)
            stock_row = db.execute("SELECT * FROM stocks WHERE symbol = :symbol", symbol=symbol)
        stock_id = stock_row[0]["id"]
        db.execute("""INSERT INTO portfolio(stock_id, user_id, shares, price)
        VALUES (:stock, :usr, :share, :price)""", stock=stock_id, usr=user_id, share=shares, price=price * -1)
        db.execute("UPDATE users SET cash = :cash WHERE id = :usrid", cash=user_cash, usrid=user_id)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rowlist = []
    rows = db.execute("""SELECT stocks.symbol, stocks.name, portfolio.shares, portfolio.date, portfolio.price
    FROM stocks JOIN portfolio ON portfolio.stock_id = id
    WHERE portfolio.user_id = :usrid ORDER BY portfolio.date DESC""", usrid=session["user_id"])
    for row in rows:
        symbol = row["symbol"]
        stockname = row["name"]
        sharecount = row["shares"]
        date = row["date"]
        price = row["price"]
        rowlist.append([symbol, stockname, sharecount, date, usd(price)])
    return render_template("history.html", rows=rowlist)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """ Quotes a share"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Incorrect quote symbol")
        quote_symbol = request.form.get("symbol")
        # Longest ticker symbol length
        if len(quote_symbol) > 5:
            return apology("Invalid ticker symbol")
        if not lookup(quote_symbol.upper()):
            return apology("Invalid ticker")
        lookup_result = lookup(quote_symbol.upper())
        if len(lookup_result) != 3:
            return apology("Invalid ticker")
        else:
            price = usd(float(lookup_result["price"]))
            symbol = lookup_result["symbol"]
            name = lookup_result["name"]
            string = f"A share of {name} ({symbol}) costs {price}"

            return render_template("quoted.html", quote_response=string)
    else:
        return render_template("quotesearch.html")


@app.route("/resetpass", methods=["GET", "POST"])
def resetpass():
    """ Get users id for password reset"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Please enter your username", 403)
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            # Ensure username exists and password is correct
            if len(rows) == 0:
                return apology("Can't find the user in our database", 403)
            else:
                username = request.form.get("username")
                question = rows[0]["secretquestion"]
                if question == None:
                    return apology("You didn't set a secret question", 403)
                return render_template("resetpass.html", username=username, question=question)

    else:
        return render_template("resetpassusername.html")


@app.route("/resetpassw", methods=["POST"])
def resetpassw():
    """ Reset user password with secret question"""
    if request.method == "POST":
        if not request.form.get("secretkey") or not request.form.get("password"):
            return apology("Please fill all fields", 403)
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            if check_password_hash(rows[0]["secretanswer"], request.form.get("secretkey")):
                password = getHash(request.form.get("password"))
                if not passwordCheck(password):
                    return apology("Your password must be at least 8 characters long including at least one capitalised letter and one numeral.", 403)
                username = request.form.get("username")
                db.execute("UPDATE users SET hash = :password WHERE username = :username", password=password, username=username)
            else:
                return apology("Wrong answer", 403)

            return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            # return flash("You have to get an username")
            return apology("must provide username", 400)
        elif not request.form.get("password") or not passwordCheck(request.form.get("password")):
            return apology("Your password must be at least 8 characters long including at least one capitalised letter and one numeral.", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Please make sure both password fields are the same", 400)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) > 0:
            return apology("Username already in use", 400)
        username = request.form.get("username")
        password = getHash(request.form.get("password"))

        if not request.form.get("secretquestion") and not request.form.get("secretkey"):
            db.execute(
                "INSERT INTO users(id, username, hash, secretquestion, secretanswer) VALUES (NULL,:username, :password, NULL, NULL)",
                username=username, password=password)
        elif not request.form.get("secretquestion") or not request.form.get("secretkey"):
            return apology("If you want to have a secret question you have to fill both fields.", 400)

        elif len(request.form.get("secretquestion")) > 128 or len(request.form.get("secretkey")) > 128:
            return apology("Secret question and answer can't exceed 128 characters")
        else:
            secretq = request.form.get("secretquestion")
            secretkey = getHash(request.form.get("secretkey"))
            db.execute(
                "INSERT INTO users(id, username, hash, secretquestion, secretanswer) VALUES (NULL,:username, :password, :q, :a)",
                username=username, password=password, q=secretq, a=secretkey)
        row = db.execute("SELECT id FROM users WHERE username = :username", username=username)
        session["user_id"] = row[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    rows = db.execute("""SELECT stocks.symbol, sum(portfolio.shares) AS shares FROM stocks JOIN portfolio
    ON portfolio.stock_id = stocks.id WHERE user_id = :usrid GROUP BY stocks.symbol
    ORDER BY stocks.symbol""", usrid=user_id)
    sharedict = {}
    sharelist = []
    for row in rows:
        if row["shares"] > 0:
            sharedict[row["symbol"]] = row["shares"]
            sharelist = list(sharedict.keys())

    if len(rows) == 0:
        return apology("Nothing to sell", 400)

    if request.method == "POST":
        if not request.form.get("shares") or not request.form.get("symbol"):
            return apology("Please make a selection and enter how many stocks you want to sell", 400)
        elif not request.form.get("shares").isdigit() or int(request.form.get("shares")) < 1:
            return apology("Please enter a positive amount of shares", 400)

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if sharedict[symbol] < shares:
            return apology("You don't have enough shares to sell", 400)
        price = lookup(symbol.upper())["price"]
        total_gain = price * shares
        shares *= -1
        stock_id = db.execute("SELECT id FROM stocks WHERE symbol = :symbol", symbol=symbol)[0]["id"]
        db.execute("""INSERT INTO portfolio(stock_id, user_id, shares, price)
        VALUES (:stock, :usr, :share, :price)""", stock=stock_id, usr=user_id, share=shares, price=total_gain)
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :usrid", cash=total_gain, usrid=user_id)
        return redirect("/")
    else:

        return render_template("sell.html", rows=sharelist)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


def passwordCheck(password):
    """ Makes sure prompted password is longer than 8 chars and includes a capital letter and a number"""
    numeral_count = 0
    capitalized_count = 0
    if len(password) < 8:
        return False
    for c in password:
        if c.isupper():
            capitalized_count += 1
        elif c.isdigit():
            numeral_count += 1
        if numeral_count > 0 and capitalized_count > 0:
            return True
    return False


def getHash(password):
    """ Returns hashed password"""
    password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    return password


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)