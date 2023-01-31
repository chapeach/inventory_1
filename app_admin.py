from flask import Blueprint, redirect, render_template, request, session
import sqlite3
import time

app_admin = Blueprint("admin", __name__)

######### page user #################################################################################
@app_admin.route("/admin/user")
def page_user():
    if "email" not in session:
        return redirect("/login")
    else:
        # connect db
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()

        # select userlogin
        sql_select_userlogin = 'select * from tb_userlogin'
        curs = cur.execute(sql_select_userlogin)
        data = curs.fetchall()

        # select access
        sql_select_access = 'select * from tb_access'
        curs = cur.execute(sql_select_access)
        access = curs.fetchall()
        con.close()

        return render_template("admin/user.html", data=data, access=access)

# fn add user
@app_admin.route("/admin/user/fn_add_user", methods=["POST"])
def fn_add_user():
    if "email" not in session:
        return redirect("/login")
    else:
        # connect db
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()

        # request form
        email = request.form["email"]
        password = request.form["password"]
        
        # check e-mail duplicate
        sql_select_email = 'select * from tb_userlogin where email = "{}"'.format(email)
        curs = cur.execute(sql_select_email)
        data_email = curs.fetchall()
        if len(data_email) > 0:
            con.close()
            return redirect("/admin/user")

        # e-mail no duplicate is record to db
        sql_insert_user = 'insert into tb_userlogin (email, password, access, status, level) values ("{}", "{}", "- No -", "disable", "0")'.format(email, password)
        curs = cur.execute(sql_insert_user)
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
        level = request.form["level"]
        status = request.form["status"]
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'update tb_userlogin set password = "{}", access = "{}", status = "{}", level = "{}" where no = "{}"'.format(password, access, status, level, no)
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

######### access #################################################################################
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
        # connect db
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()

        # check access duplicate
        access = request.form["access"]
        sql_select_access = 'select * from tb_access where access = "{}"'.format(access)
        curs = cur.execute(sql_select_access)
        data_access = curs.fetchall()
        if len(data_access) > 0:
            con.close()
            return redirect("/admin/access")

        # data no duplicate is record to db
        sql_insert_access = 'insert into tb_access (access) values ("{}")'.format(access)
        curs = cur.execute(sql_insert_access)
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

######### fn delete user #################################################################################
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

######### store #################################################################################
@app_admin.route("/admin/store")
def page_location():
    if "email" not in session:
        return redirect("/login")
    else:
        # connect db
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()

        # select store
        sql_select_store = 'select * from tb_store'
        curs = cur.execute(sql_select_store)
        store_name = curs.fetchall()

        # select access
        sql_select_access = 'select * from tb_access'
        curs = cur.execute(sql_select_access)
        access_name = curs.fetchall()
        con.close()

        return render_template("admin/store.html", store_name=store_name, access_name=access_name)

# fn add store
@app_admin.route("/admin/store/fn_add_store", methods=["POST"])
def fn_add_store():
    if "email" not in session:
        return redirect("/login")
    else:
        # connect db
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()

        # request form
        access_name = request.form["access"]
        store = request.form["store"]

        # check store duplicate
        sql_select_store = 'select * from tb_store where access = "{}" and store = "{}"'.format(access_name, store)
        curs = cur.execute(sql_select_store)
        data_access_name = curs.fetchall()
        if len(data_access_name) > 0:
            return redirect("/admin/store")

        # data no duplicate is record to db
        sql = 'insert into tb_store (access, store) values ("{}", "{}")'.format(access_name, store)
        curs = cur.execute(sql)
        con.commit()
        con.close()

        return redirect("/admin/store")

# fn edit store
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

# fn delete store
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

######### item #################################################################################
@app_admin.route("/admin/item")
def page_item():
    if "email" not in session:
        return redirect("/login")
    else:
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql_1 = 'select * from tb_item order by date_rec desc'
        curs = cur.execute(sql_1)
        data = curs.fetchall()
        return render_template("admin/item.html", data=data)

# fn add item
@app_admin.route("/admin/user/fn_add_item", methods=["POST"])
def fn_add_item():
    if "email" not in session:
        return redirect("/login") 
    else:
        # connect db
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()

        # request form
        item = request.form["item"]
        description = request.form["description"]
        unit = request.form["unit"]

        # check item duplicate
        sql_select_item = 'select * from tb_item where item = "{}"'.format(item)
        curs = cur.execute(sql_select_item)
        data_item = curs.fetchall()
        if len(data_item) > 0:
            con.close()
            return redirect("/admin/item")

        # item no duplicate is record to db
        sql_insert_item = 'insert into tb_item (item, description, unit, date_rec) values ("{}", "{}", "{}", "{}")'.format(item, description, unit, time.time())
        curs = cur.execute(sql_insert_item)
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

# log #####################################################################
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