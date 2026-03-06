# Посты

## Создать пост
```python
post = c.create_post(
    content='чиенбурбе круче чем #иванговно',
    spans=[],
    wall_recipient_id=None,
    attachemnt_ids=[],
    poll=None
)
```

### Параметры

#### content
Содержание поста.

#### spans
Стилизация.

!!! example

    Для получения этого списка можно использовать парсинг (на данный момент поддерживается только `html`):

    ```python
    from itd.utils import parse_html

    c.create_post(*parse_html('<b>Толстый</b> <i>и</i> тонкий'))
    ```
    **Результат:** **толстый** *и* тонкий

    !!! info

        `*` - символ для "разархивации". `parse_html` возвращает список, который `*` разделяет на `content` (читый контент без тэгов) и `spans`

#### wall_recipient_id
ID получателя поста (для постов на стене). `Username` не работает.

#### attachment_ids
ID вложений.

#### poll
Опросник.

!!! example

    ```python
    from itd.models.post import PollData

    c.create_post(
        poll=PollData(
            'вапро', # (1)
            ['орешки макадамья', 'мне офень нгахвятся'], # (2)
            False # (3)
        )
    )
    ```

    1. Вопрос опроса
    2. Варианты ответа
    3. Можно ли ответить сразу несколько вариантов (по умолчанию - `False`)


### Ошибки

#### NotFound
Получатель поста не найден.

!!! example

    ```python
    c.create_post(
        '123',
        wall_recipient_id=UUID('6b791b8b-e8b7-41ee-8e12-1d48ca0b4cf0') # !
    )
    ```

#### Forbidden
Некоторые вложения не принадлежат вам или файл не существует. Вложения должны быть загружены вами через `upload_file`.
!!! example

    ```python
    c.create_post(
        attachment_ids=[UUID('6b791b8b-e8b7-41ee-8e12-1d48ca0b4cf2')] # !
    )
    ```

#### ValidationError
Ошибка валидации, скорее всего из-за слишком большого количества символов.
!!! example

    ```python
    c.create_post(
        'шкебетоилет' * 1000 # !
    )
    ```

#### VideoRequiresVerification
Возникает при попытке загрузить видео с неверифицированого аккаунта.
!!! example

    ```python
    c.create_post(
        attachment_ids=[UUID('bc073a52-0d8a-4039-b33a-74b5a01b689f')] # !
    )
    ```

---

## Проголосовать
```python
poll = c.vote(
    id=UUID('aa612e16-eb1f-4323-89ce-4eacda133672'),
    option_ids=[UUID('f12c70c7-141e-4dff-9e5b-87f039c7ba58')]
)
```

### Параметры

#### id
ID поста.

#### option_ids
ID опций для выбора (даже если в опросе можно выбрать только 1 вариант, все равно пишите как список).

!!! example

    === "1 опция"

        ```python
        c.vote(
            UUID('aa612e16-eb1f-4323-89ce-4eacda133672'),
            [UUID('f12c70c7-141e-4dff-9e5b-87f039c7ba58')]
        )
        ```

    === "несколько опций"

        ```python
        c.vote(
            UUID('a6135f23-bd75-441b-93b7-cf9cf04ef76c'),
            [
                UUID('6daf7815-b30a-4f98-8091-7a0e24caba6c'),
                UUID('3add69ee-4dae-4a81-9e4a-3e0fe77c7be0'),
                UUID('ac758a37-2cb5-45ba-b743-a0a11a2b8d3d')
            ]
        )
        ```

---

## Получить посты
```python
posts, pagination = c.get_posts(
    cursor=0,
    tab=PostsTab.POPULAR
)
```
Лимит - 20 постов (не меняется).

### Параметры

#### cursor
Курсор для пагинации (из `pagination.next_cursor`).

!!! example

    ```python
    cursor = None

    while True:
        posts, pagination = c.get_posts(cursor=cursor)
        cursor = pagination.next_cursor
    ```

#### tab
Вкладка.

 - `POPULAR`: Популярные
 - `FOLLOWING`: Подписки
 - `CLAN`: Лента кланов

!!! example

    ```python
    from itd.enums import PostsTab

    c.get_posts(tab=PostsTab.FOLLOWING)
    ```
