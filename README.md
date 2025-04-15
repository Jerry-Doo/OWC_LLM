@Time    :   2025/04/11
@Author  :   Yansong Du 
@Contact :   dys24@mails.tsinghua.edu.cn


# Env Setup
```
conda create -n qwen25_ins python=3.10
conda activate qwen25_ins
pip install transformers==4.44.2
pip install sentencepiece==0.2.0
pip install accelerate==0.34.2
pip install datasets==2.20.0
pip install peft==0.11.1
pip install swanlab
```

# Preparation
```
Get the key on [swanlab](https://swanlab.cn/) first
```
# please input your key to login
swanlab login #https://swanlab.cn/


# Lora ft and infer
```
python qwen25_1-5B_lora_OWC.py > output.log 2>&1 & # When using multi-GPU setups in the lab environment, + CUDA_VISIBLE_DEVICES=0
python infer.py # When using multi-GPU setups in the lab environment, + CUDA_VISIBLE_DEVICES=0
```
# load website
```
python chat_backend.py
python web_chat.py  # change another cmd to take this step
```

# demo output

![demooutput](./assets/demo_output.png)

# Acknowledgments
We would like to thank the contributors to the [datawhale's self-llm](https://github.com/datawhalechina/self-llm) for their open research and exploration.