from gewechat_client import GewechatClient
import os
import requests
#import base64
#from PIL import Image
from flask import Flask, request, jsonify

def main():
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
                return 
        else:
            print("Token请求失败")
            return
    
    headers = {"X-GEWE-TOKEN": token}

    '''
    if app_id is None or app_id == "":
        print("没有配置 APP_ID")
        
        url = f"{base_url}/login/getLoginQrCode"
        print(url)
        reponse =  requests.post(url, headers=headers, json={"appId": app_id or ""})
        if reponse.status_code == 200:
            data = reponse.json()
            try:
                app_id = data["data"]["appId"]

            except Exception as e:
                print("登陆失败")
                print(f"err:{e}")
                return
        else:
            return
    '''

    # 创建 GewechatClient 实例
    client = GewechatClient(base_url, token)

    # 登录, 自动创建二维码，扫码后自动登录
    app_id, error_msg = client.login(app_id=app_id)
    if error_msg:
        print("登录失败")
        return

    # 设置回调地址
    try:
        reponse = client.set_callback(token=token, callback_url="http://101.43.97.96:8888/")
    except Exception as e:
        print(f"设置回调地址失败:{e}")
        return
    print("完成登陆操作")

if __name__ == "__main__":
    main()
