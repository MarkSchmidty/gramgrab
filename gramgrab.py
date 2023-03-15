import os
import argparse
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import MessageMediaDocument
from telethon.errors.rpcerrorlist import FileReferenceExpiredError

# ...

async def download_zip_file(client, message, max_retries=3):
    file_name = message.media.document.attributes[0].file_name
    file_path = os.path.join(os.getcwd(), file_name)
    print(f'Downloading {file_name}...')

    retries = 0
    while retries < max_retries:
        try:
            await client.download_media(message, file_path)
            print(f'{file_name} downloaded.')
            break
        except FileReferenceExpiredError:
            print(f'File reference expired for {file_name}, retrying...')
            retries += 1
            # Refresh the message to get a new file reference
            message = await client.get_messages(message.to_id, ids=message.id)
            if message is None:
                print(f'Failed to refresh file reference for {file_name}, aborting...')
                break
    else:
        print(f'Failed to download {file_name} after {max_retries} retries.')

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
