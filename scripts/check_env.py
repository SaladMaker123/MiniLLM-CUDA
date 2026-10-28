
import sys
import shutil
import subprocess

import numpy
import torch
import transformers

print("=== MiniLLM-CUDA Environment Check ===")

print(f"Python: {sys.version.split()[0]}")
print(f"Python Path: {sys.executable}")
print(f"NumPy: {numpy.__version__}")
print(f"Transformers: {transformers.__version__}")
print(f"PyTorch: {torch.__version__}")
print(f"PyTorch CUDA: {torch.version.cuda}")

nvcc_path = shutil.which("nvcc")

if nvcc_path is None:
    raise RuntimeError("NVCC was not found!")

nvcc_result = subprocess.run(
    [nvcc_path, "--version"],
    capture_output=True,
    text=True,
    check=True
)

print(f"NVCC: {nvcc_result.stdout.strip().splitlines()[-1]}")

if not torch.cuda.is_available():
    raise RuntimeError("CUDA is not available!")

print(f"GPU: {torch.cuda.get_device_name(0)}")

a = torch.tensor([1.0, 2.0, 3.0], device="cuda")
b = a * 2

torch.cuda.synchronize()

expected = torch.tensor([2.0, 4.0, 6.0], device="cuda")

if not torch.equal(b, expected):
    raise RuntimeError("GPU computation failed!")

print(f"GPU Calculation Result: {b}")

print("Environment check passed!")
