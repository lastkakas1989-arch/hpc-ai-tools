#!/bin/bash
# 每日运行脚本

set -e

echo "🚀 启动HPC/AI每日内容生成与发布系统"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 进入项目目录
cd "$(dirname "$0")/.."

# 激活虚拟环境（如果使用）
if command -v pyenv &> /dev/null; then
    echo "🐍 激活虚拟环境..."
    pyenv activate hpc-ai-tools 2>/dev/null || true
fi

# 检查依赖
echo "📦 检查Python依赖..."
python -c "import sys; print(f'Python版本: {sys.version}')"

# 生成内容
echo ""
echo "🎯 生成今日HPC/AI内容..."
python src/main.py generate

# 发布内容（模拟模式）
echo ""
echo "📤 发布内容（模拟模式）..."
python src/main.py post --mock

# 或者使用真实模式（需要配置API）
# python src/main.py post --real

echo ""
echo "✅ 每日任务完成!"
echo "日志文件: logs/hpc_ai_tools_$(date '+%Y%m%d').log"
echo "输出文件: output/$(date '+%Y%m%d')_*.txt"