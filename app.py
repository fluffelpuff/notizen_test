from db_io import add_notice_to_db_and_get_id, get_all_notice_from_db, delete_notice_by_id, update_notice_by_id
from flask import Flask, render_template, request
from db import get_connection
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

if __name__ == "__main__":
    INIT_SQL = """
    CREATE TABLE IF NOT EXISTS notes (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        title      TEXT,
        text       TEXT,
        timestamp  TEXT,
        notice_id  TEXT
    );

    -- sinnvolle Indizes (optional, aber hilfreich fürs Suchen/Sortieren)
    CREATE INDEX IF NOT EXISTS idx_notes_notice_id ON notes(notice_id);
    CREATE INDEX IF NOT EXISTS idx_notes_timestamp ON notes(timestamp);
    """

    conn = get_connection("app.db", init_sql=INIT_SQL)

    app.run(debug=True, host="127.0.0.1", port=5000)