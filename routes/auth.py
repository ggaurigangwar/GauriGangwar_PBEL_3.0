from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route("/auth")
def authentication():
    return render_template("auth.html")