# -*- encoding: utf-8 -*-
'''
@File    :   chat_backend.py
@Time    :   2025/04/11
@Author  :   Yansong Du 
@Contact :   dys24@mails.tsinghua.edu.cn
'''

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, LoraConfig, TaskType
from fastapi.middleware.cors import CORSMiddleware
import torch

app = FastAPI()

# 跨域支持（允许网页访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 首页提示
@app.get("/")
def root():
    return {"message": "🌐 Qwen + LoRA API 已就绪，使用 POST /chat 接口发送 {'question': '...'}。"}

# 输入数据结构
class Query(BaseModel):
    question: str

# 模型配置
model_path = "./qwen/Qwen2___5-1___5B-Instruct"
lora_path = "output/Qwen2.5-1.5b/checkpoint-24"

try:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # ✅ 固定加载到 cuda:0，避免 device_map="auto" 分卡导致错误
    base_model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map={"": 0},
        torch_dtype=torch.bfloat16
    )

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        inference_mode=True, r=64, lora_alpha=16, lora_dropout=0.1
    )

    model = PeftModel.from_pretrained(base_model, model_id=lora_path, config=lora_config)
    model = model.to("cuda:0")
    model.eval()
    print("✅ 模型加载完成，服务已就绪。")

except Exception as e:
    print(f"❌ 模型加载失败：{e}")
    raise e

# 对话接口
@app.post("/chat")
def chat(query: Query):
    if not query.question.strip():
        return {"response": "⚠️ 请输入一个有效的问题。"}

    try:
        messages = [
            {"role": "system", "content": "你是一个无线光通信领域的专家，请根据给出的无线光通信专业领域内的问题回答相关的内容"},
            {"role": "user", "content": query.question}
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        # ✅ 保留 BatchEncoding 类型，同时迁移输入张量到 cuda:0
        inputs = tokenizer([text], return_tensors="pt", padding=True)
        inputs = inputs.to("cuda:0")
        inputs["attention_mask"] = (inputs["input_ids"] != tokenizer.pad_token_id).long()

        outputs = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_new_tokens=512
        )
        outputs = outputs[:, inputs.input_ids.shape[1]:]
        response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        return {"response": response}

    except Exception as e:
        return {"response": f"❌ 模型推理失败：{str(e)}"}

if __name__ == "__main__":

   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)