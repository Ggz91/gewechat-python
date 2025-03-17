from gewechat_client import GewechatClient
import os
import requests
#import base64
#from PIL import Image
from flask import Flask, request, jsonify, render_template
from request_handler.RequestHandler import *

host_server = Flask(__name__)

class Server():
    def __init__(self):
        pass

    def run(self, gewechat_client):
        print("=============开始初始化Server===================")
        if gewechat_client is None:
            print("gewechat未初始化")
            return
        
        g_gewechat_client = gewechat_client

        @host_server.route('/data')
        def get_data():
            return jsonify({"values": [10, 20, 30, 40]})

        @host_server.route('/', methods=['GET', 'POST'])
        def handle_request():
            print("\n=============================================================")
            print("enter handler_request")
            
            if gewechat_client is None:
                print("gewechat未初始化")
                print("=============================================================")
                return "Handle request"

            print("enter handler_request", request.method)

            request_handler = None
            # 处理 GET 请求
            if request.method == 'GET':
                request_handler = GetRequestHandler(request=request, client=gewechat_client)

            # 处理 POST 请求
            elif request.method == 'POST':
                # 获取 POST 请求的 JSON 数据
                request_handler = PostRequestHandler(request=request, client=gewechat_client)
            res = request_handler.process()
            print("=============================================================\n")
            return render_template("index.html")
        
        host_server.run(host='0.0.0.0', port=8888, debug=True)

