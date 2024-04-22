import os
from telegram import Bot
from telegram.error import TelegramError
# github_username = os.environ.get('GITHUB_USERNAME')
# Your Telegram bot token
TOKEN = os.environ.get('TELEGRAM_TOKEN')

# ID of the chat where you want to send the files
CHAT_ID = os.environ.get('CHAT_ID')

# Directory containing the files you want to send
FILES_DIRECTORY = 'Outputs/Phones/Images'

def send_files(bot, chat_id, files_directory):
    for filename in os.listdir(files_directory):
        file_path = os.path.join(files_directory, filename)
        try:
            with open(file_path, 'rb') as file:
                bot.send_document(chat_id=chat_id, document=file)
                print(f"File '{filename}' sent successfully")
        except TelegramError as e:
            print(f"Failed to send file '{filename}': {e}")

def main():
    bot = Bot(TOKEN)
    send_files(bot, CHAT_ID, FILES_DIRECTORY)

if __name__ == '__main__':
    main()
