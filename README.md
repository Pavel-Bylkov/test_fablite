# test_fablite

Простое веб-приложение для демонстрации

## Описание тестового задания:

- Разработать простое серверное приложение на выбранном вами языке программирования.
- Реализовать базу данных.
- Реализовать функции регистрации и аутентификации пользователей.
- Реализовать обработку следующих типов запросов:
    - Получение списка пользователей.
    - Добавление нового пользователя.
    - Обновление информации о пользователе.
    - Удаление пользователя.
- Обеспечить минимальную защиту приложения (например, защита от SQL-инъекций).

## Критерии оценки тестового задания:

- Чистота и качество кода.
- Правильность и логичность реализации функционала.
- Способность обеспечить базовую защиту данных.
- Документация кода и комментарии.

## Принятые решения для выполнения задания

На основе требований принял решение продемонстрировать свои навыки на примере
Приложения на Flask + SQLAlchemy с базой данных PostgreSQL - принимающего запросы и отвечающее JSON данными:

### Эндпоинты:

#### 1. POST /auth/register

Регистрация пользователя.

**Пример запроса:**

```json
{
  "email": "testuser@mail.ru",
  "password": "testpassword"
}
```

**Пример успешного ответа:**

```json
{
  "message": "User registered successfully"
}
```

**Пример ответа при ошибке:**

```json
{
  "error": "User already exists"
}
```

#### 2. POST /auth/login

Вход пользователя.

**Пример запроса:**

```json
{
  "email": "testuser@mail.ru",
  "password": "testpassword"
}
```

**Пример успешного ответа:**

```json
{
  "access_token": "<your_access_token>"
}
```

**Пример ответа при ошибке:**

```json
{
  "error": "Invalid credentials"
}
```

#### 3. POST /new_team

Создание команды и регистрация руководителя.

**Пример запроса:**

```json
{
  "team_name": "TeamA"
}
```

**Пример успешного ответа:**

```json
{
  "message": "Team created successfully",
  "invite_link": "http://site.ru/TeamA/add_member"
}
```

**Пример ответа при ошибке:**

```json
{
  "error": "Team name already exists"
}
```

#### 4. POST /<name_team>/add_member

Регистрация пользователя самостоятельно или добавление руководителем.

**Пример запроса:**

```json
{
  "name": "Петр",
  "surname": "Петров",
  "email": "petr.petrov@mail.ru",
  "password": "securepassword123"
}
```

**Пример успешного ответа:**

```json
{
  "message": "Member added successfully"
}
```

**Пример ответа при ошибке:**

```json
{
  "error": "User already exists or unauthorized access"
}
```

#### 5. DELETE /<name_team>/<user_name>

Удаление пользователя. Только руководитель может удалить любого пользователя.

**Пример успешного ответа:**

```json
{
  "message": "User deleted successfully"
}
```

**Пример ответа при ошибке:**

```json
{
  "error": "Unauthorized access or user not found"
}
```

#### 6. PUT /<name_team>/<user_name>/profile

Обновление профиля пользователя.

**Пример запроса:**

```json
{
  "name": "Петр",
  "surname": "Петров"
}
```

**Пример успешного ответа:**

```json
{
  "message": "Profile updated successfully"
}
```

**Пример ответа при ошибке:**

```json
{
  "error": "Unauthorized access or invalid data"
}
```

#### 7. GET /<name_team>

Получение списка всех участников команды.

**Пример успешного ответа:**

```json
{
  "team_name": "TeamA",
  "members": [
    {
      "name": "Иван",
      "surname": "Иванов",
      "role": "Leader"
    },
    {
      "name": "Петр",
      "surname": "Петров",
      "role": "Member"
    }
  ]
}
```

**Пример ответа при ошибке:**

```json
{
  "error": "Team not found"
}
```

## Дополнительные функции:

- **Реализация JWT аутентификации**: Обеспечит более безопасную и современную систему аутентификации.
- **Реализация ролей и прав доступа**: Руководитель может управлять всеми пользователями, а обычные пользователи имеют
  ограниченные права.
- **Защита от SQL-инъекций**: Внедрение механизмов защиты от распространенных веб-уязвимостей.
  SQLAlchemy автоматически защищает от SQL-инъекций.
- **Документация API**: Использование Swagger для документирования API.

## Запуск и проверка приложения

После запуска приложения, вы сможете увидеть сгенерированную документацию API, перейдя по
адресу `http://127.0.0.1:5000/apidocs`.

1. Убедитесь, что PostgreSQL запущен и настроен:
   Установите PostgreSQL, если он еще не установлен.
   Инструкции по установке можно найти на официальном сайте PostgreSQL: https://www.postgresql.org/download/

2. Активируйте виртуальное окружение:
   На Windows:

```
.\venv\Scripts\activate
```

На macOS/Linux:

```
source venv/bin/activate
```

3. Убедитесь, что все зависимости установлены:

```
pip install -r requirements.txt
```

4. Запустите скрипт для настройки базы данных:
   Проверьте, что база данных test_fablite создана и пользователь test_user имеет к ней доступ.

```commandline
python app/create_db.py
```

Выполните миграции для базы данных

```commandline
rm -r migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Запустите Flask приложение:

```
python run.py
```

6. Проверьте работу приложения с помощью команды:

```
python test_client.py
```

или вручную с помощью cURL или Postman:

### Примеры запросов

#### 1. Регистрация пользователя

```
curl -X POST http://localhost:5000/auth/register -H "Content-Type: application/json" -d '{ "email":"testuser@example.com", "password":"testpassword"}'
```

#### 2. Вход пользователя

```
curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d '{"email":"testuser@example.com", "password":"testpassword"}'
```

#### 3. Создание команды

```
curl -X POST http://localhost:5000/new_team -H "Content-Type: application/json" -H "Authorization: Bearer <your_access_token>" -d '{"team_name":"TeamA"}'
```

#### 4. Добавление участника без авторизации

```
curl -X POST http://localhost:5000/TeamA/add_member -H "Content-Type: application/json" -d '{"name":"Петр", "surname":"Петров", "email":"petr.petrov@mail.ru", "password":"securepassword123"}'
```

#### 5. Удаление пользователя

```
curl -X DELETE http://localhost:5000/TeamA/petr.petrov@mail.ru -H "Authorization: Bearer <your_access_token>"
```

#### 6. Обновление профиля

```
curl -X PUT http://localhost:5000/TeamA/petr.petrov@mail.ru/profile -H "Content-Type: application/json" -H "Authorization: Bearer <your_access_token>" -d '{"name":"Петр", "surname":"Петров"}'
```

#### 7. Получение списка участников команды без авторизации

```
curl -X GET http://localhost:5000/TeamA
```

**Примечание**
Замените <your_access_token> на токен, полученный после успешного входа пользователя.
