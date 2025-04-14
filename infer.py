# -*- encoding: utf-8 -*-
'''
@File    :   infer.py
@Time    :   2025/04/11
@Author  :   Yansong Du 
@Contact :   dys24@mails.tsinghua.edu.cn
'''

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel

from peft import LoraConfig, TaskType

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    inference_mode=True, # 
    r=64, # Lora 秩
    lora_alpha=16, # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.1# Dropout 比例
)
model_path = './qwen/Qwen2___5-1___5B-Instruct'
lora_path = 'output/Qwen2.5-1.5b/checkpoint-24/'

# 加载tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 加载模型
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto",torch_dtype=torch.bfloat16)

# 加载lora权重
model = PeftModel.from_pretrained(model, model_id=lora_path, config=config)

prompt = "无线光通信的原理是什么？"
messages = [
    {"role": "system", "content": "你是一个无线光通信领域的专家，请根据给出的无线光通信专业领域内的问题回答相关的内容"},
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

#model_inputs = tokenizer([text], return_tensors="pt").to('cuda')
model_inputs = tokenizer(
    [text],
    return_tensors="pt",
    padding=True,
    truncation=True
).to('cuda')

if model_inputs.get('attention_mask', None) is None:
    model_inputs['attention_mask'] = (model_inputs.input_ids != tokenizer.pad_token_id).long()

'''
generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512
)
'''

generated_ids = model.generate(
    input_ids=model_inputs.input_ids,
    attention_mask=model_inputs.attention_mask,
    max_new_tokens=512
)

generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print("-------------------------------------------------------------")
print("question:")
print(prompt)
print("-------------------------------------------------------------")
print("response:")
print(response)
print("-------------------------------------------------------------")