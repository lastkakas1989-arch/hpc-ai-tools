#!/bin/bash
# HPC/AI每日自动化脚本

set -e

echo "🚀 HPC/AI每日自动化任务启动"
echo "============================="

# 设置工作目录
WORKSPACE="/Users/attaxu/.openclaw/workspace"
PROJECT_DIR="$WORKSPACE/python_projects/hpc_ai_tools"
TWEETS_DIR="$WORKSPACE/tweets"
LOGS_DIR="$WORKSPACE/logs"
OUTPUT_DIR="$PROJECT_DIR/output"

# 创建目录
mkdir -p "$TWEETS_DIR" "$LOGS_DIR" "$OUTPUT_DIR"

# 日志文件
LOG_FILE="$LOGS_DIR/hpc_ai_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "📅 日期: $(date)"
echo "📁 项目目录: $PROJECT_DIR"
echo "📝 日志文件: $LOG_FILE"

# 1. 激活conda环境
echo "🔧 步骤1: 激活conda环境..."
source "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
conda activate hpc-ai

if [ $? -ne 0 ]; then
    echo "❌ Conda环境激活失败"
    exit 1
fi
echo "✅ Conda环境已激活: hpc-ai"

# 2. 生成内容
echo "📝 步骤2: 生成HPC/AI内容..."
cd "$PROJECT_DIR"
python src/main.py generate

if [ $? -ne 0 ]; then
    echo "❌ 内容生成失败"
    exit 1
fi
echo "✅ 内容生成成功"

# 3. 复制内容到tweets目录
echo "📋 步骤3: 复制内容文件..."
LATEST_MORNING=$(ls -t "$OUTPUT_DIR"/*morning.txt | head -1)
LATEST_AFTERNOON=$(ls -t "$OUTPUT_DIR"/*afternoon.txt | head -1)

if [ -f "$LATEST_MORNING" ]; then
    cp "$LATEST_MORNING" "$TWEETS_DIR/$(date +%Y%m%d)_morning.txt"
    echo "✅ 上午内容已复制: $TWEETS_DIR/$(date +%Y%m%d)_morning.txt"
fi

if [ -f "$LATEST_AFTERNOON" ]; then
    cp "$LATEST_AFTERNOON" "$TWEETS_DIR/$(date +%Y%m%d)_afternoon.txt"
    echo "✅ 下午内容已复制: $TWEETS_DIR/$(date +%Y%m%d)_afternoon.txt"
fi

# 4. 发送Telegram通知
echo "📱 步骤4: 发送通知..."
MORNING_CONTENT=$(cat "$LATEST_MORNING" 2>/dev/null || echo "无内容")
AFTERNOON_CONTENT=$(cat "$LATEST_AFTERNOON" 2>/dev/null || echo "无内容")

# 创建通知消息
NOTIFICATION="📅 HPC/AI每日内容已生成

🌅 上午推文：
$MORNING_CONTENT

🌇 下午推文：
$AFTERNOON_CONTENT

📁 文件位置：
$TWEETS_DIR/$(date +%Y%m%d)_*.txt

⏰ 生成时间：$(date)"

echo "$NOTIFICATION" > "$TWEETS_DIR/notification_$(date +%Y%m%d_%H%M%S).txt"
echo "✅ 通知已保存到文件"

# 5. 清理旧文件（保留最近7天）
echo "🧹 步骤5: 清理旧文件..."
find "$OUTPUT_DIR" -name "*.txt" -mtime +7 -delete
find "$TWEETS_DIR" -name "*.txt" -mtime +7 -delete
find "$LOGS_DIR" -name "*.log" -mtime +30 -delete
echo "✅ 旧文件清理完成"

# 6. 生成报告
echo "📊 步骤6: 生成执行报告..."
REPORT_FILE="$LOGS_DIR/report_$(date +%Y%m%d).md"
cat > "$REPORT_FILE" << EOF
# HPC/AI每日自动化报告 - $(date +%Y-%m-%d)

## 执行状态
- **时间**: $(date)
- **状态**: ✅ 成功
- **环境**: hpc-ai (Python 3.11.14)

## 生成内容
### 上午推文
\`\`\`
$MORNING_CONTENT
\`\`\`

### 下午推文
\`\`\`
$AFTERNOON_CONTENT
\`\`\`

## 文件位置
- 内容文件: $TWEETS_DIR/$(date +%Y%m%d)_*.txt
- 日志文件: $LOG_FILE
- 报告文件: $REPORT_FILE

## 系统状态
- Conda环境: 正常
- 内容生成: 正常
- 文件管理: 正常
- 通知系统: 就绪

## 下一步
1. 手动发布推文到X
2. 检查内容质量
3. 如有需要，调整内容模板

---
*生成时间: $(date)*
EOF

echo "✅ 报告已生成: $REPORT_FILE"

echo ""
echo "🎉 HPC/AI每日自动化任务完成！"
echo "============================="
echo "📋 生成的内容已保存到:"
echo "   - $TWEETS_DIR/$(date +%Y%m%d)_morning.txt"
echo "   - $TWEETS_DIR/$(date +%Y%m%d)_afternoon.txt"
echo ""
echo "📱 请手动发布推文到X平台"
echo "🔄 系统将在明天自动运行"