# this class is only for scraping data from the iron prices cetion of "iranjib website"
import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

Logger = logging.getLogger(__name__)

class Iron_Scraper :

    Output_Path = None

    def Make_Paths(self):

        self.Output_Path = f"Outputs/Iron/Scraped_Data"
        os.makedirs(self.Output_Path, exist_ok=True)

    def Scrap ( self, Now) :

        self.Make_Paths()

        # link to the webpage which data is there
        URL = "https://www.iranjib.ir/showgroup/38/%D9%82%DB%8C%D9%85%D8%AA-%D8%A2%D9%87%D9%86-%D8%A2%D9%84%D8%A7%D8%AA/"

        #Scraping
        try:
            # saving html code of the page
            HTML_Code = urlopen(URL).read().decode("utf-8")
        except:
            Logger.critical('Scrapping Faild')
        else:
            Logger.info('Data Scaraped Successfully')

        #Pre process
        try:
            # making a soup of the html code to handle it easier
            Main_Soup = BeautifulSoup(HTML_Code, 'lxml')

            # finding all tables in the page
            All_Tables = Main_Soup.find_all("table")

            # choosing the table which we want
            Price_Table_Soup = BeautifulSoup(str(All_Tables[1]), 'lxml')

            # the needed data will be save in this array 
            All_Data = []

            # making a soup of all rows in the the table.
            Rows = Price_Table_Soup.find_all("tr")

            # iterating between rows and cells to extracting data
            for Row in Rows :

                # making a soup of each row to find data in html code
                Row_Soup = BeautifulSoup(str(Row), 'lxml')

                # making a soup of cells in a row
                Cell = Row_Soup.find_all("td")

                # deleting the tale
                if len(Cell) <= 1 :
                    continue
                
                # appending data to the holder array
                for Data in Cell :
                    All_Data.append(Data.get_text() + "\n")
        except:
            Logger.critical('Something Went Wrong About Scraped Data')
        else:
            Logger.info('Scrapped Data Has No Problem')

        #Save2
        try:        
            # saving the output in a textfile
            file_name = f"Scraped_Data-{Now}.txt"
            file_path = os.path.join(self.Output_Path, file_name)
            with open(file_path, 'w', encoding='utf-8') as File:
                for data in All_Data:
                    File.write(data)
        except :
            Logger.critical('Saving Data Failed')
        else:
            Logger.info('Data Saved Successfully')
