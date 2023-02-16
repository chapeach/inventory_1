from flask import Blueprint, redirect, render_template, request, session
import sqlite3

app_home = Blueprint("home", __name__)

# page home
@app_home.route("/")
def page_home():
    if "email" not in session:
        return redirect("/login")
    else:
        return render_template("home.html")

# page change user password
@app_home.route("/changepassword")
def page_change_password():
    if "email" not in session:
        return redirect("/login")
    else:
        box_msg = 0
        return render_template("changepassword.html", box_msg=box_msg)

# fn change user password
@app_home.route("/fn_changepassword", methods=["POST"])
def fn_changepassword():
    if "email" not in session:
        return redirect("/login")
    else:
        current_pass = request.form["current_pass"]
        new_pass = request.form["new_pass"]
        confirm_pass = request.form["confirm_pass"]
        email = session["email"]

        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'select * from tb_userlogin where email = "{}"'.format(email)
        curs = cur.execute(sql)
        data = curs.fetchall()
        user_pass = data[0][2]

        # check current pass
        if user_pass != current_pass:
            box_msg = 1
            sand_msg = "รหัสเดิมไม่ถูกต้อง"
            return render_template("changepassword.html", box_msg=box_msg, sand_msg=sand_msg)

        # new pass
        if new_pass != confirm_pass:
            box_msg = 1
            sand_msg = "new password ไม่ตรงกับ confirm password"
            return render_template("changepassword.html", box_msg=box_msg, sand_msg=sand_msg)

        sql_2 = 'update tb_userlogin set password = "{}" where email = "{}"'.format(new_pass, email)
        curs = cur.execute(sql_2)
        con.commit()
        con.close()
        box_msg = 1
        sand_msg = 'user : {} change password done.'.format(email)
        return render_template("changepassword.html", box_msg=box_msg, sand_msg=sand_msg)