## Jetbrains AI Code Completion Internship Report

> Generate a dataset of code completion examples from one of your own repositories. You can take a few files from your personal projects.

As repository, I decided to choose a solution of a test task about code completion I did 6 months ago. You can access this repository [here](https://github.com/PioneerAlexander/Improving-LLMs-on-underrepresented-programming-languages?tab=readme-ov-file). This repository is well-structured, as it has a lot of separate modules. For the purpose of this task, I implemented some preprocessing functions to delete all unrelevant files (init.py files and non-py files: configs, markdown and text files), removed directory nested structure. From each file, the comments and annotations were deleted, as well as empty lines, before passing to a script which splits a given code snippet. The preprocessing functions can be found in this [module](src/code_preprocess_utils.py).

> Write a script that would split them into three parts simulating the user cursor position: the prefix - code before the cursor, the suffix - code after the cursor, and the middle - code that is missing and we assume should be typed next. You should aim to obtain between 20 and 50 examples.

For this task, I split the code into smaller parts, referred to as "code snippets" in this file, rather than using the entire code at once. This was necessary because using the full code would exceed the model's `max_length` limit. Simply increasing the `max_length` parameter didn’t solve the issue, as it caused a "CUDA out of memory" error.

Due to this memory limitation, I had to limit the input to just 6 lines: 4 lines as the prefix and 2 lines as the suffix. This constraint makes it significantly more challenging for the model to generate accurate code completions.

By using a random cursor split, I created 48 examples from my code. The code for this process can be found in the [script file](src/split_python_files.py).

> Take an open source code completion model, for example tiny_starcoder, or bigger starcoder or codellama variations if you prefer. Run the selected model on the examples from the previous point to obtain its completions.

Initially, I experimented with the tiny-StableCoder model for this fill-in-the-middle task. However, I encountered challenges in selecting the correct prompt format, even though the StarCoder tokenizer included special tokens intended for this purpose (`fim_prefix`, `fim_middle`, `fim_suffix`). Unfortunately, there was no clear documentation on the exact prompt structure required or any information on how the model was specifically trained for fill-in-the-middle tasks—at least, none that I could find before moving on to CodeLlama.

After encountering challenges with the tiny-StableCoder model, I explored CodeLlama to see if it better suited my fill-in-the-middle task. I used [model CodeLlama-7b-hf](https://huggingface.co/codellama/CodeLlama-7b-hf),  which explicitly supports infilling tasks. Moreover, on another official [codellama page](https://ollama.com/library/codellama), even the expected Fill-In-Middle prompt is given:

```
<PRE> {prefix} <SUF>{suffix} <MID>
```

This experience underscored the importance of thoroughly reviewing model documentation to identify those that align with specific tasks before proceeding with experimentation.

When running the model, I set the `max_length` parameter to match the exact size of the code snippet I was attempting to reconstruct. In my experience, allowing large language models to generate many tokens often results in excessive, irrelevant code continuations. To prevent this, I adjusted the generation parameter each time, limiting the length of the output instead of trimming it afterward.

However, this approach introduced an additional challenge: the model frequently generated comments (which were removed from original code during preprocessing). You can see this effect in the [resulting dataset](resulting_dataset.json) file. By restricting the model’s token count, it sometimes couldn’t complete the code as expected due to running out of tokens. When this occurred, I scored the model's output accordingly.

> Review them manually and analyze the differences with actual missing code from the middle, try to assign labels according to your judgment of whether the proposed code is correct.

The `pairs.json` file contains the model completions and the expected completions for the Fill-In-Middle task. I evaluated each model response by score from 0 to 5, where 0 is the worst score and 5 is the best score, and added this score to the `pairs.json` file. Note that the content of this file is the part of a [resulting dataset](resulting_dataset.json) file.


Due to the limited context window, the model's responses often lacked an understanding of the broader project context, leading to certain errors related to this issue. In my evaluation, I avoided penalizing heavily for these context-related mistakes, as well as for missing more complex logic. This choice was motivated by the fact that the metrics I used in the next step don’t account for the broader context; they simply compare variations in the middle code segments.

Inspired by the idea of labeling model outputs based on the given context, I thought it could be interesting to evaluate predictions by assessing which code snippet aligns best with the context. This approach might involve assigning a probability or “odds” score to show how well each prediction fits within the original context. 

> Try to propose some automatic metrics for evaluating the quality of this model. Find which of the proposed metrics correlates better with your own judgment. Try computing at least exact match, chrf, and two or more metrics of your choice.

Proposed automatic metrics: 

* The **BLEU** metric is a popular and natural choice in standard NLP tasks. It is computed based on modified n-gram precision, which measures how closely the generated text matches the reference text in terms of overlapping n-grams.
* The **edit similarity** metric calculates the edit distance between reference and predicted texts, making it a useful metric in code evaluation tasks. For further details, refer to this [table](https://www.researchgate.net/figure/Exact-match-and-edit-similarity-performance-on-CrossCodeEval_tbl1_381152954), where code language models were evaluated using Exact Match and Edit Similarity metrics.

The proposed metrics, including exact match and chrf metrics, are implemented in this [module](src/metrics.py).

As the result, chrf metric correlates the most with my judgment. the results and experiments code can be accessed in the attached [Jupyter Notebook file](src/Jetbrains_AI_Code_Completion_Internship.ipynb).





