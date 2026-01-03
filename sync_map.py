import time
import os
import requests
import subprocess

# --- 配置区 ---
# 你的游戏地图地址
LOCAL_URL = "http://localhost:8888"
# 多少秒同步一次（建议不要太快，避免游戏卡顿）
INTERVAL = 60 
# --- 配置结束 ---

def save_page():
    try:
        print(f"正在尝试获取 {LOCAL_URL} ...")
        # 1. 下载网页内容
        response = requests.get(LOCAL_URL)
        response.encoding = 'utf-8' # 根据实际情况调整，如果是乱码改成 'gbk'
        
        # 2. 保存为 index.html
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("网页已保存为 index.html")
        return True
    except Exception as e:
        print(f"获取失败 (游戏可能未启动): {e}")
        return False

def git_push():
    try:
        # 3. 执行 Git 命令上传
        print("正在上传到 GitHub...")
        subprocess.run(["git", "add", "."], check=True)
        # 这里的 commit message 使用时间戳
        msg = f"Auto update {time.strftime('%H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", msg], check=False) # 没变化时忽略错误
        subprocess.run(["git", "push"], check=True)
        print(f"上传成功！最后更新时间: {time.strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"Git 上传失败: {e}")

if __name__ == "__main__":
    print("=== 游戏地图自动镜像脚本启动 ===")
    print("功能：即使关闭游戏，GitHub 上也能看到最后一次的状态")
    
    while True:
        if save_page():
            git_push()
        else:
            print("等待游戏启动中...")
        
        print(f"等待 {INTERVAL} 秒后进行下一次同步...\n")
        time.sleep(INTERVAL)