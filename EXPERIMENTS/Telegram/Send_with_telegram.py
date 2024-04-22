import asyncio
import os
import telegram

TOKEN = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

print("token:  ",TOKEN)
print("chat_id:  ",chat_id)
bot = telegram.Bot(token=TOKEN)

async def send_document(document, chat_id):
    async with bot:
        await bot.send_document(document=document, chat_id=chat_id)

async def main():
    # Sending a document
    await send_document(document=open('Outputs/Phones/Images/samsung0.png', 'rb'), chat_id=chat_id)

if __name__ == '__main__':
    asyncio.run(main())


# import os
# from telegram import Bot
# from telegram.error import TelegramError
# # github_username = os.environ.get('GITHUB_USERNAME')
# # Your Telegram bot token
# TOKEN = os.environ.get('TELEGRAM_TOKEN')

# # ID of the chat where you want to send the files
# CHAT_ID = os.environ.get('CHAT_ID')

# # Directory containing the files you want to send
# FILES_DIRECTORY = 'Outputs/Phones/Images'

# def send_files(bot, chat_id, files_directory):
#     for filename in os.listdir(files_directory):
#         file_path = os.path.join(files_directory, filename)
#         try:
#             with open(file_path, 'rb') as file:
#                 bot.send_document(chat_id=chat_id, document=file)
#                 print(f"File '{filename}' sent successfully")
#         except TelegramError as e:
#             print(f"Failed to send file '{filename}': {e}")

# def main():
#     bot = Bot(TOKEN)
#     send_files(bot, CHAT_ID, FILES_DIRECTORY)

# if __name__ == '__main__':
#     main()





# import os
# from telethon import TelegramClient

# # Your Telegram bot token
# TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
# CHAT_ID = os.environ.get('CHAT_ID')
# FILES_DIRECTORY = 'Outputs/Phones/Images'

# async def send_files():
#     async with TelegramClient('session_name', api_id=None, api_hash=None, bot_token=TOKEN) as client:
#         for filename in os.listdir(FILES_DIRECTORY):
#             file_path = os.path.join(FILES_DIRECTORY, filename)
#             try:
#                 await client.send_file(CHAT_ID, file_path)
#                 print(f"File '{filename}' sent successfully")
#             except Exception as e:
#                 print(f"Failed to send file '{filename}': {e}")

# if __name__ == '__main__':
#     with TelegramClient('anon', api_id=None, api_hash=None, bot_token=TOKEN) as client:
#         client.loop.run_until_complete(send_files())
