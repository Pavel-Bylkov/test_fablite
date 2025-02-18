from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Регистрация нового пользователя.
    ---
    parameters:
      - name: email
        in: body
        type: string
        required: true
        description: Email пользователя
      - name: password
        in: body
        type: string
        required: true
        description: Пароль пользователя
      - name: role
        in: body
        type: string
        required: false
        description: Роль пользователя
      - name: name
        in: body
        type: string
        required: false
        description: Имя пользователя
      - name: surname
        in: body
        type: string
        required: false
        description: Фамилия пользователя
    responses:
      201:
        description: Пользователь успешно зарегистрирован
      400:
        description: Пользователь уже существует или неверный запрос
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')
    name = data.get('name', None)
    surname = data.get('surname', None)

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, role=role, name=name, surname=surname)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Вход пользователя.
    ---
    parameters:
      - name: email
        in: body
        type: string
        required: true
        description: Email пользователя
      - name: password
        in: body
        type: string
        required: true
        description: Пароль пользователя
    responses:
      200:
        description: Успешный вход
      401:
        description: Неверные учетные данные
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Получение защищенной информации пользователя.
    ---
    responses:
      200:
        description: Успешное получение информации
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"email": user.email}), 200