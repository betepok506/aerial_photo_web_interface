# 1. Описание

Данный репозиторий содеожит Web-интерфейс для [проекта](https://github.com/betepok506/aerial-photography-server). 

*Примечание: Проект находится в разработке, подробное описание будет позже*

# 2. Интерфейс
Интерфейс главной страницы карты с отображенными полигонами объектов

![](docs/interface_map.png)

# 3. Запуск

## 3.1 Локальная установка зависимостей

Для локального запуска необходимо произвесту установку зависимостей, выполнив команду:
```commandline
pip install -r requirements.txt
```
Далее необходимо запустить `app/main.py`

## 3.2 Запуск в docker контейнере

Для запуска в docker контейнере необходимо указать в `.env` необходимые переменные окружения, указанные в 
`.env_example`.

Назначения переменных:
```commandline
WEB_PORT --- Порт, по которому будет доступен web интерфейс
SERVER_HOST --- IP-адрес сервера aerial-photography-server (https://github.com/betepok506/aerial-photography-server)
SERVER_PORT --- Порт сервера aerial-photography-server (https://github.com/betepok506/aerial-photography-server)
```

Далее необходимо выполнить команду:
```commandline
bash ./tools/run.sh
```

# Дальнейшая работа:
- Улучшение интерфейса
- Добавление функционала вывода информации об объекте по клику
- Добавление возможности выбора объекта из списка
- Добавление разных карт/слоев
- ...
