#!/usr/bin/env python3
import json
import subprocess
import os
import sys
sys.path.insert(0, "/home/admin/.opencode/skills/dingtalk-robot/src")

from queue_manager import QueueManager

CONFIG_PATH = "/home/admin/.opencode/skills/dingtalk-robot/config.json"
with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

qm = QueueManager(CONFIG["QUEUE_DIR"])
OPENCODE_BIN = "/home/admin/.npm-global/bin/opencode"

def run_opencode(message):
    try:
        cmd = [OPENCODE_BIN, "run", message]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd="/home/admin")
        if result.stdout:
            return result.stdout.strip()
        return "OpenCode 执行完成"
    except Exception as e:
        return "错误: " + str(e)

def process_task(task):
    msg = task.get("message", "")
    print("Processing: " + msg)
    response = run_opencode(msg)
    qm.complete_task(tid, response)
    qm.add_result(tid, task["user_id"], response)
    return response

def main():
    print("OpenCode processor starting...")
    processed = set()
    while True:
        try:
            tasks = qm.get_pending_tasks()
            for tid, task in tasks.items():
                if tid in processed:
                    continue
                response = process_task(task)
                processed.add(tid)
                print("Done: " + tid)
        except Exception as e:
            print("Error: " + str(e))
        time.sleep(2)

if __name__ == "__main__":
    main()
