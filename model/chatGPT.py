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
    cg = ChatGPT('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')
    print(cg.chat("你好"))
