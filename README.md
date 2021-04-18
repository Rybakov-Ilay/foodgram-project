# Foodgram

![CI project](https://github.com/Rybakov-Ilay/foodgram-project/actions/workflows/main/badge.svg)

## Проект развернут по адресу [http://130.193.54.57/](http://130.193.54.57/)
 Логин и пароль для теста
```
login: test
password: zaqwsxzaqwsx
```

## Описание
«Продуктовый помощник» - дипломный проект курса [Яндекс.Практикума](https://praktikum.yandex.ru) по профессии python-разработчик.

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
##  Основные возможности

-   Просматривать рецепты на главной странице.
-   Просматривать отдельные страницы рецептов.
-   Просматривать страницы пользователей.
-   Фильтровать рецепты по тегам.
-   Входить в систему под своим логином и паролем.
-   Выходить из системы (разлогиниваться).
-   Восстанавливать свой пароль.
-   Менять свой пароль.
-   Создавать/редактировать/удалять собственные рецепты
-   Просматривать рецепты на главной.
-   Просматривать страницы пользователей.
-   Просматривать отдельные страницы рецептов.
-   Работать с персональным списком избранного: добавлять/удалять чужие рецепты, просматривать свою страницу избранных рецептов.
-   Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингредиентов для рецептов из списка покупок.
-   Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

## Как развернуть проект

* Установите Docker и Docker-Compose.
* Клонируйте репозиторий 
`git@github.com:Rybakov-Ilay/foodgram-project.git`
* Создаййте в папке foodgram-project файл `.env` с переменными окружения.
Пример:  
```
SECRET_KEY="@ermwao0zi_esf-93ca!&x=_ptlzp0j9l=jo$qe-g3$5lu+!l0"

# DATABASES

DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
* Откройте терминал и запустите сборку docker-контейнеров командой:  
`sudo docker-compose up -d`.    
Приложение развернется в трех контейнерах работу которых можно посмотреть комадой:    
`sudo docker container <id_container> ls -a`
* Остается создать миграции, суперюзера, собрать статику и загрузить базу ингридиентов и тэгов.
Для этого зайдем в контейнер foodgram-project_web_1    
`sudo docker-compose exec foodgram-project_web_1 -it bash`  
и применим следующие команды:
```
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py createsuperuser
python manage.py loaddata ingredients_load.json
python manage.py loaddata recipes_tag.json
python manage.py collectstatic
```
Проект развернется по адресу http://localhost:8005/  
Пример рабочего проекта можно посмотреть [тут](http://130.193.54.57/).

## Стек технологий
* [Pyhton](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Nginx](https://nginx.org/ru/)
* [Gunicorn](https://gunicorn.org/)
* [Yandex.Cloud](https://cloud.yandex.ru/)

## Автор 
Рыбков Илья