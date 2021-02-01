from flask import Flask, render_template, redirect, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    if session.get("userID"):
        return render_template("index.html")
    else:
        return render_template("greet.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    else:
        # if user was redirected, pass parameter to login.html to tell user that login was required for their previous action
        if session.get("redirectedToLogin"):
            return render_template("login.html", redirected=session.get("redirectedToLogin"))
        else:
            return render_template("login.html")
        