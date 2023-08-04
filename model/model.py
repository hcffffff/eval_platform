from .ChatGPT import ChatGPT
from .SparkDesk import SparkAPI
from .ErnieBot import ErnieBot
import random

class Model(object):
    def __init__(self, apikey):
        self.keys = apikey
        self.ChatGPT = ChatGPT(random.choice(self.keys["ChatGPT"]))
        self.SparkDeskKey = random.choice(self.keys["SparkDesk"])
        self.SparkDesk = SparkAPI(self.SparkDeskKey["appid"], self.SparkDeskKey["api_key"], self.SparkDeskKey["api_secret"])
        self.ErnieBotKey = random.choice(self.keys["ErnieBot"])
        self.ErnieBot = ErnieBot(self.ErnieBotKey["api_key"], self.ErnieBotKey["secret_key"])
    
    def chat(self, model, query, role="", temperature=0.05, max_tokens=4096):
        '''
        temperature 越低可以使回答更单一，取值越高随机性越强即相同的问题得到的不同答案的可能性越高
            Sparkdesk: [0, 1], 
            ChatGPT: [0, 2],
            Ernie: (0, 1]
        max_tokens 最高输入token数量，ChatGPT的定义可能有点不一样
            Sparkdesk: [0, 4096]
            ChatGPT: [0, 4096]
        '''
        if model == 'ChatGPT':
            self.ChatGPT = ChatGPT(random.choice(self.keys["ChatGPT"]))
            return self.ChatGPT.chat(query=query, temperature=temperature, max_tokens=max_tokens, role=role)
        elif model == '讯飞星火':
            self.SparkDeskKey = random.choice(self.keys["SparkDesk"])
            self.SparkDesk = SparkAPI(self.SparkDeskKey["appid"], self.SparkDeskKey["api_key"], self.SparkDeskKey["api_secret"])
            return self.SparkDesk.chat(query=query, temperature=temperature, max_tokens=max_tokens)
        elif model == '百度文心一言':
            self.ErnieBotKey = random.choice(self.keys["ErnieBot"])
            self.ErnieBot = ErnieBot(self.ErnieBotKey["api_key"], self.ErnieBotKey["secret_key"])
            return self.ErnieBot.chat(query=query, temperature=temperature)
        elif model == '百度文心一言-turbo':
            self.ErnieBotKey = random.choice(self.keys["ErnieBot"])
            self.ErnieBot = ErnieBot(self.ErnieBotKey["api_key"], self.ErnieBotKey["secret_key"])
            return self.ErnieBot.chat(query=query, temperature=temperature, useTurbo=True)
        else:
            return "ERROR: 请指定模型"

if __name__ == "__main__":
    model = model()
