from flask import request, jsonify
from functools import wraps


def validate_json(*expected_args):
    """
    Декоратор для проверки наличия ожидаемых аргументов в JSON данных запроса.

    :param expected_args: Ожидаемые аргументы в JSON данных.
    :type expected_args: tuple

    :return: Результат выполнения функции или сообщение об ошибке, если аргументы отсутствуют.
    :rtype: dict
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            Проверяет наличие ожидаемых аргументов в JSON данных запроса.

            :param args: Позиционные аргументы функции.
            :param kwargs: Именованные аргументы функции.

            :return: Результат выполнения функции или сообщение об ошибке, если аргументы отсутствуют.
            :rtype: dict
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400
            for arg in expected_args:
                if arg not in data:
                    return jsonify({"error": f"Missing argument: {arg}"}), 400
            return f(*args, **kwargs)

        return wrapper

    return decorator