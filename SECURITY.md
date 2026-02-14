# 安全配置指南

本机器人需要配置钉钉开发者凭证才能运行。

## 配置步骤

1. 复制配置模板
   ```bash
   cp config.example.json config.local.json
   ```

2. 编辑 config.local.json
   使用你的钉钉机器人凭证填写以下字段：
   
   ```json
   {
     "CLIENT_ID": "your_dingtalk_app_key",
     "CLIENT_SECRET": "your_dingtalk_app_secret",
     "WEBHOOK_URL": "your_webhook_url"
   }
   ```

3. 获取凭证
   - 登录钉钉开放平台: https://open-dev.dingtalk.com/
   - 创建或选择你的机器人应用
   - 在"凭证与基础信息"页面获取 Client ID 和 Client Secret
   - 在"机器人"页面配置机器人的消息接收地址

## 安全注意事项

- **永远不要提交** `config.local.json` 到 git
- **永远不要分享**你的 Client Secret
- 定期轮换访问凭证
- 配置适当的IP白名单

## 环境变量（可选）

也可以通过环境变量设置凭证（优先级高于配置文件）：

```bash
export DINGTALK_CLIENT_ID="your_app_key"
export DINGTALK_CLIENT_SECRET="your_app_secret"
```

## 更多信息

- 钉钉开放平台文档: https://open.dingtalk.com/document/
- 机器人开发指南: https://open.dingtalk.com/document/robots/intro
