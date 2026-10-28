import torch
from transformers import AutoTokenizer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 第一步：先创建 prompt 变量
prompt = input("请输入一个问题：")

# 第二步：再检查 prompt 是否为空
while not prompt.strip():
    print("输入不能为空，请重新输入。")
    prompt = input("请输入一个问题：")

# 第三步：输入有效后，开始编码
token_ids = tokenizer.encode(prompt, add_special_tokens=False)

input_ids = torch.tensor([token_ids], dtype=torch.long)

print(f"原始文本：{prompt}")
print(f"Token ID 列表：{token_ids}")
print(f"模型输入 Tensor：{input_ids}")
print(f"Tensor Shape：{input_ids.shape}")
print(f"Tensor Dtype：{input_ids.dtype}")
print(f"Tensor Device：{input_ids.device}")