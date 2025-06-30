from flask import Flask, jsonify, render_template
import json
import random

# 创建 Flask 应用
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 新增：定义抽选接口
@app.route('/draw', methods=['GET'])
def draw():
    id1, char1, id2, char2 = draw_two(characters)
    return jsonify({
        "char1": {"id": id1, "name": char1["name"]},
        "char2": {"id": id2, "name": char2["name"]}
    })

# 读取人物数据
def load_characters(filename="characters.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# 随机抽选两个不同的角色
def draw_two(characters):
    ids = list(characters.keys())
    if len(ids) < 2:
        raise ValueError("人物数量不足两个！")

    first_id = random.choice(ids)
    remaining_ids = [cid for cid in ids if cid != first_id]
    second_id = random.choice(remaining_ids)

    return (
        first_id, characters[first_id],
        second_id, characters[second_id]
    )

# 主程序
if __name__ == "__main__":
    characters = load_characters()
    app.run(debug=True)