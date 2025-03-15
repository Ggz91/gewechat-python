from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_requests():
    # 处理 GET 请求
    if request.method == 'GET':
        # 获取 GET 请求的查询参数（如 /api?name=John）
        name = request.args.get('name', 'Unknown')
        return 'Get'
        return jsonify({"message": f"GET 请求成功，参数 name={name}"})

    # 处理 POST 请求
    elif request.method == 'POST':
        # 获取 POST 请求的 JSON 数据
        data = request.get_json()
        print("Received data:", data["Data"]["Content"]["string"])
        return jsonify({"message": "POST 请求成功", "received_data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)