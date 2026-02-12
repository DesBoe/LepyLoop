import os
import shutil
import pandas as pd

def merge_content(run_name):
    print("##LL: Merging content")
    try:
        os.rename(os.path.join(run_name, "package01_result", "config.yml"), os.path.join(run_name, "configuration_Lepy.yml"))
    except FileNotFoundError:
        print("##LL: could not find merging files")
    # Suche nach allen Ordnern, die mit package anfangen und mit _result enden
    for folder in os.listdir(run_name):
        if folder.startswith("package") and folder.endswith("_result"):
            run_number = folder[len("package"):-len("_result")]
            source_folder = os.path.join(run_name, folder)

            # Verschiebe Dateien aus den entsprechenden Unterordnern
            subfolders = {
                "contours": "contours_txt",
                "gbuv": "false_color_jpg",
                "json": "stats_json",
                "visualisations": "visualisations_png"  # Korrekt benannt
            }

            for subfolder, target in subfolders.items():
                source_path = os.path.join(source_folder, subfolder)
                target_path = os.path.join(run_name, target)
                os.makedirs(target_path, exist_ok=True)  # Zielordner erstellen, falls nicht vorhanden
                if os.path.exists(source_path):
                    for file in os.listdir(source_path):
                        if not file.startswith("._") and file.endswith(".png"):  # Nur PNG-Dateien verschieben
                            shutil.move(os.path.join(source_path, file), os.path.join(target_path, file))

            # Verschiebe errors.log und stats.csv
            for file_name in ["errors.log", "stats.csv"]:
                source_file = os.path.join(source_folder, file_name)
                if os.path.exists(source_file):
                    new_file_name = f"{file_name.split('.')[0]}{run_number}.{file_name.split('.')[1]}"
                    target_path = os.path.join(run_name, f"{file_name.split('.')[0]}_log" if file_name == "errors.log" else "stats_per_run_csv")
                    os.makedirs(target_path, exist_ok=True)  # Zielordner erstellen, falls nicht vorhanden
                    shutil.move(source_file, os.path.join(target_path, new_file_name))

def delete_folders(run_name):
    print("##LL: delete package_folders")
    for folder in os.listdir(run_name):
        if folder.startswith("package"):
            folder_path = os.path.join(run_name, folder)
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.startswith("._"):
                        os.remove(os.path.join(root, file))
            shutil.rmtree(folder_path)

def create_excel(run_name):
    print("##LL: Creating combined CSV and Excel file")
    stats_folder = os.path.join(run_name, "stats_per_run_csv")
    combined_csv_path = os.path.join(run_name, "stats_combined.csv")
    excel_path = os.path.join(run_name, "stats_combined.xlsx")
    
    all_data = []
    columns = None
    for file in os.listdir(stats_folder):
        if file.startswith("._") or not file.endswith(".csv"):
            continue
        file_path = os.path.join(stats_folder, file)
        try:
            df = pd.read_csv(file_path, delimiter='\t', encoding='utf-8')
            if columns is None:
                columns = df.columns
            elif not df.columns.equals(columns):
                print(f"##LL: Skipping {file_path} due to column mismatch")
                continue
            all_data.append(df)
        except UnicodeDecodeError:
            print(f"##LL: Error reading {file_path}: Non-UTF-8 encoding detected")
        except Exception as e:
            print(f"##LL: Error reading {file_path}: {e}")
    
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        combined_data.to_csv(combined_csv_path, index=False, sep='\t')
        combined_data.to_excel(excel_path, index=False)
        print(f"##LL: Combined CSV file created at {combined_csv_path}")
        print(f"##LL: Excel file created at {excel_path}")
    else:
        print("##LL: No valid CSV files found to combine.")
