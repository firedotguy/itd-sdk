#!/usr/bin/env python3

import argparse
import os
import sys
from itd import ITDClient

def main():
    parser = argparse.ArgumentParser(
        description='Create a post on ITD via CLI'
    )

    parser.add_argument(
        '--token',
        default=os.getenv('ITD_TOKEN'),
        help='Refresh token (or set ITD_TOKEN environment variable)'
    )

    parser.add_argument(
        '--text',
        required=True,
        help='Text content of the post'
    )

    parser.add_argument(
        '--file',
        help='Optional file to attach to the post'
    )

    parser.add_argument(
        '--filename',
        help='Filename on server (if --file is used, default: local filename)'
    )

    args = parser.parse_args()

    if not args.token:
        print('❌ Token not provided (--token or ITD_TOKEN)', file=sys.stderr)
        sys.exit(1)

    try:
        client = ITDClient(None, args.token)

        file_id = None
        if args.file:
            if not os.path.isfile(args.file):
                print(f'❌ File not found: {args.file}', file=sys.stderr)
                sys.exit(1)

            server_name = args.filename or os.path.basename(args.file)
            with open(args.file, 'rb') as f:
                response = client.upload_file(server_name, f)

            file_id = str(getattr(response, 'id', None))
            if not file_id:
                print('❌ Failed to get file ID')
                sys.exit(1)
            print(f'✅ File uploaded: {response.filename} (id={file_id})')

        # Создаём пост с правильным аргументом 'content'
        if file_id:
            post_resp = client.create_post(content=args.text, file_ids=[file_id])
        else:
            post_resp = client.create_post(content=args.text)

        # Вывод результата
        print('✅ Post created successfully!')
        print(f'  id: {post_resp.id}')
        if hasattr(post_resp, 'url'):
            print(f'  url: {post_resp.url}')
        print(f'  text: {args.text}')
        if file_id:
            print(f'  attached file id: {file_id}')

    except Exception as e:
        print('❌ Error:', e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
