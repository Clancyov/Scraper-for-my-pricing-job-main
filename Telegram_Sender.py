import os
import telegram
import logging
import zipfile

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
                    
    def zipper(self,target,*sources):
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for directory in sources:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Create a relative path for the file inside the zip archive
                        relative_path = os.path.relpath(file_path, os.path.dirname(directory))
                        zipf.write(file_path, arcname=relative_path)

    async def runner(self,Now):
        # try:
        directories_to_zip = [f"Outputs/Phones/Images/{Now}", f"Outputs/Iron/Images/{Now}/Currency_Gold" , f'Outputs/Iron/Images/{Now}/Akhbar_Eghtesadi']
        output_zip_file = f"zips/{Now}output.zip"
        os.makedirs(output_zip_file, exist_ok=True)
        self.zipper(output_zip_file, *directories_to_zip)
        # except:
            # logger.critical('Files Didnt zipped')
        # else:
            # logger.info("all files have been ziped successfully")

        try:
            # await self.Send_Directory_Containing(f"Outputs/Phones/Images/{Now}")
        
            # await self.Send_Directory_Containing(f"Outputs/Iron/Images/{Now}/Currency_Gold")
            
            # await self.Send_Directory_Containing(f'Outputs/Iron/Images/{Now}/Akhbar_Eghtesadi')

            # Sending all documents in the directory
            await self.send_document(f'Log/Main_Logs/{Now}.log')
            await self.send_document(f'zips/{Now}output.zip')
        except:
            logger.critical("didnt sent")
        else:
            logger.info("sent successfully")
