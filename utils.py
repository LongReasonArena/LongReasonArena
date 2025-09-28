import json
import os
from typing import List
import signal
import re

def load_jsonl(path: str):
    input_list = []
    with open(path, 'r', encoding='utf8') as f:
        lines = f.read().strip().split('\n')
        for line in lines:
            try:
                item = json.loads(line)
                input_list.append(item)
            except Exception as e:
                print(e)
    return input_list

def write_jsonl(path: str, data: List):
    directory = os.path.dirname(path)
    
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            try:
                json_line = json.dumps(item)
                f.write(json_line + "\n")
                f.flush()
            except Exception as e:
                print("Error in write_jsonl:", e)
                print("#"*10)

def timeout_handler(signum, frame):
    raise TimeoutError("Time out!")

def timeout_decorator(timeout):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator

def extract_code(markdown_text):
    pattern = r"```python\n(.*?)```"
    code_blocks = re.findall(pattern, markdown_text, re.DOTALL)
    if code_blocks:
        return code_blocks[-1]
    else:
        return None

def extract_box(text):
    result = []
    start = 0
    pattern = "\\boxed{"
    while True:
        start = text.find(pattern, start)
        if start == -1:
            break
        
        start_content = start + len(pattern)
        bracket_count = 1
        i = start_content
        
        while i < len(text) and bracket_count > 0:
            if text[i] == '{':
                bracket_count += 1
            elif text[i] == '}':
                bracket_count -= 1
            i += 1
        
        if bracket_count == 0:
            result.append(text[start_content:i-1])
        
        start = i
    
    if len(result) > 0:
        return result[-1]
    else:
        return None