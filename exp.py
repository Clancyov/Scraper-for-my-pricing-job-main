from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from tabulate import tabulate
from datetime import datetime
import numpy as np

Now = time.strftime('(%Y_%m_%d--%H_%M)')
class Phone_Scraper :

    def Scrap ( self ,Now ) :

        # link to the webpage which data is there
        URL = "https://webskymobile.com/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA/"
        # saving html code of the page
        HTML_Code = urlopen(URL).read().decode("utf-8")

        # making a soup of the html code to handle it easier
        Main_Soup = BeautifulSoup(HTML_Code, 'lxml')
        
        Table = Main_Soup.find("table")
        # saving the output in a textfile
        Table_Soup = BeautifulSoup(str(Table) , 'lxml')

        Rows = Table_Soup.find_all("tr")

        All_Data = []

        for row in Rows:
            Row_Soup = BeautifulSoup(str(row),'lxml')
            cell = Row_Soup.find_all("td")
            for data in cell:
                All_Data.append(data.get_text()+"\n")

        with open(f"Outputs\\Phones\\Scraped_data\\Scraped_data-{Now}.txt",'w',encoding='utf-8') as file:
            for data in All_Data : 
                file.write(data)

    def tableit():
        # Read the entire file as one column
        with open("E:\\Live Projects\\Scraper-for-my-pricing-job-main\\Outputs\\Phones\\Scraped_data\\Scraped_data-(2024_02_07--19_00).txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Reshape the data into a table with 7 columns
        num_rows = -(-len(lines) // 7)  # Ceiling division to calculate number of rows
        reshaped_data = np.array_split(lines, num_rows)

        # Print the table using tabulate
        print(tabulate(reshaped_data, tablefmt='grid'))

Phone_Scraper.tableit()






# driver=Phone_Scraper()
# driver.Scrap(Now)