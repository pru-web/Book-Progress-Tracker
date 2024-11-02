#script to know the project dir structure 

import os

def write_directory_structure(root_dir, exclude_dirs=None, level=0, file=None):
    exclude_dirs = exclude_dirs or []
    for root, dirs, files in os.walk(root_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        indent = ' ' * 4 * level
        if file:
            file.write(f"{indent}{os.path.basename(root)}/\n")
            for f in files:
                file.write(f"{indent}    {f}\n")
        else:
            print(f"{indent}{os.path.basename(root)}/")
            for f in files:
                print(f"{indent}    {f}")
        # Recursively print subdirectories
        for d in dirs:
            write_directory_structure(os.path.join(root, d), exclude_dirs, level + 1, file)

# Specify the root directory and directories to exclude
root_directory = "C:/progress_tracker_project"
exclude_directories = ['venv', '__pycache__', 'node_modules']

# Create or open the file where the output will be written
with open("directory_structure.txt", "w") as f:
    write_directory_structure(root_directory, exclude_directories, file=f)

print("Directory structure saved to directory_structure.txt")
