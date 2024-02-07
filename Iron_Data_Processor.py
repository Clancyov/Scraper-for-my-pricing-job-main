import os
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import csv

Images_Paths = ["Inputs\\Iron\\Canvas_Images\\Currency_Gold",
                "Inputs\\Iron\\Canvas_Images\\Akhbar_Eghtesadi"]

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

Output_Paths = ["Outputs\\Iron\\Images\\Currency_Gold",
                "Outputs\\Iron\\Images\\Akhbar_Eghtesadi"]

class Page :

    def __init__ ( self, Name, Capacity, Image, Data = None, Positions = None) :
        self.Name=Name
        self.Capacity=Capacity
        self.Image=Image
        self.Data=Data
        self.Positions=Positions


class Iron_Data_Processor :


    def Data_Reader ( self, Now) :

        All_Tables=[]
        with open ( f"Outputs\\Iron\\Scraped_data\\Scraped_data-{Now}.txt" , "r" , encoding = "utf-8" ) as Data_File :
            for Line in Data_File :
                All_Tables.append(Line)        
        return All_Tables
    

    def Shaper ( self, All_Tables ) :

        Columns = 7
        All_Tables = np.array (All_Tables)
        Rows = len(All_Tables) // Columns
        All_Tables_2d = All_Tables.reshape((Rows, Columns))
        Needed_Columns = All_Tables_2d.shape[1] - 2
        Shaped_Data = All_Tables_2d[0:, 4:5]
        return Shaped_Data


    def Clean_Data ( self, Cell ) :

        Cell = re.sub(r"(?<!\n)\n(?!\n)", "", Cell)
        Cell = Cell.replace("\n", " ")
        return Cell
    

    def Make_Pages_Objects ( self, Path ) :

        Pages_Objects = []
        for name, capacity in zip(Names, Capacities) :
            Page_Object = Page(name, capacity, (Path + "\\" + name + ".jpg") )
            Pages_Objects.append( Page_Object )
        return Pages_Objects


    def Load_Data( self, Pages, Data ) :

        Page_Data = []
        for Page in Pages :
            Page_Data.extend( Data[:Page.Capacity] )
            Page.Data = Page_Data
            Data = Data[Page.Capacity:]
            Page_Data = []
        return Pages


    def Load_positions( self, Pages_With_Data):

        Positions = []
        with open ('Inputs\\Iron\\positions\\positions.csv' , mode='r' , encoding = 'utf-8' ) as File :
            reader = csv.reader(File)
            for row in reader :
                Positions.append(row)
        Page_Positions = []
        for Page in Pages_With_Data:
            Page_Positions.extend(Positions[:Page.Capacity])
            Page.Positions = Page_Positions
            Positions = Positions[Page.Capacity:]
            Page_Positions = []
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

        Font_File = "Inputs\\Iron\\Fonts\\IRANSans_Black.ttf"
        Font_Size = 35
        Font = ImageFont.truetype(Font_File, int(Font_Size))
        for Page in Completed_Pages :
            Raw_Canvas_Image = Image.open(Page.Image)
            Drawer = ImageDraw.Draw(Raw_Canvas_Image)
            for Position, Data in zip(Page.Positions,Page.Data) :
                X, Y = int(Position[0]), int(Position[1])
                access = Iron_Data_Processor()
                Final_Data = access.Convert_Data_To_ENG_Numbers(Data[0])
                Drawer.text((X, Y),Final_Data,fill="black",font=Font)
            Raw_Canvas_Image.save(os.path.join(Path,f"{Page.Name}.png"))
        

    def Process( self, Now ) :

        Processor = Iron_Data_Processor()
        Table = Processor.Data_Reader(Now)
        Shaped_Table = Processor.Shaper(Table)
        Cleaned_Table = [[Processor.Clean_Data(cell) for cell in row] for row in Shaped_Table]
        Pages_0 = Processor.Make_Pages_Objects(Images_Paths[0])
        Pages_1 = Processor.Make_Pages_Objects(Images_Paths[1])
        Pages_With_Data_0= Processor.Load_Data(Pages_0,Cleaned_Table)
        Pages_With_Data_1= Processor.Load_Data(Pages_1,Cleaned_Table)
        Completed_Pages_0=Processor.Load_positions(Pages_With_Data_0)
        Completed_Pages_1=Processor.Load_positions(Pages_With_Data_1)
        Tagged_Images_0=Processor.Make_Tagged_Images(Completed_Pages_0,Output_Paths[0])
        Tagged_Images_1=Processor.Make_Tagged_Images(Completed_Pages_1,Output_Paths[1])