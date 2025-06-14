from ai.AiClient import *
import xml.etree.ElementTree as ET

g_admins = ["GgZ529038378"]
g_groups = ["49715495297@chatroom", "44648936251@chatroom"]
g_listen_groups = ["49650497008@chatroom"]
g_listen_users = ["wxid_kwiwriatxphi21", "wxid_zxmdgghaiahi22"]
g_app_id = "wx_u4c2FuUaLD3L_WuyGxJ2N"
g_admin_broadcast_prefix = "ToGroups:"
g_ai_prefix = "@Bot"
g_test = True
g_avilable_msg_types = [1, 3, 10002] # 1 普通消息 3 图片消息 10002 群公告
class RequestHandler():
    def __init__(self, request, client):
        self._request = request
        self._client = client
        pass

    def process(self):
        return "Handle Request"

class GetRequestHandler(RequestHandler):
    def __init__(self, request, client):
        super().__init__(request, client)
        pass

    def process(self):
        return super().process()

class AdminRequestHandler(RequestHandler):
    def __init__(self, request, client):
        super().__init__(request, client)
        pass

    def process(self):
        return super().process()

class PostRequestHandler(RequestHandler):
    pass 

class AdminBroadcastToGroupRequestHandler(PostRequestHandler):
    def __init__(self, request, client):
        super().__init__(request, client)
        pass

    def process(self):
        # 解析数据
        data = self._request.get_json()
        self._Content = data["Data"]["Content"]["string"]
        is_pic_msg = self._MsgType =  data["Data"]["MsgType"] == 3
        for group in g_groups:
            if is_pic_msg:
                self._client.forward_image(g_app_id, group, self._Content)
            else:
                self._client.post_text(g_app_id, group, self._Content)
        return super().process()

class ForwardToGroupRequestHandler(PostRequestHandler):
    def __init__(self, request, client):
        super().__init__(request, client)
        pass

    def process(self):
        # 解析数据
        data = self._request.get_json()
        self._Content = data["Data"]["Content"]["string"]
        is_pic_msg = data["Data"]["MsgType"] == 3
        is_notification = data["Data"]["MsgType"] == 10002

        if is_pic_msg:
            for group in g_groups:
                self._client.forward_image(g_app_id, group, self._Content)
        elif is_notification:
            # 解析content中json字符串
            content = self._Content = self._Content.split(":", 1)[1].strip()
            sysmsg = ET.fromstring(content)
            if sysmsg:
                type = sysmsg.get('type')
                if type == 'mmchatroombarannouncememt':
                    # 确定是群通告
                    mmcn = sysmsg.find('mmchatroombarannouncememt')
                    content = mmcn.find('content').text.strip()
                    for group in g_groups:
                        self._client.post_text(g_app_id, group, "From 欧阳:\n" + content)
            pass
        else:
            self._Content = self._Content.split(":", 1)[1].strip()
            for group in g_groups:
                self._client.post_text(g_app_id, group, "From 欧阳:\n" + self._Content)
        
        return super().process()

class AIRequestHandler(PostRequestHandler):
    def __init__(self, request, client):
        super().__init__(request, client)
        pass

    def process(self):
        print("AI ask")
         # 解析数据
        data = self._request.get_json()
        self._FromUserName = data["Data"]["FromUserName"]["string"]
        self._Content = data["Data"]["Content"]["string"]
        is_listen_group_message = False
        if self._FromUserName in g_groups:
            is_listen_group_message = True
        if is_listen_group_message:
            self._Content = self._Content.split(":", 1)[1].strip()
        self._Content = self._Content.replace(g_ai_prefix, "", 1).strip()
        ai_client = AiClient()
        sucess,answer = ai_client.ask(self._Content)
        if sucess:
            self._client.post_text(g_app_id, self._FromUserName, answer)
        return super().process()

class PostRequestHandler(RequestHandler):
    def __init__(self, request, client):
        super().__init__(request, client)
        self._MsgType = None
        self._FromUserName = None
        self._ToUserName = None
        self._Content = None
        self._PushContent = None
        self._IsPicMsg = False
        pass

    def process(self):
        super().process()
        print("process PostRequestHandler")
        # 解析数据
        data = self._request.get_json()
        if data.get("Data") is None or data["Data"].get("MsgType") is None:
            # 暂时只支持文本消息/图片消息/群公告
            print("No Data")
            return "Handle Request"
        if g_test:
            print("Data :", str(data))
            
        self._MsgType =  data["Data"]["MsgType"]
        if self._MsgType not in g_avilable_msg_types:
            # 暂时只支持文本消息/图片消息/群公告
            print("MsgType :" + str(self._MsgType))
            return "Handle Request"
        self._FromUserName = data["Data"]["FromUserName"]["string"]
        self._ToUserName = data["Data"]["ToUserName"]
        self._Content = data["Data"]["Content"]["string"]
        
        self._IsPicMsg = self._MsgType == 3
        self._IsNotification = self._MsgType == 10002

        # 好像只有好友才有PushContent
        if data["Data"].get("PushContent") is not None:
            self._PushContent = data["Data"]["PushContent"]
        # 消息分类
        is_admin = False
        if self._FromUserName in g_admins:
            is_admin = True
        is_listen_group_message = False
        if self._FromUserName in g_listen_groups:
            is_listen_group_message = True
        
        is_server_group_message = False
        if self._FromUserName in g_groups:
            is_server_group_message = True

        is_ai = False
        if self._Content.startswith(g_ai_prefix):
            is_ai = True
        elif not self._IsPicMsg:
            if is_listen_group_message or is_server_group_message:
                content = self._Content.split(":")[1].strip()
            else:
                content = self._Content
            print("content: " + str(content))
            if content.startswith(g_ai_prefix):
                is_ai = True
        if g_test:
            #print("Data :", str(data))
            print("FromUserName: " + str(self._FromUserName))
            print("is_admin: " + str(is_admin))
            print("is_listen_group_message: " + str(is_listen_group_message))
            print("self._Content: " + str(self._Content))
            print("is_ai: " + str(is_ai))


        # 管理员消息
        # 根据前缀分类
        # 0. 群发消息
        real_handler = None

        if is_ai:
            real_handler = AIRequestHandler(self._request, self._client)
        else:
            if is_admin:
                # 群发消息
                real_handler = AdminBroadcastToGroupRequestHandler(self._request, self._client)
                '''
                if self._Content.startswith(g_admin_broadcast_prefix):
                    real_handler = AdminBroadcastToGroupRequestHandler(self._request, self._client)
                else:
                    real_handler = AdminRequestHandler(self._request, self._client)
                pass
                '''
            if is_listen_group_message:
                # 过滤
                user = self._Content.split(":")[0].strip()
                if g_test:
                    print("group user: " + str(user))
                if user in g_listen_users:
                    print("is listen user")
                    real_handler = ForwardToGroupRequestHandler(self._request, self._client)
                else:
                    pass
            
        if real_handler is None:
            print("handler is none")
            return "Handle Request"
        return real_handler.process()