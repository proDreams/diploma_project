# Дипломный проект - Сервис для сотрудников службы поддержки.

## Содержание

- [Описание проекта](#описание-проекта)
- [Используемые технологии](#используемые-технологии)
- [Файлы](#файлы)
- [Демо](#демо)
- [Подготовка к запуску](#подготовка-к-запуску)
- [Запуск проекта](#запуск-проекта)
- [Автор](#автор)
- [Дата написания](#дата-написания)

## Описание проекта

Проект представляет собой сервис для работника службы поддержки.  
Сервис состоит из двух частей: сайта и Telegram-бота.  
Цель проекта - предоставить сотрудникам службы поддержки быстрый доступ к "скрипту" или "порядку действий" в ответ на
соответствующий запрос клиента.

## Используемые технологии
- Django 4 и Django REST Framework
- Bootstrap 5
- nginx
- PostgreSQL
- Docker и Docker Compose
- AIOgram 3
- requests

## Файлы

- Отчёт по дипломному проекту: _будет опубликован после защиты_
- Презентация дипломного проекта: _будет опубликована после защиты_

## Демо

- Демонстрационный сайт доступен по адресу: https://pressanybutton.press/
- Telegram-бот доступен по адресу: https://t.me/wb_scripts_bot

**Для доступа к сайту необходимо пройти регистрацию в Telegram-боте.**

## Подготовка к запуску

- Клонировать репозиторий:

```bash
git clone https://github.com/proDreams/diploma_project.git
```

- Перейти в директорию:

```bash
cd diploma_project
```

- Изменить права доступа:

```bash
chmod -vR 777 .
```

- Открыть `docker-compose.yaml`.
- В параметре `BOT_TOKEN=token` заменить `token` на ваш токен для Telegram-бота.
- В параметре `ADMIN_ID=id` заменить `id` на ваш Telegram-ID.

## Запуск проекта

- Запустить сервис:

```bash
sudo docker compose up -d
```

- Применить Миграции:

```bash
sudo docker exec -it diploma_project-web-1 python /code/WB_Scripts/wb_scripts/manage.py makemigrations
```  

```bash
sudo docker exec -it diploma_project-web-1 python /code/WB_Scripts/wb_scripts/manage.py migrate
```

- Собрать статические файлы:

```bash
sudo docker exec -it diploma_project-web-1 python /code/WB_Scripts/wb_scripts/manage.py collectstatic
```

- Добавить суперпользователя:

```bash
sudo docker exec -it diploma_project-web-1 python /code/WB_Scripts/wb_scripts/manage.py createsuperuser
```

- Перезапустить контейнер с Django:

```bash
sudo docker restart diploma_project-web-1
```

- Перейти по адресу http://127.0.0.1/ для доступа к сайту.
- Перейти по адресу http://127.0.0.1/admin/ для доступа к панели администратора.

## Автор

Иван Ашихмин

## Дата написания

Сайт - 10 марта 2023 - 29 марта 2023  
Бот - 18 мая 2023 - 26 мая 2023  
Деплой - 03 июня 2023 - 04 июня 2023  