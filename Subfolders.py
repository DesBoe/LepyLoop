import os

def create_folder(run_name):
    subfolders = [
        'contours_txt',
        'false_color_jpg',
        'stats_json',
        'errors_log',
        'stats_per_run_csv',
        'images_unpair',
    ]

    for folder in subfolders:
        os.makedirs(os.path.join(run_name, folder), exist_ok=True)
    
    input_dir = os.path.join(run_name, 'images_input')
    print('##LL:All subfolders created')
    
    return input_dir