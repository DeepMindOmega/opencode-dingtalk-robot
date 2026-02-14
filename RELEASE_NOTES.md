# 发布说明

## v1.0 - 2026-02-15

### 新功能
- ✨ 完整的钉钉机器人集成
- 🖼️ 支持图片发送（上传到钉钉服务器）
- 🔄 OpenCode会话管理
- 📝 自动Markdown格式检测
- 🤖️ 心跳监控和自动重连
- 📊 任务队列管理系统

### 功能特性

#### 核心功能
- **消息接收**: 通过钉钉WebSocket接收消息
- **消息发送**: 支持文本、Markdown、ActionCard
- **图片处理**: 支持发送图片到钉钉群聊和私聊
- **OpenCode集成**: 无缝对接OpenCode AI系统
- **会话管理**: 自动管理多个用户的会话上下文

#### 消息类型
- 普通文本消息
- Markdown格式消息（自动检测）
- ActionCard交互卡片
- 图片消息（支持上传）

#### 系统特性
- Token自动缓存（5分钟刷新缓冲）
- WebSocket连接监控
- 消息自动分割（支持长消息）
- 错误重试机制（指数退避）

### 安装说明

1. **安装依赖**
   ```bash
   pip install dingtalk-stream
   ```

2. **配置机器人**
   ```bash
   cp config.example.json config.local.json
   # 编辑config.local.json，填入钉钉凭证
   ```

3. **启动服务**
   ```bash
   bash start.sh
   ```

4. **配置Webhook**
   在钉钉开发者后台配置消息接收地址

### 安全说明

- 配置文件`config.local.json`包含敏感信息，不会提交到git
- 查看`SECURITY.md`了解详细的安全配置步骤

### 文档

- `README.md` - 快速开始指南
- `QUICKSTART.md` - 详细安装步骤
- `SECURITY.md` - 安全配置指南
- `SKILL.md` - 技能说明

### 测试

- ✅ 图片发送测试通过
- ✅ 文本消息测试通过
- ✅ OpenCode集成测试通过
- ✅ WebSocket连接测试通过
