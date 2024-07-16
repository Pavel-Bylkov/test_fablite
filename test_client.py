import requests

BASE_URL = "http://localhost:5000"

def register_user(email, password, name=None, surname=None):
    url = f"{BASE_URL}/auth/register"
    payload = {
        "email": email,
        "password": password,
        "name": name,
        "surname": surname
    }
    response = requests.post(url, json=payload)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print(f"Register User: {response.status_code}, {response_json}")

def login_user(email, password):
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print(f"Login User: {response.status_code}, {response_json}")
    if response.status_code == 200:
        return response_json.get("access_token")
    return None

def create_team(token, team_name):
    url = f"{BASE_URL}/new_team"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "team_name": team_name
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print(f"Create Team: {response.status_code}, {response_json}")

def add_member(team_name, name, surname, email, password):
    url = f"{BASE_URL}/{team_name}/add_member"
    payload = {
        "name": name,
        "surname": surname,
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print(f"Add Member: {response.status_code}, {response_json}")

def delete_user(token, team_name, user_email):
    url = f"{BASE_URL}/{team_name}/{user_email}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print(f"Delete User: {response.status_code}, {response_json}")

def update_profile(token, team_name, user_email, name, surname):
    url = f"{BASE_URL}/{team_name}/{user_email}/profile"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "name": name,
        "surname": surname
    }
    response = requests.put(url, json=payload, headers=headers)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print(f"Update Profile: {response.status_code}, {response_json}")

def get_team_members(team_name):
    url = f"{BASE_URL}/{team_name}"
    response = requests.get(url)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print(f"Get Team Members: {response.status_code}, {response_json}")

if __name__ == "__main__":
    # Регистрация пользователя
    register_user("testuser@mail.ru", "testpassword", "Иван", "Иванов")

    # Вход пользователя
    token = login_user("testuser@mail.ru", "testpassword")

    if token:
        # Создание команды
        create_team(token, "TeamA")

        # Добавление участника без авторизации
        add_member("TeamA", "Петр", "Петров", "petr.petrov@mail.ru", "securepassword123")

        # Вход нового участника
        member_token = login_user("petr.petrov@mail.ru", "securepassword123")

        if member_token:
            # Получение списка участников команды
            get_team_members("TeamA")

            # Обновление профиля участника
            update_profile(member_token, "TeamA", "petr.petrov@mail.ru", "Петр", "Петров")

            # Удаление участника
            delete_user(token, "TeamA", "petr.petrov@mail.ru")