#!/usr/bin/env python3
from argparse import ArgumentParser
from os import getenv
from os.path import isfile
import sys

from itd import ITDClient

def main():
    parser = ArgumentParser(
        description='Upload image and set it as profile banner'
    )

    parser.add_argument(
        '--token',
        default=getenv('ITD_TOKEN'),
        help='API token (or ITD_TOKEN env var)'
    )

    parser.add_argument(
        '--file',
        required=True,
        help='Path to image file'
    )

    args = parser.parse_args()

    if not args.token:
        print('❌ Токен не задан (--token или ITD_TOKEN)', file=sys.stderr)
        quit()

    file_path = args.file

    if not isfile(file_path):
        print(f'❌ Файл не найден: {file_path}', file=sys.stderr)
        quit()

    try:
        client = ITDClient(None, args.token)
        data, _ = client.update_banner_new(file_path)

        print('✅ Баннер обновлён!')
        print('📄 Информация о файле:')
        print(f'  id: {data.id}')
        print(f'  filename: {data.filename}')
        print(f'  mime_type: {data.mime_type}')
        print(f'  size: {data.size} bytes')
        print(f'  url: {data.url}')

    except Exception as e:
        print('❌ Произошла ошибка:', e, file=sys.stderr)
        quit()


if __name__ == '__main__':
    main()
