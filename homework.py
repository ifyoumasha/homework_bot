from asyncio.log import logger
from http import HTTPStatus
import logging
import os
from typing import Type
import requests
import telegram
import time
from dotenv import load_dotenv
from exceptions import(
    HTTPStatusErrorException,
    MessageException,
    NegativeValueException,
    KeyException,
    StatusException
)


load_dotenv()

logging.basicConfig(
    filename='program.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        raise MessageException('Ошибка при отправке сообщения.') from error
    else:
        logger.info('Сообщение отправлено.')
        

def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        homework_status = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
        if homework_status.status_code != HTTPStatus.OK:
            logger.error('Страница недоступна.')
            raise HTTPStatusErrorException('Страница недоступна.')
    except Exception as error:
        raise NegativeValueException('Недоступность эндпоинта.') from error
    return homework_status.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    if not isinstance(response, dict):
        raise TypeError('Объект не является словарём.')
    homeworks = response.get('homeworks')
    if homeworks is None:
        logger.error('Oтсутствует ожидаемый ключ.')
        raise KeyException('Oтсутствует ожидаемый ключ.')
    if not isinstance(homeworks, list):
        raise TypeError('Объект не является списком.')
    return homeworks

def parse_status(homework):
    """
    Извлекает из информации о конкретной домашней работе
    статус этой работы.
    """
    if not isinstance (homework, dict):
        raise TypeError('Неизвестный тип.')
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status is None:
        logger.error('Недокументированный статус.')
        raise StatusException('Недокументированный статус.')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """
    Проверяет доступность переменных окружения,
    которые необходимы для работы программы.
    """
    return all ([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Нет обязательных переменных окружения.')
        raise NegativeValueException
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    past_time = ''
    message_error = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            for homework in homeworks:
                if homework['date_updated'] != past_time:
                    past_time = homework['date_updated']
                    message = parse_status(homework)
                    send_message(bot, message)
                else:
                    logger.debug('Отсутствует новый статус.')
            current_timestamp = response('current_data')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if message != message_error:
                send_message(bot, message)
                message_error = message
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
