class MessageException(Exception):
    """Ошибка при отправке сообщения."""
    pass

def send_message(message):
    if message is None:
        raise MessageException('Ошибка при отправке сообщения.')


class EndpointNotAvailableException(Exception):
    """Недоступность эндпоинта."""
    pass

def endpoint_api(endpoint):
    if endpoint is None:
        raise EndpointNotAvailableException(f'Недоступность эндпоинта.')


class HTTPStatusErrorException(Exception):
    """Страница недоступна."""
    pass

def page_bot(page):
    if page is None:
        raise HTTPStatusErrorException(f'Страница недоступна.')


class KeyException(Exception):
    """Oтсутствует ожидаемый ключ.'"""
    pass

def dictionary_key(key):
    if key is None:
        raise KeyException(f'Oтсутствует ожидаемый ключ.')


class StatusException(Exception):
    """Недокументированный статус домашней работы.'"""
    pass

def status_page(status):
    if status is None:
        raise StatusException('Недокументированный статус домашней работы.')
