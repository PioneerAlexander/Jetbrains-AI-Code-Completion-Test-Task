"""
This script splits the python files into three parts simulating the cursor position.
"""
import os
import random

from code_preprocess_utils import remove_comments_and_annotations

def split_python_files(directory, num_splits=3) -> list[dict]:
    """
    Splits python files in the given directory into three parts simulating the user cursor position.
    
    Args:
        directory (str): The path to the directory containing the python files.
        num_splits (int, optional): The number of times to split each file. Defaults to 3.
    
    Returns:
        list: A list of tuples containing the prefix, middle, and suffix for each split file.
    """
    split_files = []

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            content = file.read()
            content = remove_comments_and_annotations(content)
            lines = content.split('\n')

            if len(lines) > 110:
                continue

            for _ in range(num_splits):
                # select a split point in the middle of the file to ensure split is reasonable
                split_point = random.randint(len(lines) // 3, len(lines) * 2 // 3)

                # ensure the middle part is one or two lines
                if split_point < len(lines) - 1:
                    middle = '\n'.join(lines[split_point:split_point + 2])
                    prefix = '\n'.join(lines[:split_point])
                    suffix = '\n'.join(lines[split_point + 2:])
                else:
                    middle = lines[split_point - 1]
                    prefix = '\n'.join(lines[:split_point - 1])
                    suffix = ''

                split_files.append({"prefix": prefix, "middle": middle, "suffix": suffix})

    return split_files
