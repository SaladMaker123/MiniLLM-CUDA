# MiniLLM-CUDA 云 GPU 环境部署指南

## 1. 文档目的

本文档说明如何在兼容的 Vast.ai Linux 云 GPU 实例上，自动部署 MiniLLM-CUDA 项目开发环境。

项目使用 CUDA C++、PyTorch 和 Hugging Face Transformers，运行 Qwen2.5-0.5B-Instruct，并在后续集成自定义 CUDA Kernel。

GitHub 仓库：

https://github.com/SaladMaker123/MiniLLM-CUDA

## 2. 已验证的环境

| 组件 | 已验证配置 |
|---|---|
| GPU | NVIDIA GeForce RTX 3090 24GB |
| 操作系统 | Ubuntu 22.04 容器 |
| CPU 架构 | x86_64 |
| Docker 镜像 | `nvidia/cuda:12.6.3-devel-ubuntu22.04` |
| CUDA Toolkit | 12.6 |
| Python | 3.10.12 |
| PyTorch | 2.10.0+cu126 |
| Transformers | 5.20.2 |
| NumPy | 2.2.6 |

以上是已验证的参考环境，不代表其他 GPU 或系统版本一定不兼容。

当前自动安装脚本主要针对 Ubuntu 22.04、Python 3.10 与 CUDA 12.6 开发环境设计。

## 3. 部署前提

新的云实例应具备：

- 可用的 NVIDIA CUDA GPU 和兼容驱动。
- 包含 `nvcc` 的 CUDA 开发环境。
- Python 3.10。
- Git。
- 可用的网络连接。
- 足够的磁盘空间，建议至少 40–50 GB。
- 必要时具有安装系统软件包的权限。

宿主机 NVIDIA 驱动、GPU 分配和性能分析权限由云平台提供，不由项目安装脚本管理。

## 4. 克隆项目

连接 Vast.ai Linux 实例后：

```bash
cd /root
git clone https://github.com/SaladMaker123/MiniLLM-CUDA.git
cd MiniLLM-CUDA
```

公开仓库可以通过 HTTPS 克隆。

如果需要从云端向 GitHub 推送代码，必须另外配置具有写入权限的 GitHub 认证，例如专用 SSH Deploy Key。

不要将 SSH 私钥或访问令牌上传到仓库。

## 5. 自动安装开发环境

在项目根目录执行：

```bash
bash scripts/setup_cloud.sh
```

脚本将：

1. 检查 Python 及 NVCC。
2. 创建或复用 `.venv` Python 虚拟环境。
3. 在支持的 Ubuntu 环境中，必要时安装 Python venv 组件。
4. 从 CUDA 12.6 对应的 PyTorch 软件包仓库安装 PyTorch。
5. 安装 `requirements-cloud.txt` 中的项目依赖。
6. 使用 `pip check` 检查依赖一致性。

默认虚拟环境路径：

```text
/root/MiniLLM-CUDA/.venv
```

脚本不会自动安装宿主机 GPU 驱动。

## 6. 验证 GPU 环境

安装完成后执行：

```bash
.venv/bin/python scripts/check_env.py
```

该程序检查：

- Python 版本与解释器路径。
- NumPy、Transformers、PyTorch 版本。
- PyTorch CUDA 版本。
- NVCC 是否存在。
- CUDA GPU 是否可用。
- GPU Tensor 计算是否正确。

成功时会显示：

```text
Environment check passed!
```

## 7. 运行 Qwen2.5 推理

执行：

```bash
.venv/bin/python inference/generate.py
```

输入一个问题，例如：

```text
请用一句话解释GPU的作用。
```

程序将加载 Qwen2.5-0.5B-Instruct，执行 CUDA 推理并生成回答。

首次加载可能需要从 Hugging Face 下载 Tokenizer、模型配置与模型权重，需要网络连接。

模型文件通常使用 Hugging Face 缓存，不属于 Python 依赖清单的一部分。

## 8. 使用独立测试环境

可以通过环境变量指定其他虚拟环境目录。

例如：

```bash
MINILLM_VENV_DIR="$PWD/.venv-test" bash scripts/setup_cloud.sh
```

使用该环境进行验证：

```bash
.venv-test/bin/python scripts/check_env.py
```

运行模型：

```bash
.venv-test/bin/python inference/generate.py
```

这种方式可以测试新的 Python 依赖环境，而不直接操作原来的 `.venv`。

## 9. 环境依赖文件说明

`requirements-cloud.txt`

记录项目主动要求安装的主要 Python 依赖。

`requirements-cloud.snapshot.txt`

由以下命令生成：

```bash
.venv/bin/python -m pip freeze > requirements-cloud.snapshot.txt
```

记录参考环境中全部已安装的软件包及版本。

完整快照用于版本排查和复现参考，并不意味着每次部署都应直接安装快照中的全部依赖。

GPU 版 PyTorch 由安装脚本单独指定版本及 CUDA 软件包索引。

## 10. 已完成的测试

当前已经验证：

- 原始环境可正常运行。
- 自动安装脚本可在已有环境执行。
- 可以自动创建新的 `.venv-test` 环境。
- 新环境能够正常使用 PyTorch CUDA。
- 新环境能够运行 Qwen2.5 推理。
- 重复运行安装脚本后，依赖检查正常。
- 重复安装后 GPU Tensor 计算正常。

目前测试是在同一台 RTX 3090 云实例中进行的，复用了相同的 CUDA 开发镜像及可能已有的模型缓存。

**尚未验证在另一台全新 Vast.ai 实例上的完整恢复流程。**

## 11. 云实例删除与代码安全

删除 Vast.ai 实例前：

1. 将所有重要代码提交并推送到 GitHub。
2. 保存必要的性能测试结果和工程数据。
3. 确认是否需要备份未提交的本地文件。
4. 确认模型文件是否需要重新下载。
5. 删除实例后，在 GitHub 中撤销该实例对应的 Deploy Key。

Python 虚拟环境、下载缓存与临时文件不应该直接提交到 GitHub。

新实例启动后，可重新克隆项目并运行自动部署脚本。

## 12. 已知限制

- 当前脚本主要面向固定的 CUDA 12.6 / Python 3.10 环境。
- 它不负责安装宿主机 NVIDIA 驱动。
- 不保证所有 GPU 架构和操作系统版本都兼容。
- 不保证云平台开放 Nsight Compute 硬件性能计数器权限。
- PyTorch 和模型下载仍可能受到网络条件影响。
- 完整跨实例部署尚待实际验证。

后续应根据实际需求继续完善部署兼容性与错误处理。