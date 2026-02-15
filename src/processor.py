#!/usr/bin/env python3
import json
import subprocess
import os
import sys
import time
from datetime import datetime
from pathlib import Path

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)
from queue_manager import QueueManager
from session_manager import SessionManager

CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.local.json")
if not os.path.exists(CONFIG_PATH):
    CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

try:
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    print(f"错误: 找不到配置文件 {CONFIG_PATH}")
    sys.exit(1)

qm = QueueManager(CONFIG["QUEUE_DIR"])
sm = SessionManager(os.path.join(CONFIG_DIR, "sessions.json"))
OPENCODE_BIN = CONFIG.get("OPENCODE_BIN", "/home/admin/.npm-global/bin/opencode")

print(f"配置文件: {CONFIG_PATH}")
print(f"OpenCode路径: {OPENCODE_BIN}")


def run_opencode(message, continue_session=False, images=None, timeout=120):
    opencode_dir = CONFIG.get("OPENCODE_DATA_DIR", "/home/admin/.local/share/opencode")
    screenshots_before = set()

    if os.path.exists(opencode_dir):
        for root, dirs, files in os.walk(opencode_dir):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    screenshots_before.add(os.path.join(root, file))

    try:
        cmd = [OPENCODE_BIN, "run", message, "--format", "json"]
        if continue_session:
            cmd.append("--continue")
        if images:
            for img_path in images:
                if os.path.exists(img_path):
                    cmd.extend(["--file", img_path])
                    print(f"    → 附加文件: {img_path}")
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd="/home/admin"
        )
        output = result.stdout if result.stdout else ""
        error = result.stderr if result.stderr else ""

        if error:
            print(f"    → OpenCode 错误输出: {error[:200]}")

        screenshots_after = set()
        if os.path.exists(opencode_dir):
            for root, dirs, files in os.walk(opencode_dir):
                for file in files:
                    if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                        screenshots_after.add(os.path.join(root, file))

        generated_images = list(screenshots_after - screenshots_before)

        if not output and not generated_images:
            return "OpenCode 执行完成（无输出）", None, generated_images

        lines = output.strip().split("\n")
        response_text = []
        extracted_session_id = None

        for line in lines:
            try:
                data = json.loads(line)
                if data.get("type") == "text":
                    response_text.append(data.get("part", {}).get("text", ""))
                if "sessionID" in data:
                    extracted_session_id = data["sessionID"]
            except json.JSONDecodeError:
                pass

        response = "\n".join(response_text) if response_text else "无输出"
        return response, extracted_session_id, generated_images
    except subprocess.TimeoutExpired:
        return f"命令超时 ({timeout}s)", None, []
    except FileNotFoundError:
        return f"错误: 找不到 OpenCode: {OPENCODE_BIN}", None, []
    except Exception as e:
        return f"执行异常: {str(e)}", None, []


def execute_shell(cmd, timeout=30, cwd="/home/admin"):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd
        )
        output = result.stdout + result.stderr
        return output[:2000] if output else "(无输出)"
    except subprocess.TimeoutExpired:
        return "命令超时 (" + str(timeout) + "s)"
    except Exception as e:
        return "执行错误: " + str(e)


def process_task(task):
    msg = task.get("message", "").strip()
    user_id = task.get("user_id", "")
    user_nick = task.get("user_nick", "用户")
    conv_id = task.get("conv_id", "")
    conv_type = task.get("conv_type", "1")
    images = task.get("images", [])
    msg_lower = msg.lower()
    parts = msg.split()
    first_word = parts[0] if parts else ""

    if msg in ["新对话", "new", "reset"]:
        new_session = sm.create_new_session(user_id, conv_id, conv_type)
        return "✅ 已创建新对话，之前的上下文已清除", []

    if first_word in ["私聊", "发私信", "发私聊", "dm"] and len(parts) > 1:
        target_user = parts[1].strip("@")
        target_msg = " ".join(parts[2:]) if len(parts) > 2 else "你好"

        if target_user:
            return f"[私聊:{target_user}] {target_msg}", []
        else:
            return "❌ 请指定要发送私聊的用户，例如：私聊 @用户ID 你好", []

    if (
        any(k in msg for k in ["列出", "文件列表", "目录"])
        and "文件" not in msg
        or msg_lower == "ls"
    ):
        return "📁 目录文件:\n```\n" + execute_shell("ls -la") + "\n```", []

    if first_word in ["查看", "读取", "cat"] and len(parts) > 1:
        filename = parts[-1].strip("'\"")
        filepath = "/home/admin/" + filename
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(2000)
            return "📄 " + filename + ":\n\n" + content, []
        return "❌ 文件不存在: " + filename, []

    if first_word in ["执行", "运行"] and len(parts) > 1:
        cmd = " ".join(parts[1:])
        return "🔧 " + cmd + "\n```\n" + execute_shell(cmd) + "\n```", []

    if msg in ["状态", "status", "/status"]:
        return "📊 系统状态\n⏰ " + str(datetime.now()) + "\n📂 /home/admin", []

    if msg in ["帮助", "help", "/help"]:
        return (
            """🤖 OpenCode 助手

📝 可用指令:
• 直接发送任意指令 - OpenCode 会执行并回复（带上下文记忆）
• 新对话 - 清除上下文，开启新对话
• 列出目录 - 查看文件
• 查看 <文件> - 读取文件
• 执行 <命令> - 运行命令
• 状态 - 系统信息
• 帮助 - 显示帮助

💬 每个对话会自动记忆上下文！
📷 支持发送和接收图片！""",
            [],
        )

    continue_session = sm.should_continue_session(user_id, conv_id, conv_type)

    opencode_msg = msg

    valid_images = None
    if images:
        print(f"  → 附加 {len(images)} 张图片")
        valid_images = [img for img in images if os.path.exists(img)]
        if valid_images:
            opencode_msg = msg
            for img_path in valid_images:
                opencode_msg += f"\n[已附加图片: {img_path}]"
        else:
            opencode_msg = msg + "\n[无法读取图片文件]"

    print("  → 转发给 OpenCode: " + opencode_msg[:50] + "...")
    print("  → 继续会话: " + ("是" if continue_session else "否"))
    response, new_session_id, generated_images = run_opencode(
        opencode_msg,
        continue_session=continue_session,
        images=valid_images if valid_images else None,
    )

    if new_session_id:
        print("  → 新会话 ID: " + new_session_id)
        sm.update_session_id(user_id, conv_id, conv_type, new_session_id)

    if generated_images:
        print(f"  → 生成图片: {len(generated_images)} 张")
        for img in generated_images:
            print(f"      - {img}")

    if len(response) > 5000:
        response = response[:5000] + "\n\n...(输出过长，已截断)"

    return response, generated_images


def main():
    print("[" + str(datetime.now()) + "] 钉钉任务处理器启动 (OpenCode 集成版)")
    print("队列目录: " + CONFIG["QUEUE_DIR"])
    print("OpenCode 路径: " + OPENCODE_BIN)
    processed = set()

    while True:
        try:
            tasks = qm.get_pending_tasks()
            for tid, task in tasks.items():
                if tid in processed:
                    continue

                print("\n[" + datetime.now().strftime("%H:%M:%S") + "] 处理: " + tid)
                print("  用户: " + task.get("user_nick"))
                print("  消息: " + task.get("message"))

                response, images = process_task(task)
                print("  回复长度: " + str(len(response)) + " 字符")

                qm.complete_task(tid, response)
                qm.add_result(
                    tid,
                    task["user_id"],
                    response,
                    task.get("conv_id", ""),
                    task.get("conv_type", "1"),
                    images,
                )
                processed.add(tid)
                print("  ✓ 完成")
        except Exception as e:
            print("错误: " + str(e))
            import traceback

            traceback.print_exc()

        time.sleep(2)


if __name__ == "__main__":
    main()
