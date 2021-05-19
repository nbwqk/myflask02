from flask import Flask

import settings
from apps.article.view import article_bp
from apps.users.view import user_bp
from exts import db, bootstrap


def create_app():
    app=Flask(__name__,template_folder='../templates',static_folder='../static')
    app.config.from_object(settings.DevelopmentConfig)
    db.init_app(app)
    bootstrap.init_app(app=app)
    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)
    return app