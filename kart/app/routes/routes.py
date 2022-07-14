from flask import render_template, send_from_directory, request, make_response
from . import main
from .scrum import is_admin
import urllib.parse
import sqlite3 as sql
import datetime


db_conn = lambda: sql.connect("database.db")

def get_users():
    users = []
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, class, admin FROM crew_users ORDER BY class ASC")
        users = cur.fetchall()

    return users

@main.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory("static/images", "favicon.ico", mimetype="image/vnd.microsoft.icon")

@main.route("/", methods=["GET"])
def home():
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM coupon_users")
        users = cur.fetchall()
        if len(users) > 0:
            return render_template("home.html", users=users)

        return render_template("home.html", users=[])

@main.route("/scrum", methods=["GET"])
def scrum():
    users = get_users()
        
    return render_template("scrum.html", users=users)

@main.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        try:
            flag = False
            username = urllib.parse.unquote(request.cookies.get("username"))
            print(username)
            if is_admin(username) == '1':
                flag = True

            enter = request.cookies.get("f6523489dsg")
            if enter == "f02938f9sdf_33" or flag:
                users = get_users()
                return render_template("users.html", users=users)
            else:
                return render_template("users_enter.html")

        except:
            return render_template("users_enter.html")
    
    elif(request.method == "POST"):
        password = request.form["password"]
        if password == "새채벽고":
            users = get_users()
            resp = make_response(render_template("users.html", users=users))
            expire_date = datetime.datetime.now() - datetime.timedelta(hours=9) + datetime.timedelta(minutes=10)
            resp.set_cookie("f6523489dsg", "f02938f9sdf_33", expires=expire_date)
            return resp
        else:
            return render_template("users_enter.html", err="비밀번호가 일치하지 않습니다.")