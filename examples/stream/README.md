# Stream - Прослушивание уведомлений

Примеры работы с SSE (Server-Sent Events) потоком уведомлений в реальном времени.

## Подготовка

1. Установите зависимости:
```bash
pip install -r ../../requirements.txt
```

2. Получите cookies с `refresh_token` (см. [главный README](../README.md))

3. Запускайте примеры из корня проекта или из папки `examples/stream/`

## Примеры

### basic_stream.py
Базовое прослушивание всех уведомлений.

```bash
python basic_stream.py
```

Показывает все входящие уведомления в реальном времени.

### stop_stream.py
Программная остановка потока через `client.stop_stream()`.

```bash
python stop_stream.py
```

Полезно для интеграции в многопоточные приложения.

### filter_notifications.py
Фильтрация уведомлений по типу.

```bash
python filter_notifications.py
```

Показывает только выбранные типы (like, follow, comment). Настраивается через `SHOW_TYPES`.

### notification_logger.py
Логирование всех уведомлений в JSON файл.

```bash
python notification_logger.py
```

Создает файл `notifications_YYYYMMDD_HHMMSS.log` с полной историей событий.

## Типы уведомлений

- **like** - Лайк на пост
- **follow** - Новый подписчик
- **wall_post** - Пост на вашей стене
- **comment** - Комментарий к посту
- **reply** - Ответ на комментарий
- **repost** - Репост вашего поста

## Особенности

- ✅ Автоматическое переподключение при разрыве
- ✅ Автоматическое обновление токена (при использовании cookies)
- ✅ Обработка всех типов уведомлений
- ✅ Graceful shutdown по Ctrl+C

## API Reference

Подробная документация по методам и моделям:
- [Основной README](../../README.md) - Общая информация об SDK
- [itd/client.py](../../itd/client.py) - Метод `stream_notifications()`
- [itd/models/event.py](../../itd/models/event.py) - Модели `StreamConnect` и `StreamNotification`
