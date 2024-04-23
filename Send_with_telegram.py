import os
import telegram

TOKEN = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

print("token:  ", TOKEN)
print("chat_id:  ", chat_id)
bot = telegram.Bot(token=TOKEN)

def send_files_in_directory(directory, chat_id):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'rb') as file:
            bot.send_document(document=file, chat_id=chat_id)
            print(f"File '{filename}' sent successfully")

def main():
    # Sending all files in the directory
    send_files_in_directory('Outputs/Phones/Images', chat_id)

if __name__ == '__main__':
    main()
