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


def check_working_directory():
    cwd = os.getcwd()
    if not cwd.lower().endswith("lepy"):
        print(f"\n##LL: Error: working directory '{cwd}' does not end with 'Lepy'.")
        print("##LL: Please run the script within the installation folder of 'Lepy'.")
        exit(1)
        return False
    

if __name__ == "__main__":

    print("##LL: Welcome to LepyLoop ")
    print("##LL: this assistant will guide you through a setup process to execute Lepy with your images")
    print("##LL: Note that you can go back to the previous step by entering 'back' at any time")
    print("##LL: -------------------------------")
    check_working_directory()

    step = "path"
    while step != "done":
        while step == "path":
            print("\n##LL: Enter the path of the of your input folder containing the pictures of individuals")
            image_path = input().strip().strip("'\"")
            if image_path.lower() in ["back", "zurück", "b", "zurueck", "retour", "zurückgehen", "go back"]:
                print("##LL: You are already at the first step.")
            if os.path.exists(image_path):
                step = "mode"
            elif image_path.lower() not in ["back", "zurück", "b", "zurueck", "retour", "zurückgehen", "go back"]:
                print("##LL: Invalid path.")

        if step == "mode":
            print("\n##LL: No discrimination between RGB and UV images will be made in this step. All images will be processed.")
            print("##LL: insted, you will find a table with unmatched images in the output folder of this script")
            step = "individuals_count"

            
        '''while step == "mode":
            print("##LL: Do you want to analyse paired images: is one specimen photographed in RGB and UV light?\nplease enter\n 'RGB' if you only want to analyse RGB images\n 'UV' if you  want to analyse paires RGB and UV images")
            mode = input().strip().lower()
            if mode.lower() in ["back", "zurück", "b", "zurueck", "retour", "zurückgehen", "go back"]:
                step = "path"
            elif mode not in ["rgb", "uv", "r", "u", "3", "4", "rbg", "bgr", "brg", "gbr", "grb", "vu"]:
                print("##LL: Invalid mode selected. Please enter 'RGB' or 'UV'.")
            elif mode.lower() in ["rgb", "r", "3", "bgr", "brg", "gbr", "grb"]:
                mode = "rgb"
                step = "individuals_count"
            elif mode.lower() in ["uv", "u", "4", "vu"]:
                mode = "uv"
                step = "case_rgb_only"

        while step == "case_rgb_only": 
            print('##LL: upaired images might be detected: RGB present, UV missing. Do you want to process RGB only images? Enter "yes" or "no"')
            gb_only_input = input().strip().lower()

            if gb_only_input.lower() not in ["yes", "ja", "ok", "j", "y", "si", "oui",  
                                        "no", "nein", "n", "n", "non"]:
                print("##LL: Invalid input. Please enter 'yes' or 'no'.")
            elif gb_only_input.lower() in ["no", "nein", "n", "non"]:
                rgb_only_input = "no"
                step = "individuals_count"
            elif gb_only_input.lower() in ["yes", "ja", "ok", "j", "y", "si", "oui"]:
                rgb_only_input = "yes"
                step = "individuals_count"'''
                
        
        while step == "individuals_count":
            print("\n##LL: Enter the number of individuals you want to process per run. select between 1 and 1000. We recomend 100")
            individuals_count = input()
            if individuals_count in ["back", "zurück", "b", "zurueck", "retour", "zurückgehen", "go back"]:
                step = "mode"
            try:
                individuals_count = int(individuals_count)
                if 1 <= individuals_count <= 1000:
                    step = "export_jpg_input"
                else:
                    print("##LL: Invalid.")
            except ValueError:
                print("##LL: Invalid. Please enter a positive integer.")

        while step == "export_jpg_input":
            print("\n##LL: Export JPGs for visual check of the input images? Enter 'yes' or 'no'")
            
            export_jpg_input = input().strip().lower()
            if export_jpg_input.lower() in ["back", "zurück", "b", "zurueck", "retour", "zurückgehen", "go back"]:
                step = "individuals_count"
            elif export_jpg_input.lower() not in ["yes", "ja", "ok", "j", "y", "si", "oui",  
                                        "no", "nein", "n", "n", "non"]:
                print("##LL: Invalid input. Please enter 'yes' or 'no'.")
            
            elif export_jpg_input.lower() in ["yes", "ja", "ok", "j", "y", "si", "oui"]:
                export_jpg = True
                step = "repoint_input"
            elif export_jpg_input.lower() in ["no", "nein", "n", "non"]:
                export_jpg = False
                step = "repoint_input"

        
        while step == "repoint_input":
            print("\n##LL: Do you want to run LEPY with Data from a previous run that have been corrected using rePoint tool?")
            repoint_input = input("##LL: Enter 'yes' or 'no'").strip().lower()

            if repoint_input.lower() in ["back", "zurück", "b", "zurueck", "retour", "zurückgehen", "go back"]:
                step = "export_jpg_input"
            elif repoint_input.lower() not in ["yes", "ja", "ok", "j", "y", "si", "oui",  
                                            "no", "nein", "n", "n", "non"]:
                print("##LL: Invalid input. Please enter 'yes' or 'no'.")

            elif repoint_input.lower()  in ["yes", "ja", "ok", "j", "y", "si", "oui"]:
                repoint_check = True
                step = "repoint_path"
            elif repoint_input.lower() in ["no", "nein", "n", "non"]:
                repoint_check = False
                repoint_path = None
                step = "done"

        while step == "repoint_path":
            print("\n##LL: Please enter the path to the directory containing the data from a previous run that have been corrected using rePoint tool")
            repoint_path = input().strip().strip("'\"")
            if repoint_path.lower() in ["back", "zurück", "b", "zurueck", "retour", "zurückgehen", "go back"]:
                step = "repoint_input"
            if os.path.exists(repoint_path):
                step = "done"
            elif not os.path.exists(repoint_path):
                    print("##LL: Invalid path. Please enter a valid path to the input folder.")

        if step == "done":
            print("\n##LL: Setup completed. Starting LepyLoop execution...")
            print("##LL: Setup summary")
            print("-" * 40)
            print(f"{'Input path':<20} {image_path}")
            print(f"{'Individuals per run':<20} {individuals_count}")
            print(f"{'Export JPGs':<20} {'yes' if export_jpg else 'no'}")
            print(f"{'rePoint enabled':<20} {'yes' if repoint_check else 'no'}")
            if repoint_check:
                print(f"{'rePoint path':<20} {repoint_path}")
            print("-" * 40)
            print("##LL: Starting Lepy execution...\n")

    args = Parser.arguments(
        image_path=image_path,
        individuals_count=individuals_count,
        repoint_check=repoint_check,
        repoint_path=repoint_path
    )

    run_name = args.image_path + "_Lepy_Execution_" + datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.mkdir(run_name)
    input_dir = Subfolders.create_folder(run_name)

    image_files = find_image_files(args.image_path)
    print(f"##LL: Number of input images: {len(image_files)}")
    original_paths = create_input(run_name, image_files)
    if export_jpg:
        print("##LL: Exporting JPGs for visual check of the input images")
        export_as_jpp(run_name)
    '''
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
    '''
    try:
        process_images(run_name,input_dir, individuals_count)
    except Exception as e:
        print(f"##LL: Error during image processing: {e}")
        pass

    
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
        except Exception as e:
            print(f"##LL: Error during merging: {e}")
        try:
            excel_path = create_excel(run_name) 
            report_errors(excel_path)  
        except Exception as e:
            print(f"##LL: Error during Excel creation: {e}")
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