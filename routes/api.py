from flask import Blueprint, request, jsonify, send_file
from utils.db import get_db
from PIL import Image
from rembg import remove, new_session
import io, datetime

api_bp = Blueprint("api", __name__)
bg_session = new_session("isnet-general-use")

# --- Background Removal API (Requires Authentication) ---
@api_bp.route("/api/remove", methods=["POST"])
def remove_bg():
    api_key = request.headers.get("X-API-KEY")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_keys WHERE key_string=?", (api_key,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid API key"}), 401

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file"}), 400

    try:
        img = Image.open(file.stream)
        output = remove(img, session=bg_session)

        img_io = io.BytesIO()
        output.save(img_io, "PNG")
        img_io.seek(0)

        # Log usage
        cursor.execute(
            "INSERT INTO usage_logs (key_string, timestamp, status) VALUES (?, ?, ?)",
            (api_key, datetime.datetime.now(), "SUCCESS")
        )
        conn.commit()

        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Image Processing API (Public) ---
@api_bp.route("/api/process-image", methods=["POST"])
def process_image():
    file = request.files.get("file")
    mode = request.form.get("mode")

    if not file or not mode:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        img = Image.open(file.stream)
        img_io = io.BytesIO()

        if mode == "resize":
            width = int(request.form.get("width", img.width))
            height = int(request.form.get("height", img.height))
            
            resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
            resized_img.save(img_io, "PNG")
            mimetype = "image/png"

        elif mode == "compress":
            # Convert to RGB if necessary for JPEG format
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            quality = int(request.form.get("quality", 80))
            img.save(img_io, "JPEG", quality=quality, optimize=True)
            mimetype = "image/jpeg"

        else:
            return jsonify({"error": "Invalid processing mode"}), 400

        img_io.seek(0)
        return send_file(img_io, mimetype=mimetype)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
