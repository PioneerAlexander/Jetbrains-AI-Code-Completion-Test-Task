"""
This script splits the python files into three parts simulating the cursor position.
"""
import os
import random
from typing import List, Dict

from code_preprocess_utils import remove_comments_and_annotations

def split_python_files(directory, context_length, num_splits=4) -> List[Dict]:
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

            if len(lines) > context_length:
                split_points = []
                for _ in range(num_splits):
                    # For the large enough files, we trim the prefix and suffix, such that they can be fed to a model 
                    split_point = random.randint(0, len(lines) - context_length)
                    if split_point not in split_points:
                        middle_length = 2
                        
                        prefix_length = context_length // 2
                        middle = '\n'.join(lines[split_point + prefix_length:split_point + prefix_length + middle_length])
                        prefix = '\n'.join(lines[split_point:split_point + prefix_length])
                        suffix = '\n'.join(lines[split_point+prefix_length+middle_length:split_point+context_length])

                        split_files.append({"prefix": prefix, "middle": middle, "suffix": suffix})
                        split_points.append(split_point) # ensure no occasional duplications
            else:
                split_point = len(lines) // 2

                middle_length = 2
                        
                middle = '\n'.join(lines[split_point:split_point + middle_length])
                prefix = '\n'.join(lines[:split_point])
                suffix = '\n'.join(lines[split_point + middle_length:])

                split_files.append({"prefix": prefix, "middle": middle, "suffix": suffix})

    return split_files
