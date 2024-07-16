from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from app.models import db, User, Team
from app.utils import validate_json

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/new_team', methods=['POST'])
@jwt_required()
@validate_json('team_name')
def new_team():
    data = request.get_json()
    team_name = data.get('team_name')
    leader_id = get_jwt_identity()
    leader = User.query.get(leader_id)

    if Team.query.filter_by(name=team_name).first():
        return jsonify({"error": "Team name already exists"}), 400

    new_team = Team(name=team_name, leader_id=leader_id)
    db.session.add(new_team)
    db.session.commit()

    # Обновляем пользователя, чтобы указать его команду
    leader.teams.append(new_team)
    db.session.commit()

    return jsonify({
        "message": "Team created successfully",
        "invite_link": f"http://site.ru/{team_name}/add_member"
    }), 201

@routes_bp.route('/<name_team>/add_member', methods=['POST'])
@validate_json('name', 'surname', 'email', 'password')
def add_member(name_team):
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')

    team = Team.query.filter_by(name=name_team).first()
    if not team:
        return jsonify({"error": "Team not found"}), 404

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, surname=surname, email=email, password=hashed_password, role='member')
    new_user.teams.append(team)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Member added successfully"}), 201

@routes_bp.route('/<name_team>/<user_email>', methods=['DELETE'])
@jwt_required()
def delete_user(name_team, user_email):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user_to_delete = User.query.filter_by(email=user_email).first()
    team = Team.query.filter_by(name=name_team).first()

    if not user_to_delete:
        return jsonify({"error": "User not found"}), 404

    if not team:
        return jsonify({"error": "Team not found"}), 404

    if current_user.id != team.leader_id:
        return jsonify({"error": "Unauthorized access"}), 403

    if team not in user_to_delete.teams:
        return jsonify({"error": "User does not belong to this team"}), 400

    # Удаляем пользователя из команды
    user_to_delete.teams.remove(team)
    db.session.commit()

    # Проверяем, состоит ли пользователь еще в каких-либо командах
    if not user_to_delete.teams:
        # Если нет, удаляем пользователя из базы данных
        db.session.delete(user_to_delete)
        db.session.commit()

    return jsonify({"message": "User removed from team successfully"}), 200

@routes_bp.route('/<name_team>/<user_email>/profile', methods=['PUT'])
@jwt_required()
@validate_json('name', 'surname')
def update_profile(name_team, user_email):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user_to_update = User.query.filter_by(email=user_email).first()

    if not user_to_update:
        return jsonify({"error": "User not found"}), 404

    if current_user.email != user_email:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    user_to_update.name = data.get('name', user_to_update.name)
    user_to_update.surname = data.get('surname', user_to_update.surname)
    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200

@routes_bp.route('/<name_team>', methods=['GET'])
def get_team_members(name_team):
    team = Team.query.filter_by(name=name_team).first()

    if not team:
        return jsonify({"error": "Team not found"}), 404

    members = [{
        "name": member.name,
        "surname": member.surname,
        "role": member.role
    } for member in team.members]

    # Добавляем лидера команды в список участников, если его там нет
    if team.leader not in team.members:
        members.append({
            "name": team.leader.name,
            "surname": team.leader.surname,
            "role": "leader"
        })

    return jsonify({
        "team_name": team.name,
        "members": members
    }), 200