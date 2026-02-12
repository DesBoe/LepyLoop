import argparse

def arguments(image_path = None, parent_dir=None, individuals_count=None, repoint_check=False, repoint_path=None):
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("image_path", type=str, help="Path to the input folder containing the pictures of individuals")
    parser.add_argument("parent_dir", type=str, help="Parent directory of the dataset")
    parser.add_argument('individuals_count', type=int, help="The number of individuals for processing per run.")
    parser.add_argument('--repoint_check', action='store_true', help="Flag to indicate if data from a previous run that have been corrected using rePoint tool should be used.")
    parser.add_argument('--repoint_path', type=str, help="Path to the directory containing the data from a previous run that have been corrected using rePoint tool")

    # Argumentliste für parse_args zusammenstellen
    arg_list = []
    if image_path is not None:
        arg_list.append(str(image_path))
    if parent_dir is not None:
        arg_list.append(str(parent_dir))
    if individuals_count is not None:
        arg_list.append(str(individuals_count))
    if repoint_check:
        arg_list.append('--repoint_check')
    if repoint_path:
        arg_list.append('--repoint_path')
        arg_list.append(str(repoint_path))

    args = parser.parse_args(arg_list)
    return args