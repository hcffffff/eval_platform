from .ChatGPT import ChatGPT
from .SparkDesk import SparkDesk
import random

class Model(object):
    def __init__(self, apikey):
        self.keys = apikey
        self.ChatGPT = ChatGPT(random.choice(self.keys["ChatGPT"]))
        self.SparkDeskKey = random.choice(self.keys["sparkDesk"])
        self.SparkDesk = SparkDesk(self.SparkDeskKey["appid"], self.SparkDeskKey["api_key"], self.SparkDeskKey["api_secret"])
    
    def chat(self, model, question, role=""):
        if model == 'ChatGPT':
            self.ChatGPT = ChatGPT(random.choice(self.keys["ChatGPT"]))
            return self.ChatGPT.chat(question, role)
        elif model == 'SparkDesk':
            self.SparkDeskKey = random.choice(self.keys["sparkDesk"])
            self.SparkDesk = SparkDesk(self.SparkDeskKey["appid"], self.SparkDeskKey["api_key"], self.SparkDeskKey["api_secret"])
            return self.SparkDesk.chat(question)
        else:
            return ""

if __name__ == "__main__":
    model = model()