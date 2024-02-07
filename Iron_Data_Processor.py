import os
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

Image_Path ="Inputs\\Iron\\Canvas_Images"

names=[
    "1-Tir_Ahan",
    "2-Milgerd",
    "3-Profill",
    "4-Nawdani",
    "5-Nabshi",
    "6-Waraq_Siah",
    "7-Tasme_Maftoul",
    "8-Khamoot",
    "9-Waraq_Galwanize"
]

capacities=[
    9,12,10,8,7,12,10,6,10
]

class page:
    def __init__(self, name, Capacity, Image,Data=None ,positions=None):
        self.name=name
        self.Capacity=Capacity
        self.Image=Image
        self.Data=Data
        self.positions=positions

class Iron_Data_processor :

    def Data_Reader (self,Now) :

        All_Tables=[]
        with open(f"Outputs\\Iron\\Scraped_data\\Scraped_data-({Now}).txt", "r", encoding="utf-8") as Data_File :
            for line in Data_File :
                All_Tables.append(line)        
        return All_Tables
    
    def Shaper(self, All_Tables):
        Columns = 7
        All_Tables = np.array(All_Tables)
        Rows = len(All_Tables) // Columns
        All_Tables_2d = All_Tables.reshape((Rows, Columns))
        Needed_Columns = All_Tables_2d.shape[1] - 2
        Shaped_data = All_Tables_2d[0:, 4:5]
        return Shaped_data

    def Clean_Data(self, Cell):

        Cell= re.sub(r"(?<!\n)\n(?!\n)", "", Cell)
        Cell= Cell.replace("\n"," ")
        return Cell
    
    def Make_Pages_Objects(self):
        page_objects=[]
        for name, capacity in zip(names,capacities):
            
            Page_obj=page(name,capacity,(Image_Path+"\\" + name+".jpg"))
            page_objects.append(Page_obj)
        return page_objects

    def Load_data(self,pages, data):
        page_data=[]
        for page in pages:
            page_data.extend(data[:page.Capacity])
            page.Data=page_data
            data=data[page.Capacity:]
            page_data=[]
        return pages

    def Load_positions(self,Pages_with_data):
        positions=[]
        with open ('Inputs\\Iron\\positions\\positions.csv', mode='r', encoding='utf-8') as file:
            reader=csv.reader(file)
            for row in reader:
                positions.append(row)
        Page_positions=[]
        for Page in Pages_with_data:
            Page_positions.extend(positions[:Page.Capacity])
            Page.positions=Page_positions
            positions=positions[Page.Capacity:]
            Page_positions=[]
        return(Pages_with_data)
    
    def Convert_Data_To_ENG_Numbers(self,data):
        Persian_to_Latin={
            '۰': '0',
            '۱': '1',
            '۲': '2',
            '۳': '3',
            '۴': '4',
            '۵': '5',
            '۶': '6',
            '۷': '7',
            '۸': '8',
            '۹': '9'
        }
        if (data!="---"):
            for persian_digit,latin_digit in Persian_to_Latin.items():
                data=data.replace(persian_digit,latin_digit)
            data=data.replace(',','')
            try:
                result=int(data)
            except ValueError:
                result=float(data)
                print("Value Error: result turned into float")
            formatted_result="{:,}".format(result)
            return formatted_result
        else:
            return data
    
    def Make_Tagged_Images (self,Completed_Pages,Now):
        font_file="Inputs\\Iron\\Fonts\\IRANSans_Black.ttf"
        font_size= 35
        font=ImageFont.truetype(font_file,int(font_size))
        directory=f"Outputs\\Iron\\Images\\{Now}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        for page in Completed_Pages:
            raw_canvas_image=Image.open(page.Image)
            Drawer=ImageDraw.Draw(raw_canvas_image)
            for position,data in zip(page.positions,page.Data):
                x,y=int(position[0]),int(position[1])
                access=Iron_Data_processor()
                Final_data = access.Convert_Data_To_ENG_Numbers(data[0])
                Drawer.text((x,y),Final_data,fill="black",font=font)
                print("drew")
            raw_canvas_image.save(os.path.join(directory,f"{page.name}.png"))
        files=os.listdir(directory)
        image_files=[file for file in files if file.endswith(('.jpg','.png'))]
        for filename in image_files:
            filepath=os.path.join(directory,filename)
            image=mpimg.imread(filepath)
            plt.imshow(image)
            plt.title(filename)
            plt.axis('off')
            plt.show()
        
    def Process(self,Now):
        Processor=Iron_Data_processor()

        Table = Processor.Data_Reader(Now)
        Shaped_Table = Processor.Shaper(Table)
        Cleaned_Table = [[Processor.Clean_Data(cell) for cell in row] for row in Shaped_Table]
        Pages = Processor.Make_Pages_Objects()
        Pages_with_data= Processor.Load_data(Pages,Cleaned_Table)
        Completed_Pages=Processor.Load_positions(Pages_with_data)
        Tagged_Images=Processor.Make_Tagged_Images(Completed_Pages,Now)