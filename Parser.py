import argparse

def arguments(parent_dir=None, individuals_count=None):
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("parent_dir", type=str, help="Parent directory of the dataset")
    parser.add_argument('individuals_count', type=int, help="The number of individuals for processing per run.")
    
    if parent_dir and individuals_count:
        args = parser.parse_args([parent_dir, str(individuals_count)])
    else:
        args = parser.parse_args()
    
    return args