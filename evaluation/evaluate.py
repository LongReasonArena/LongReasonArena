from utils import load_jsonl, extract_code, extract_box
import re
import fire

def replace_boolean_strings(s):
    return re.sub(r'\btrue\b', 'True', re.sub(r'\bfalse\b', 'False', s, flags=re.IGNORECASE))

def extract_answer(text):
    split_text = text.split("</think>")[-1]
    answer = extract_box(split_text)
    if answer:
        matches = re.findall(r"\\text{(.*)}", answer)
        if matches:
            answer = matches[-1]
        return replace_boolean_strings(answer)
    else:
        return None

def is_primitive(value):
    return isinstance(value, (int, float, bool, str, bytes))

def get_score(input_path):
    origin = load_jsonl("data/problems.jsonl")
    problem_compare = {}
    for item in origin:
        problem_compare[item["problem"]] = extract_code(item["compare_func"])

    data = load_jsonl(input_path)
    true = []
    false = []
    invalid = []
    for item in data:
        func_text = problem_compare[item["problem"]]
        exec(func_text)
        answer_text = extract_answer(item["generation"])

        if answer_text:
            try:
                if isinstance(item["output"], str):
                    if answer_text[0] in ['"',"'"] or answer_text[-1] in ['"',"'"]:
                        answer = answer_text[1:-1]
                    else:
                        answer = answer_text
                else:
                    answer = eval(answer_text)
                if is_primitive(item["output"]):
                    equal = (answer == item["output"])
                else:
                    equal = compare(answer,item["output"])
                if equal:
                    true.append(item)
                else:
                    false.append(item)
            except Exception as e:
                false.append(item)
                pass
        else:
            invalid.append(item)
    print("Number of correct answers:", len(true))
    print("Number of wrong answers:", len(false))
    print("Number of formatting errors:", len(invalid))
    print(f"Accuracy: {100 * len(true)/len(data):.3g}")

if __name__ == "__main__":
    fire.Fire(get_score)