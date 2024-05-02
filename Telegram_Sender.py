import os
import telegram
import logging

logger = logging.getLogger(__name__)

class Sender:
    # 
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    # 
    chat_id = os.environ.get('CHAT_ID')

    bot = telegram.Bot(token=TOKEN)

    async def send_document(self, document):
        async with self.bot:
            await self.bot.send_document(document=document, chat_id=self.chat_id)

    async def Send_Directory_Containing(self, directory):
        async with self.bot:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'rb') as file:
                    await self.bot.send_document(document=file,chat_id=self.chat_id)

    async def runner(self,Now):
        try:

            await self.Send_Directory_Containing(f"Outputs/Phones/Images/{Now}")
        
            await self.Send_Directory_Containing(f"Outputs/Iron/Images/{Now}/Currency_Gold")
            
            await self.Send_Directory_Containing(f'Outputs/Iron/Images/{Now}/Akhbar_Eghtesadi')

            # Sending all documents in the directory
            await self.send_document(f'Log/Main_Logs/{Now}.log')
            
        except:
            logger.critical('Files Didnt sent')
        else:
            logger.info("all files have been sent successfully")
