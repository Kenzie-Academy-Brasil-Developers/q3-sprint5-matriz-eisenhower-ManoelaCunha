from flask import Flask
from app.routes.categories_route import bp as bp_categories

def init_app(app: Flask):
    app.register_blueprint(bp_categories)
