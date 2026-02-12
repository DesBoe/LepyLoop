import os
import subprocess
import platform
import time
import csv

def get_os():
    os_name = platform.system()
    if os_name == "Darwin":
        return "Mac"
    elif os_name == "Windows":
        return "Windows"
    else:
        print("##LL:Warning: Unknown OS\n the LepyLoop script may not work properly\n continue anyway")
        return "Unknown"


def execute_lepy(run_name, image_path, repoint_check = False, repoint_directory = None):
    
    os_name = get_os()
    csv_file = f"{run_name}/execution_times.csv"
    

    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Run Name", "Execution Time (seconds)"])

    for folder in os.listdir(run_name):
        folder_path = os.path.join(run_name, folder)
        if os.path.isdir(folder_path) and folder.startswith('package') and not folder.endswith('_result'):
            if os_name == "Mac":
                if repoint_check and repoint_directory:
                    try:
                        command = ["python3", "main.py", folder_path, "config.yml", "-y", "-f", "-kp", repoint_directory]
                    except Exception as e:
                        print(f"##LL: Error on {folder_path}: {e}")
                else:
                    try:
                        command = ["python3", "main.py", folder_path, "config.yml", "-y", "-f"]
                    except Exception as e:
                        print(f"##LL: Error on {folder_path}: {e}")
            elif os_name == "Windows":
                if repoint_check and repoint_directory:
                    try:
                        command = ["python", "main.py", folder_path, "config.yml", "-y", "-f", "-kp", repoint_directory]
                    except Exception as e:
                        print(f"##LL: Error on {folder_path}: {e}")
                else:
                    try:
                        command = ["python", "main.py", folder_path, "config.yml", "-y", "-f"]
                    except Exception as e:
                        print(f"##LL: Error on {folder_path}: {e}")        
            try:
                print(f"\n##LL: Executing: {folder}\n")
                start_time = time.time()  # Start timing
                subprocess.run(command)
                end_time = time.time()  # End timing
                execution_time = end_time - start_time

                # Write the execution time to the CSV file
                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([folder, execution_time])

                time.sleep(1)
            except Exception as e:
                print(f"##LL: Error: {e}")
                print(f"##LL: Error: Lepy execution failed for {folder_path}")    
            
            print(f"##LL: {folder_path} has been processed")