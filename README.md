# pyClient
Клиент ITD для python


## Установка

```bash
pip install itd-iter-api
```

## Пример

```python
from iter import Client

c = Client() # вход через встроенный браузер или из файла
c = Client(email='mail@example.com', password='1234') # вход через встроенный браузер и автозаполнение или из файла
c = Client(token='afvrc...', cookies='refresh_token=...;__ddg1=...; ...') # вход используя токен и куки или из файла
c = Client(use_manual_login=False) # можно отключить вход через браузер
c = Client(session_file='session.jsoon') # файл сессии с токеном и куки

print(c.get_me())
```

---
### Скрипт на обновление имени
Этот код сейчас работает на @itd_sdk (обновляется имя и пост)
```python
from itd import Client
from time import sleep
from random import randint
from datetime import datetime
from datetime import timezone

c = Client(None, '...')

while True:
    c.update_profile(display_name=f'PYTHON ITD SDK | Рандом: {randint(1, 100)} | {datetime.now().strftime("%m.%d %H:%M:%S")}')
    sleep(1)
```

### Скрипт на смену баннера
```python
from itd import Client

c = Client(None, '...')

id = c.upload_file('любое-имя.png', open('реальное-имя-файла.png', 'rb'))['id']
c.update_profile(banner_id=id)
print('баннер обновлен')

```

### Встроенные запросы
Существуют встроенные эндпоинты для комментариев, хэштэгов, уведомлений, постов, репортов, поиска, пользователей, итд.
```python
c.get_user('ITD_API') # получение данных пользователя
c.get_me() # получение своих данных (me)
c.update_profile(display_name='22:26') # изменение данных профиля, например имя, био итд
c.create_post('тест1') # создание постов
# итд
```

### Кастомные запросы

```python
from iter.request import fetch

fetch(c.token, 'метод', 'эндпоинт', {'данные': 'данные'})
```
Из методов поддерживается `get`, `post`, `put` итд, которые есть в `requests`
К названию эндпоинта добавляется домен итд и `api`, то есть в этом примере отпарвится `https://xn--d1ah4a.com/api/эндпоинт`.

> [!NOTE]
> `xn--d1ah4a.com` - punycode от "итд.com"