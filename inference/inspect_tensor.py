import torch
token_ids = [14990, 38434]
input_ids = torch.tensor([token_ids], dtype=torch.long)
print(f"原始 List：{token_ids}")
print(f"Tensor 内容：{input_ids}")
print(f"Tensor Shape：{input_ids.shape}")
print(f"Tensor Dtype：{input_ids.dtype}")
print(f"Tensor Device：{input_ids.device}")
