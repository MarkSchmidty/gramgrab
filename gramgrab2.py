#!/usr/bin/env python3

import argparse
import os
import sys
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Channel
from concurrent.futures import ThreadPoolExecutor

def download_file(client, message, download_path):
    file_path = os.path.join(download_path, message.document.attributes[0].file_name)
    if os.path.exists(file_path) and os.path.getsize(file_path) == message.document.size:
        print(f"Skipping {file_path}, already downloaded.")
        return

    print(f"Downloading {file_path}...")
    client.download_media(message, file_path)
    print(f"Downloaded {file_path}.")

def download_files(client, messages, download_path, min_size, threads):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for message in messages:
            if message.document and message.document.size >= min_size:
                while len(executor._threads) >= threads:
                    time.sleep(0.05)
                executor.submit(download_file, client, message, download_path)

def main():
    parser = argparse.ArgumentParser(description='Download files from a public Telegram channel.')
    parser.add_argument('-i', '--api-id', type=int, required=True, help='API ID from my.telegram.org.')
    parser.add_argument('-a', '--api-hash', type=str, required=True, help='API hash from my.telegram.org.')
    parser.add_argument('-c', '--channel-link', type=str, required=True, help='Public Telegram channel link.')
    parser.add_argument('-m', '--min-kb', type=int, help='Minimum file size in KB (exclusive).')
    parser.add_argument('-M', '--min-mb', type=int, help='Minimum file size in MB (exclusive).')
    parser.add_argument('-t', '--threads', type=int, default=5, help='Number of download threads (default: 5).')
    parser.add_argument('-d', '--download-path', type=str, default='downloads', help='Download path (default: downloads).')
    args = parser.parse_args()

    if not args.min_kb and not args.min_mb:
        min_size = 10 * 1024 * 1024
    else:
        min_size = (args.min_kb * 1024 if args.min_kb else 0) + (args.min_mb * 1024 * 1024 if args.min_mb else 0)

    os.makedirs(args.download_path, exist_ok=True)

    with TelegramClient('telegram_downloader', args.api_id, args.api_hash) as client:
        entity = client.get_entity(args.channel_link)
        if not isinstance(entity, Channel):
            print("Invalid channel link.")
            sys.exit(1)

        full_channel = client(GetFullChannelRequest(entity))
        messages = client.iter_messages(entity, limit=None)
        download_files(client, messages, args.download_path, min_size, args.threads)

if __name__ == '__main__':
    main()
