import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
class Phone_Scraper :

    def Scrap ( self, Now) :
        try:
            # link to the webpage which data is there
            URL = "https://webskymobile.com/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA/"

            # saving html code of the page
            HTML_Code = urlopen(URL).read().decode("utf-8")

            # making a soup of the html code to handle it easier
            Main_Soup = BeautifulSoup(HTML_Code, 'lxml')

            # finding the table of data which we need
            Table = Main_Soup.find("table")

            # making a soup of the data
            Table_Soup = BeautifulSoup(str(Table), 'lxml')

            # finding all rows
            Rows = Table_Soup.find_all("tr")

            # making a list to save data
            All_Data = []

            # iterating between rows and cells to extracting data
            for row in Rows:

                # making a soup of each row to find data in html code
                Row_Soup = BeautifulSoup(str(row), 'lxml')

                # making a soup out of each cell in a row
                cell = Row_Soup.find_all("td")

                # appending data to the list
                for data in cell:
                    All_Data.append(data.get_text() + "\n")
        except:
            logger.critical('Couldent Scrap Data')
        else:
            logger.info('Data Scraped')
        
        try:
            # saving the output in a textfile
            with open(f"Outputs\\Phones\\Scraped_data\\Scraped_data-{Now}.txt", 'w', encoding='utf-8') as File:
                for data in All_Data:
                    File.write(data)
        except:
            logging.critical('Couldent Save Scraped Data') 
        else:
            logging.info('Scraped Data Successfully')           