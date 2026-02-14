# 钉钉机器人控制插件 (增强版)

通过钉钉私聊或群聊@机器人来控制 OpenCode。

## 功能
- 接收钉钉消息（私聊/群聊@机器人）
- 任务队列处理
- 多代理协作执行任务
- 执行 shell 命令
- 文件操作
- 智能对话
- **Token 自动缓存和刷新**
- **Markdown 富文本消息支持**
- **图片/文件上传**
- **增强的错误处理和重试机制**

## 配置
在 `config.json` 中设置钉钉应用凭证：
```json
{
  "CLIENT_ID": "your_app_key",
  "CLIENT_SECRET": "your_app_secret",
  "AUTHORIZED_USERS": ["user_id_1", "user_id_2"],
  "QUEUE_DIR": "/path/to/queue"
}
```

## 使用
```bash
# 启动完整服务
python3 start.py

# 或分别启动
python3 src/gateway.py    # 消息网关
python3 src/processor.py  # 任务处理器
```

## 钉钉命令
- 直接发消息 - 智能对话
- `列出文件` - 列出目录
- `查看 <文件>` - 读取文件
- `执行 <命令>` - 运行命令
- `状态` - 系统状态
- `帮助` - 显示帮助

## 新增功能
- **自动 Markdown 检测**: 消息中包含 Markdown 格式时自动使用富文本显示
- **Token 缓存**: 自动管理 Access Token，减少 API 调用
- **错误重试**: 失败的请求会自动重试（最多3次）
- **媒体上传**: 支持上传图片和文件到钉钉
- **详细日志**: 更完善的日志记录，方便调试
