from transformers import AutoTokenizer
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
prompt = input("请输入一个问题：")
token_ids = tokenizer.encode(prompt, add_special_tokens=False)
tokens = tokenizer.convert_ids_to_tokens(token_ids)
decoded_text = tokenizer.decode(token_ids)
print(f"原始文本：{prompt}")
print(f"字符数量：{len(prompt)}")
print(f"Token ID：{token_ids}")
print(f"Token 内容：{tokens}")
print(f"Token 数量：{len(token_ids)}")
print(f"解码结果：{decoded_text}")
