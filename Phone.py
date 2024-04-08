import logging
from Phone_Scraper import Phone_Scraper
from Phone_Data_Processor import Phone_Data_Processor

logger = logging.getLogger(__name__)

class Phone :

    def Scrap ( self, Now) :

        Scraper = Phone_Scraper()
        Scraper.Scrap(Now)


    def Process_Data ( self, Now) :

        Processor = Phone_Data_Processor()
        Processor.Process(Now)


    def Run (self, Now) :
        
        Runner=Phone()
        
        Runner.Scrap(Now)
        logger.info('Scraping Phase Complete')

        Runner.Process_Data(Now)
        logger.info('Imagination Phase Complete')