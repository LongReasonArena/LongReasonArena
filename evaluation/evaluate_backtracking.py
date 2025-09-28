from utils import load_jsonl, extract_box
from collections import defaultdict
import numpy as np
import fire

def get_score(output_path):
    data = load_jsonl(output_path)
    answer = defaultdict(list)
    for item in data:
        box = extract_box(item["generation"])
        board = item["input"]["board"]
        word = item["input"]["word"]
        score = 1
        valid = 0
        if box:
            path = eval(box)

            if len(word) == len(path):
                valid = 1
                for i in range(len(path)):
                    x,y = path[i]
                    if board[x][y] != word[i]:
                        score = 0
                        break
            else:
                score = 0
        else:
            score = 0
        item["score"] = score
        item["valid"] = valid
        answer[len(word)].append(item)
    
    for k,v in answer.items():
        mean_score = np.mean([item["score"] for item in v])
        print(f"Word length {k}: {mean_score}")

if __name__ == "__main__":
    fire.Fire(get_score)