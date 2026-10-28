
#!/usr/bin/env bash

set -euo pipefail

# ==================================================
# MiniLLM-CUDA Cloud Environment Setup
# ==================================================

# 获取项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_DIR"

# 允许自定义虚拟环境目录
# 默认使用项目根目录下的 .venv
VENV_DIR="${MINILLM_VENV_DIR:-$PROJECT_DIR/.venv}"

# 要求使用绝对路径，避免操作错误的目录
if [[ "$VENV_DIR" != /* ]]; then
    echo "Error: MINILLM_VENV_DIR must be an absolute path."
    exit 1
fi

echo "=========================================="
echo " MiniLLM-CUDA Cloud Environment Setup"
echo "=========================================="
echo "Project directory: $PROJECT_DIR"
echo "Virtual environment: $VENV_DIR"

# ==================================================
# Step 1: Check development tools
# ==================================================

echo "[1/5] Checking development tools..."

command -v python3 >/dev/null || {
    echo "Error: Python 3 is not installed."
    exit 1
}

command -v nvcc >/dev/null || {
    echo "Error: CUDA Toolkit with nvcc is required."
    exit 1
}

python3 --version
nvcc --version

# ==================================================
# Step 2: Prepare Python virtual environment
# ==================================================

echo "[2/5] Preparing Python virtual environment..."

if [[ ! -x "$VENV_DIR/bin/python" ]] || \
   ! "$VENV_DIR/bin/python" -m pip --version >/dev/null 2>&1; then

    echo "Creating Python virtual environment..."

    if ! python3 -m venv "$VENV_DIR"; then

        if [[ "$(id -u)" -ne 0 ]]; then
            echo "Error: Python venv support is missing."
            echo "Root permissions are required to install it."
            exit 1
        fi

        echo "Installing Python venv support..."

        apt-get update
        apt-get install -y python3.10-venv

        python3 -m venv "$VENV_DIR"
    fi

else
    echo "Existing Python virtual environment detected."
fi

# 使用目标虚拟环境的 Python
PYTHON="$VENV_DIR/bin/python"

echo "Python environment: $PYTHON"

# ==================================================
# Step 3: Install CUDA PyTorch
# ==================================================

echo "[3/5] Installing CUDA PyTorch..."

"$PYTHON" -m pip install --no-cache-dir \
    "torch==2.10.0" \
    --index-url https://download.pytorch.org/whl/cu126

# ==================================================
# Step 4: Install project dependencies
# ==================================================

echo "[4/5] Installing project dependencies..."

"$PYTHON" -m pip install --no-cache-dir \
    -r "$PROJECT_DIR/requirements-cloud.txt"

# ==================================================
# Step 5: Validate installed dependencies
# ==================================================

echo "[5/5] Checking installed dependencies..."

"$PYTHON" -m pip check

echo "=========================================="
echo " Cloud Python environment setup complete!"
echo "=========================================="
echo "Virtual environment: $VENV_DIR"
