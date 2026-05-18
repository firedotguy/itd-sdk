# Клиент

```py
c = ITDClient(
    refresh=getenv('TOKEN')
    access=None,
    config=ITDConfig()
)
```

### Параметры
#### refresh <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Refresh токен.

#### access <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Access токен (JWT).

#### config <span class="mdx-badge"><span class="mdx-badge__icon">:fontawesome-solid-gear:</span><span class="mdx-badge__text">ITDConfig</span></span>
Конфиг (см. [параметры](../config.md)).

---

## Сделать запрос
```py
from itd.enums import AuthLevel

res = c.request(
    method='post',
    url='v1/auth/refresh',
    params={},
    files={},
    level=AuthLevel.REFRESH
)
```
Сделать кастомный запрос на ИТД (эта функция используется внутри самого sdk).

### Параметры
#### method <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Метод запроса (`get`/`post`/`put`/`delete` и тд).

#### url <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Адрес запроса (без /api).

#### params <span class="mdx-badge"><span class="mdx-badge__icon">:material-code-braces:</span><span class="mdx-badge__text">dict</span></span>
Параметры к запросу.

#### files <span class="mdx-badge"><span class="mdx-badge__icon">:material-code-braces: :material-text:, :material-code-parentheses: :material-file:</span><span class="mdx-badge__text">dict[str, tuple[str, BufferedReader | bytes]]</span></span>
Файл для загрузке в формате `{'file': ('имя файла', 'содержание')}`

#### level <span class="mdx-badge"><span class="mdx-badge__icon">:material-code-braces:</span><span class="mdx-badge__text">dict</span></span>
Требуемый уровень авторизации для запроса. По умолчанию AuthLevel.ACCESS.


### Ошибки
 - `InsufficientAuthLevelError` - недостаточный уровень авторизации

---

## Обновить статистики постов
```py
c.update_post_stats()
```
Обновить статистики (лайки, комментарии, репосты итд) просмотров в зоне видимости.  
Для добавления поста в зону видимости используйте `post.set_visible()` или `c.visible_posts.append(post)`

### Ошибки
 - `NotFoundError` - пост(ы) не найден(ы)

---

## Изменить пароль
```python
c.change_password(
    old='12345678',
    new='12345679'
)
```
!!! caution

    После сброса пароля `refresh token` сбросится. Нужно входить заново.

### Параметры

#### old <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span> <span class="mdx-badge mdx-badge_required"><span class="mdx-badge__icon">:material-information:</span> <span class="mdx-badge__text">Required</span></span>
Старый пароль.

#### new <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span> <span class="mdx-badge mdx-badge_required"><span class="mdx-badge__icon">:material-information:</span> <span class="mdx-badge__text">Required</span></span>
Новый пароль. 10+ символов, цифры, знаки пунктуации, латиница

### Ошибки
 - `SamePasswordError` - пароли повторяются.
 - `InvalidOldPasswordError` - старый пароль неверный.
 - `InvalidPasswordError` - пароль не соответствует требованиям.

---

## Выйти
```python
c.logout()
```

!!! caution

    После выхода `refresh token` сбросится. Нужно входить заново.

---

## Обновить `access_token`
```python
token = c.refresh_auth()
```

### Ошибки
 - `SessionExpiredError` - рефреш токен истек (7 дней)
 - `SessionNotFoundError` - сессия не найдена (неправильный рефреш токен)
 - `SessionRevokedError` - сессия была ревокнута (выход из аккаунта)

