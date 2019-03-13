# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:33:23
# @Last Modified time: 2019-03-13 17:06:37
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    from config import config
    app.config.from_object(config[config_name])

    from .main.view import bp as main_bp
    app.register_blueprint(main_bp)

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    return app
