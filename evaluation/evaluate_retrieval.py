from utils import load_jsonl, extract_box
from collections import defaultdict
import numpy as np
import fire

def get_score(output_path):
    data = load_jsonl(output_path)
    answer = defaultdict(list)
    for item in data:
        box = extract_box(item["generation"])
        length_index = len(item["input"]["nums"])
        if box:
            valid = 1
            generated_answer = eval(box)
            if set(generated_answer) == set(item["output"]):
                score = 1
            else:
                score = 0
        else:
            valid = 0
            score = 0

        item["score"] = score
        item["valid"] = valid
        answer[length_index].append(item)
    
    for k,v in answer.items():
        mean_score = np.mean([item["score"] for item in v])
        print(f"Array length {k}: {mean_score}")

if __name__ == "__main__":
    fire.Fire(get_score)