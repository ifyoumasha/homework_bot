class MessageException(Exception):
    """Ошибка при отправке сообщения."""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'MessageException' .format(self.message)
        else:
            return 'MessageException, ошибка при отправке сообщения.'


class EndpointNotAvailableException(Exception):
    """Недоступность эндпоинта."""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'EndpointNotAvailableException' .format(self.message)
        else:
            return 'EndpointNotAvailableException, недоступность эндпоинта.'


class HTTPStatusErrorException(Exception):
    """Страница недоступна."""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'HTTPStatusErrorException' .format(self.message)
        else:
            return 'HTTPStatusErrorException, страница недоступна.'


class KeyException(Exception):
    """Oтсутствует ожидаемый ключ."""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'KeyException' .format(self.message)
        else:
            return 'KeyException, отсутствует ожидаемый ключ.'


class StatusException(Exception):
    """Недокументированный статус домашней работы."""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'StatusException' .format(self.message)
        else:
            return 'StatusException, недокументированный статус домашней работы.'
