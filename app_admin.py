from flask import Blueprint, redirect, render_template, request, session
import sqlite3

app_admin = Blueprint("admin", __name__)

# page user
@app_admin.route("/admin/user")
def page_user():
    if "email" not in session:
        return redirect("/login")
    else:
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql_1 = 'select * from tb_userlogin'
        curs = cur.execute(sql_1)
        data = curs.fetchall()
        sql_2 = 'select * from tb_access'
        curs = cur.execute(sql_2)
        access = curs.fetchall()
        return render_template("admin/user.html", data=data, access=access)

# fn add user
@app_admin.route("/admin/user/fn_add_user", methods=["POST"])
def fn_add_user():
    if "email" not in session:
        return redirect("/login")
    else:
        email = request.form["email"]
        password = request.form["password"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'insert into tb_userlogin (email, password, access, status) values ("{}", "{}", "- No -", "disable")'.format(email, password)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/user")

# fn edit user
@app_admin.route("/admin/user/fn_edit_user", methods=["POST"])
def fn_edit_user():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        email = request.form["email"]
        password = request.form["password"]
        access = request.form["access"]
        status = request.form["status"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'update tb_userlogin set password = "{}", access = "{}", status = "{}" where no = "{}"'.format(password, access, status ,no)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/user")

# fn delete user
@app_admin.route("/admin/user/fn_delete_user", methods=["POST"])
def fn_delete_user():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        email = request.form["email"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'delete from tb_userlogin where no = "{}"'.format(no)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/user")

# page access
@app_admin.route("/admin/access")
def page_access():
    if "email" not in session:
        return redirect("/login")
    else:
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'select * from tb_access'
        curs = cur.execute(sql)
        data = curs.fetchall()
        return render_template("admin/access.html", data=data)

# fn add access
@app_admin.route("/admin/user/fn_add_access", methods=["POST"])
def fn_add_access():
    if "email" not in session:
        return redirect("/login")
    else:
        access = request.form["access"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'insert into tb_access (access) values ("{}")'.format(access)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/access")

# fn edit access
@app_admin.route("/admin/fn_edit_access", methods=["POST"])
def fn_edit_access():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        access = request.form["access"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'update tb_access set access = "{}" where no = "{}"'.format(access, no)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/access")

# fn delete user
@app_admin.route("/admin/fn_delete_access", methods=["POST"])
def fn_delete_access():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'delete from tb_access where no = "{}"'.format(no)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/access")

# store
@app_admin.route("/admin/store")
def page_location():
    if "email" not in session:
        return redirect("/login")
    else:
        def get_data_tb():
            con = sqlite3.connect("db/db.db")
            cur = con.cursor()
            sql = 'select * from tb_store'
            curs = cur.execute(sql)
            data = curs.fetchall()
            return data
        data = get_data_tb()
        return render_template("admin/store.html", data=data)

# fn add store : pass
@app_admin.route("/admin/store/fn_add_store", methods=["POST"])
def fn_add_store():
    if "email" not in session:
        return redirect("/login")
    else:
        store = request.form["store"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'insert into tb_store (store) values ("{}")'.format(store)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/store")

# fn edit store : pass
@app_admin.route("/admin/store/fn_edit_store", methods=["POST"])
def fn_edit_location():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        store = request.form["store"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'update tb_store set store = "{}" where no = "{}"'.format(store, no)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/store")

# fn delete store : pass
@app_admin.route("/admin/store/fn_delete_store", methods=["POST"])
def fn_delete_location():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'delete from tb_store where no = "{}"'.format(no)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/store")
# store


# item
@app_admin.route("/admin/item")
def page_item():
    if "email" not in session:
        return redirect("/login")
    else:
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql_1 = 'select * from tb_item'
        curs = cur.execute(sql_1)
        data = curs.fetchall()
        return render_template("admin/item.html", data=data)

@app_admin.route("/admin/user/fn_add_item", methods=["POST"])
def fn_add_item():
    if "email" not in session:
        return redirect("/login") 
    else:
        item = request.form["item"]
        description = request.form["description"]
        unit = request.form["unit"]

        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql_1 = 'insert into tb_item (item, description, unit) values ("{}", "{}", "{}")'.format(item, description, unit)
        curs = cur.execute(sql_1)
        con.commit()
        con.close()
        return redirect("/admin/item")

@app_admin.route("/admin/user/fn_edit_item", methods=["POST"])
def fn_edit_item():
    if "email" not in session:
        return redirect("/login") 
    else:
        no = request.form["no"]
        item = request.form["item"]
        description = request.form["description"]
        unit = request.form["unit"]

        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql_1 = 'update tb_item set item = "{}", description = "{}", unit = "{}" where no = "{}"'.format(item, description, unit ,no)
        curs = cur.execute(sql_1)
        con.commit()
        con.close()
        return redirect("/admin/item")

@app_admin.route("/admin/user/fn_delete_item", methods=["POST"])
def fn_delete_item():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'delete from tb_item where no = "{}"'.format(no)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/item")
# item

# log
@app_admin.route("/admin/log/upload_csv")
def log_upload_csv():
    if "email" not in session:
        return redirect("/login")
    else:
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'select * from tb_upload_csv order by rec_no desc'
        curs = cur.execute(sql)
        data = curs.fetchall()
        return render_template("admin/log/upload_csv.html", data=data)

@app_admin.route("/admin/log/upload_csv/fn_delete_row", methods=["POST"])
def fn_upload_csv_delete_row():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'delete from tb_upload_csv where no = "{}"'.format(no)
        curs = cur.execute(sql)
        con.commit()
        con.close()
        return redirect("/admin/log/upload_csv")
# log