import logging
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re
import os
import jdatetime

logger = logging.getLogger(__name__)

# Class to process phone data and generate images.
class Phone_Data_Processor:

    # Constructor method to initialize instance variables.
    def __init__(self):

        # Get current Jalali date
        self.date = jdatetime.datetime.now().strftime("%Y/%m/%d")
        # Path to plain images directory
        self.plain_images_path = "Inputs\\Phones\\plain images\\"
        # Path to output images directory
        self.output_path = "Outputs\\Phones\\Images\\"  


    # Method to read data from a file.
    def data_reader(self,Now):
        lines=[]
        try:
            with open(f"Outputs\\Phones\\Scraped_data\\Scraped_data-{Now}.txt", 'r', encoding='utf-8') as file:
                # Read lines from file
                lines = file.readlines()
            # Return the red lines
        except:
            logger.critical('Failed To Load Scraped Data File')
        else:
            logger.info('Scraped Data Loaded')
        return lines
    

    # Method to filter out Persian phrases from text lines.
    def filter_persian_phrases(self, text_lines):

        filtered_text_lines = []
        for line in text_lines:
            # Replace Persian characters with empty string
            filtered_line = re.sub(r'[\u0600-\u06FF]+', '', line) 
            # Append filtered line to the list 
            filtered_text_lines.append(filtered_line)
        # Return the list of filtered text lines  
        return filtered_text_lines  


    # Method to filter out Persian phrases from a list of text lines.
    def filter_list(self, text_lines):

        try:
            # Call filter_persian_phrases method
            no_persian_phrases = self.filter_persian_phrases(text_lines)  
            # Return the list of text lines without Persian phrases
        except:
            logger.error('Failed To Delete Persian Phrases')
        else:
            logger.info('Persian Phrases Are deleted')

        return no_persian_phrases  


    # Method to reshape a list of text lines into a structured format.
    def reshape_list(self, text_lines):
        filtered_data = None
        try:
            # Calculate the number of rows based on the length of the text lines
            num_rows = -(-len(text_lines) // 7)  
            # Split the text lines into rows
            reshaped_data = np.array_split(text_lines, num_rows)  
            # Convert the reshaped data to string type
            reshaped_data_str = np.array(reshaped_data).astype(str)  
            # Remove unwanted columns
            reshaped_data_without_unwanted_columns = np.delete(reshaped_data_str, np.s_[1:6], axis=1)  
            # Filter out rows containing "call" in the last column
            filtered_data = [row for row in reshaped_data_without_unwanted_columns if "call" not in row[-1].lower()]
        except:
            logger.error('Failed To Reshape Data')
        else:
            logger.info('Date Reshaped')
        # Return the filtered data
        return filtered_data  
    

    # Method to separate the reshaped data into different brand lists.
    def separate_brands(self, reshaped_data):

        samsung = []
        xiaomi = []
        nokia = []
        # List of brand lists
        brands = [samsung, xiaomi, nokia]  

        current_brand=None

        try:
            for row in reshaped_data:
                if "SAMSUNG" in row[0]:
                    current_brand=samsung
                elif "XIAOMI" in row[0]:
                    current_brand=xiaomi
                elif "NOKIA" in row[0]:
                    current_brand=nokia
                elif current_brand==None or "Tab" in row[0]:
                    continue
                elif row[1]=="  \n" :
                    break
                current_brand.append(row)

            # Delete the first element (Header) 
            del samsung[0]  
            del xiaomi[0]   
            del nokia[0]
        except:
            logger.critical('Couldnt Separate Brands From Each Other')
        else:
            logger.info('Brands Are Separated')
        # Return the list of brand lists
        return brands   


    # Method to delete extra spaces from the text in each cell of the brand lists.
    def delete_extra_spaces(self, brands):

        try:
            for brand_list in brands:
                for row in brand_list:
                    # Replace multiple spaces with single space in each cell
                    row[:] = [re.sub(r'\s+', ' ', cell) for cell in row] 
            # Return the modified brand lists 
        except:
            logger.warning('Failed to Delete Extra Space Characters')
        else:
            logger.info('Extra Spaces Are Deleted')

        return brands   


    # Method to write data onto images.
    def write_on_images(self, data_list, name, c):

        # Get the path of the plain image
        plain_image = os.path.join(self.plain_images_path, f"{name}.jpg")  
        # Path to the font file
        font_file = "Inputs\\Iron\\Fonts\\IRANSans_Black.ttf"
        # Font size  
        font_size = 40  
        # Load the font
        font = ImageFont.truetype(font_file, int(font_size)) 
        # Open the plain image 
        plain_image = Image.open(plain_image)  
        # Create an image drawer
        drawer = ImageDraw.Draw(plain_image)  
        # Initial x-coordinate
        x = 10  
        # Initial y-coordinate
        y = 113  

        for item in data_list:
            # Write the date on the image
            drawer.text((100, 30), self.date, fill="white", font=ImageFont.truetype(font_file, 30))  
            # Write the first item on the image
            drawer.text((x, y), item[0], fill="white", font=font)  
            # Get the bounding box of the second item
            bbox = drawer.textbbox((x, y), item[1], font=font)  
            # Calculate the width of the text
            text_width = bbox[2] - bbox[0]  
            # Adjusted x coordinate to center the text
            drawer.text((x + 965 - text_width/2, y), item[1], fill="white", font=font)  
            # Increase y-coordinate for next item
            y += 65  
            # Save the modified image

        plain_image.save(os.path.join(self.output_path, f"{name}{c}.png"))


    # Method to divide the data into chunks and create images for each chunk.
    def divide_and_make_images(self, brands):

        try:
            # Counter for naming images
            counter = 0  
            # Temporary list to store data for each image
            temp_list = []  
            for brand in brands:
                for idx, item in enumerate(brand):
                    # Add item to temporary list
                    temp_list.append(item)  
                    # Check if the temporary list is full or if it's the last item in the brand list
                    if len(temp_list) == 15 or idx == len(brand) - 1:
                        if brand == brands[0]:
                            # Set the name based on the brand
                            name = "samsung"  
                        elif brand == brands[1]: 
                            name = "xiaomi"
                        elif brand == brands[2]:
                            name = "nokia"
                        # Write data onto image
                        self.write_on_images(data_list=temp_list, name=name, c=counter) 
                        # Increment counter 
                        counter += 1  
                        # Reset temporary list
                        temp_list = []
        except:
            logging.critical('Couldnt Make Images')
        else:
            logging.info('Images Have Been Made')
            
        return 0


    # Method to execute the data processing pipeline.
    def Process(self,Now):

        # Read raw data
        raw_list = self.data_reader(Now)  
        # Filter the raw data
        filtered_list = self.filter_list(raw_list)  
        # Reshape the filtered data
        reshaped_list = self.reshape_list(filtered_list)  
        # Separate the data by brand
        separated_brands = self.separate_brands(reshaped_list)  
        # Delete extra spaces in the data
        no_extra_spaces = self.delete_extra_spaces(separated_brands)  
        # Divide the data into images
        self.divide_and_make_images(no_extra_spaces)  
