from flask import Blueprint, redirect, render_template, request, session
import sqlite3

app_login = Blueprint("login", __name__)

# page login
@app_login.route("/login")
def page_login():
    return render_template("/login/login.html")

# fn login
@app_login.route("/fn_login", methods=["POST"])
def fn_login():
    try:
        email = request.form["email"]
        password = request.form["password"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'SELECT * from tb_userlogin WHERE email = "{}" AND password = "{}"'.format(email,password)
        curs = cur.execute(sql)
        data = curs.fetchall()
        data = data[0]
        print(data[3])
        if data[3] == "disable":
            return redirect("/login")
        else:
            if len(data) > 0:
                session['email'] = data[1]
                session['acces'] = data[3]
                print(session)
                return redirect("/")
            else:
                return redirect("/login")
    except:
        return redirect("/login")

# fn logout
@app_login.route("/fn_logout")
def fn_logout():
    session.clear()
    return redirect("/login")