from ..gewechat_client.client import GewechatClient
from ..wecom_client import WeComClient

class ClientWrapper:
    def __init__(self, client : GewechatClient):
        self.gewechat_client = client
        self.wecom_client = None
        self.use_wecom = False

    def __init__(self, client : WeComClient):
        self.gewechat_client = None
        self.wecom_client = client
        self.use_wecom = True

    @property
    def client(self):
        return self.gewechat_client if self.use_gewechat else self.wecom_client
    
    '''
        重载的函数
    '''

    def forward_image(self, app_id, to_wxid, xml):
        """转发图片"""
        if not self.use_wecom:
            self.gewechat_client.forward_image(app_id, to_wxid, xml)
            return

    def post_text(self, app_id, to_wxid, content, ats: str = ""):
        """发送文字消息"""
        if not self.use_wecom:
            self.gewechat_client.post_text(app_id, to_wxid, content, ats)
            return
        
        self.wecom_client.post_text(content)