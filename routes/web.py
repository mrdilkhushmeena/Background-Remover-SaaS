from flask import Blueprint, render_template, request, send_file, jsonify
from PIL import Image
from rembg import remove, new_session
import io

web_bp = Blueprint("web", __name__)

bg_session = new_session("isnet-general-use")

# --- UI Routes ---

@web_bp.route("/")
def home():
    return render_template("home.html")

@web_bp.route("/background-remover")
def tool():
    return render_template("tool.html")

@web_bp.route("/image-resizer")
def resizer():
    return render_template("resizer.html")

# --- Web Tool Endpoints ---

@web_bp.route("/web_remove", methods=["POST"])
def web_remove():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        img = Image.open(file.stream)
        output = remove(img, session=bg_session)

        img_io = io.BytesIO()
        output.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
