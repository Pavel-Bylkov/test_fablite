from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)  # Инициализация JWTManager

# Импортируем маршруты после инициализации приложения и базы данных
from app import routes, models
from app.auth import auth_bp
from app.routes import routes_bp  # Импортируем Blueprint для маршрутов

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(routes_bp)  # Регистрируем Blueprint для маршрутов