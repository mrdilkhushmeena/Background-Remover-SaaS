from flask import Flask
from config import Config
from utils.db import init_db

from routes.api import api_bp
from routes.admin import admin_bp
from routes.web import web_bp

app = Flask(__name__)
app.config.from_object(Config)

# Init DB
init_db()

# Register routes
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(web_bp)

if __name__ == "__main__":
    app.run(debug=True)