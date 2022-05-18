from flask import request
from . import scrum_api
import requests
import datetime
import json
import sqlite3 as sql


requests.packages.urllib3.disable_warnings()

db_conn = lambda: sql.connect("database.db")

START_TIME = 20
END_TIME = 26

# conn.execute("CREATE TABLE IF NOT EXISTS crew_users (idx integer primary key, username text, class text)")
# conn.execute("CREATE TABLE IF NOT EXISTS scrum (idx integer primary key, date text, time text, team text)")
# conn.execute("CREATE TABLE IF NOT EXISTS scrum_member (idx integer primary key, scrum_idx integer, member text)")

def get_today():
    today = datetime.date.today()
    hour = datetime.datetime.today().hour
    if int(hour) < 5:
        today -= datetime.timedelta(days=1)

    today = today.strftime("%Y-%m-%d")

    return today

@scrum_api.route("/scrum_state", methods=["GET"])
def scrum_state():
    today = get_today()
    with db_conn() as conn:
        cur = conn.cursor()

        cur.execute("SELECT date, time, team, closed FROM scrum WHERE date = ? order by time asc, team asc", (today, ))
        res = cur.fetchall()
        if len(res) < (END_TIME - START_TIME + 1):
            for i in range(START_TIME, END_TIME + 1):
                cur.execute("INSERT OR IGNORE INTO scrum(date, time, team, closed) VALUES(?,?,?,?)", (today, i, 1, 0))

            cur.execute("SELECT date, time, team, closed FROM scrum WHERE date = ?", (today, ))
            res = cur.fetchall()

        return json.dumps(res)

@scrum_api.route("/scrum_data", methods=["GET"])
def scrum_data():
    today = get_today()
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT time, team, member, class FROM (scrum a INNER JOIN scrum_member b ON (a.idx=scrum_idx)) c INNER JOIN crew_users d ON (c.member=d.username) WHERE date = ? ORDER BY class asc", (today, ))
        res = cur.fetchall()

        return json.dumps(res)

@scrum_api.route("/scrum_submit", methods=["POST"])
def scrum_submit():
    hour = request.form["hour"]
    team = int(request.form["team"])
    username = request.form["username"]

    if username == "":
        return "1"

    today = get_today()
    
    with db_conn() as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT idx FROM scrum WHERE date = ? AND time = ? AND team = ?", (today, hour, team))
        scrum_idx = cur.fetchall()
        scrum_idx = (len(scrum_idx) > 0) and scrum_idx[0][0] or -1

        cur.execute("SELECT 1 FROM scrum_member WHERE (scrum_idx = ?) AND (member = ?)", (scrum_idx, username))
        res = cur.fetchall()
        if len(res) > 0:
            cur.execute("DELETE FROM scrum_member WHERE (scrum_idx = ?) AND (member = ?)", (scrum_idx, username))
            return "1"

        cur.execute("SELECT member FROM scrum_member WHERE (scrum_idx = ?)", (scrum_idx, ))
        scrum_count = cur.fetchall()
        
        if len(scrum_count) >= 4:
            team += 1
            cur.execute("SELECT 1 FROM scrum WHERE date = ? AND time = ? AND team = ?", (today, hour, team))
            res = cur.fetchall()
            if len(res) == 0:
                cur.execute("INSERT OR IGNORE INTO scrum(date, time, team, closed) VALUES(?,?,?,?)", (today, hour, team, 0))
            return "1"

        cur.execute("INSERT OR IGNORE INTO scrum_member(scrum_idx, member) VALUES(?,?)", (scrum_idx, username))
            
    return "1"

@scrum_api.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    userclass = request.form["class"]

    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO crew_users(username, class) VALUES(?,?)", (username, userclass))

        return "크루원 등록이 완료되었습니다."

@scrum_api.route("/edit_user", methods=["POST"])
def edit_user():
    org_username = request.form["org_username"]
    username = request.form["username"]
    userclass = request.form["class"]

    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE crew_users SET username = ?, class = ? WHERE username = ?", (username, int(userclass), org_username))

        return "크루원 수정이 완료되었습니다."

@scrum_api.route("/delete_user", methods=["POST"])
def delete_user():
    username = request.form["username"]
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM crew_users WHERE username = ?", (username, ))

        return "크루원 삭제가 완료되었습니다."

@scrum_api.route("/all_users", methods=["GET"])
def all_users():
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, class FROM crew_users")
        users = cur.fetchall()
        
        if len(users) > 0:
            return users

        return []

@scrum_api.route("/check_class", methods=["POST"])
def check_class():
    username = request.form["username"]
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM crew_users WHERE username = ?", (username, ))
        res = cur.fetchall()
        if len(res) > 0:
            return "1"
    
    return "0"

@scrum_api.route("/scrum_closed", methods=["POST"])
def scrum_closed():
    hour = request.form["hour"]
    team = request.form["team"]
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE scrum SET closed=ABS(closed-1) WHERE time = ? AND team = ?", (hour, team))
        cur.execute("SELECT closed FROM scrum WHERE time = ? AND team = ?", (hour, team))
        res = cur.fetchall()
        return str(res[0][0])

@scrum_api.route("/d", methods=["GET"])
def test_d():
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM scrum")
        cur.execute("DELETE FROM scrum_member")
    
    return "1"

@scrum_api.route("/du", methods=["GET"])
def test_du():
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM crew_users")
    
    return "1"