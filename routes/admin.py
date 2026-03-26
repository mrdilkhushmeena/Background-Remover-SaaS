from flask import Blueprint, request, session, redirect, url_for, render_template
from utils.auth import login_required
from utils.db import get_db
from config import Config
import datetime, secrets

admin_bp = Blueprint("admin", __name__)

# LOGIN
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == Config.ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin.dashboard"))
    return "<form method='post'><input type='password' name='password'><button>Login</button></form>"


# DASHBOARD
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    c = conn.cursor()

    # total usage
    c.execute("SELECT COUNT(*) FROM usage_logs")
    total_calls = c.fetchone()[0]

    # keys
    c.execute("SELECT * FROM api_keys")
    keys = c.fetchall()

    # logs
    c.execute("SELECT * FROM usage_logs ORDER BY id DESC LIMIT 10")
    logs = c.fetchall()

    conn.close()

    return render_template("dashboard.html", total=total_calls, keys=keys, logs=logs)


# GENERATE KEY
@admin_bp.route("/generate_key", methods=["POST"])
@login_required
def generate_key():
    name = request.form["name"]
    key = "nk_" + secrets.token_hex(16)

    conn = get_db()
    conn.cursor().execute(
        "INSERT INTO api_keys (name, key_string, created_at) VALUES (?, ?, ?)",
        (name, key, str(datetime.datetime.now()))
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin.dashboard"))


# DELETE KEY
@admin_bp.route("/delete_key/<int:key_id>", methods=["POST"])
@login_required
def delete_key(key_id):
    conn = get_db()
    conn.cursor().execute("DELETE FROM api_keys WHERE id=?", (key_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin.dashboard"))


# UPDATE LIMIT
@admin_bp.route("/update_limit/<int:key_id>", methods=["POST"])
@login_required
def update_limit(key_id):
    new_limit = request.form["limit"]

    conn = get_db()
    conn.cursor().execute(
        "UPDATE api_keys SET limit_count=? WHERE id=?",
        (new_limit, key_id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin.dashboard"))


# RESET USAGE
@admin_bp.route("/reset_usage/<int:key_id>", methods=["POST"])
@login_required
def reset_usage(key_id):
    conn = get_db()
    conn.cursor().execute(
        "UPDATE api_keys SET used_count=0 WHERE id=?",
        (key_id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("admin.dashboard"))