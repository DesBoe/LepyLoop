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
        print("##LL: Warning: Unknown OS\n the LepyLoop script may not work properly\n continue anyway")
        return "Unknown"
    

if __name__ == "__main__":
    print("##LL: Enter the path of the of your input folder containing the pictures of individuals")
    image_path = input().strip().strip("'\"")
    print("##LL: Do you want to analyse paired images: is one specimen photographed in RGB and UV light?\nplease enter\n 'RGB' if you only want to analyse RGB images\n 'UV' if you  want to analyse paires RGB and UV images")
    mode = input()
    print("##LL: Enter the number of individuals you want to process per run. we recommend 100")
    individuals_count = int(input())
    print("##LL: Export JPGs for visual check of the input images? Enter 'yes' or 'no'")
    export_jpg_input = input().strip().lower()
    export_jpg = export_jpg_input in ["yes", "ja", "ok"]
    print("##LL: Do you want to run LEPY with Data from a previous run that have been corrected using rePoint tool?")
    repoint_input = input("##LL: Enter 'yes' or 'no'").strip().lower()
    repoint_check = repoint_input in ["yes", "ja", "ok"]
    if repoint_check:
        print("##LL: Please enter the path to the directory containing the data from a previous run that have been corrected using rePoint tool")
        repoint_path = input().strip().strip("'\"")
    elif not repoint_check:
        repoint_path = None
    args = Parser.arguments(
        image_path=image_path,
        parent_dir=os.path.dirname(image_path),
        individuals_count=individuals_count,
        repoint_check=repoint_check,
        repoint_path=repoint_path
    )


    run_name = args.parent_dir + "_Lepy_Execution_" + datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.mkdir(run_name)
    input_dir = Subfolders.create_folder(run_name)

    image_files = find_image_files(args.parent_dir)
    print(f"##LL: Number of input images: {len(image_files)}")
    original_paths = create_input(run_name, image_files)
    if export_jpg:
        print("##LL: Exporting JPGs for visual check of the input images")
        export_as_jpp(run_name)
    if mode.lower() == "rgb":
        print("##LL: LepyLoop will be executed with RGB images only")
        process_images_RGB(run_name,input_dir, individuals_count)
        print("##LL: All packages been created successfully. Continue with Lepy in RGB mode")
    elif mode.lower() == "uv":
        print("##LL: LepyLoop will be executed with paired RGB and UV images")
        process_images_UV(run_name,input_dir, individuals_count)
        print("##LL: All packages been created successfully. Continue with Lepy in RGB + UV mode")
    else:
        print("##LL: Invalid mode selected. Please enter 'RGB' or 'UV'.")
        exit(1)    

    
    try:
        execute_lepy(run_name, image_path, repoint_check = repoint_check, repoint_directory = repoint_path)
        execution_success = True
    except Exception as e:
        print(f"##LL: Error during Lepy execution: {e}")
        execution_success = False
    if execution_success:
        try:
            time.sleep(1)
            merge_content(run_name)
            time.sleep(1)
            create_excel(run_name)     
        except Exception as e:
            print(f"##LL: Error during merging or Excel creation: {e}")
    try:     
        time.sleep(1)
        restore_order(run_name, original_paths, input_dir)    
    except Exception as e:
        print(f"##LL: Error during restoring order: {e}")
    try: 
        time.sleep(1)
        delete_folders(run_name)
    except Exception as e:
        print(f"##LL: Error during folder deletion: {e}")

    print("###############\n##LL:All done##\n###############")