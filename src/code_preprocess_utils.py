"""
Utility functions for preprocessing the code before splitting it into three parts.
"""
import os
import shutil
import re

def delete_non_py_files(directory):
    """
    Delete all non-Python files in the specified directory.

    Args:
    directory (str): The path to the directory.
    """
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)

            if not filename.endswith('.py') or filename == '__init__.py':
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"Skipped: {file_path}")


def move_files_and_cleanup(root_directory):
    """
    Move files to a given directory from nested subdirectories and delete empty directories.

    Args:
    directory (str): The path to the target directory.
    """
    for root, dirs, files in os.walk(root_directory, topdown=False):
        for filename in files:
            file_path = os.path.join(root, filename)

            shutil.move(file_path, os.path.join(root_directory, filename))
            print(f"Moved: {file_path} -> {root_directory}")

        for directory in dirs:
            dir_path = os.path.join(root, directory)
            if not os.listdir(dir_path):  # check if the directory is empty
                os.rmdir(dir_path)
                print(f"Deleted empty directory: {dir_path}")
            move_files_and_cleanup(dir_path)


def remove_comments_and_annotations(func_str):
    """
    Removes single-line comments, multi-line string annotations from a function string.
    
    Args:
        func_str (str): The function code as a string.
        
    Returns:
        str: The function code without comments and annotations.
    """
    # remove single-line comments
    func_str = re.sub(r'#.*', '', func_str)
    
    # remove multi-line docstrings (triple double or single quotes)
    func_str = re.sub(r'"""(.*?)"""', '', func_str, flags=re.DOTALL)
    func_str = re.sub(r"'''(.*?)'''", '', func_str, flags=re.DOTALL)
    
    # remove any excessive empty lines or spaces
    func_str = re.sub(r'\n\s*\n', '\n', func_str).strip()
    
    return func_str

