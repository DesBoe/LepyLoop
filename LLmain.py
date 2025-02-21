import os
from datetime import datetime
import subprocess
import platform
from PIL import Image
import Parser
import Subfolders
from ImageMover import *
from Merger import *


def get_os():
    os_name = platform.system()
    if os_name == "Darwin":
        return "Mac"
    elif os_name == "Windows":
        return "Windows"
    else:
        print("Warning: Unknown OS\n the LepyLoop script may not work properly\n continue anyway")
        return "Unknown"


def execute_lepy(run_name):
    os_name = get_os()

    for folder in os.listdir(run_name):
        folder_path = os.path.join(run_name, folder)
        if os.path.isdir(folder_path) and folder.startswith('package') and not folder.endswith('_result'):
            if os_name == "Mac":
                command = ["python3", "main.py", folder_path, "config.yml", "-y", "-f"]
            elif os_name == "Windows":
                command = ["python", "main.py", folder_path, "config.yml", "-y", "-f"]
            
            try:
                subprocess.run(command)  
                time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Error: Lepy execution failed for {folder_path}")    
            
            print(f"{folder_path} has been processed")
    

def proceed_check(message: str, default: bool = False) -> bool:
    if default:
        prompt = f"{message} [Y/n]: "
    else:
        prompt = f"{message} [y/N]: "
    
    user_input = input(prompt).lower()

    if user_input in ('y', 'yes'):
        return True
    else:
        return False
    

if __name__ == "__main__":
    print("Enter the path of the of your input folder containing the pictures of individuals")
    path = input()
    print("Enter the number of individuals you want to process per run. we recommend 100")
    individuals_count = int(input())
    args = Parser.arguments(path, individuals_count)

    run_name = args.parent_dir + "_Lepy_Execution_" + datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.mkdir(run_name)
    input_dir = Subfolders.create_folder(run_name)

    image_files = find_image_files(args.parent_dir)
    print(f"Number of input images: {len(image_files)}")
    original_paths = create_input(run_name, image_files)

    process_images(run_name,input_dir, individuals_count)

    if proceed_check("All packages been created successfully. Continue with Lepy? y/n", default=False):
        execute_lepy(run_name)
        merge_content(run_name)
        create_excel(run_name)     
        restore_order(run_name, original_paths, input_dir)           
        delete_folders(run_name)

    print("All analysis done")