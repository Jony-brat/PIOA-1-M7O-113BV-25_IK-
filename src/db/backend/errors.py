class StudentTableError(Exception):
    """Базовый класс для исключений, связанных с работой таблицы студентов."""

    pass


class InvalidAgeError(StudentTableError):
    """Исключение, возникающее при попытке добавить запись с неподходящим значением возраста."""

    pass


class DuplicateIDError(StudentTableError):
    """Исключение, возникающее при попытке добавить запись с идентификатором, который уже используется."""

    pass