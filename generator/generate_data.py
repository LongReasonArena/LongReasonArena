from utils import load_jsonl, write_jsonl, timeout_decorator
from tqdm import tqdm
import ast
from time import perf_counter
import tracemalloc
import linecache
from transformers import AutoTokenizer
import fire

import numpy as np
from typing import *

from string import *
from re import *
from datetime import *
from collections import *
from heapq import *
from bisect import *
from copy import *
from math import *
from random import *
from statistics import *
from itertools import *
from functools import *
from operator import *
from io import *
from sys import *
from json import *
from builtins import *

import string
import re
import datetime
import collections
import heapq
import bisect
import copy
import math
import random
import statistics
import itertools
import functools
import operator
import io
import sys
import json

sys.setrecursionlimit(10000)
sys.set_int_max_str_digits(100000)

def extract_code_blocks(markdown_text):
    pattern = r"```python\n(.*?)```"
    code_blocks = re.findall(pattern, markdown_text, re.DOTALL)
    for code in reversed(code_blocks):
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "generate":
                    return ast.unparse(node) # Python 3.9+
        except SyntaxError:
            continue

    return None

def get_params_num(class_code):
    tree = ast.parse(class_code)
    
    class_node = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    
    main_func_node = next(
        node for node in class_node.body if isinstance(node, ast.FunctionDef) and node.name == "_main"
    )
    
    param_names = [arg.arg for arg in main_func_node.args.args if arg.arg != "self"]    
    return len(param_names)

def get_missing_lines(file_path, line_numbers):
    lines = {}
    with open(file_path, 'r') as file:
        for i, line in enumerate(file, start=1):
            if i in line_numbers and not ("class" in line or "def" in line):
                lines[i] = line.strip()
    return lines

def convert_to_serializable(obj):
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_to_serializable(item) for item in obj)
    elif isinstance(obj, np.ndarray):
        return convert_to_serializable(obj.tolist())
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    else:
        return obj

def reformat_input(class_code, input):
    tree = ast.parse(class_code)
    
    class_node = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    
    main_func_node = next(
        node for node in class_node.body if isinstance(node, ast.FunctionDef) and node.name == "_main"
    )
    
    param_names = [arg.arg for arg in main_func_node.args.args if arg.arg != "self"]
    if len(param_names) == len(input):
        output = {k:v for k,v in zip(param_names, input)}
    else:
        output = None
    return convert_to_serializable(output)

class CodeProfiler:
    def __init__(self):
        self.line_count = 1

    def trace_calls(self, frame, event, arg):
        if event == "line":
            self.line_count += 1
        
        return self.trace_calls

    def start(self):
        sys.settrace(self.trace_calls)

    def stop(self):
        sys.settrace(None)

def get_info(solution, input):
    profiler = CodeProfiler()
    
    kwargs = deepcopy(input)
    
    profiler.start()
    result = solution._main(*kwargs)
    profiler.stop()
    line_count = profiler.line_count
    return line_count

def generate_data(tokenizer_path, repeat_time = 10, timeout_thres = 3, parallel_idx = 42):
    seed(int(parallel_idx))
    data = load_jsonl("data/problems.jsonl")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    
    output_list = []
    for item in tqdm(data):
        idx = item["idx"]
        params_num = get_params_num(item["code"])
        exec(f"from solution.Solution{idx} import Solution", globals())

        for _ in range(repeat_time):
            try:
                # print(extract_code_blocks(item["generate_func"]))
                exec(extract_code_blocks(item["generate_func"]), globals())
                wrapped_generate = timeout_decorator(timeout=timeout_thres)(generate)
                random_input = wrapped_generate()
                if params_num == 1:
                    random_input = (random_input, )

                solution = Solution()
                temp_input = deepcopy(random_input)
                solution._main = timeout_decorator(timeout=timeout_thres)(solution._main)
                result = solution._main(*temp_input)
                
                solution = Solution()
                input_new = reformat_input(item["code"], random_input)
                input_len = len(tokenizer.encode(str(input_new)))
                
                # DON'T use idx as key. Some indexes correspond same problem.
                line_count = get_info(solution, random_input)
                output_list.append({
                    "problem": item["problem"],
                    "tags": item["tags"],
                    "input": input_new,
                    "output": result,
                    "input_len": input_len,
                    "line": line_count,
                })
            except Exception as e:
                print("Error in generate_data:", e)
                print("#"*10)

    data_len = len(data) * repeat_time
    print(f"Used Ratio: {len(output_list)}/{data_len} = {(len(output_list))/data_len:.2f}")

    print("Sample Num", len(output_list))
    write_jsonl(f"outputs/data_{parallel_idx}.jsonl", output_list)

if __name__ == "__main__":
    fire.Fire(generate_data)