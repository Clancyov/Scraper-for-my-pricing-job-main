from Iron_Scraper import Iron_Scraper
from Iron_Data_Processor import Iron_Data_processor
class Iron:

    def Scrap (self) :

        Scraper = Iron_Scraper()
        Scraper.Scrap()
    
    def Process_Data (self) :

        Processor = Iron_Data_processor()
        Processor.Process()

    def Run(self):

        Runner=Iron()

        Runner.Scrap()
        Runner.Process_Data()