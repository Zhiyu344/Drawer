import sys
import importlib.util
import subprocess
import os

def is_flask_installed():
    return importlib.util.find_spec("flask") is not None

def install_flask():
    print("正在安装 Flask，请稍候...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("\033[36m[INFO] Flask was successfully installed globally! \033[0m")
    except subprocess.CalledProcessError:
        print("\n[ERROR] Flask can't be installed globally, probably due to insufficient permissions.")
        print("You can choose from the following:")
        print("- Install only for the current user: \033[36mpip install --user flask\033[0m")
        print("- Run the program with Administrator privileges and try again")
        print("- Run manually in a Linux/macOS terminal: sudo pip install flask")
        print("\n程序即将退出，请按提示操作后再运行。")

        sys.exit(1)

def prompt_install_flask():
    print("Detected that you don't have Flask installed.")
    choice = input("Do you want to install Flask now? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        install_flask()
    else:
        print("The program requires Flask to run. Please type \033[36mpip install flask\033[0m to install flask before running.")
        sys.exit(0)

if __name__ == "__main__":
    if not is_flask_installed():
        prompt_install_flask()

    from flask import Flask, jsonify, render_template
    import json
    import random

    # 创建 Flask 应用
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    # 抽选接口
    @app.route('/draw', methods=['GET'])
    def draw():
        id1, char1, id2, char2 = draw_two(characters)
        return jsonify({
            "char1": {"id": id1, "name": char1["name"]},
            "char2": {"id": id2, "name": char2["name"]}
        })

    # 刷新角色数据接口
    @app.route('/reload')
    def reload_data():
        global characters
        characters = load_characters()
        return jsonify({"status": "success", "message": "The reload was successful!"})
    
    # 读取人物数据
    def load_characters(filename="characters.json"):
        try:
            with open('characters.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("\033[36m[INFO] The characters data is loaded successfully!\033[0m")
                return data
        except FileNotFoundError:
            print("\033[31m[ERROR] The characters.json file could not be found!\033[0m")
            sys.exit(1)
        except json.JSONDecodeError:
            print("\033[31m[ERROR] characters.json The file format is incorrect, please check the grammar!\033[0m")
            sys.exit(1)

    # 随机抽选两个不同的角色
    def draw_two(characters):
        ids = list(characters.keys())
        if len(ids) < 2:
            raise ValueError("人物数量不足两个！")

        # 随机选择第一个角色 ID
        first_id = random.choice(ids)

        # 构建剩余可选的角色列表（排除 first_id）
        remaining_ids = [cid for cid in ids if cid != first_id]

        # 确保还有至少一个可选项
        if not remaining_ids:
            raise ValueError("没有其他角色可供抽取！")
        
        second_id = random.choice(remaining_ids)

        return (
            first_id, characters[first_id],
            second_id, characters[second_id]
        )

    # 主程序
    characters = load_characters()
    app.run(host='0.0.0.0', debug=True)