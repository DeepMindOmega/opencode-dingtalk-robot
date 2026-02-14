#!/usr/bin/env python3
import json
import subprocess
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from queue_manager import QueueManager

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__))), "config.json"
with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

qm = QueueManager(CONFIG["QUEUE_DIR"])
OPENCODE_BIN = "/home/admin/.npm-global/bin/opencode"


def run_opencode(message: str, timeout=120):
    try:
        cmd = [OPENCODE_BIN, "run", message]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="/home/admin"
        )
        output = result.stdout if result.stdout else ""
        error = result.stderr if result.stderr else ""
        if output:
            return output.strip()
        elif error:
            return f"执行错误:\n{error}"
        else:
            return "OpenCode 执行完成（无输出）"
    except subprocess.TimeoutExpired:
        return f"命令超时 ({timeout}s)"
    except FileNotFoundError:
        return f"错误: 找不到 OpenCode: {OPENCODE_BIN}"
    except Exception as e:
        return f"执行异常: {str(e)}"


def execute_shell(cmd, timeout=30, cwd="/home/admin"):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd
        )
        output = result.stdout + result.stderr
        return output[:2000] if output else "(无输出)"
    except subprocess.TimeoutExpired:
        return f"命令超时 ({timeout}s)"
    except Exception as e:
        return f"执行错误: {e}"


def process_task(task):
    msg = task.get("message", "").strip()
    user_nick = task.get("user_nick", "用户")
    msg_lower = msg.lower()
    parts = msg.split()
    first_word = parts[0] if parts else ""

    if (
        any(k in msg for k in ["列出", "文件列表", "目录"])
        and "文件" not in msg
        or msg_lower == "ls"
    ):
        return f"📁 目录文件:\n\`\`\n{execute_shell('ls -la')}\n\`\`\n"

    if first_word in ["查看", "读取", "cat"] and len(parts) > 1:
        filename = parts[-1].strip("'\"")
        filepath = f"/home/admin/{filename}"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(2000)
            return f"📄 {filename}:\n\n{content}"
        return f"❌ 文件不存在: {filename}"

    if first_word in ["执行", "运行"] and len(parts) > 1:
        cmd = " ".join(parts[1:])
        return f"🔧 {cmd}\n\`\`\n{execute_shell(cmd)}\n\`\`\n"

    if msg in ["状态", "status", "/status"]:
        return f"📊 系统状态\n⏰ {datetime.now()}\n📂 /home/admin"

    if msg in ["帮助", "help", "/help"]:
        return """🤖 OpenCode 助手

📝 可用指令:
• 直接发送任意指令 - OpenCode 会执行并回复
• 列出目录 - 查看文件
• 查看 <文件> - 读取文件
• 执行 <命令> - 运行命令
• 状态 - 系统信息
• 帮助 - 显示帮助

💬 直接发送任何消息给 OpenCode 执行！"""

    if "天气" in msg:
        import urllib.request
        try:
            city = (
                msg.replace("天气", "").replace("显示", "").replace("查询", "").strip()
                or "北京"
            )
            url = f"https://wttr.in/{city}?format=3&lang=zh"
            req = urllib.request.Request(url, headers={"User-Agent": "curl"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                weather = resp.read().decode("utf-8").strip()
            return f"🌤️ {weather}"
        except Exception as e:
            return f"天气查询失败: {e}"

    print(f"  → 转发给 OpenCode: {msg[:50]}...")
    response = run_opencode(msg)

    if len(response) > 5000:
        response = response[:5000] + "\n\n...(输出过长，已截断)"

    return response


def main():
    print(f"[{datetime.now()}] 钉钉任务处理器启动 (OpenCode 集成版)")
    print(f"队列目录: {CONFIG['QUEUE_DIR']}")
    print(f"OpenCode 路径: {OPENCODE_BIN}")
    processed = set()

    while True:
        try:
            tasks = qm.get_pending_tasks()
            for tid, task in tasks.items():
                if tid in processed:
                    continue

                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 处理: {tid}")
                print(f"  用户: {task.get('user_nick')}")
                print(f"  消息: {task.get('message')}")

                response = process_task(task)
                print(f"  回复长度: {len(response)} 字符")

                qm.complete_task(tid, response)
                qm.add_result(
                    tid,
                    task["user_id"],
                    response,
                    task.get("conv_id", ""),
                    task.get("conv_type", "1"),
                )

                processed.add(tid)
                print(f"  ✓ 完成")
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()

        time.sleep(2)


if __name__ == "__main__":
    main()
