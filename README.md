# food-plan-website
 Food plan service website

### Установить зависимости
```
pip install -r requirements.txt
```
### Назначить виртуальные переменные
Создать в корне файл `.env` и прописать в нем:
```
DEBUG=True
STRIPE_PUBLISHABLE_KEY = sk_test_4eC39HqLyjWDarjtT1zdp7dc
```

### Создать суперпользователя для админки
```
python manage.py createsuperuser
```

### Запуск
Запустить сервер командой
```
python manage.py runserver
```
Зайти в админку по адресу [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/),
использую данные суперпользователя.

## Цель проекта
Учебный проект [Devman](https://dvmn.org/)