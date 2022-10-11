import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (EndpointNotAvailableException,
                        HTTPStatusErrorException, KeyException,
                        MessageException, StatusException)

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))


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
        logger.info(f'Бот начал отправлять сообщение {message}.')
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except telegram.TelegramError as error:
        raise MessageException('Ошибка при отправке сообщения.') from error
    else:
        logger.info('Сообщение отправлено.')


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        logger.info('Бот начал запрос к API.')
        homework_status = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
    except Exception as error:
        raise EndpointNotAvailableException(
            f'Сбои при запросе к эндпоинту {error}.'
            f'Недоступны параметры запроса {ENDPOINT}, {params}.'
        ) from error
    else:
        if homework_status.status_code != HTTPStatus.OK:
            raise HTTPStatusErrorException(
                f'Страница недоступна {error}.'
                f'Недоступны параметры запроса {ENDPOINT}, {params}.'
            )
    return homework_status.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    if not isinstance(response, dict):
        raise TypeError('Объект не является словарём.')
    homeworks = response.get('homeworks')
    if homeworks is None:
        raise KeyException('Oтсутствует ожидаемый ключ homeworks.')
    if not isinstance(homeworks, list):
        raise IndexError('Объект не является списком.')
    return homeworks


def parse_status(homework):
    """Отправляет статус домашней работы."""
    if not isinstance(homework, dict):
        raise TypeError('Объект не является словарём.')
    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise KeyError('Oтсутствует ожидаемый ключ homework_name.')
    homework_status = homework.get('status')
    if homework_status is None:
        raise KeyException('Oтсутствует ожидаемый ключ homework_status.')
    if homework_status not in HOMEWORK_STATUSES:
        raise StatusException('Недокументированный статус домашней работы.')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        error_tokens = 'Нет обязательных переменных окружения.'
        logger.critical(error_tokens)
        sys.exit(error_tokens)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    past_time = ''
    message_error = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            if homework == []:
                logger.debug('Отсутствует домашняя работа.')
            else:
                homework = homework[0]
                if homework['date_updated'] != past_time:
                    past_time = homework['date_updated']
                    message = parse_status(homework)
                    send_message(bot, message)
                else:
                    logger.debug('Отсутствует новый статус домашней работы.')
            current_timestamp = response.get('current_data')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message, exc_info=True)
            if message != message_error:
                send_message(bot, message)
                message_error = message
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
