import asyncio
import os
import telegram

TOKEN = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

print("token:  ", TOKEN)
print("chat_id:  ", chat_id)
bot = telegram.Bot(token=TOKEN)

async def send_document(document, chat_id):
    async with bot:
        await bot.send_document(document=document, chat_id=chat_id)

async def send_all_documents_in_directory(directory, chat_id):
    async with bot:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as file:
                await bot.send_document(document=file, chat_id=chat_id)
                print(f"File '{filename}' sent successfully")

async def main():
    # Sending all documents in the directory
    await send_all_documents_in_directory('Outputs/Phones/Images', chat_id)

if __name__ == '__main__':
    asyncio.run(main())
