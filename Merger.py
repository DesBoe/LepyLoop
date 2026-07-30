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
                        if not file.startswith("._"):
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
    return excel_path

def report_errors(excel_path):
    print("##LL: check zeros from the Excel file")
    columns_to_check = ['poi_dist_inner']
    found_errors = {}
    try:
        df = pd.read_excel(excel_path)
        for col in columns_to_check:
            if col in df.columns:
                error_rows = df[df[col] == 0]
                if not error_rows.empty:
                    found_errors[col] = error_rows['Code'].tolist()
    except Exception as e:
        print(f"##LL: Error reading Excel file {excel_path}: {e}")

    report_path = os.path.join(os.path.dirname(excel_path), "morphological_errors_overview.txt")
    with open(report_path, "w", encoding="utf-8") as report_file:
        if found_errors:
            report_file.write("Found errors\n")
            report_file.write("===========\n")
            for col, codes in found_errors.items():
                report_file.write(f"{col}: {', '.join(map(str, codes))}\n")
        else:
            report_file.write("No errors found.\n")

    print(f"##LL: Error report written to {report_path}")

    morphological_errors_path = os.path.join(os.path.dirname(excel_path), "morphological_errors")
    os.makedirs(morphological_errors_path, exist_ok=True)

    for col, codes in found_errors.items():
        for code in codes:
            code_str = str(code)
            visualisations_dir = os.path.join(os.path.dirname(excel_path), "visualisations_png")
            if not os.path.exists(visualisations_dir):
                continue

            for file_name in os.listdir(visualisations_dir):
                if file_name.startswith("._"):
                    continue
                if code_str in file_name:
                    source_path = os.path.join(visualisations_dir, file_name)
                    target_path = os.path.join(morphological_errors_path, file_name)
                    if os.path.exists(source_path) and not os.path.exists(target_path):
                        shutil.move(source_path, target_path)

    print(f"##LL: Moved visualisations for error codes to {morphological_errors_path}")
            

    
