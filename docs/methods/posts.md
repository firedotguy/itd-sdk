# Пост

## Получить
```python
post = Post(
    id=UUID('c2f443df-61eb-4bfc-b52f-13aacecb9c46')
)
```

### Параметры

#### id <span class="mdx-badge"><span class="mdx-badge__icon">:material-identifier:</span><span class="mdx-badge__text">UUID</span></span> <span class="mdx-badge mdx-badge_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">Required</span></span>
ID поста.

> [!NOTE]
> Для проверки на существование (`NotFoundError`) вызовите [`post.refresh()`](#Обновить) или любой аттрибут (если не включен [`config.auto_load`](/config.md#auto_load-bool))

---

## Создать
```python
from itd import Post

post = Post.new(
    content='чиенбурбе круче чем #иванговно',
    spans=[],
    wall_recipient=None,
    attachemnts=[],
    poll=None
)
```
Должно быть указан хотя бы что-то одно из `content`, `attachments` и `poll`.

### Параметры

#### content <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span> <span class="mdx-badge mdx-badge_one_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">One of required</span></span>
Содержание поста.

#### spans <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-list-unordered-16: :material-text-short:</span><span class="mdx-badge__text">list[Span]</span></span>
Стилизация (жирный, курсив, подчеркивание итд). Автоматически заполняется, если установлен [parse_mode](/config.md#parse_mode-parsemode). У ручного заполнения приоритет большем, чем у дефолтного (если у вас стоит parse_mode в конфиге, и вы напишите свой spans, применится ваш вариант).

#### wall_recipient <span class="mdx-badge"><span class="mdx-badge__icon">:material-identifier: | :fontawesome-regular-user:</span><span class="mdx-badge__text">UUID | User</span></span>
Получатель поста (для постов на стене). Может быть объектом пользователя или UUID.  
Для поста на стене также можно использовать `user.post()`.

#### attachments <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-list-unordered-16: :material-identifier: | :octicons-list-unordered-16: :material-file: | :material-identifier: | :material-file:</span><span class="mdx-badge__text">list[UUID | File] | File | UUID</span></span> <span class="mdx-badge mdx-badge_one_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">One of required</span></span>
Вложения. Может быть списком, объектом файла или UUID.

#### poll <span class="mdx-badge"><span class="mdx-badge__icon">:material-poll:</span><span class="mdx-badge__text">NewPoll</span></span> <span class="mdx-badge mdx-badge_one_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">One of required</span></span>
Опросник.

!!! example

    ```python
    from itd.poll import NewPoll

    Post.new(
        poll=NewPoll(
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
 - `NotFoundError` - получатель поста не найден.
 - `ForbiddenError` - некоторые вложения не принадлежат клиенту или не существуют. Вложения должны быть загружены одним и тем же клиентом через `upload_file`.
 - `ValidationError` - ошибка валидации, скорее всего из-за слишком большого количества символов.
 - `RequiresSubscriptionError` - для публикации видео нужна верификация или НУКСТА.
 - `BannedWordError` - в посте содержатся [запрещенные слова](https://itdsdk.qzz.io/banned-words).

---

## Проголосовать
```python
post.poll.vote(
    options=UUID('f12c70c7-141e-4dff-9e5b-87f039c7ba58')
)
```
или
```python
post.vote(
    options=UUID('f12c70c7-141e-4dff-9e5b-87f039c7ba58')
)
```
или
```python
post.poll.options[0].vote()
```

### Параметры

#### options <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-list-unordered-16: :material-identifier:</span><span class="mdx-badge__text">list[UUID | PollOption] | UUID | PollOption</span></span> <span class="mdx-badge mdx-badge_required"> <span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">Required</span></span>
Опции для голосования. Может быть списком, объектом опции (можно взять из `poll.options`) или UUID.

!!! example

    === "1 опция"

        ```python
        post.vote(UUID('f12c70c7-141e-4dff-9e5b-87f039c7ba58'))
        ```

    === "несколько опций"

        ```python
        post.vote(
            [
                UUID('6daf7815-b30a-4f98-8091-7a0e24caba6c'),
                UUID('3add69ee-4dae-4a81-9e4a-3e0fe77c7be0'),
                UUID('ac758a37-2cb5-45ba-b743-a0a11a2b8d3d')
            ]
        )
        ```

---

## Обновить
```python
post.refresh()
```

### Ошибки
 - `NotFoundError` - пост не найден.

---

## Лайкнуть
```python
likes_count = post.like()
```
Если пост уже лайкнут, ничего не произойдет.

### Ошибки
 - `NotFoundError` - пост не найден.

---

## Убрать лайк
```python
likes_count = post.unlike()
```
Если пост итак не лайкнут, ничего не произойдет.

### Ошибки
 - `NotFoundError` - пост не найден.

---

## Репостнуть
```python
post = post.repost(
    content='Какой-то комментарий к репосту'
)
```

### Ошибки
 - `NotFoundError` - пост не найден.
 - `AlreadyRepostedError` - пост уже репостнут.
 - `CantRepostYourselfPost` - нельзя репостить свои посты.
 - `ValidationError` - ошибка валидации (вероятно из-за слишком большого количества символов).
 - `BannedWordError` - в посте есть [запрещенные слова](https://itdsdk.qzz.io/banned-words).

---

## Просмотреть
```python
post.view()
```

### Ошибки
 - `NotFoundError` - пост не найден.

---

## Закрепить
```python
post.pin()
```

### Ошибки
 - `NotFoundError` - пост не найден.
 - `ForbiddenError` - нет прав на закрепление (пост должен быть на вашей стене).

---

## Открепить
```python
post.unpin()
```

### Ошибки
 - `NotPinnedError` - пост не закреплен или не найден.

---

## Удалить
```python
post.delete()
```

### Ошибки
 - `NotFoundError` - пост не найден.
 - `ForbiddenError` - нету прав на удаление (пост должен быть на вашей стене).

---

## Закрепить
```python
post.restore()
```
Если пост итак не удален, ничего не произойдет.

### Ошибки
 - `NotFoundError` - пост не найден.
 - `ForbiddenError` - нету прав на восстановление (пост должен быть на вашей стене).

---

## Редактировать
```python
edited_at = post.edit(
    content='Новый контент',
    spans=[]
)
```
> [!WARNING]
> Редактировать пост можно только в первые 48 часов после публикации. После этого будет выходить ошибка `EditExpiredError`.

### Параметры

#### content <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span> <span class="mdx-badge mdx-badge_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">Required</span></span>
Содержание поста.

#### spans <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-list-unordered-16: :material-text-short:</span><span class="mdx-badge__text">list[Span]</span></span>
Стилизация. Автоматически заполняется, если установлен [parse_mode](/config.md#parse_mode-parsemode).

### Ошибки
 - `NotFoundError` - пост не найден.
 - `ForbiddenError` - нету прав на редактирование (вы должны быть автором поста).
 - `EditExpiredError` - истекло время на редактирование ("edit window expired").
 - `BannedWordError` - в посте есть [запрещенные слова](https://itdsdk.qzz.io/banned-words).

---

## Прокомментировать
```python
post.add_comment(
    content='комментарие',
    attachments=[]
)
```
или
```python
post.comments.new(
    content='комментарий новый только другой',
    attachments=[]
)
```
или
```python
from itd.comment import Comment

Comment.new(
    post.id,
    content='странный немножка комментарий',
    attachments=[]
)
```

### Параметры

#### content <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span> <span class="mdx-badge mdx-badge_one_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">One of required</span></span>
Содержание комментария (стилизация не поддерживается на стороне ИТД).

#### attachments <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-list-unordered-16: :material-identifier: | :octicons-list-unordered-16: :material-file: | :material-identifier: | :material-file:</span><span class="mdx-badge__text">list[UUID | File] | File | UUID</span></span> <span class="mdx-badge mdx-badge_one_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">One of required</span></span>
Вложения. Может быть списком, объектом файла или UUID.

### Ошибки
 - `NotFoundError` - пост не найден.
 - `ValidationError` - ошибка валидации (вероятно из-за большого количества символов).
 - `BannedWordError` - в комментарии есть [запрещенные слова](https://itdsdk.qzz.io/banned-words).
 - `ForbiddenError` - некоторые вложения не принадлежат клиенту или не существуют. Вложения должны быть загружены одним и тем же клиентом через `upload_file`.
 - `RequiresSubscriptionError` - для загрузки видео требуется верификация или подписка НУКСТА.

---

## Пожаловаться
```python
from itd.enums import ReportReason

post.report(
    reason=ReportReason.SPAM,
    description='описание'
)
```

### Параметры
#### reason <span class="mdx-badge"><span class="mdx-badge__icon">:octicons-report-16:</span><span class="mdx-badge__text">ReportReason</span></span> <span class="mdx-badge mdx-badge_required"><span class="mdx-badge__icon">:material-information:</span><span class="mdx-badge__text">Required</span></span>

#### content <span class="mdx-badge"><span class="mdx-badge__icon">:material-text:</span><span class="mdx-badge__text">str</span></span>
Описание жалобы.

### Ошибки
 - `NotFoundError` - пост не найден.
 - `AlreadyReportedError` - вы уже оставляли жалобу на этот пост.
 - `ValidationError` - ошибка валидации (слишком длинное описание).

---

## Получить ссылку на пост
```python
url = post.url
```

---

# Посты

## Лента
```python
posts = Posts()
```

### Популярное
Обычная лента постов.
```python
posts = Posts()
```
или
```python
posts = Posts.popular()
```
или
```python
posts = Posts.trending()
```

### Подписки
Лента постов от авторов, на которых вы подписаны.
```python
posts = Posts.following()
```

### Лента клана
Лента постов от авторов, у которых одинаковый с вами клан.
```python
posts = Posts.clan()
```

### Ошибки
Ошибки появляются только при загрузке постов (`posts.load()` / `for post in posts` / `posts[0]`).

 - `ValidationError`: ошибка валидации (из-за слишком большого лимита батча).

---

## Посты пользователя
```python
from itd.enums import UserPostSorting

posts = UserPosts(
    user='fdg',
    sorting=UserPostSorting.NEW
)
```
или
```python
from itd import User

posts = User('fdg').posts
```

### Новые посты
```python
posts = UserPosts('fdg')
```
или
```python
posts = UserPosts.new('fdg')
```
или
```python
posts = UserPosts('fdg', UserPostSotring.NEW)
```
Сортировка постов по дате создания.

### Популярные посты
```python
UserPosts.popular('fdg')
```
или
```python
UserPosts('fdg', UserPostSotring.POPULAR)
```
Сортировка постов по количеству лайков.

### Параметры

#### user <span class="mdx-badge"><span class="mdx-badge__icon">:material-identifier: | :fontawesome-regular-user:</span><span class="mdx-badge__text">UUID | User</span></span>
Пользователь для получения постов с его стены. Может быть объектом пользователя или UUID.

### Ошибки
Ошибки появляются только при загрузке постов (`posts.load()` / `for post in posts` / `posts[0]`).

 - `NotFoundError`: пользователь не найден.
 - `ValidationError`: ошибка валидации (может быть из-за слишком большого лимита батча).

---

## Лайкнутые посты пользователя
```python
LikedPosts('fdg')
```
или
```python
User('fdg').liked_posts
```