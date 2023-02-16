from flask import Blueprint, redirect, render_template, request, session

app_manual = Blueprint("manual", __name__)

# page manual ###################################################################
@app_manual.route("/manual")
def page_manual():
    if "email" not in session:
        return redirect("/login")
    else:
        return render_template("manual/manual.html")