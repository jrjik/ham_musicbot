"""Модуль с кастомными исключениями."""

class RequestFailed(Exception):
    """Исключение, выбрасываемое при неудачном HTTP-запросе."""

    def __init__(self, message: str = 'Ошибка при выполнении запроса'):
        super().__init__(message)
