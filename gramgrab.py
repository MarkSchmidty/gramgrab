import os
import argparse
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import MessageMediaDocument

parser = argparse.ArgumentParser(description='Download zip files from a public Telegram channel concurrently.',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog='''\
Example usage:
  python gramgrab.py -i <API_ID> -a <API_HASH> -c <CHANNEL_URL> -d <CONCURRENT_DOWNLOADS>

Example:
  python gramgrab.py -i 123456 -a abcd1234abcd1234abcd1234abcd1234 -c https://t.me/public_channel_url -d 5
''')

parser.add_argument('-i', '--api_id', required=True, help='Your API ID')
parser.add_argument('-a', '--api_hash', required=True, help='Your API Hash')
parser.add_argument('-c', '--channel_url', required=True, help='Public Telegram channel URL')
parser.add_argument('-d', '--concurrent_downloads', type=int, default=5, help='Number of concurrent downloads (default: 5)')

args = parser.parse_args()

api_id = args.api_id
api_hash = args.api_hash
channel_url = args.channel_url
concurrent_downloads = args.concurrent_downloads

async def download_zip_file(client, message):
    file_name = message.media.document.attributes[0].file_name
    file_name_utf8 = bytes(file_name, 'ascii').decode('unicode_escape')
    file_path = os.path.join(os.getcwd(), file_name_utf8)
    print(f'Downloading {file_name_utf8}...')
    await client.download_media(message, file_path)
    print(f'{file_name_utf8} downloaded.')

async def download_zip_files(client, channel_url):
    channel = await client.get_entity(channel_url)
    full_channel = await client(GetFullChannelRequest(channel))
    messages = client.iter_messages(channel, limit=full_channel.full_chat.participants_count)

    semaphore = asyncio.Semaphore(concurrent_downloads)
    tasks = []

    async def process_message(message):
        if message.media and isinstance(message.media, MessageMediaDocument):
            file_ext = message.media.document.attributes[0].file_name.split('.')[-1]
            if file_ext.lower() == 'zip':
                async with semaphore:
                    await download_zip_file(client, message)

    async for message in messages:
        task = asyncio.create_task(process_message(message))
        tasks.append(task)

    # Wait for all downloads to complete
    await asyncio.gather(*tasks)

async def main():
    async with TelegramClient('anon', api_id, api_hash) as client:
        await download_zip_files(client, channel_url)

if __name__ == '__main__':
    asyncio.run(main())
