---
license: other
license_name: seallms
license_link: https://huggingface.co/SeaLLMs/SeaLLM-13B-Chat/blob/main/LICENSE
language:
- en
- zh
- id
- vi
- th
- ms
- tl
- ta
- jv
tags:
- sea
- multilingual
---

# *SeaLLMs-v3* - Large Language Models for Southeast Asia


<p align="center">
<a href="https://damo-nlp-sg.github.io/SeaLLMs/" target="_blank" rel="noopener">Website</a>
&nbsp;&nbsp;
<a href="https://huggingface.co/SeaLLMs/SeaLLMs-v3-1.5B-Chat" target="_blank" rel="noopener">Model</a>
&nbsp;&nbsp;
<a href="https://huggingface.co/spaces/SeaLLMs/SeaLLM-Chat" target="_blank" rel="noopener"> 🤗 DEMO</a>
&nbsp;&nbsp;
<a href="https://github.com/DAMO-NLP-SG/SeaLLMs" target="_blank" rel="noopener">Github</a>
&nbsp;&nbsp;
<a href="https://arxiv.org/pdf/2407.19672" target="_blank" rel="noopener">[NEW] Technical Report</a>
</p>

We introduce **SeaLLMs-v3**, the latest series of the SeaLLMs (Large Language Models for Southeast Asian languages) family. It achieves state-of-the-art performance among models with similar sizes, excelling across a diverse array of tasks such as world knowledge, mathematical reasoning, translation, and instruction following. In the meantime, it was specifically enhanced to be more trustworthy, exhibiting reduced hallucination and providing safe responses, particularly in queries closed related to Southeast Asian culture.

## 🔥 Highlights
- State-of-the-art performance compared to open-source models of similar sizes, evaluated across various dimensions such as human exam questions, instruction-following, mathematics, and translation.
- Significantly enhanced instruction-following capability, especially in multi-turn settings.
- Ensures safety in usage with significantly reduced instances of hallucination and sensitivity to local contexts.

## Uses

SeaLLMs is tailored for handling a wide range of languages spoken in the SEA region, including English, Chinese, Indonesian, Vietnamese, Thai, Tagalog, Malay, Burmese, Khmer, Lao, Tamil, and Javanese.

This page introduces the **SeaLLMs-v3-1.5B-Chat** model, specifically fine-tuned to follow human instructions effectively for task completion, making it directly applicable to your applications.

You may also refer to the [SeaLLMs-v3-7B-Chat](https://huggingface.co/SeaLLMs/SeaLLM3-7B-Chat) model for enhanced performance, although it requires higher computational resources.


### Get started with `Transformers`

To quickly try the model, we show how to conduct inference with `transformers` below. Make sure you have installed the latest transformers version (>4.40).

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained(
  "SeaLLMs/SeaLLMs-v3-1.5B-Chat",
  torch_dtype=torch.bfloat16, 
  device_map=device
)
tokenizer = AutoTokenizer.from_pretrained("SeaLLMs/SeaLLMs-v3-1.5B-Chat")

# prepare messages to model
prompt = "Hiii How are you?"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
model_inputs = tokenizer([text], return_tensors="pt").to(device)
print(f"Formatted text:\n {text}")
print(f"Model input:\n {model_inputs}")

generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512, do_sample=True)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

print(f"Response:\n {response[0]}")
```

You can also utilize the following code snippet, which uses the streamer `TextStreamer` to enable the model to continue conversing with you:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import TextStreamer

device = "cuda" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained(
  "SeaLLMs/SeaLLMs-v3-1.5B-Chat",
  torch_dtype=torch.bfloat16, 
  device_map=device
)
tokenizer = AutoTokenizer.from_pretrained("SeaLLMs/SeaLLMs-v3-1.5B-Chat")

# prepare messages to model
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

while True:
    prompt = input("User:")
    messages.append({"role": "user", "content": prompt})
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512, streamer=streamer)
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    messages.append({"role": "assistant", "content": response})
```

### Inference with `vllm`

You can also conduct inference with [vllm](https://docs.vllm.ai/en/stable/index.html), which is a fast and easy-to-use library for LLM inference and serving. To use vllm, first install the latest version via `pip install vllm`.

```python
from vllm import LLM, SamplingParams

prompts = [
    "Who is the president of US?",
    "Can you speak Indonesian?"
]

llm = LLM(ckpt_path, dtype="bfloat16")
sparams = SamplingParams(temperature=0.1, max_tokens=512)
outputs = llm.generate(prompts, sparams)

# print out the model response
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt}\nResponse: {generated_text}\n\n")
```

### Bias, Risks, and Limitations
<blockquote style="color:red">
<p><strong style="color: red">Terms of Use and License</strong>: 
By using our released weights, codes, and demos, you agree to and comply with the terms and conditions specified in our <a href="https://huggingface.co/SeaLLMs/SeaLLM-Chat-13b/edit/main/LICENSE" target="_blank" rel="noopener">SeaLLMs Terms Of Use</a>.
</blockquote>

> **Disclaimer**:
> We must note that even though the weights, codes, and demos are released in an open manner, similar to other pre-trained language models, and despite our best efforts in red teaming and safety fine-tuning and enforcement, our models come with potential risks, including but not limited to inaccurate, misleading or potentially harmful generation.
> Developers and stakeholders should perform their own red teaming and provide related security measures before deployment, and they must abide by and comply with local governance and regulations.
> In no event shall the authors be held liable for any claim, damages, or other liability arising from the use of the released weights, codes, or demos.


## Evaluation

We briefly compare SeaLLMs-v3-1.5B-Chat with models of similar sizes with the M3Exam benchmark.

[M3Exam](https://arxiv.org/abs/2306.05179) consists of local exam questions collected from each country. It reflects the model's world knowledge (e.g., with language or social science subjects) and reasoning abilities (e.g., with mathematics or natural science subjects).

| Model                    | en   | zh   | id   | th   | vi   | avg  | avg_sea |
|--------------------------|------|------|------|------|------|------|---------|
| gemma-2b-it              | 44.1 | 37.4 | 31.5 | 28.2 | 35.8 | 35.4 | 31.8    |
| Sailor-1.8B-Chat         | 43.8 | 35.9 | 34.2 | 32.3 | 37.5 | 36.7 | 34.7    |
| Sailor-4B-Chat           | 54.1 | 48.1 | 40.7 | 35.6 | 42.5 | 44.2 | 39.6    |
| Qwen2-1.5B-Instruct      | 63.4 | 75.3 | 41.2 | 41.2 | 47.2 | 53.7 | 43.2    |
| **SeaLLMs-v3-1.5B-Chat** | 61.9 | 74.2 | 43.2 | 42.4 | 48.7 | 54.1 | 44.7    |



## Acknowledgement to Our Linguists
We would like to express our special thanks to our professional and native linguists, Tantong Champaiboon, Nguyen Ngoc Yen Nhi and Tara Devina Putri, who helped build, evaluate, and fact-check our sampled pretraining and SFT dataset as well as evaluating our models across different aspects, especially safety.


## Citation

If you find our project useful, we hope you would kindly star our repo and cite our work as follows: 
```
@article{damonlp2024seallm3,
  author = {Wenxuan Zhang*, Hou Pong Chan*, Yiran Zhao*, Mahani Aljunied*,
            Jianyu Wang*, Chaoqun Liu, Yue Deng, Zhiqiang Hu, Weiwen Xu,
            Yew Ken Chia, Xin Li, Lidong Bing},
  title = {SeaLLMs 3: Open Foundation and Chat Multilingual Large Language Models for Southeast Asian Languages},
  year = {2024},
  url = {https://arxiv.org/abs/2407.19672}
}
```
Corresponding Author: l.bing@alibaba-inc.com