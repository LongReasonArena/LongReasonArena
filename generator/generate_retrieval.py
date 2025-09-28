import random
from utils import write_jsonl
import fire

random.seed(42)

def generate_sample(pos, array_size, value_range=10 ** 9):
    max_val = value_range // 2
    min_val = -1 * max_val
    def get_num():
        return random.randint(min_val, max_val)
    
    target = get_num()

    nums = []

    while len(nums) < array_size:
        new_num = get_num()
        if target - new_num in nums or new_num in nums:
            continue
        nums.append(new_num)
    
    nums[pos[1]] = target - nums[pos[0]]

    return {
        "nums": nums,
        "target": target
    }

def solution(nums, target):
    d = {}
    for i, x in enumerate(nums):
        if (y := target - x) in d:
            return [d[y], i]
        d[x] = i

def generate_data(array_size_list = [40,100,200,400,1000], repeat_time = 20):
    value_range_list = [10 ** 5, 10 ** 6, 10 ** 7,10 ** 8, 10 ** 9]
    pos_dict = {array_size: [random.sample(range(array_size), 2) for _ in range(repeat_time)] 
                for array_size in array_size_list}
    output = []
    for array_size in array_size_list:
        for value_range in value_range_list:
            for i in range(repeat_time):
                random_input = generate_sample(pos_dict[array_size][i], array_size, value_range)
                answer = solution(**random_input)
                assert set(pos_dict[array_size][i]) == set(answer), str(answer)+'--'+str(pos_dict[array_size][i])
                output.append({
                    "problem": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\nYou can return the answer in any order.",
                    "input": random_input,
                    "output": answer,
                })

    write_jsonl("outputs/retrieval.jsonl", output)

if __name__ == "__main__":
    fire.Fire(generate_data)