from flask import Blueprint, redirect, render_template, request, session
import sqlite3
import os
from datetime import datetime
import csv
import time

app_equipment = Blueprint("equipment", __name__)

# path ที่ใช้เก็บไฟล์ csv
UPLOAD_FOLDER_CSV = os.getcwd()+'/static/files/csv/'

# page equipment list ###################################################################
@app_equipment.route("/equipment")
def page_equipment():
    if "email" not in session:
        return redirect("/login")
    else:
        access_name = session["access"]

        con = sqlite3.connect("db/db.db")
        cur = con.cursor()

        sql = 'select * from tb_store where access = "{}"'.format(access_name)
        curs = cur.execute(sql)
        store_name = curs.fetchall()

        con.close()

        return render_template("equipment/equipment.html", store_name=store_name, access_name=access_name)

# page equipment add csv file
@app_equipment.route("/equipment/add_csv")
def page_add_csv():
    if "email" not in session:
        return redirect("/login")
    else:
        access = session["access"]
        print(access)
        # return date table
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'select * from tb_upload_csv where access = "{}" group by rec_no order by rec_no desc'.format(access)
        print(sql)
        curs = cur.execute(sql)
        data = curs.fetchall()
        con.close()
        return render_template("equipment/add_csv.html", data=data)

# fn add csv file
@app_equipment.route("/equipment/fn_add_csv", methods=["POST"])
def addFileCSV():
    if "email" not in session:
        return redirect("/login")
    else:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':

            file_path = UPLOAD_FOLDER_CSV + uploaded_file.filename
            uploaded_file.save(file_path)

            #record_path_datetime_csv(name_upload_file, date_time, file_path)
            
            # get date time
            date_time = time.ctime()
            date_time = date_time[8:10] + " " + date_time[4:7] + " " + date_time[20:24] + " " + date_time[11:19]

            # get name upload file
            rec_name = session["email"]

            # get rec_no
            rec_no = time.time()
            rec_no = rec_no *100000
            rec_no = int(rec_no)
            rec_no = str(rec_no)

            # get file csv to list
            file_name = file_path
            with open(file_name) as file:
                reader = csv.reader(file)
                check_row = 0
                for row in reader:
                    check_row = check_row + 1
                    if check_row != 1:
                        item = row[0]
                        description = row[1]
                        move_from = row[2]
                        move_to = row[3]
                        quantity = row[4]
                        remark = row[5]
                        fn_rec_csv(date_time, rec_name, rec_no, item, description, move_from, move_to, quantity, remark, session["access"])
                        
                return redirect("/equipment/add_csv")
        else:
            return redirect("/equipment/add_csv")

# SQL
def fn_rec_csv(date_time, rec_name, rec_no, item, description, move_from, move_to, quantity, remark, session_access):
    con = sqlite3.connect("db/db.db")
    cur = con.cursor()
    sql = 'insert into tb_upload_csv (date_time, rec_name, rec_no, item, description, move_from, move_to, quantity, remark, status, access) values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "wait_approve_draff", "{}")'.format(date_time, rec_name, rec_no, item, description, move_from, move_to, quantity, remark, session_access)
    curs = cur.execute(sql)
    con.commit()
    con.close()

# fn record path and datetime upload csv
def record_path_datetime_csv(name_upload_file, date_time, file_path):
    con = sqlite3.connect("db/db.db")
    cur = con.cursor()
    sql = 'insert into tb_path_upload_csv (name_upload_file, datetime, path) values ("{}", "{}", "{}")'.format(name_upload_file, date_time, file_path)
    curs = cur.execute(sql)
    con.commit()
    con.close()

# page equipment list ###################################################################

# page view by rec_no ###################################################################
@app_equipment.route('/equipment/add_csv/<rec_no>')
def page_view_by_rec_no(rec_no):
    if "email" not in session:
        return redirect("/login")
    else:
        rec_no = rec_no

        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'select * from tb_upload_csv where rec_no = "{}"'.format(rec_no)
        curs = cur.execute(sql)
        data = curs.fetchall()
        con.close()

        return render_template("equipment/view_by_rec_no.html", rec_no=rec_no, data=data)

@app_equipment.route('/equipment/add_csv/delete_by_rec', methods=["POST"])
def fn_delete_by_rec_no():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        rec_no = request.form["rec_no"]

        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql_1 = 'delete from tb_upload_csv where no = {}'.format(no)
        curs = cur.execute(sql_1)
        con.commit()
        con.close()

        return redirect("/equipment/add_csv/{}".format(rec_no))

@app_equipment.route('/equipment/add_csv/edit_by_rec', methods=["POST"])
def fn_edit_by_rec_no():
    if "email" not in session:
        return redirect("/login")
    else:
        no = request.form["no"]
        rec_no = request.form["rec_no"]
        qty = request.form["qty"]

        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql_1 = 'update tb_upload_csv set quantity = {} where no = {}'.format(qty, no)
        curs = cur.execute(sql_1)
        con.commit()
        con.close()

        return redirect("/equipment/add_csv/{}".format(rec_no))

# page view by equ by location ###################################################################
@app_equipment.route('/equipment/<access>/<location>')
def page_view_equ_by_location(access, location):
    if "email" not in session:
        return redirect("/login")
    else:
        # connect db and get data
        access = access
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql_1 = 'select item, description, move_from, move_to, status, access from tb_upload_csv where status = "received" and access = "{}" group by item'.format(access)
        curs = cur.execute(sql_1)
        result = curs.fetchall()

        # convert data to list
        result_1 = []
        for i in result:
            data = list(i)
            result_1.append(data)
            
        # add qty.
        result_list = []
        for i in result_1:
            sql_2 = 'SELECT sum(quantity) FROM tb_upload_csv WHERE status = "received" and item = "{}" and move_to = "{}" and access = "{}"'.format(i[0], location, access)
            curs = cur.execute(sql_2)
            result_2 = curs.fetchall()
            result_2 = result_2[0][0]
            if result_2 == None:
                result_2 = 0

            sql_3 = 'SELECT sum(quantity) FROM tb_upload_csv WHERE status = "received" and item = "{}" and move_from = "{}" and access = "{}"'.format(i[0], location, access)
            curs = cur.execute(sql_3)
            result_3 = curs.fetchall()
            result_3 = result_3[0][0]
            if result_3 == None:
                result_3 = 0

            result_4 = result_2-result_3
            row = i
            row.append(result_4)
            result_list.append(row)
        dataset = result_list
        con.close()

        return render_template("equipment/equ_list_by_location.html", dataset=dataset)

# approve draff ###################################################################
@app_equipment.route('/equipment/approve_draff', methods=["POST"])
def approve_draff():
    if "email" not in session:
        return redirect("/login")
    else:
        rec_no = request.form["rec_no"]
        
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'update tb_upload_csv set status = "wait_receive" where rec_no = "{}"'.format(rec_no)
        curs = cur.execute(sql)
        con.commit()
        con.close()

        return redirect('/equipment/add_csv/'+rec_no)

@app_equipment.route('/equipment/approve_receive', methods=["POST"])
def approve_receive():
    if "email" not in session:
        return redirect("/login")
    else:
        rec_no = request.form["rec_no"]
        
        con = sqlite3.connect("db/db.db")
        cur = con.cursor()
        sql = 'update tb_upload_csv set status = "received" where rec_no = "{}"'.format(rec_no)
        curs = cur.execute(sql)
        con.commit()
        con.close()

        return redirect('/equipment/add_csv/'+rec_no)