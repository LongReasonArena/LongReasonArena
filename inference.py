import utils
import re
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
import sys
import fire

def infer(model_path, difficulty, output_path=None, reasoning=True, tp_size=8):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    llm = LLM(model=model_path, tensor_parallel_size=tp_size)
    if reasoning:
        max_tokens = 32000
    else:
        max_tokens = 8000
    sampling_params = SamplingParams(temperature=0.6, 
                                     top_p=0.95,
                                     top_k=20,
                                     max_tokens=max_tokens)

    input_list = utils.load_jsonl(f"data/{difficulty}.jsonl")

    prompt_list = []
    for item in input_list:
        prompt=f"""Solve the given problem based on the given inputs.
Don't just reply with code. You should calculate the final answer step by step. Put your final answer within \\boxed{{}}.
Problem:
{item["problem"]}

Inputs:
{item["input"]}"""
        if reasoning:
            messages = [{"role": "user", "content": prompt}]
        else:
            system = "You are a helpful assistant."
            messages = [{"role": "system", "content": system},
                        {"role": "user", "content": prompt}]
            
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=reasoning
        )
        prompt_list.append(text)

    output_list = []
    outputs = llm.generate(prompt_list, sampling_params)
    for i in range(len(outputs)):
        output_list.append(input_list[i].copy())
        output_list[-1]["generation"] = outputs[i].outputs[0].text

    if output_path is None:
        utils.write_jsonl(f"outputs/eval_{difficulty}.jsonl", output_list)
    else:
        utils.write_jsonl(output_path, output_list)

if __name__ == "__main__":
    fire.Fire(infer)