# itd-sdk
Клиент ITD для python


## Установка

```bash
pip install itd-sdk
```

## Пример

```python
from itd import ITDClient

c = ITDClient('TOKEN', 'refresh_token=...; __ddg1_=...; __ddgid_=...; is_auth=1; __ddg2_=...; ddg_last_challenge=...; __ddg8_=...; __ddg10_=...; __ddg9_=...')
# можно указать только токен, тогда после просрочки перестанет работать, либо только куки чтобы токен сразу подтянулся, либо оба сразу

print(c.get_me())
```

> [!NOTE]
> Берите куки из запроса /auth/refresh. В остальных запросах нету refresh_token
> ![cookie](cookie-screen.png)

---
### Скрипт на обновление имени
Этот код сейчас работает на @itd_sdk (обновляется имя и пост)
```python
from itd import ITDClient
from time import sleep
from random import randint
from datetime import datetime
from datetime import timezone

c = ITDClient(None, '...')

while True:
    c.update_profile(display_name=f'PYTHON ITD SDK | Рандом: {randint(1, 100)} | {datetime.now().strftime("%m.%d %H:%M:%S")}')
    # редактирование поста
    # c.edit_post('82ea8a4f-a49e-485e-b0dc-94d7da9df990', f'рил ща {datetime.now(timezone.utc).isoformat(" ")} по UTC (обновляется каждую секунду)')
    sleep(1)
```

### Скрипт на смену баннера
```python
from itd import ITDClient

c = ITDClient(None, '...')

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

### SSE - прослушивание уведомлений в реальном времени

```python
from itd import ITDClient, StreamConnect, StreamNotification

# Используйте cookies для автоматического обновления токена
c = ITDClient(cookies='refresh_token=...; __ddg1_=...; is_auth=1')

for event in c.stream_notifications():
    if isinstance(event, StreamConnect):
        print(f'! Подключено к SSE: {event.user_id}')
    elif isinstance(event, StreamNotification):
        print(f'-- {event.type.value}: {event.actor.display_name} (@{event.actor.username})')
```

> [!NOTE]
> SSE автоматически переподключается при истечении токена

Типы уведомлений:
- `like` - лайк на пост
- `follow` - новый подписчик
- `wall_post` - пост на вашей стене
- `comment` - комментарий к посту
- `reply` - ответ на комментарий
- `repost` - репост вашего поста

### Кастомные запросы

```python
from itd.request import fetch

fetch(c.token, 'метод', 'эндпоинт', {'данные': 'данные'})
```
Из методов поддерживается `get`, `post`, `put` итд, которые есть в `requests`
К названию эндпоинта добавляется домен итд и `api`, то есть в этом примере отпарвится `https://xn--d1ah4a.com/api/эндпоинт`.

> [!NOTE]
> `xn--d1ah4a.com` - punycode от "итд.com"

## Планы

 - Форматированные сообщения об ошибках
 - Логирование (через logging)
 - Добавление ООП (отдеьные классы по типу User или Post вместо обычного JSON)
 - Голосовые сообщения


## Прочее
Лицезия: [MIT](./LICENSE)
Идея (и часть эндпоинтов): https://github.com/FriceKa/ITD-SDK-js
 - По сути этот проект является реворком, просто на другом языке

Автор: [itd_sdk](https://xn--d1ah4a.com/itd_sdk) (в итд) [@desicars](https://t.me/desicars) (в тг)
