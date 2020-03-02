import os

from flask import Flask

from app.view import bp as main_bp

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

app = Flask(__name__)

app.register_blueprint(main_bp)
