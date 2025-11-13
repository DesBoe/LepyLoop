import os
from datetime import datetime
import platform
from PIL import Image
import Parser
import Subfolders
from ImageMover import *
from Merger import *
from execute_lepy import execute_lepy


def get_os():
    os_name = platform.system()
    if os_name == "Darwin":
        return "Mac"
    elif os_name == "Windows":
        return "Windows"
    else:
        print("Warning: Unknown OS\n the LepyLoop script may not work properly\n continue anyway")
        return "Unknown"
    

if __name__ == "__main__":
    print("Enter the path of the of your input folder containing the pictures of individuals")
    path = input().strip().strip("'\"")
    print("Do you want to analyse paired images: is one specimen photographed in RGB and UV light?\nplease enter\n 'RGB' if you only want to analyse RGB images\n 'UV' if you  want to analyse paires RGB and UV images")
    mode = input()
    print("Enter the number of individuals you want to process per run. we recommend 100")
    individuals_count = int(input())
    args = Parser.arguments(path, individuals_count)

    run_name = args.parent_dir + "_Lepy_Execution_" + datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.mkdir(run_name)
    input_dir = Subfolders.create_folder(run_name)

    image_files = find_image_files(args.parent_dir)
    print(f"Number of input images: {len(image_files)}")
    original_paths = create_input(run_name, image_files)
    export_as_jpp(run_name)
    if mode.lower() == "rgb":
        print("LepyLoop will be executed with RGB images only")
        process_images_RGB(run_name,input_dir, individuals_count)
 
    elif mode.lower() == "uv":
        print("LepyLoop will be executed with paired RGB and UV images")
        process_images_UV(run_name,input_dir, individuals_count)
    else:
        print("Invalid mode selected. Please enter 'RGB' or 'UV'.")
        exit(1)    

    print("All packages been created successfully. Continue with Lepy")
    
    execute_lepy(run_name, path)
    merge_content(run_name)
    create_excel(run_name)     
    restore_order(run_name, original_paths, input_dir)           
    delete_folders(run_name)

    print("All analysis done")