from .db_io import add_notice_to_db_and_get_id, get_all_notice_from_db, delete_notice_by_id, update_notice_by_id
from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/")
def index():
    entries = get_all_notice_from_db()
    return render_template("index.html", items=entries)

@app.route("/add_notice", methods = ["POST"])
def add_notice():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        msg = "Content-Type not supported!"
        return msg

    jsonv = request.json
    resolve = add_notice_to_db_and_get_id(jsonv["title"], jsonv["text"])

    return json.dumps({"noticeid":resolve["id"], "timestamp":resolve["timestamp"]})

@app.route("/delete_notice", methods = ["POST"])
def delete_route():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        msg = "Content-Type not supported!"
        return msg

    jsonv = request.json
    delete_notice_by_id(jsonv["id"])

    return json.dumps({})

@app.route("/edit_notice", methods = ["POST"])
def edit_route():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        msg = "Content-Type not supported!"
        return msg

    jsonv = request.json
    update_notice_by_id(jsonv["id"], jsonv["title"], jsonv["text"])
    return json.dumps({})