import os
import time
import csv
from tqdm import tqdm

def find_image_files(parent_dir):
    image_extensions = ('.tif', '.tiff', '.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG')
    image_files = []

    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.lower().endswith(image_extensions) and not file.startswith('._'):
                image_files.append(os.path.join(root, file))
    return image_files

def create_input(run_name, image_files):
    os.mkdir(os.path.join(run_name, 'images_input'))
    original_paths = {}
    for image_file in tqdm(image_files, desc="Moving images", unit="file"):
        original_paths[os.path.basename(image_file)] = os.path.dirname(image_file)
        os.rename(image_file, os.path.join(run_name, 'images_input', os.path.basename(image_file)))
        time.sleep(0.001)
    print("Images moved to input folder")
    return original_paths

def process_images(run_name, input_dir, individuals_count):
    unpair_dir = os.path.join(input_dir, '../images_unpair')
    os.makedirs(unpair_dir, exist_ok=True)

    unpair_log = os.path.join(run_name, 'images_unpair_protokoll.csv')
    with open(unpair_log, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['file', 'missing'])

        image_files = os.listdir(input_dir)
        image_files.sort()

        pairs = {}
        for image_file in image_files:
            time.sleep(0.05)
            if image_file.startswith('._'):
                continue
            if 'uv' in image_file.rsplit('.', 1)[0]:
                base_name = image_file.rsplit('uv', 1)[0]
                pairs.setdefault(base_name, [None, None])[1] = image_file
            else:
                base_name = image_file.rsplit('.', 1)[0]
                pairs.setdefault(base_name, [None, None])[0] = image_file

        print("create packages for analyses with Lepy")        

        package_count = 1
        pair_count = 0
        package_dir = os.path.join(input_dir, f'../package{package_count:02d}')
        os.makedirs(package_dir, exist_ok=True)
        print(f"Creating package {package_count:02d}")

        for base_name, (rgb_image, uv_image) in pairs.items():
            time.sleep(0.01)
            if rgb_image and uv_image:
                if pair_count >= individuals_count:
                    package_count += 1
                    pair_count = 0
                    package_dir = os.path.join(input_dir, f'../package{package_count:02d}')
                    os.makedirs(package_dir, exist_ok=True)
                    print(f"Creating package {package_count:02d}")

                os.rename(os.path.join(input_dir, rgb_image), os.path.join(package_dir, rgb_image))
                os.rename(os.path.join(input_dir, uv_image), os.path.join(package_dir, uv_image))
                pair_count += 1
            else:
                if rgb_image:
                    os.rename(os.path.join(input_dir, rgb_image), os.path.join(unpair_dir, rgb_image))
                    writer.writerow([rgb_image, 'UV'])
                elif uv_image:
                    os.rename(os.path.join(input_dir, uv_image), os.path.join(unpair_dir, uv_image))
                    writer.writerow([uv_image, 'RGB'])

    # Überprüfen, ob das Verzeichnis input_dir leer ist
    if not os.listdir(input_dir):
        os.rmdir(input_dir)
    else:
        print(f"Warning: {input_dir} is not empty and has been retained.")

    print("Image processing completed")

def restore_order(run_name, original_paths, input_dir):
    for folder in os.listdir(run_name):
        folder_path = os.path.join(run_name, folder)
        if os.path.isdir(folder_path) and folder.startswith('package') and not folder.endswith('_result'):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if file_name in original_paths:
                    os.rename(file_path, os.path.join(original_paths[file_name], file_name))
                
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
            else:
                print(f"Warning: {folder_path} is not empty and has been retained.")

    unpair_dir = os.path.join(run_name, 'images_unpair')
    for file_name in os.listdir(unpair_dir):
        file_path = os.path.join(unpair_dir, file_name)
        if file_name in original_paths:
            os.rename(file_path, os.path.join(original_paths[file_name], file_name))
        time.sleep(0.01)

    if not os.listdir(unpair_dir):
        os.rmdir(unpair_dir)
        time.sleep(0.001)
    else:
        print(f"Warning: {unpair_dir} is not empty and has been retained.")

    print("Images restored to original locations")