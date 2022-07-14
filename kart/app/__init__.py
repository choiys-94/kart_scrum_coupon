from flask import Flask
import uuid
import sqlite3 as sql

app = Flask(__name__)

db_conn = lambda: sql.connect("database.db")


def create_app():
    with db_conn() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS coupon_users (idx integer primary key, username text, userid text)")
        conn.execute("CREATE TABLE IF NOT EXISTS crew_users (idx integer primary key, username text unique, class integer, admin integer)")
        conn.execute("CREATE TABLE IF NOT EXISTS scrum (idx integer primary key, date text, time text, team text, closed integer, type integer)")
        conn.execute("CREATE TABLE IF NOT EXISTS scrum_member (idx integer primary key, scrum_idx integer, member text)")

        print("[*] init database complete")

    # migration
    migration = False
    # migration = True
    if migration:
        with open("users.json", "r", encoding="utf-8") as f:
            import json
            data = f.read()
            users = json.loads(data)
            with db_conn() as conn:
                cur = conn.cursor()
                for user in users:
                    cur.execute("INSERT INTO coupon_users(username, userid) VALUES(?,?)", (user["username"], user["userid"]))
            
            print("[*] migration complete")


    app.config["SECRET_KEY"] = uuid.uuid4().hex

    from .routes import main, coupon_api, scrum_api
    app.register_blueprint(main)
    app.register_blueprint(coupon_api)
    app.register_blueprint(scrum_api)

    __version__ = "0.1.0.0"

    return app