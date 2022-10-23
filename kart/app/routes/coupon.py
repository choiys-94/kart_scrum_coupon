from flask import request
from . import coupon_api
import requests
import sqlite3 as sql


requests.packages.urllib3.disable_warnings()

db_conn = lambda: sql.connect("database.db")

@coupon_api.route("/check_id", methods=["POST"])
def check_id():
    username = request.form["username"]

    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT userid FROM coupon_users where username = ?", (username, ))
        res = cur.fetchall()
        
        if len(res) > 0:
            print(res[0])
            return res[0][0]
        
        return "Error"

@coupon_api.route("/check_coupon", methods=["POST"])
def check_coupon():
    userid = request.form["userid"]
    coupon = request.form["coupon"]
    
    data = {
        # "npaCode": "07901CQ10406Q",
        # "couponNum": "LUPU2VAVWN",
        "npaCode": userid,
        "coupon": coupon,
        "region": "KR"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "Cookie": "PCID=16357799776188379794221; _hjid=388a4ac5-d5c5-4786-b50c-186ca50fe7a7; _ga_GWPD7HDK9M=GS1.1.1636541618.3.0.1636541618.0; _hjSessionUser_1327448=eyJpZCI6ImQyODBmM2Q1LTA1NDctNWIyNS04NmY0LWJmNjk1YTdmMmI1ZSIsImNyZWF0ZWQiOjE2NDA3ODMxNTU0MzYsImV4aXN0aW5nIjp0cnVlfQ==; _ga_YVXQ064DKG=GS1.1.1647848642.1.1.1647848657.0; _ga_HN5G885YR0=GS1.1.1648661345.1.1.1648661379.0; _gcl_au=1.1.431093251.1650895379; A2SK=act:16508953894741024103; NXTPA=-; NXGID=A52EFC5DCE0C0B06702254975E0B4ABF; PS_NexonID=4UIl8SD5INus8zbw6iJKlGDyqKSc9flnNPOsOG1pzM4%253d; NXABP=; GGAN=0; NXMP=; _gid=GA1.2.1191055630.1652186280; JSESSIONID=FB3F4D3DFE96BFFECD5A046F6874AE16; isCafe=false; _ga_NEHB476HQQ=GS1.1.1652472456.5.1.1652472460.0; _hjSession_1327448=eyJpZCI6IjhkNDg5YzMzLWFjZGMtNDI3MS05NzI5LThiOTE3ZTk0YTdhYiIsImNyZWF0ZWQiOjE2NTI0NzkwMTMwMjIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; IL=; NXCH=; IM=0; RDB=; NPP=; ENC=; NXLW=SID=0DDB8056192AD20D2F9ADCC48B593E4F&PTC=https:&DOM=kartrideresports.nexon.com&ID=&CP=; _ga=GA1.2.1575722911.1635779978; _ga_3Q73DZJDDP=GS1.1.1652479902.37.0.1652479902.0; _ga_D78NYXY4CE=GS1.1.1652479012.7.1.1652479903.0"
    }
    # r = requests.post("https://mcoupon.nexon.com/kartrush/findUserNpa", headers=headers, json=data, verify=False)
    r = requests.post("https://mcoupon.nexon.com/kartrush/coupon/api/v1/characters-by-npacode", headers=headers, json=data, verify=False)
    # code 2200 : 이미 사용한 쿠폰 입니다. 번호 확인 후 다시 입력해주세요.
    # code 1101 : 잘못된 쿠폰번호 입니다. 번호 확인 후 다시 입력해주세요
    # https://mcoupon.nexon.com/kartrush/findUserNpa
    # {"result":true,"info":[{"id":"16520000001680394","name":"첫사랑선이"}]}
    
    print(r.text)

    if "\"code\":2200" in r.text:
        return "{\"result\":\"false\", \"message\":\"이미 사용한 쿠폰 입니다.\"}"        
    elif "\"code\":1101" in r.text:
        return "{\"result\":\"false\", \"message\":\"잘못된 쿠폰번호 입니다.\"}"
    elif "\"code\":1105" in r.text:
        return "{\"result\":\"false\", \"message\":\"다른 유저가 이미 사용한 쿠폰입니다.\"}"
    elif "\"code\":91001" in r.text:
        return "{\"result\":\"false\", \"message\":\"계정 번호를 정확히 입력해주세요.\"}"
    elif "\"code\":91002" in r.text:
        return "{\"result\":\"false\", \"message\":\"쿠폰 번호를 정확히 입력해주세요.\"}"
    elif "\"result\":true" in r.text:
        return r.text
    else:
        return "{\"result\":\"false\", \"message\":\"쿠폰 확인 오류\"}"

@coupon_api.route("/submit_coupon", methods=["POST"])
def submit_coupon():
    # https://mcoupon.nexon.com/kartrush/useGiftCoupon
    # {"npaCode":"07901CQ10406Q","couponNum":"LUPU2VAVWN","id":"16520000001680394","name":"첫사랑선이","region":"KR"}
    userid = request.form["userid"]
    coupon = request.form["coupon"]
    account_id = request.form["account_id"]
    account_name = request.form["account_name"]
    data = {
        # "npaCode": "07901CQ10406Q",
        # "couponNum": "LUPU2VAVWN",
        "npaCode": userid,
        "coupon": coupon,
        "id": account_id,
        "name": account_name,
        "world": "",
        "region": "KR"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "Cookie": "PCID=16357799776188379794221; _hjid=388a4ac5-d5c5-4786-b50c-186ca50fe7a7; _ga_GWPD7HDK9M=GS1.1.1636541618.3.0.1636541618.0; _hjSessionUser_1327448=eyJpZCI6ImQyODBmM2Q1LTA1NDctNWIyNS04NmY0LWJmNjk1YTdmMmI1ZSIsImNyZWF0ZWQiOjE2NDA3ODMxNTU0MzYsImV4aXN0aW5nIjp0cnVlfQ==; _ga_YVXQ064DKG=GS1.1.1647848642.1.1.1647848657.0; _ga_HN5G885YR0=GS1.1.1648661345.1.1.1648661379.0; _gcl_au=1.1.431093251.1650895379; A2SK=act:16508953894741024103; NXTPA=-; NXGID=A52EFC5DCE0C0B06702254975E0B4ABF; PS_NexonID=4UIl8SD5INus8zbw6iJKlGDyqKSc9flnNPOsOG1pzM4%253d; NXABP=; GGAN=0; NXMP=; _gid=GA1.2.1191055630.1652186280; JSESSIONID=FB3F4D3DFE96BFFECD5A046F6874AE16; isCafe=false; _ga_NEHB476HQQ=GS1.1.1652472456.5.1.1652472460.0; _hjSession_1327448=eyJpZCI6IjhkNDg5YzMzLWFjZGMtNDI3MS05NzI5LThiOTE3ZTk0YTdhYiIsImNyZWF0ZWQiOjE2NTI0NzkwMTMwMjIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; IL=; NXCH=; IM=0; RDB=; NPP=; ENC=; NXLW=SID=0DDB8056192AD20D2F9ADCC48B593E4F&PTC=https:&DOM=kartrideresports.nexon.com&ID=&CP=; _ga=GA1.2.1575722911.1635779978; _ga_3Q73DZJDDP=GS1.1.1652479902.37.0.1652479902.0; _ga_D78NYXY4CE=GS1.1.1652479012.7.1.1652479903.0"
    }

    # r = requests.post("https://mcoupon.nexon.com/kartrush/useGiftCoupon", headers=headers, json=data, verify=False)
    r = requests.post("https://mcoupon.nexon.com/kartrush/coupon/api/v1/redeem-coupon-by-npacode", headers=headers, json=data, verify=False)
    print(r.text)

    return "1"

@coupon_api.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    userid = request.form["userid"]
    password = request.form["password"]
    if password != "2468":
        return "패스워드가 일치하지 않습니다."
    
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO coupon_users(username, userid) VALUES (?,?)", (username, userid))
        print(f"[*] {username}, {userid} added")
        
    return "계정 생성이 완료되었습니다."