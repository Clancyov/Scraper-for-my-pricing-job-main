import logging
from Iron_Scraper import Iron_Scraper
from Iron_Data_Processor import Iron_Data_Processor

Logger = logging.getLogger(__name__)

class Iron :

    def Scrap ( self, Now) :

        Scraper = Iron_Scraper()
        Scraper.Scrap(Now)
    

    def Process_Data ( self, Now) :

        Processor = Iron_Data_Processor()
        Processor.Process(Now)


    def Run( self, Now) :

        Runner=Iron()

        Runner.Scrap(Now)
        Logger.info('Scraping Phase Completed')

        Runner.Process_Data(Now)
        Logger.info('Imagination Phase Completed')