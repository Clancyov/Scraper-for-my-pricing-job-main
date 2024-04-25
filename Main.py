import logging
from Iron import Iron
from Phone import Phone
from Telegram_Sender import Sender

import time

Now=time.strftime('(%Y_%m_%d--%H_%M)')

Logger = logging.getLogger(__name__)
log_format= '[{asctime}]: [{filename}]: {funcName}: {lineno}:       {levelname}:    [{message}]'
logging.basicConfig(filename=f"Log\\Main_Logs_'{Now}'.log",encoding='utf-8',level=logging.DEBUG,format=log_format,style='{')

Logger.info('Started')

class main:

    def Make_Iron_Pricelists(self):
        
        iron = Iron()
        iron.Run(Now)

    def Make_Phone_Pricelists(self):

        phone = Phone()
        phone.Run(Now)

    def Make_Car_Pricelists(self):
        pass

    # def Send_Outputs_With_Telegram(self):
        
    #     Sender = Sender()
    #     Sender.Send(Now)
    
Runner=main()
Runner.Make_Iron_Pricelists()
Runner.Make_Phone_Pricelists()
# Runner.Send_Outputs_with_Telegram()

Logger.info('Finished')
