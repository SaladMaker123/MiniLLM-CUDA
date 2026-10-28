import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
model_name = "Qwen/Qwen2.5-0.5B-Instruct"

prompt = input("请输入一个问题：")
while not prompt.strip():
    print("输入不能为空，请重新输入。")
    prompt = input("请输入一个问题：")

print("正在加载 Tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
print("正在加载 Qwen2.5 模型...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float16
)

model = model.to("cuda")
model.eval()
messages = [{"role": "user", "content": prompt}]

inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt"
).to("cuda")

with torch.inference_mode():
    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        do_sample=False
    )

input_length = inputs["input_ids"].shape[1]
new_token_ids = outputs[0, input_length:]

last_token_id = outputs[0, -1].item()

print(f"最后一个 Token ID：{last_token_id}")
print(f"最后一个 Token 内容：{tokenizer.convert_ids_to_tokens(last_token_id)}")
print(f"模型 EOS Token ID：{model.generation_config.eos_token_id}")

response = tokenizer.decode(
    new_token_ids,
    skip_special_tokens=True
)

print(f"模型设备：{model.device}")
print(f"输入 Token 数：{input_length}")
print(f"生成 Token 数：{len(new_token_ids)}")
print(f"模型回答：{response}")
