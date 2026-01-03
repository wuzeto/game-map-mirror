import time
import os
import subprocess
import shutil

# --- 配置区 ---
LOCAL_URL = "http://localhost:8888"
INTERVAL = 60


# --- 配置结束 ---

def mirror_site():
    print(f"[{time.strftime('%H:%M:%S')}] 开始克隆网页...")

    # 1. 清理旧文件（防止旧文件干扰，但保留 .git 目录和脚本自己）
    # 注意：为了安全，这里只删除 index.html 和常见的资源目录，视你实际情况而定
    if os.path.exists("index.html"):
        os.remove("index.html")
    # 如果有特定的资源文件夹（如 images, js, css），建议在这里添加代码删除它们
    # 例如: if os.path.exists("js"): shutil.rmtree("js")

    # 2. 调用 wget 进行全站克隆
    # 参数解释：
    # -E: 将扩展名转换为 .html (如果需要)
    # -H: 允许跨域
    # -k: 将链接转换为本地相对链接（关键！否则传上去还会找 localhost）
    # -K: 备份原文件
    # -p: 下载显示页面所需的所有资源（图片、CSS、JS）
    # -nH: 不创建主机目录
    cmd = [
        "wget.exe",
        "-E", "-H", "-k", "-K", "-p", "-nH",
        LOCAL_URL
    ]

    try:
        # 运行 wget，隐藏输出以免刷屏
        subprocess.run(cmd, check=True, shell=True)
        print("网页克隆完成！")
        return True
    except subprocess.CalledProcessError:
        print("克隆失败！(可能 wget.exe 不在当前目录，或游戏未启动)")
        return False


def git_push():
    try:
        print("正在上传到 GitHub...")
        subprocess.run(["git", "add", "."], check=True)
        msg = f"Auto update {time.strftime('%H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", msg], check=False)
        subprocess.run(["git", "push"], check=True)
        print("上传成功！")
    except Exception as e:
        print(f"Git 上传失败: {e}")


if __name__ == "__main__":
    # 检查 wget 是否存在
    if not os.path.exists("wget.exe"):
        print("错误：找不到 wget.exe！")
        print("请下载 wget.exe 并放到此脚本的同一级目录下。")
        input("按回车键退出...")
        exit()

    print("=== 全站镜像脚本启动 (Wget版) ===")

    while True:
        if mirror_site():
            git_push()
        else:
            print("等待游戏启动...")

        print(f"等待 {INTERVAL} 秒...\n")
        time.sleep(INTERVAL)