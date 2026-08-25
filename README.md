# LongReasonArena: A Long Reasoning Benchmark for Large Language Models

LongReasonArena is a benchmark designed to assess the long reasoning capabilities of LLMs, rather than the capabilities of LLMs to comprehend long inputs. Our tasks require models to solve problems by executing multi-step algorithms that reflect key aspects of human reasoning, such as retrieval and backtracking. By controlling the inputs, the required reasoning length can be arbitrarily scaled, reaching up to 1 million tokens of reasoning for the most challenging tasks.

## 🏆 Results

| Model | Reasoning Model | Level 1 | Level 2 | Level 3 |
|--------------------------------|-----------------|---------|---------|---------|
| GPT-5 | ✓ | 84.2 | 48.3 | 27.8 |
| Claude Opus 4.5 | ✓ | 66.1 | 29.1 | 17.6 |
| o3 | ✓ | 65.4 | 36.6 | 22.4 |
| o1 | ✓ | 62.8 | 32.0 | 20.0 |
| Qwen3-32B | ✓ | 56.3 | 20.3 | 13.5 |
| QwQ | ✓ | 56.2 | 20.6 | 13.4 |
| Qwen3-14B | ✓ | 55.6 | 20.0 | 11.4 |
| Claude Sonnet 4.5 | ✓ | 54.3 | 18.9 | 10.9 |
| Qwen3-8B | ✓ | 50.4 | 14.9 | 8.5 |
| Qwen3-4B | ✓ | 47.3 | 13.0 | 8.3 |
| DeepSeek-R1 | ✓ | 42.2 | 16.4 | 9.9 |
| DeepSeek-R1-Distill-Qwen-32B | ✓ | 42.1 | 11.2 | 7.7 |
| GPT-4o | ✗ | 25.0 | 7.3 | 4.3 |
| Llama 3.3 70B Instruct | ✗ | 22.7 | 8.7 | 5.9 |

## 🚀 How to Evaluate Your Own Models

**1. Generate responses using your model.**

```bash
python inference.py --model_path <your_model_path> --difficulty lvl3 --tp_size 8
```
**2. Compute evaluation scores.**

```bash
python -m evaluation.evaluate --input_path outputs/eval_lvl3.jsonl
```

## 📄 How to Generate Data

**1. Generate raw data**

Adjust --repeat_time based on the amount of data you want to generate. The tokenizer is used to compute input lengths:

```bash
python -m generator.unfold
python -m generator.generate_data --tokenizer_path <tokenizer_path> --repeat_time 10
```
**2. Split data into difficulty levels**

Adjust --base_factor depending on how much data you want to keep:

```bash
python -m generator.merge_and_split --base_factor 1
```