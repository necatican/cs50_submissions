import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        # response = requests.get(f"https://api.iextrading.com/1.0/stock/{urllib.parse.quote_plus(symbol)}/quote")
        response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id=")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        quote = quote["rates"]
        targetcurrency = str(quote[symbol])
        targetcurrency.replace(",", "")
        lira = quote["TRY"]
        return todecimal(float(lira) / float(targetcurrency))
    except (KeyError, TypeError, ValueError):
        return None


def tryc(value):
    """Format value as USD."""
    return f"{value:,.2f} TRY"


def todecimal(value):
    """Format value to two point decimal"""
    return f"{value:.2f}"


def threepoint(value):
    """Format value to two point decimal"""
    return f"{value:.3f}"
