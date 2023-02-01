import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel


class NewAccount(BaseModel):
    username: str
    password: str
    email: str


class GetAccount(BaseModel):
    username: str


class LoginAccount(BaseModel):
    email: str
    password: str


app = FastAPI()
base_route = "/api/v1"


@app.post(base_route + "/login")
def login(account: LoginAccount):
    with sqlite3.connect("accounts.db") as con:
        cur = con.cursor()
        query = f"SELECT username " \
                f"FROM accounts " \
                f"WHERE email='{account.email}' " \
                f"AND password='{account.password}'"
        res = cur.execute(query)

        if len(res.fetchall()) > 0:
            return {
                "success": True,
                "auth_token": "example_auth_token"
            }
        else:
            return {
                "success": False
            }


@app.post(base_route + "/signup")
async def signup(account: NewAccount):
    with sqlite3.connect("accounts.db") as con:
        # Encrypt email
        hashed_email = account.email
        # Encrypt password
        hashed_password = account.password

        cur = con.cursor()
        query = f"SELECT count(*) " \
                f"FROM accounts " \
                f"WHERE email='{hashed_email}' " \
                f"OR username='{account.username}' "
        res = cur.execute(query)

        if res.fetchone()[0] > 0:
            return {
                "success": False,
                "message": "An account already exists with this email or username."
            }

        print(f"hashed_email: {hashed_email}")
        print(f"hashed_password: {hashed_password}")

        query = f"INSERT INTO accounts (email, username, password)" \
                f" VALUES (" \
                f"'{account.username}'," \
                f"'{hashed_email}'," \
                f"'{hashed_password}'" \
                f")"
        res = cur.execute(query)

        return {
            "success": True,
        }


@app.post(base_route + "/getAccount")
async def get_account(account: GetAccount):
    with sqlite3.connect("accounts.db") as con:
        cur = con.cursor()
        query = f"SELECT username " \
                f"FROM accounts " \
                f"WHERE username='{account.username}'"
        res = cur.execute(query)

        return {
            "success": True,
            "data": res.fetchall()
        }
