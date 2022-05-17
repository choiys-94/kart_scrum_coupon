from flask import render_template, send_from_directory
from . import main
import sqlite3 as sql


db_conn = lambda: sql.connect("database.db")

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
    users = []
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, class FROM crew_users")
        users = cur.fetchall()
        
    return render_template("scrum.html", users=users)