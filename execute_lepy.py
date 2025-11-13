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
        print("Warning: Unknown OS\n the LepyLoop script may not work properly\n continue anyway")
        return "Unknown"


def execute_lepy(run_name, path):
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
                command = ["python3", "main.py", folder_path, "config.yml", "-y", "-f"]
            elif os_name == "Windows":
                command = ["python", "main.py", folder_path, "config.yml", "-y", "-f"]
            
            try:
                print(f"\nExecuting: {folder}\n")
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
                print(f"Error: {e}")
                print(f"Error: Lepy execution failed for {folder_path}")    
            
            print(f"{folder_path} has been processed")