# :fontawesome-solid-user: Пользователь

## Получить пользователя
```python
user = User('itd_sdk')
```

### Получить пользователя по ID
```py
user = User.by_id('587167e9-25ad-4948-afc0-2ee5bc9097ea')
```

### Получить пользователя по username
```py
user = User.by_username('itd_sdk')
```
или
```py
user = User.by_u('itd_sdk')
```

### Получить текущего пользователя
```py
user = User.me()
```
или
```py
user = Me()
```


### Параметры
#### username_or_id <span class="mdx-badge"><span class="mdx-badge__icon">:material-text: | :material-identifier:</span><span class="mdx-badge__text">str | UUID</span></span> <span class="mdx-badge mdx-badge_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">Required</span></span>
Username или ID пользователя.

!!! note
    Для проверки на существование (`NotFoundError`) вызовите [`user.refresh()`](#_9) или любой аттрибут (если не включен [`config.auto_load`](../config.md#auto_load-bool))

---

## :octicons-report-16: Пожаловаться
```py
report = user.report(
    reason=ReportReason.SPAM,
    description='описание'
)
```
Пожаловаться на пользователя

### Параметры
#### reason <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-report-16:</span><span class="mdx-badge__text">ReportReason</span></span> <span class="mdx-badge mdx-badge_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">Required</span></span>
Причина жалобы.
 - `ReportReason.SPAM`: Спам или нежелательный контент
 - `ReportReason.VIOLENCE`: Насилие или опасные действия
 - `ReportReason.HATE`: Ненависть или травля
 - `ReportReason.ADULT`: Контент для взрослых (18+)
 - `ReportReason.FRAUD`: Дезинформация или обман
 - `ReportReason.OTHER`: Другое

#### description <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Описание жалобы.

### Ошибки
 - `NotFoundError` - пользователь не найден.
 - `AlreadyReportedError` - вы уже оставляли жалобу на этого пользователя.
 - `ValidationError` - ошибка валидации (слишком длинное описание).

---

## :fontawesome-solid-user-plus: Подписаться
```py
followers_count = user.follow()
```
Подписаться на пользователя.

### Ошибки
 - `NotFoundError` - пользователь не найден.
 - `AlreadyFollowingError` - вы уже подписаны на этого пользователя.
 - `TooLargeError` - слишком длинный юзернейм.
 - `CantFollowYouself` - нельзя подписываться на самого себя.
 - `UserBlockedError` - пользователь заблокирован (или вы заблокировали его).
 - `TargetUserBannedError` - пользователь забанен.

---

## :fontawesome-solid-user-minus: Отписаться
```py
followers_count = user.unfollow()
```
Отписаться от пользователя.

### Ошибки
 - `NotFoundError` - пользователь не найден.
 - `TooLargeError` - слишком длинный юзернейм.
 - `TargetUserBannedError` - пользователь забанен.

---

## :material-block-helper: Заблокировать
```py
user.block()
```

### Ошибки
 - `NotFoundError` - пользователь не найден.
 - `TooLargeError` - слишком длинный юзернейм.
 - `AlreadyBlockedError` - пользователь итак заблокирован.
 - `CantBlockYourselfError` - нельзя заблокировать самого себя.
 - `TargetUserBannedError` - пользователь забанен.

---

## Разблокировать
```py
user.unblock()
```

### Ошибки
 - `NotFoundError` - пользователь не найден.
 - `TooLargeError` - слишком длинный юзернейм.
 - `NotBlockedError` - пользователь итак не заблокирован.
 - `TargetUserBannedError` - пользователь забанен.

---

## :material-post: Пост на стене
```py
user.post(
    content='содержание',
    spans=[],
    attachments=[],
    poll=NewPoll(
        question='тест',
        options=['1', '2', '3', '4', '5'],
        multiple=True
    )
)
```

### Параметры
#### content <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span> <span class="mdx-badge mdx-badge_one_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">One of required</span></span>
Содержание поста.

#### spans <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-list-unordered-16: :material-text-short:</span><span class="mdx-badge__text">list[Span]</span></span>
Стилизация (жирный, курсив, подчеркивание итд). Автоматически заполняется, если установлен [parse_mode](../config.md#parse_mode-parsemode). У ручного заполнения приоритет большем, чем у дефолтного (если у вас стоит parse_mode в конфиге, и вы напишите свой spans, применится ваш вариант).

#### wall_recipient <span class="mdx-badge"><span class="mdx-badge__icon">:material-identifier: | :fontawesome-solid-user:</span><span class="mdx-badge__text">UUID | User</span></span>
Получатель поста (для постов на стене). Может быть объектом пользователя или UUID.  
Для поста на стене также можно использовать `user.post()`.

#### attachments <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-list-unordered-16: [:material-identifier: | :material-file:] | :material-identifier: | :material-file:</span><span class="mdx-badge__text">list[UUID | File] | File | UUID</span></span> <span class="mdx-badge mdx-badge_one_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">One of required</span></span>
Вложения. Может быть списком, объектом файла или UUID.

#### poll <span class="mdx-badge"><span class="mdx-badge__icon">:material-poll:</span><span class="mdx-badge__text">NewPoll</span></span> <span class="mdx-badge mdx-badge_one_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">One of required</span></span>
Опросник.

### Ошибки
 - `NotFoundError` - получатель поста не найден.
 - `ForbiddenError` - некоторые вложения не принадлежат клиенту или не существуют. Вложения должны быть загружены одним и тем же клиентом через `upload_file`.
 - `ValidationError` - ошибка валидации, скорее всего из-за слишком большого количества символов.
 - `RequiresSubscriptionError` - для публикации видео нужна верификация или НУКСТА.
 - `BannedWordError` - в посте содержатся [запрещенные слова](https://itdsdk.qzz.io/banned-words).

---

## :material-refresh: Обновить
```python
user.refresh()
```

### Ошибки
 - `NotFoundError` (`User`) - пользователь не найден.
 - `TooLargeError` - слишком дилнный юзернейм.
 - `NotFoundError` (`Profile`) - профиль не найден (пользователь только привязал почту, но еще не добавил эмоджи клан и имя)
 - `TargetUserBannedError` - пользователь забанен.

---

## :material-link: Получить ссылку на пользователя
```py
link = user.url
```
или
```python
link = user.link
```

---

## Выполнить действия для постов на стену
```py
is_succeed = user.complete_actions_for_wall_access()
```

---

## Выполнить действия для просмотра лайков
```py
is_success = user.complete_actions_for_likes_visibility()
```

---

## :octicons-list-unordered-16: :fontawesome-solid-user: Список подписчиков
```py
followers = user.followers # list
```

## :octicons-list-unordered-16: :fontawesome-solid-user: Список подписок
```py
following = user.following # list
```

## :octicons-list-unordered-16: :material-post: Список постов
```py
posts = user.posts # UserPosts
posts.load(10)
```

## :octicons-list-unordered-16: :material-post: :material-heart: Список лайкнутых постов
```py
posts = user.liked_posts # LikedPosts
post.load(5)
```
Если нет доступа, вернетсся пустой список.

---

# Текущий пользователь

## :fontawesome-solid-user-edit: Обновить профиль
```python
profile = me.update(
    bio='био',
    display_name='имя',
    username='username',
    banner_id=UNSET
)
```

### Обновить из текущих аттрибутов
```py
me.username = 'username2'
me.bio = 'другое био'
me.update_from_fields()

```

### Параметры
#### username <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Новый юзернейм.

#### display_name <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Новое имя.

#### bio <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Биография (о себе).

#### banner_id <span class="mdx-badge"><span class="mdx-badge__icon">:material-identifier: | UNSET</span><span class="mdx-badge__text">UUID | Unset</span></span>
ID баннера (должен быть загружен через `upload_file`).

!!! tip

    Для удаления баннера используйте `UNSET`:

    ```python
    from itd.enums import UNSET

    me.update(banner_id=UNSET)
    ```

### Ошибки
 - `ValidationError` - ошибка валидации (например слишком длинное имя).
 - `RequiresVerificationError` - требуется верификация для загрузки GIF-баннера.
 - `UsernameTakenError` - username уже занят.

---

## :fontawesome-solid-user-lock: Обновить настройки приватности
```python
from itd.models.user import UserPrivacyData
from itd.enums import AccessType

privacy = me.update_privacy(
    is_private=False,
    wall_access=AccessType.EVERYONE,
    likes_visibility=AccessType.FOLLOWERS,
    show_last_seen=True
)
```

### Параметры
#### is_private <span class="mdx-badge"><span class="mdx-badge__icon">:material-toggle-switch:</span><span class="mdx-badge__text">bool</span></span>
Приватный профиль. Посты не будут попадать в ленту, профиль будет виден только для подписчиков.

#### wall_access <span class="mdx-badge"><span class="mdx-badge__icon">:material-form-select:</span><span class="mdx-badge__text">AccessType</span></span>
Доступ к стене.

 - `AccessType.NOBODY` - никто
 - `AccessType.MUTUAL` - взаимные подписки
 - `AccessType.FOLLOWERS` - подписчики
 - `AccessType.EVERYONE` - все

#### likes_visibility <span class="mdx-badge"><span class="mdx-badge__icon">:material-form-select:</span><span class="mdx-badge__text">AccessType</span></span>
Доступ к лайкнутым постам.

#### show_last_seen <span class="mdx-badge"><span class="mdx-badge__icon">:material-toggle-switch:</span><span class="mdx-badge__text">bool</span></span>
Показывать дату последнего захода.

### Ошибки
 - `ValidationError` (скорее всего ошибка в sdk)

---

## :material-delete: Удалить аккаунт
```python
me.delete()
```

!!! danger
    У вас будет 30 дней на восстановление аккаунта (см. восстановление аккунта ниже). После этого аккаунт безвозратно удалится.

### Ошибки
 - `AlreadyDeletedError` - аккаунт уже удален.

---

## :material-delete-off: Восстановить аккаунт
```python
me.restore()
```

### Ошибки
 - `NotDeletedError`: Аккаунт итак не удален.

!!! note
    Здесь также должна быть ошибка, что уже слишком поздно, но к сожалению у меня нет дополнительного аккаунта для удаления, чтобы посмотреть как она называется 🫤.

---

## :material-pin: Установить пин
```py
me.set_pin(me.pins[0])
```

### Параметры
#### pin <span class="mdx-badge"><span class="mdx-badge__icon">:material-text: | :material-pin:</span><span class="mdx-badge__text">str | Pin</span></span>
Объект пина или слаг. Если None - устанавливается первый из списка.

### Ошибки
 - `ValueError` - список пинов пустой (если pin is None).
 - `PinNotOwnedError` - пин не принадлежит вам.

---

## :material-pin-off: Снять пин
```py
me.remove_pin()
```

---

## :octicons-list-unordered-16: :fontawesome-solid-user: Список подписчиков
```py
followers = me.followers # Followers
followers.load(5)
```

## :octicons-list-unordered-16: :fontawesome-solid-user: Список подписок
```py
following = me.following # Following
following.load(10)
```

## :octicons-list-unordered-16: :material-pin: Список пинов
```py
pins = me.pins # list
```

## :octicons-list-unordered-16: :material-block-helper: Список заблокированных пользователей
```python
blocked = me.blocked
blocked.load(5)
blocked.load_all()
```