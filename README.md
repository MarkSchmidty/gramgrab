# gramgrab
Grab zip files from public Telegram channels using python.

Downloads zip files concurrently from a public Telegram channel using the Telethon library.

## Installation

1. Make sure you have Python 3.7 or later installed on your system. You can check the Python version by running `python --version` or `python3 --version`.

2. Install the required packages:
`pip install telethon`

3. Save the `gramgrab.py` script to your local machine.

## Usage

1. First, obtain your Telegram API credentials (API ID and API Hash) by following the instructions here: https://my.telegram.org/auth

2. Run the script with the following command-line arguments:
`python gramgrab.py -i <API_ID> -a <API_HASH> -c <CHANNEL_URL> -d <CONCURRENT_DOWNLOADS>`


Replace the following placeholders with the appropriate values:
- `<API_ID>`: Your API ID obtained from Telegram.
- `<API_HASH>`: Your API Hash obtained from Telegram.
- `<CHANNEL_URL>`: The public Telegram channel URL containing the zip files.
- `<CONCURRENT_DOWNLOADS>`: The number of concurrent downloads (default: 5).

Example:
`python gramgrab.py -i 123456 -a abcd1234abcd1234abcd1234abcd1234 -c https://t.me/public_channel_url -d 5`

3. The script will download the zip files from the specified channel concurrently and save them to the current working directory.

## Help

For help with command-line arguments, run:
`python gramgrab.py -h`

This README provides instructions for installing the required packages and using the gramgrab.py script. You can add this README to the repository containing the script, which will display the instructions on the GitHub repository page.
