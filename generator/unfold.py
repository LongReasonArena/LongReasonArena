from utils import load_jsonl
import os

import_text = """from typing import *

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
"""

if __name__ == "__main__":
    os.makedirs("solution/", exist_ok=True)
    data = load_jsonl("data/problems.jsonl")
    for item in data:
        with open(f"solution/Solution{item["idx"]}.py", "w") as file:
            # Replace 'class Solution' with 'class Solution<idx>'
            origin = import_text+ '\n' + item["code"]
            split = origin.splitlines()
            for i in range(len(split)):
                if "import" in split[i]:
                    split[i] = split[i] + " # pragma: no cover"
            output = '\n'.join(split)
            file.write(output)