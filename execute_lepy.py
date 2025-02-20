import os
import subprocess
import platform
import time

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
