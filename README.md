# math-abiturient
Сайт подготовки абитуриентов по некоторым разделам математики
## Запуск при помощи [`Docker Compose`](https://www.docker.com/products/docker-desktop)
### 1. Создание `.env` файла
Добавьте файл `.env` рядом с файлом `settings.py` следующем формате:
```
SECKET_KEY=строка_используемая_для_хеширования_паролей
```
Для генерации такой строки можно воспользоваться [встроенной функцией.](https://stackoverflow.com/a/57678930)

[Зачем это вообще всё нужно?](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key)
### 2. Docker compose up
В репозитории выполните команду `docker-compose up`, уточнив логин, пароль и почту администратора в `Dockerfile`, например:

```
ENV DJANGO_SUPERUSER_PASSWORD=123456
ENV DJANGO_SUPERUSER_EMAIL=example@example.com
ENV DJANGO_SUPERUSER_USERNAME=admin
```
```
docker compose up
``` 

Сервис будет запущен на `localhost:8000`. Впоследствии, для удаления всех данных Docker из системы можно использовать
команду `docker system prune -fa`.

## Запуск вручную

### Предустановка
* Установите [git;](https://git-scm.com/downloads)
* Установите Python. Использовалась [эта версия.](https://www.python.org/downloads/release/python-388/)

### Скачивание проекта, установка библиотек

Для создания на рабочем столе проекта и установки всех зависимостей из консоли последовательно введите:
```
cd %userprofile%/desktop
git clone https://github.com/ivanovskii/math-abiturient
cd math-abiturient && python -m venv env
env/scripts/activate
pip install -r requirements.txt
```
### Настройка проекта и первый запуск

1. Поместите файл `.env` рядом с `settings.py`. [Подробнее.](#1-создание-env-файла)
2. Выполните миграции:

```
    python manage.py makemigrations
    python manage.py migrate
```

3. Создайте суперпользователя командой `python manage.py createsuperuser`
4. Запустите проект командой `python manage.py runserver`
5. Перейдите на [localhost.](http://127.0.0.1:8000/)

### Последующие запуски

* Каждый раз из консоли нужно запускать `env\scripts\activate`, `python manage.py runserver` или сконфигурировать
  запуск из IDE. Например, для VS Code это делается [так.](https://code.visualstudio.com/docs/python/tutorial-django)