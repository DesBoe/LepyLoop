import re
import os
import csv
from ImageMover import *

print("##LL: This script helps you to check for unpaired images of RGB and UV photos in your database \nImage names must follow a uniform naming convention \nUV photos are expected to be indicated by the same name as RGB but extended with 'uv' \ne.g. \n EcEs-Lep-00001 \n EcEs-Lep-00001uv \n EcEs-Lep-00002  \n EcEs-Lep-00002uv \n EcEs-Lep-00003  \n EcEs-Lep-00003uv\n ... \n")

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None

if __name__ == "__main__":
    print("##LL: Please enter the path of the of your input folder containing the pictures of individuals")
    path_for_check = input()
    image_files = find_image_files(path_for_check)

    print("##LL: Please enter the number of digits in the image names")
    Numberlength = input()
    Numberlength = int(Numberlength)
    
    numbers = [extract_number(os.path.basename(file)) for file in image_files]
    numbers = [num for num in numbers if num is not None]
    
    if numbers:
        highest_number = max(numbers)
        print(f"##LL: The highest number found in the image filenames is: {highest_number}")
    else:
        print("##LL: No numbers found in the image filenames.")
        highest_number = 0

    csv_filename = os.path.join(path_for_check, 'image_check.csv')
    log_filename = os.path.join(path_for_check, 'missing_images.log')
    os.makedirs(os.path.join(path_for_check, 'unpaired_images'), exist_ok=True)

    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Running Number', 'Photo Proboscis', 'Photo Upper', 'Extra Photo', 'Photo UV', 'ID'])

        with open(log_filename, 'w') as logfile:
            logfile.write("incomplete cases log\n")

            for i in range(1, highest_number + 1):
                running_number_str = str(i).zfill(Numberlength)  
                id_pattern = re.compile(rf"(\D+-?)({running_number_str})")
                
                photo_upper = None
                photo_uv = None
                extra_photos = []
                base_name = None

                for filename in image_files:
                    if re.search(rf"{running_number_str}\.tif$", filename):
                        photo_upper = os.path.basename(filename)
                        base_name = photo_upper.rsplit('.', 1)[0]  
                    elif re.search(rf"{running_number_str}uv\.tif$", filename, re.IGNORECASE):  
                        photo_uv = os.path.basename(filename)
                        base_name = photo_uv.rsplit('.', 1)[0].replace('uv', '')  
                    elif re.search(rf"{running_number_str}[^\d]*\.tif$", filename):
                        extra_photos.append(os.path.basename(filename))
                    elif re.search(rf"{running_number_str}(-I|-II|-Iuv|-IIuv|_1|_2|_3|_4)?\.tif$", filename, re.IGNORECASE):
                        extra_photos.append(os.path.basename(filename))    

                csvwriter.writerow([
                    i,
                    '',  
                    photo_upper or '',
                    ', '.join(extra_photos) or '',  
                    photo_uv or '',
                    base_name or ''  
                ])

                if not photo_upper and not photo_uv:
                    continue  
                if not photo_upper:
                    logfile.write(f"{base_name} - RGB is missing\n")
                elif not photo_uv:
                    logfile.write(f"{base_name} - UV is missing\n")  