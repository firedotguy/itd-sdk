#!/usr/bin/env python3

import argparse
import os
import sys
from itd import ITDClient

def main():
    parser = argparse.ArgumentParser(
        description='Upload image and set it as profile banner'
    )

    parser.add_argument(
        '--token',
        default=os.getenv('ITD_TOKEN'),
        help='API token (or ITD_TOKEN env var)'
    )

    parser.add_argument(
        '--file',
        required=True,
        help='Path to image file'
    )

    parser.add_argument(
        '--name',
        help='Filename on server (default: local filename)'
    )

    args = parser.parse_args()

    if not args.token:
        print('❌ Токен не задан (--token или ITD_TOKEN)', file=sys.stderr)
        sys.exit(1)

    file_path = args.file

    if not os.path.isfile(file_path):
        print(f'❌ Файл не найден: {file_path}', file=sys.stderr)
        sys.exit(1)

    server_name = args.name or os.path.basename(file_path)

    try:
        client = ITDClient(None, args.token)

        # Загружаем файл
        with open(file_path, 'rb') as f:
            response = client.upload_file(server_name, f)

        # Проверяем, что получили id
        file_id = getattr(response, 'id', None)
        if file_id is None:
            print('❌ Не удалось получить id файла')
            print(response)
            sys.exit(1)

        # Преобразуем UUID в строку
        file_id_str = str(file_id)

        # Обновляем баннер
        update_resp = client.update_profile(banner_id=file_id_str)

        print('✅ Баннер обновлён!')
        print('📄 Информация о файле:')
        print(f'  id: {file_id_str}')
        print(f'  filename: {response.filename}')
        print(f'  mime_type: {response.mime_type}')
        print(f'  size: {response.size} bytes')
        print(f'  url: {response.url}')

    except Exception as e:
        print('❌ Произошла ошибка:', e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
