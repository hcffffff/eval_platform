from .ChatGPT import ChatGPT
from .SparkDesk import SparkAPI
import random

class Model(object):
    def __init__(self, apikey):
        self.keys = apikey
        self.ChatGPT = ChatGPT(random.choice(self.keys["ChatGPT"]))
        self.SparkDeskKey = random.choice(self.keys["sparkDesk"])
        self.SparkDesk = SparkAPI(self.SparkDeskKey["appid"], self.SparkDeskKey["api_key"], self.SparkDeskKey["api_secret"])
    
    def chat(self, model, question, role="", temperature=0, max_tokens=4096):
        '''
        temperature 越低可以使回答更单一，取值越高随机性越强即相同的问题得到的不同答案的可能性越高
            Sparkdesk: [0, 1], 
            ChatGPT: [0, 2]
        max_tokens 最高输入token数量，ChatGPT的定义可能有点不一样
            Sparkdesk: [0, 4096]
            ChatGPT: [0, 4096]
        '''
        if model == 'ChatGPT':
            self.ChatGPT = ChatGPT(random.choice(self.keys["ChatGPT"]))
            return self.ChatGPT.chat(question, temperature=temperature, max_tokens=max_tokens, role=role)
        elif model == 'SparkDesk':
            self.SparkDeskKey = random.choice(self.keys["sparkDesk"])
            self.SparkDesk = SparkAPI(self.SparkDeskKey["appid"], self.SparkDeskKey["api_key"], self.SparkDeskKey["api_secret"])
            return self.SparkDesk.chat(query=question, temperature=temperature, max_tokens=max_tokens-74)
        else:
            return ""

if __name__ == "__main__":
    model = model()
