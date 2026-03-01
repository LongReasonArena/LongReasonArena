# LongReasonArena: A Long Reasoning Benchmark for Large Language Models

LongReasonArena is a benchmark designed to assess the long reasoning capabilities of LLMs, rather than the capabilities of LLMs to comprehend long inputs. Our tasks require models to solve problems by executing multi-step algorithms that reflect key aspects of human reasoning, such as retrieval and backtracking. By controlling the inputs, the required reasoning length can be arbitrarily scaled, reaching up to 1 million tokens of reasoning for the most challenging tasks.

## 🏆 Results

| Model | Reasoning Model | Level 1 | Level 2 | Level 3 |
|--------------------------------|-----------------|---------|---------|---------|
| GPT-5 | ✓ | 81.5 | 41.8 | 26.4 |
| o1 | ✓ | 59.3 | 29.6 | 16.4 |
| Qwen3-32B | ✓ | 49.4 | 19.3 | 11.3 |
| QwQ | ✓ | 49.4 | 20.4 | 10.7 |
| Qwen3-14B | ✓ | 50.4 | 16.9 | 8.6 |
| Claude 3.7 Sonnet | ✓ | 44.2 | 15.5 | 7.8 |
| DeepSeek-R1 | ✓ | 40.1 | 15.7 | 7.5 |
| DeepSeek-R1-Distill-Qwen-32B | ✓ | 38.5 | 13.9 | 7.5 |
| Qwen3-8B | ✓ | 43.2 | 16.3 | 7.1 |
| Qwen3-4B | ✓ | 42.4 | 13.4 | 6.7 |
| QwQ-preview | ✓ | 29.0 | 8.9 | 3.6 |
| DeepSeek-R1-Distill-Qwen-14B | ✓ | 32.7 | 9.8 | 3.3 |
| GPT-4o | ✗ | 23.0 | 5.7 | 2.1 |
| Qwen2.5-72B | ✗ | 20.6 | 5.2 | 2.1 |
| DeepSeek-R1-Distill-Qwen-7B | ✓ | 16.3 | 3.3 | 1.9 |
| Llama 3.1 70B | ✗ | 12.8 | 3.3 | 1.2 |
| DeepSeek-R1-Distill-Qwen-1.5B | ✓ | 1.0 | 0.3 | 0.0 |

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