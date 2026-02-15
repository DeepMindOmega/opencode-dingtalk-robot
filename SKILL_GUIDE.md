---
name: opencode-dingtalk-integration
description: 通过钉钉机器人远程控制和与OpenCode交互，支持私聊和群聊
license: MIT
compatibility: opencode
metadata:
  integration: dingtalk
  type: remote-control
  category: automation
---

## 功能概述

这个技能提供了一个完整的钉钉机器人集成方案，让您可以通过钉钉私聊或群聊与OpenCode进行交互。

### 主要功能

- 🖥️  **远程控制**: 通过钉钉私聊或群聊@机器人控制OpenCode
- 💬 **智能对话**: 发送任何消息给OpenCode，获取AI智能回复
- 📝 **任务执行**: 在钉钉中直接执行shell命令
- 📄 **文件操作**: 查看和读取文件
- 🎨 **Markdown支持**: 自动识别和发送Markdown格式消息
- 🖼️ **图片支持**: 支持图片上传和发送
- 🔄 **会话记忆**: 保持上下文对话历史
- 💾 **自动保存**: 会话状态持久化

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/DeepMindOmega/opencode-dingtalk-robot.git
cd opencode-dingtalk-robot
```

### 2. 配置钉钉应用

访问 [钉钉开放平台](https://open-dev.dingtalk.com/) 并：

1. 创建企业内部应用
2. 获取 `AppKey` 和 `AppSecret`
3. 配置机器人权限：
   - 接收群消息
   - 发送消息
4. 发布机器人

### 3. 配置插件

```bash
# 复制配置模板
cp config.example.json config.local.json

# 编辑配置
vi config.local.json
```

`config.local.json` 内容：

```json
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
```

### 4. 启动服务

```bash
# 启动完整服务
./start.sh

# 或分别启动
python3 src/gateway.py    # 消息网关
python3 src/processor.py  # 任务处理器
```

### 5. 添加机器人到钉钉

在钉钉中：
- **私聊**: 搜索并添加机器人
- **群聊**: 在群设置中添加机器人

## 使用方法

### 基本对话

直接发送消息：

```
你好，帮我写一个Python函数来读取文件
```

### 快捷命令

- `列出文件` - 查看当前目录
- `查看 <文件名>` - 读取文件内容
- `执行 <命令>` - 运行shell命令
- `状态` - 查看系统状态
- `帮助` - 显示帮助信息
- `新对话` - 清除上下文，开始新对话

### 示例

**代码编写**:
```
写一个REST API的Python Flask应用
```

**文件操作**:
```
查看 main.py
执行 cat README.md
```

**调试帮助**:
```
我的代码报错了，错误信息是：...
```

## 架构说明

### 组件

1. **Gateway (gateway.py)**
   - WebSocket连接钉钉服务
   - 接收和发送消息
   - 管理任务队列
   - Token自动刷新

2. **Processor (processor.py)**
   - 处理队列中的任务
   - 调用OpenCode CLI
   - 返回结果到队列
   - 会话管理

3. **Queue Manager (queue_manager.py)**
   - 任务队列存储
   - 结果队列存储
   - 并发安全

4. **Session Manager (session_manager.py)**
   - 会话ID管理
   - 上下文保持
   - 数据持久化

### 工作流程

```
钉钉消息 → Gateway → 队列 → Processor → OpenCode CLI → 返回结果 → 队列 → Gateway → 钉钉回复
```

## 配置选项

| 配置项 | 说明 | 必需 |
|--------|------|------|
| CLIENT_ID | 钉钉AppKey | 是 |
| CLIENT_SECRET | 钉钉AppSecret | 是 |
| AUTHORIZED_USERS | 允许的用户ID列表 | 是 |
| QUEUE_DIR | 队列文件目录 | 是 |
| OPENCODE_BIN | OpenCode CLI路径 | 否 |
| OPENCODE_DATA_DIR | OpenCode数据目录 | 否 |

## 获取用户ID

在钉钉中：
1. 在群聊中@机器人
2. 查看日志输出（logs/gateway.log）
3. 日志中会显示 `user_id`

或使用调试命令：
```bash
python3 -c "
import dingtalk_stream
# 调试模式下会显示详细信息
"
```

## 安全注意事项

1. **保护密钥**: `config.local.json` 已添加到 `.gitignore`，不会提交到Git
2. **限制用户**: 只在 `AUTHORIZED_USERS` 中添加信任的用户
3. **定期更新**: 定期更换AppSecret
4. **日志审计**: 定期检查 `logs/` 目录，不要提交到Git

## 故障排查

### 机器人无响应

```bash
# 检查服务状态
./status.sh

# 查看日志
tail -f logs/gateway.log
tail -f logs/processor.log
```

### 连接失败

1. 验证CLIENT_ID和CLIENT_SECRET
2. 检查网络连接
3. 确认机器人状态为"已发布"
4. 检查权限配置

### OpenCode调用失败

1. 确认OpenCode已正确安装
2. 验证 `OPENCODE_BIN` 路径
3. 检查OpenCode CLI可执行权限

## 性能优化

- Token缓存：减少API调用，5分钟刷新缓冲
- 心跳监控：自动重连，最长60s无响应触发
- 任务队列：异步处理，不阻塞消息接收
- 错误重试：指数退避策略，最多3次重试

## 文件结构

```
opencode-dingtalk-robot/
├── src/
│   ├── gateway.py         # 消息网关
│   ├── processor.py       # 任务处理器
│   ├── queue_manager.py   # 队列管理
│   └── session_manager.py # 会话管理
├── logs/                # 日志目录
├── queue/               # 队列文件
├── media/               # 图片临时存储
├── config.example.json   # 配置模板
├── start.sh            # 启动脚本
├── stop.sh             # 停止脚本
└── status.sh           # 状态脚本
```

## 更新日志

### v1.0.1 (2026-02-15)
- 优化错误处理（添加try-catch）
- 改进路径配置（支持自定义OpenCode路径）
- 改进日志输出
- 修复session_manager中的异常处理
- 添加config.example.json新选项

### v1.0 (2026-02-14)
- 初始发布
- 完整的OpenCode集成
- 支持私聊和群聊
- Markdown和图片支持
- Token自动缓存

## 许可证

MIT License - 详见 [LICENSE](https://github.com/DeepMindOmega/opencode-dingtalk-robot/blob/main/LICENSE)

## 支持和反馈

- 提交Issue: https://github.com/DeepMindOmega/opencode-dingtalk-robot/issues
- 文档: https://github.com/DeepMindOmega/opencode-dingtalk-robot/blob/main/README.md

---

**享受通过钉钉控制OpenCode的便利！** 🎉
