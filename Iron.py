from Iron_Scraper import Iron_Scraper
from Iron_Data_Processor import Iron_Data_Processor

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
        Runner.Process_Data(Now)