import logging
import os
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import csv
import jdatetime
import time

logger = logging.getLogger(__name__)

Names = ["1-Tir_Ahan",
         "2-Milgerd",
         "3-Profill",
         "4-Nawdani",
         "5-Nabshi",
         "6-Waraq_Siah",
         "7-Tasme_Maftoul",
         "8-Khamoot",
         "9-Waraq_Galwanize"]

Capacities = [9,12,10,8,7,12,10,6,10]  

class Page :

    def __init__ ( self, Name, Capacity, Image, Data = None, Positions = None) :
        self.Name=Name
        self.Capacity=Capacity
        self.Image=Image
        self.Data=Data
        self.Positions=Positions

class Iron_Data_Processor :

    Font_dir_Path = "None"
    Positions_Path = "None"
    Images_Paths = [f"Inputs/Iron/Canvas_Images/Currency_Gold",f"Inputs/Iron/Canvas_Images/Akhbar_Eghtesadi"]
    Scraped_Data_path = "None"

    def Make_Paths(self,Now):

        self.Positions_Path = "Inputs/Iron/positions/positions.csv"
        self.Font_dir_Path = "Inputs/Iron/Fonts"
        self.Scraped_Data_path = f"Outputs/Iron/Scraped_Data/Scraped_Data-{Now}.txt"

        os.makedirs(f"Inputs/Iron/Canvas_Images/{Now}/Currency_Gold", exist_ok=True)
        os.makedirs(f"Inputs/Iron/Canvas_Images/{Now}/Akhbar_Eghtesadi", exist_ok=True)


    def Data_Reader ( self, Now) :

        All_Tables=[]
      
        try:
            with open (self.Scraped_Data_path , "r" , encoding = "utf-8" ) as Data_File :
                for Line in Data_File :
                    All_Tables.append(Line)        
        except:
            logger.critical('Scraped Data File Couldent Be Read')
        else:
            logger.info('Data File Has Been Red Successfully')

        return All_Tables
    

    def Shaper ( self, All_Tables ) :

        try:
            Columns = 7
            All_Tables = np.array (All_Tables)
            Rows = len(All_Tables) // Columns
            All_Tables_2d = All_Tables.reshape((Rows, Columns))
            Needed_Columns = All_Tables_2d.shape[1] - 2
            Shaped_Data = All_Tables_2d[0:, 4:5]
        except:
            logger.error('Some Thing Is Not Right ')
        else:
            logger.info('Data Shaped')

        return Shaped_Data


    def Clean_Data ( self, Cell ) :

        Cell = re.sub(r"(?<!\n)\n(?!\n)", "", Cell)
        Cell = Cell.replace("\n", " ")

        return Cell
    

    def Make_Pages_Objects ( self, Path ) :

        try:
            Pages_Objects = []
            for name, capacity in zip(Names, Capacities) :
                Page_Object = Page(name, capacity, (Path + "/" + name + ".jpg") )
                Pages_Objects.append( Page_Object )
        except:
            logger.critical('Failed To Make Page Objects')
        else:
            logger.info('Page Objects Has Been Made')

        return Pages_Objects


    def Load_Data( self, Pages, Data ) :

        try:
            Page_Data = []
            for Page in Pages :
                Page_Data.extend( Data[:Page.Capacity] )
                Page.Data = Page_Data
                Data = Data[Page.Capacity:]
                Page_Data = []
        except:
            logger.critical('Couldnt Load Data')
        else:
            logger.info('Data Has Been Load')

        return Pages


    def Load_positions( self, Pages_With_Data):

        Positions = []
        Page_Positions = []
        try:
            with open (self.Positions_Path , mode='r' , encoding = 'utf-8' ) as File :
                reader = csv.reader(File)
                for row in reader :
                    Positions.append(row)
            for Page in Pages_With_Data:
                Page_Positions.extend(Positions[:Page.Capacity])
                Page.Positions = Page_Positions
                Positions = Positions[Page.Capacity:]
                Page_Positions = []
        except:
            logger.error('Couldnt Load Positions')
        else:
            logger.info('Positions Are Ready')

        return(Pages_With_Data)


    def Convert_Data_To_ENG_Numbers ( self, Data ) :

        Persian_To_Latin = {'۰': '0',
                            '۱': '1',
                            '۲': '2',
                            '۳': '3',
                            '۴': '4',
                            '۵': '5',
                            '۶': '6',
                            '۷': '7',
                            '۸': '8',
                            '۹': '9'}
        if (Data != "---") :
            for Persian_Digit, Latin_Digit in Persian_To_Latin.items() :
                Data = Data.replace(Persian_Digit, Latin_Digit)
            Data = Data.replace(',', '')
            try :
                Result = int(Data)
            except ValueError :
                Result = float(Data)
                print("Value Error: result turned into float")
            Formatted_Result = "{:,}".format(Result)
            return Formatted_Result
        else :
            return Data
    

    def Make_Tagged_Images ( self, Completed_Pages, Path ) :
        try:
            Font_File_path = os.path.join(self.Font_dir_Path, "IRANSans_Black.ttf")
            Font_Size = 35
            Font = ImageFont.truetype(Font_File_path, int(Font_Size))
            for Page in Completed_Pages :
                Raw_Canvas_Image = Image.open(Page.Image)
                Drawer = ImageDraw.Draw(Raw_Canvas_Image)
                for Position, Data in zip(Page.Positions,Page.Data) :
                    X, Y = int(Position[0]), int(Position[1])
                    access = Iron_Data_Processor()
                    Final_Data = access.Convert_Data_To_ENG_Numbers(Data[0])
                    Drawer.text((X, Y),Final_Data,fill="black",font=Font)
                if not os.path.exists(Path):
                    os.makedirs(Path)
                file_path = os.path.join(Path, f"{Page.Name}.png")
                Raw_Canvas_Image= Raw_Canvas_Image.resize((700,700))
                Raw_Canvas_Image.save(file_path)
        except:
            logger.critical('Couldent Make Images')
        else:
            logger.info('Images Has Been Made')
        
    def Make_Cover_Page( self, input_path, output_path ):
        try:
            Font_File_path = os.path.join(self.Font_dir_Path, "BKoodkBd.ttf")
            Font_Size = 80
            Font = ImageFont.truetype(Font_File_path,int(Font_Size))
            Path_Currencygold = os.path.join(input_path[0],"Cover.jpg")
            Path_Eqtesadi = os.path.join(input_path[1],"Cover.jpg")
            Raw_Canvas_Image_Currencygold = Image.open(Path_Currencygold)
            Raw_Canvas_Image_Eqtesadi = Image.open(Path_Eqtesadi)
            Drawer_Currencygold = ImageDraw.Draw(Raw_Canvas_Image_Currencygold)
            Drawer_Eqtesadi = ImageDraw.Draw(Raw_Canvas_Image_Eqtesadi)
            Drawer_Currencygold.text((40,950),jdatetime.datetime.now().strftime("%Y/%m/%d"),fill="white",font=Font)
            Drawer_Eqtesadi.text((40,950),jdatetime.datetime.now().strftime("%Y/%m/%d"),fill="white",font=Font)
            Raw_Canvas_Image_Currencygold= Raw_Canvas_Image_Currencygold.resize((700,700))
            Raw_Canvas_Image_Eqtesadi= Raw_Canvas_Image_Eqtesadi.resize((700,700))
            Raw_Canvas_Image_Currencygold.save(os.path.join(output_path[0],"0-cover.png"))
            Raw_Canvas_Image_Eqtesadi.save(os.path.join(output_path[1],"0-cover.png"))
        except:
            logger.warning('Couldnt Make The Cover Image')
        else:
            logger.info('Made Cover Pages') 

    def Process( self, Now ) :
        Processor = Iron_Data_Processor()
        Processor.Make_Paths(Now)
        Output_Paths = [f"Outputs/Iron/Images/{Now}/Currency_Gold",f"Outputs/Iron/Images/{Now}/Akhbar_Eghtesadi"]
        Table = Processor.Data_Reader(Now)
        Shaped_Table = Processor.Shaper(Table)
        try:
            Cleaned_Table = [[Processor.Clean_Data(cell) for cell in row] for row in Shaped_Table]
        except:
            logger.error('Cleaning Data wasnt Successful')
        else:
            logger.info('Data Cleaned')
        Pages_0 = Processor.Make_Pages_Objects(self.Images_Paths[0])
        Pages_1 = Processor.Make_Pages_Objects(self.Images_Paths[1])
        Pages_With_Data_0 = Processor.Load_Data(Pages_0,Cleaned_Table)
        Pages_With_Data_1 = Processor.Load_Data(Pages_1,Cleaned_Table)
        Completed_Pages_0 =Processor.Load_positions(Pages_With_Data_0)
        Completed_Pages_1 =Processor.Load_positions(Pages_With_Data_1)
        Tagged_Images_0 = Processor.Make_Tagged_Images(Completed_Pages_0,Output_Paths[0])
        Tagged_Images_1 = Processor.Make_Tagged_Images(Completed_Pages_1,Output_Paths[1])
        cover = Processor.Make_Cover_Page(self.Images_Paths,Output_Paths)
