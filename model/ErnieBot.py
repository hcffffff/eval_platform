import requests
import json

API_KEY = ""
SECRET_KEY = ""

class ErnieBot(object):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def _get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
        return str(requests.post(url, params=params).json().get("access_token"))

    def chat(self, query, temperature=0.01, useTurbo=False):
        ErnieBot_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + self._get_access_token()
        ErnieBotTurbo_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + self._get_access_token()
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ], 
            "temperature": temperature
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", ErnieBotTurbo_url if useTurbo else ErnieBot_url, headers=headers, data=payload)
        return json.loads(response.text)["result"]


if __name__ == '__main__':
    eb = ErnieBot(API_KEY, SECRET_KEY)
    print(eb.chat("你好"))
