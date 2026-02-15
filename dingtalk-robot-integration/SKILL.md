---
name: dingtalk-robot-integration
description: 钉钉机器人集成指南 - 通过钉钉私聊或群聊远程控制OpenCode
license: MIT
compatibility: opencode
metadata:
  type: integration-guide
  category: remote-control
  integration: dingtalk
---

# 钉钉机器人集成 OpenCode

这个技能指南提供了完整的钉钉机器人与OpenCode集成方案，让您可以通过钉钉私聊或群聊远程控制OpenCode。

## 快速开始

### 1. 克隆仓库

\`\`\`bash
git clone https://github.com/DeepMindOmega/opencode-dingtalk-robot.git
cd opencode-dingtalk-robot
\`\`\`

### 2. 配置钉钉应用

访问 [钉钉开放平台](https://open-dev.dingtalk.com/) 并：

1. 创建企业内部应用
2. 获取 \`AppKey\` 和 \`AppSecret\`
3. 配置机器人权限：
   - 接收群消息
   - 发送消息
4. 发布机器人

### 3. 配置插件

\`\`\`bash
# 复制配置模板
cp config.example.json config.local.json

# 编辑配置
vi config.local.json
\`\`\`

\`config.local.json\` 配置示例：

\`\`\`json
{
  "CLIENT_ID": "your_dingtalk_app_key",
  "CLIENT_SECRET": "your_dingtalk_app_secret",
  "AUTHORIZED_USERS": [
    "user_id_1",
    "user_id_2"
  ],
  "QUEUE_DIR": "/path/to/queue",
  "OPENCODE_BIN": "/path/to/opencode",
  "OPENCODE_DATA_DIR": "/path/to/opencode/data"
}
\`\`\`

### 4. 启动服务

\`\`\`bash
# 启动完整服务
./start.sh

# 或分别启动
python3 src/gateway.py    # 消息网关
python3 src/processor.py  # 任务处理器
\`\`\`

### 5. 添加机器人到钉钉

在钉钉中：
- **私聊**: 搜索并添加机器人
- **群聊**: 在群设置中添加机器人

## 主要功能

- 🖥️  **远程控制**: 通过钉钉私聊或群聊@机器人控制OpenCode
- 💬  **智能对话**: 发送任何消息给OpenCode，获取AI智能回复
- 📝  **任务执行**: 在钉钉中直接执行shell命令
- 📄  **文件操作**: 查看和读取文件
- 🎨  **Markdown支持**: 自动识别和发送Markdown格式消息
- 🖼️  **图片支持**: 支持图片上传和发送
- 🔄  **会话记忆**: 保持上下文对话历史
- 💾  **自动保存**: 会话状态持久化

## 使用方法

### 基本对话

直接发送消息：

\`\`\`
你好，帮我写一个Python函数来读取文件
\`\`\`

### 快捷命令

- \`列出文件\` - 查看当前目录
- \`查看 <文件名>\` - 读取文件内容
- \`执行 <命令>\` - 运行shell命令
- \`状态\` - 查看系统状态
- \`帮助\` - 显示帮助信息
- \`新对话\` - 清除上下文，开始新对话

### 示例

**代码编写**:
\`\`\`
写一个REST API的Python Flask应用
\`\`\`

**文件操作**:
\`\`\`
查看 main.py
执行 cat README.md
\`\`\`

**调试帮助**:
\`\`\`
我的代码报错了，错误信息是：...
\`\`\`

## 更多信息

- **GitHub仓库**: https://github.com/DeepMindOmega/opencode-dingtalk-robot
- **完整文档**: [README.md](https://github.com/DeepMindOmega/opencode-dingtalk-robot/blob/main/README.md)
- **快速开始**: [QUICKSTART.md](https://github.com/DeepMindOmega/opencode-dingtalk-robot/blob/main/QUICKSTART.md)

## 许可证

MIT License

---

**享受通过钉钉控制OpenCode的便利！** 🎉
