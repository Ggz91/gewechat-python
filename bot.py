from gewechat_client import GewechatClient
import os
import requests
#import base64
#from PIL import Image
from flask import Flask, request, jsonify
from request_handler import RequestHandler

host_server = Flask(__name__)

@host_server.route('/', methods=['GET', 'POST'])
def handle_request():
    # 处理 GET 请求
    if request.method == 'GET':
        # 获取 GET 请求的查询参数（如 /api?name=John）
        name = request.args.get('name', 'Unknown')
        return jsonify({"message": f"GET 请求成功，参数 name={name}"})

    # 处理 POST 请求
    elif request.method == 'POST':
        # 获取 POST 请求的 JSON 数据
        data = request.get_json()
        print("Received data:", data["Data"]["Content"]["string"])
        return jsonify({"message": "POST 请求成功", "received_data": data})

def init_server(gewechat_client):
    print("=============开始初始化Server===================")
    if gewechat_client is None:
        print("gewechat未初始化")
        return
    
    host_server.run(host='0.0.0.0', port=8888, debug=True)

def login(gewechat_client, token, app_id):
    print("=============开始登录===================")
    # 登录, 自动创建二维码，扫码后自动登录
    app_id, error_msg = gewechat_client.login(app_id=app_id)
    if error_msg:
        print("登录失败")
        return None

    # 设置回调地址
    try:
        reponse = gewechat_client.set_callback(token=token, callback_url="http://101.43.97.96:8888/")
    except Exception as e:
        print(f"设置回调地址失败:{e}")
        return 
    print("完成登陆操作")

def init_gewechat():
    print("=============开始初始化GeWechat===================")

    # 配置参数
    base_url = os.environ.get("BASE_URL", "http://localhost:2531/v2/api")
    token = os.environ.get("GEWECHAT_TOKE", "")
    app_id = os.environ.get("APP_ID", "wx_u4c2FuUaLD3L_WuyGxJ2N")
    
    if token is None or token == "":
        print("没有配置 GEWECHAT_TOKE")
    
        url = f"{base_url}/tools/getTokenId"
        print(url)
        reponse = requests.post(url)
        if reponse.status_code == 200:
            data = reponse.json()
            if data["ret"] == 200:
                token = data["data"]
                print("Token获取成功")
            else:
                print(f"Token获取失败: {data.get('msg', 'unknow')}")
                return None
        else:
            print("Token请求失败")
            return None

    # 创建 GewechatClient 实例
    client = GewechatClient(base_url, token)
    return client, token, app_id
    
def main():
    print("=============开始初始化===================")
    gewechat_client, token, app_id = init_gewechat()
    init_server(gewechat_client= gewechat_client)
    #login(gewechat_client, token, app_id)

if __name__ == "__main__":
    main()
