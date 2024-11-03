## Jetbrains AI Code Completion Internship Report

> Generate a dataset of code completion examples from one of your own repositories. You can take a few files from your personal projects.

As repository, I decided to choose a solution of a test task about code completion I did 6 months ago. You can access this repository [here](https://github.com/PioneerAlexander/Improving-LLMs-on-underrepresented-programming-languages?tab=readme-ov-file). This repository is well-structured, as it has a lot of separate modules. For the purpose of this task, I implemented some preprocessing functions to delete all unrelevant files (init.py files and non-py files: configs, markdown and text files). 

> Write a script that would split them into three parts simulating the user cursor position: the prefix - code before the cursor, the suffix - code after the cursor, and the middle - code that is missing and we assume should be typed next. You should aim to obtain between 20 and 50 examples.

For this task, I splitted not the full code but some part of it. 
