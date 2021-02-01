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
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    else:
        # pass parameter redirected to login.html to display "login required" message then clear cookie
        redirected = session.get("redirectedToLogin")
        del session["redirectedToLogin"]
        return render_template("login.html", redirected=redirected)

@app.route("/browse", methods=["GET", "POST"])
def browse():
    pass

@app.route("/search", methods=["GET", "POST"])
def search():
    pass


        