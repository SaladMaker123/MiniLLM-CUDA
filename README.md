# MiniLLM-CUDA

基于 CUDA C++ 的轻量级大语言模型推理与算子优化系统。

## 项目目标

基于 Qwen2.5-0.5B-Instruct 和 PyTorch，构建一个能够实际执行文本生成的轻量级推理系统，并将自定义 CUDA C++ 算子集成到真实模型的计算路径中。

## 技术栈

- CUDA C++
- C++
- Python
- PyTorch
- Hugging Face Transformers

## 开发计划

- [ ] V0.1：基础模型推理
- [ ] V0.2：自定义 Token 生成循环与 KV Cache
- [ ] V0.3：CUDA C++ RMSNorm 算子
- [ ] V0.4：自定义算子接入 Qwen2.5
- [ ] V1.0：性能优化、Benchmark 和工程完善

## 当前状态

项目初始化阶段。