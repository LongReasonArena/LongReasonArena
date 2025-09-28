import random
from utils import write_jsonl
import string
from itertools import pairwise
from tqdm import tqdm
from copy import deepcopy
import fire

random.seed(42)

def generate_random_word(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def generate_grid(n, word, width=5):
    max_depth = len(word)

    layer_limits = [width for _ in range(max_depth)]
    layer_limits[-1] = 1

    grid = [[0] * n for _ in range(n)]
    visited = [[False] * n for _ in range(n)]
    layer_counts = [0] * max_depth
    curr_layer = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for _ in range(layer_limits[0]):
        start_x, start_y = random.randint(0, n-1), random.randint(0, n-1)
        grid[start_x][start_y] = 1
        visited[start_x][start_y] = True
        layer_counts[0] += 1
        curr_layer.append((start_x, start_y))

    for depth in range(1, max_depth):
        next_layer = []
        random.shuffle(curr_layer)

        for x, y in curr_layer:
            if layer_counts[depth] >= layer_limits[depth]:
                break

            random.shuffle(directions)
            for dx, dy in directions:
                if layer_counts[depth] >= layer_limits[depth]:
                    break
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                    visited[nx][ny] = True
                    grid[nx][ny] = depth + 1
                    layer_counts[depth] += 1
                    next_layer.append((nx, ny))

        curr_layer = next_layer

    alphabet = list(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - set(word))
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                grid[i][j] = word[grid[i][j] - 1]
            else:
                grid[i][j] = random.choice(alphabet)

    return grid

def generate_data(word_length_list=[5,7,10,12,15,17,20],repeat_time=50):
    output = []
    for _ in range(repeat_time):
        base_word = generate_random_word(max(word_length_list))
        for word_length in word_length_list:
            random_word = base_word[:word_length]
            random_grid = generate_grid(20, random_word)

            output.append({
                "problem": "Given an m x n grid of characters board and a string word, return the list of positions that form the word in order if word exists in the grid. If the word does not exist, return an empty list.\nThe word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.",
                "input": {
                    "board": random_grid,
                    "word": random_word,
                },
            })

    write_jsonl("outputs/backtracking.jsonl", output)

if __name__ == "__main__":
    fire.Fire(generate_data)