from urllib.request import urlopen
from PIL import Image,ImageDraw,ImageFont
from bs4 import BeautifulSoup
import time
from tabulate import tabulate
from datetime import datetime
import numpy as np
import re

Now = time.strftime('(%Y_%m_%d--%H_%M)')
class Phone_Scraper:

    def Scrap(self, Now):
        # link to the webpage which data is there
        URL = "https://webskymobile.com/%D9%84%DB%8C%D8%B3%D8%AA-%D9%82%DB%8C%D9%85%D8%AA/"
        # saving html code of the page
        HTML_Code = urlopen(URL).read().decode("utf-8")

        # making a soup of the html code to handle it easier
        Main_Soup = BeautifulSoup(HTML_Code, 'lxml')

        Table = Main_Soup.find("table")
        # saving the output in a textfile
        Table_Soup = BeautifulSoup(str(Table), 'lxml')

        Rows = Table_Soup.find_all("tr")

        All_Data = []

        for row in Rows:
            Row_Soup = BeautifulSoup(str(row), 'lxml')
            cell = Row_Soup.find_all("td")
            for data in cell:
                All_Data.append(data.get_text() + "\n")

        with open(f"Outputs\\Phones\\Scraped_data\\Scraped_data-{Now}.txt", 'w', encoding='utf-8') as file:
            for data in All_Data:
                file.write(data)

    def delete_persian(self, text):
        return re.sub(r'[\u0600-\u06FF]+', '', text)

    def tableit(self):
        # Read the entire file as one column
        with open(f"Outputs\\Phones\\Scraped_data\\Scraped_data-{Now}.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()

        cleaned_lines = [self.delete_persian(line) for line in lines]
        # Reshape the data into a table with 7 columns
        num_rows = -(-len(cleaned_lines) // 7)  # Ceiling division to calculate number of rows
        reshaped_data = np.array_split(cleaned_lines, num_rows)
        reshaped_data_str = np.array(reshaped_data).astype(str)

        reshaped_data_without_columns = np.delete(reshaped_data_str, np.s_[1:6], axis=1)
        reshaped_data_filtered = [row for row in reshaped_data_without_columns if "call" not in row[-1].lower()]
        # print(reshaped_data_filtered)
        samsung=[]
        xiaomi=[]
        nokia=[]
        current_brand=None
        for row in reshaped_data_filtered:
            if "SAMSUNG" in row[0]:
                current_brand=samsung
                # print(row)
            elif "XIAOMI" in row[0]:
                current_brand=xiaomi
                # print(row)
            elif "NOKIA" in row[0]:
                current_brand=nokia
                # print(row)
            elif current_brand==None or "Tab" in row[0]:
                continue
            elif row[1]=="  \n" :
                break
            current_brand.append(row)

        # print(tabulate(samsung, tablefmt='grid'))
        # print(tabulate(xiaomi, tablefmt='grid'))
        # print(tabulate(nokia, tablefmt='grid'))

        Imageeee= Image.new(mode="RGB",size=(1080,1080),color=(255,255,255))
        # Imageeee.show()
        Font_File = "Inputs\\Iron\\Fonts\\IRANSans_Black.ttf"
        Font_Size = 35
        Font = ImageFont.truetype(Font_File, int(Font_Size))
        Drawer = ImageDraw.Draw(Imageeee)
        for i in range (0,20):
            Drawer.text((50, (i*50)),str(xiaomi[i][0]),fill="black",font=Font)
        Imageeee.show()

# Create an instance of Phone_Scraper
scraper = Phone_Scraper()

# Call the Scrap method to retrieve data
scraper.Scrap(Now)

# Call the tableit method to process and print the table
scraper.tableit()
