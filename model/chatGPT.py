import openai

class ChatGPT:
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = api_key
    
    def chat(self, question, role=""):
        chat = self.openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": role},
                        {"role": "user", "content": question}
                    ]
                )
        return chat.get("choices")[0]["message"]["content"]

if __name__ == "__main__":
    cg = ChatGPT('')
    print(cg.chat("你好"))
