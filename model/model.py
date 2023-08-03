from chatGPT import ChatGPT


class model:
    def __init__(self):
        self.ChatGPT = ChatGPT
    
    def chat(self, question, role=None):
        return self.ChatGPT.chat(question, role)