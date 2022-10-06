class MessageException(Exception):
    """Ошибка при отправке сообщения в Telegram чат."""
    pass


class HTTPStatusErrorException(Exception):
    pass


class NegativeValueException(Exception):
    pass


class KeyException(Exception):
    pass


class StatusException(Exception):
    pass
