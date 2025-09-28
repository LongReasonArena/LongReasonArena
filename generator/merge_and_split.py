import os
from utils import load_jsonl, write_jsonl, extract_code, timeout_decorator
from collections import defaultdict, Counter
from random import sample
import numpy as np
import sys
from tqdm import tqdm
import fire

sys.set_int_max_str_digits(100000)

def stratified_sample(data, base_factor):
    core_tags = set(["BFS", "DFS", "Backtracking"])
    sampled_list = []
    tags_list = []
    for value in data.values():
        tags = set(value[0]["tags"])
        tags_list.extend(value[0]["tags"])
        if tags & core_tags:
            factor = 10 * base_factor
        elif "DP" in tags:
            factor = 2 * base_factor
        else:
            factor = base_factor
        if len(value) >= factor:
            sampled_list.extend(sample(value, factor))
        else:
            sampled_list.extend(value)
    return sampled_list

def merge(base_factor=1): 
    folder_path = "outputs/"

    data = []
    print("Loading Data...")
    for filename in tqdm(os.listdir(folder_path)):
        if "data_" in filename:
            file_path = os.path.join(folder_path, filename)
            temp = load_jsonl(file_path)
            data.extend(temp)

    origin = load_jsonl("data/problems.jsonl")
    problem_guess = {}
    for item in origin:
        guess_code = extract_code(item["guess_func"])
        # avoid stuck in recursion
        if guess_code and guess_code.count("guess(") <= 2:
            problem_guess[item["problem"]] = guess_code

    lvl1_dict = defaultdict(list)
    lvl2_dict = defaultdict(list)
    lvl3_dict = defaultdict(list)
    input_dict = defaultdict(list)
    filtered = []
    for item in data:
        if item["input"] not in input_dict[item["problem"]]:
            input_dict[item["problem"]].append(item["input"])
        else:
            continue

        if item["input_len"] <= 32000:
            if item["problem"] in problem_guess:
                try:
                    exec(problem_guess[item["problem"]])
                    guess = timeout_decorator(timeout=1)(guess)
                    guess_answer = guess(**item["input"])
                    if guess_answer == item["output"]:
                        item["guess_func"] = problem_guess[item["problem"]]
                        filtered.append(item)
                        continue
                except Exception as e:
                    pass
            
            if item["line"] >= 100 and item["line"] < 10 ** 4:
                lvl1_dict[item["problem"]].append(item)
            elif item["line"] >= 10 ** 4 and item["line"] < 10 ** 5:
                lvl2_dict[item["problem"]].append(item)
            elif item["line"] >= 10 ** 5 and item["line"] < 10 ** 6:
                lvl3_dict[item["problem"]].append(item)

    lvl1_dict_filter = {k:v for k,v in lvl1_dict.items() if k in lvl3_dict}
    lvl2_dict_filter = {k:v for k,v in lvl2_dict.items() if k in lvl3_dict}

    lvl1 = stratified_sample(lvl1_dict_filter, base_factor)
    lvl2 = stratified_sample(lvl2_dict_filter, base_factor)
    lvl3 = stratified_sample(lvl3_dict, 1)
    print(f"""Level 1:
    Number of problems: {len(lvl1_dict_filter)}
    Number of samples: {len(lvl1)}""")
    print(f"""Level 2:
    Number of problems: {len(lvl2_dict_filter)}
    Number of samples: {len(lvl2)}""")
    print(f"""Level 3:
    Number of problems: {len(lvl3_dict)}
    Number of samples: {len(lvl3)}""")
    write_jsonl(f"outputs/lvl1.jsonl", lvl1)
    write_jsonl(f"outputs/lvl2.jsonl", lvl2)
    write_jsonl(f"outputs/lvl3.jsonl", lvl3)

if __name__ == "__main__":
    fire.Fire(merge)