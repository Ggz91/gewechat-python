import os
import requests
import json

class WeComClient:
    '''
        以markdown形式发送企业微信消息
    '''
    def __init__(self):
        '''
            从环境变量中获取
        '''
        self.url = os.getenv("WECOM_URL")

    def post_text(self, content):
        if self.url is None:
            print("url is None")
            return
        
        payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
            }
        }
    
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.url, headers=headers, data=json.dumps(payload, ensure_ascii=False))