from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3


class NewAccount(BaseModel):
    username: str
    password: str
    email: str


class GetAccount(BaseModel):
    username: str


app = FastAPI()
con = sqlite3.connect("accounts.db")
cur = con.cursor()


base_route = "/api/v1"


@app.post(base_route + "/login")
def login():
    return {
        "success": True
    }


@app.post(base_route + "/signup")
async def signup(account: NewAccount):
    query = "SELECT count(*) FROM accounts WHERE email='" + account.email + "' OR username='" + account.username + "'"
    res = cur.execute(query)

    if res.fetchone()[0] > 0:
        return {
            "success": False,
            "message": "An account already exists with either this username or password."
        }

    query = "INSERT INTO accounts (username, password, email) VALUES ('" + account.username + "', '" + account.password + "', '" + account.email + "') "
    res = cur.execute(query)

    return {
        "success": True
    }


@app.post(base_route + "/account")
def get_account(account: GetAccount):
    query = "SELECT count(*) FROM accounts WHERE username='" + account.username + "'"
    res = cur.execute(query)

    return {
        "success": True,
        "data": res.fetchone()[0]
    }
