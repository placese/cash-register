# Cash register

Тестовое задание - абстрактный кассовый аппарат, генерирующий чеки по входящим id товаров, предоставляющий возможность пользователю получить чек по QR коду.

#### Backend: Django, DRF
#### Tests: Django tests
#### Database: PostgreSQL, Django ORM
#### QRcode generation: qrcode
#### PDF generation: Jinja2, pdfkit

### Установка

- Установите Python 3.10 или выше
- Создайте и активируйте виртуальное окружение
- Установите все необходимые зависимости `pip install -r requirements.txt`
- Установите wkhtmltopdf
- Установите postgres
- Создайте базу данных и запишите credentials в setenv.env файл (рядом с manage.py)
Пример файла setenv.env:
```
    DEBUG={true/false}
    SECRET_KEY={Secret key}
    DB_NAME={Database name}
    DB_USER={Database user}
    DB_PASSWORD={Database user's password}
    DB_HOST={Database host}
    DB_PORT={Database port}
    ROOT_HOST={HOST TO RUN THE SERVER (ip:port)}
```
- После запуска наполните таблицу БД тестовыми данными, например через консоль Postgres:
`INSERT INTO ITEM (title, price) VALUES ('мороженое', 100.0);`

### Запуск и тестирование

Для тестирования рекомендуется в setenv.env файл в ROOT_HOSTS указать хост машины в локальной сети, например `192.168.0.1:8000`
Также при этом необходимо запустить сервер на указанном хосту, например: `python manage.py runserver 192.168.0.1:8000`

Для создания чека и получения QR когда нужно отправить **POST** запрос по адресу `http://{{ROOT_HOST}}/cash_machine/`
В теле запроса необходимо передеть JSON вида: 
```
{
	"items": [1, 1, 2, 4, 5]
}
```
Где элементы массива items - id номера товаров в базе данных

Если данные отправлены корректно, сервер отдаст QR-код, отсканировав который Вы увидите созданный чек

### Идеи для доработки

- Дописать тесты
- Отправлять задачи генерации pdf и qr кодов в celery
- Завернуть всё в docker
