#!/usr/bin/env python3
from ollama import chat
from ollama import ChatResponse
import subprocess
import os

HOME_DIR = os.path.expanduser("~")
current_dir = HOME_DIR  

def run_command(command):
    global current_dir

    try:
        if command.startswith("cd "):
            path = command.split("cd ", 1)[1].strip()
            new_path = os.path.abspath(os.path.join(current_dir, os.path.expanduser(path)))

            if os.path.isdir(new_path):
                current_dir = new_path
                print(f"📂 Changed directory to: {current_dir}")
            else:
                print(f"❌ Error: No such directory: {new_path}")
            return

        # ตรวจสอบคำสั่งอันตราย
        dangerous_cmds = ["rm -rf", "dd if=", ":(){ :|:& };:", "mkfs", "chmod 777 /", "mv /"]
        if any(danger in command for danger in dangerous_cmds):
            print("⚠️  Command blocked for safety reasons!")
            return

        process = subprocess.Popen(command, shell=True, cwd=current_dir,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in process.stdout:
            print(line, end="")

        error = process.stderr.read().strip()
        if error:
            print("❌ Error:\n", error)

    except Exception as e:
        print("🚨 Execution failed:", str(e))

def get_ai_response(text):
    response: ChatResponse = chat(model='linux-helper', messages=[
        {'role': 'user', 'content': text}
    ])
    print(response.message.content)
    return response.message.content

def main():
    try:
        while True:
            text = str(input("user: ")).strip()

            if text.lower() in ['exit', 'quit']:
                print("👋 Exiting the program...")
                break

            command = get_ai_response(text)
            run_command(command)

    except KeyboardInterrupt:
        print("\n🚪 Program interrupted. Exiting...")
        
if __name__ == "__main__":
    main()