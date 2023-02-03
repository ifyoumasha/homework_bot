### Описание проекта:

Мой бот-помощник - telegram-бот, который обращается к API сервиса Домашка и узнаёт статус домашней работы: взята ли работа в ревью, проверена ли она, принята ли ревьюером или возвращена на доработку.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ifyoumasha/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
или
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Запустить бота:

```
python3 homework.py
```
