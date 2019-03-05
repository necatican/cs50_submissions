import os
import urllib.request
import csv
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, tryc, todecimal, threepoint

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


# # Custom filter
# app.jinja_env.filters["tryc"] = tryc

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///exchange.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    rowlist = []
    cash = db.execute("SELECT cash FROM users WHERE id = :usrid", usrid=user_id)
    cash = float(cash[0]["cash"])
    networth = cash
    rows = db.execute("""SELECT currencies.acronym, sum(transactions.amount) AS txamount,
                      sum(transactions.totalcost) AS sumcost FROM transactions JOIN currencies ON
                      currencies.id = transactions.firstcurrency JOIN users ON users.id = transactions.user_id WHERE
                      users.id = :usrid GROUP BY currencies.acronym ORDER BY currencies.id""", usrid=user_id)

    # Gets a list ready for Jinja to render
    for row in rows:
        acronym = row["acronym"]
        txamount = float(row["txamount"])
        sumcost = float(row["sumcost"])
        if float(txamount) > 0 and float(sumcost) > 0:
            average = threepoint(float(sumcost / txamount))
            currentprice = threepoint(float(lookup(acronym)))
            profit = ((float(currentprice) * 1000) - (float(average) * 1000)) * (txamount * 1000) / 1000000
            rowlist.append([acronym, todecimal(txamount), average, threepoint(float(currentprice)), todecimal(sumcost),
                            threepoint(profit)])
        networth += sumcost
    return render_template("index.html", rows=rowlist, networth=tryc(networth))


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rowlist = []
    userid = session["user_id"]

    rows = db.execute(
        """SELECT currencies.acronym AS firstcurrency, curr2.acronym as secondcurrency, transactions.amount, transactions.unitprice,
        transactions.totalcost, transactions.date,txtype.type FROM transactions JOIN currencies ON currencies.id =
        transactions.firstcurrency JOIN currencies AS curr2 ON curr2.id = transactions.secondcurrency JOIN txtype ON
        transactions.tx_type = type_id WHERE transactions.user_id = :usrid AND transactions.tx_type != 3 ORDER BY transactions.date DESC
        """, usrid=userid)

    # Gets a list ready for Jinja to render
    for row in rows:
        firstcurrency = row["firstcurrency"]
        secondcurrency = row["secondcurrency"]
        amount = row["amount"]
        unitprice = row["unitprice"]
        totalcost = row["totalcost"]
        date = row["date"]
        tx_type = row["type"]

        rowlist.append([firstcurrency, secondcurrency, amount, unitprice, totalcost, date, tx_type])
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


@app.route("/checkusr")
def checkusr():
    """ Check if user already is in our database"""
    usr = request.args.get("username")
    rows = db.execute("SELECT * FROM users WHERE username = :username",
                      username=usr)
    return jsonify({
        "username": usr,
        "count": len(rows)
    })


@app.route("/pwcheck")
def pwcheck():
    # Makes sure the password is correct and returns a json with the check value
    usr = request.args.get("username")
    pw = request.args.get("password")
    check = checkPassword(usr, pw)
    return jsonify({
        "username": usr,
        "check": check
    })


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


@app.route("/addfunds", methods=["GET", "POST"])
@login_required
def addfunds():
    """Add funds to users account"""
    currencies = db.execute("SELECT acronym FROM currencies")
    if request.method == "POST":
        user_id = session["user_id"]
        currencyid = db.execute("SELECT id FROM currencies WHERE acronym = :acr", acr=request.form.get("firstcurrency"))
        currencyid = currencyid[0]["id"]
        value = lookup(request.form.get("firstcurrency"))
        amount = todecimal(float(request.form.get("amount")))
        totalcost = todecimal(float(amount) * float(value))
        db.execute(
            """INSERT INTO transactions(firstcurrency, secondcurrency, amount, unitprice, totalcost, user_id, tx_type) VALUES(:currencyid, 2, :amount, :value, :totalcost, :usrid, 1)""",
            currencyid=currencyid, amount=amount, value=value, totalcost=totalcost, usrid=user_id)
        return jsonify({
            "Currency": request.form.get("firstcurrency"),
            "Value": totalcost,
            "Amount": amount
        })
    else:

        return render_template("addfunds.html", rows=currencies)


@app.route("/exchange", methods=["GET", "POST"])
@login_required
def exchange():
    """Cross exchange"""
    currencies = db.execute("SELECT acronym FROM currencies")
    if request.method == "POST":
        """ firstcurrency: $("#firstcurrency option:selected" ).text().trim(),
            secondcurrency: $("#secondcurrency option:selected" ).text().trim(),
            amount: $("#currency1value").val(),
            value: fx.convert(1, {from:firstcurrency , to: "TRY"}),
            cost: value * amount"""
        user_id = session["user_id"]
        firstcurrency = db.execute("SELECT id FROM currencies WHERE acronym = :acr", acr=request.form.get("firstcurrency"))
        secondcurrency = db.execute("SELECT id FROM currencies WHERE acronym = :acr", acr=request.form.get("secondcurrency"))
        firstcurrency = firstcurrency[0]["id"]
        secondcurrency = secondcurrency[0]["id"]
        value = request.form.get("value")
        firstvalue = request.form.get("firstvalue")
        amount = request.form.get("amount")
        exchanged = request.form.get("exchanged")
        totalcost = request.form.get("cost")
        exchangedcost = float(exchanged) * float(firstvalue)
        db.execute(
            """INSERT INTO transactions(firstcurrency, secondcurrency, amount, unitprice, totalcost, user_id, tx_type) VALUES(:currencyid, :secondcurrencyid, :amount, :value, :totalcost, :usrid, 2)""",
            currencyid=secondcurrency, secondcurrencyid=firstcurrency, amount=(float(amount)), value=todecimal(float(value)), totalcost=todecimal(float(totalcost)), usrid=user_id)
        db.execute("""INSERT INTO transactions(firstcurrency, secondcurrency, amount, unitprice, totalcost, user_id, tx_type) VALUES(:currencyid, :secondcurrencyid, :exchanged, :value, :totalcost, :usrid, 3)""",
                   currencyid=firstcurrency, secondcurrencyid=secondcurrency, exchanged=todecimal(float(exchanged) * -1), value=todecimal(float(firstvalue) * -1), totalcost=todecimal(float(exchangedcost) * -1), usrid=user_id)
        return jsonify({
            "Currency": request.form.get("secondcurrency"),
            "Exchanged": request.form.get("firstcurrency"),
            "Value": totalcost,
            "Amount": amount
        })
    else:

        return render_template("exchange.html", rows=currencies)


@app.route("/checkbal", methods=["POST"])
@login_required
def checkbal():
    """ Checks users balance"""
    user_id = session["user_id"]
    rows = db.execute("""SELECT currencies.acronym, SUM(transactions.amount) as amount FROM transactions JOIN currencies ON currencies.id
    = transactions.firstcurrency WHERE transactions.user_id = :usrid GROUP BY currencies.acronym ORDER BY acronym ASC""", usrid=user_id)
    for row in rows:
        row["amount"] = todecimal(float(row["amount"]))
    return jsonify({
        "rowlist": rows
    })


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


def checkPassword(username, password):
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
        return False
    else:
        return True


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)