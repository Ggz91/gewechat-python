from gewechat_client import GewechatClient
import os
import requests

def login():
    base_url = os.environ.get("BASE_URL", "http://localhost:2531/v2/api")
    token = os.environ.get("GEWECHAT_TOKE", "")
    app_id = os.environ.get("APP_ID", "wx_u4c2FuUaLD3L_WuyGxJ2N")
    print("token ", token)
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
    if client is None:
        print("client is none")
    #client.log_out(app_id=app_id)
    
    app_id, error_msg = client.login(app_id=app_id)
    if error_msg:
        print("登录失败")
        return None

    # 设置回调地址
    try:
        reponse = client.set_callback(token=token, callback_url="http://101.43.97.96:8888/")
    except Exception as e:
        print(f"设置回调地址失败:{e}")
        return 
    print("完成登陆操作")

def main():
    print("=============登陆===================")
    login()

if __name__ == "__main__":
    main()