import requests


BASE_URL = "http://localhost:5000"

def register_user(email, password, name=None, surname=None):
    """
    Регистрирует нового пользователя.

    :param email: Email пользователя
    :param password: Пароль пользователя
    :param name: Имя пользователя
    :param surname: Фамилия пользователя
    """
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
    """
    Авторизует пользователя.

    :param email: Email пользователя
    :param password: Пароль пользователя
    :return: Access token при успешной авторизации, иначе None
    """
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
    """
    Создает новую команду.

    :param token: Access token пользователя
    :param team_name: Название команды
    """
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
    """
    Добавляет нового участника в команду.

    :param team_name: Название команды
    :param name: Имя участника
    :param surname: Фамилия участника
    :param email: Email участника
    :param password: Пароль участника
    """
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
    """
    Удаляет пользователя из команды.

    :param token: Access token пользователя
    :param team_name: Название команды
    :param user_email: Email пользователя для удаления
    """
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
    """
    Обновляет профиль пользователя.

    :param token: Access token пользователя
    :param team_name: Название команды
    :param user_email: Email пользователя для обновления профиля
    :param name: Новое имя пользователя
    :param surname: Новая фамилия пользователя
    """
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
    """
    Получает список участников команды.

    :param team_name: Название команды
    """
    url = f"{BASE_URL}/{team_name}"
    response = requests.get(url)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print(f"Get Team Members: {response.status_code}, {response_json}")

if __name__ == "__main__":
    # Регистрация пользователя
    leader = {'email': "testuser@mail.ru", 'pass': "testpassword", 'name': "Иван", "surname": "Иванов"}
    team_name = "TeamA"
    member = {'email': "petr.petrov@mail.ru", 'pass': "testpassword", 'name': "Петр", "surname": "Петров"}
    register_user(leader['email'], leader['pass'], leader['name'], leader['surname'])

    # Вход пользователя
    token = login_user(leader['email'], leader['pass'])

    if token:
        # Создание команды
        create_team(token, team_name)

        # Добавление участника без авторизации
        add_member(team_name, member['name'], member['surname'], member['email'], member['pass'])

        # Вход нового участника
        member_token = login_user(member['email'], member['pass'])

        if member_token:
            # Получение списка участников команды
            get_team_members(team_name)

            # Обновление профиля участника
            update_profile(member_token, team_name, member['email'], "Леонид", "Петров")

            # Получение списка участников команды
            get_team_members(team_name)

            # Удаление участника
            delete_user(token, team_name, member['email'])

            # Получение списка участников команды
            get_team_members(team_name)