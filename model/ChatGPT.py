import openai

class ChatGPT(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = api_key
    
    def chat(self, query, temperature=0, max_tokens=4096, role=""):
        chat = self.openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": role},
                        {"role": "user", "content": query}
                    ], 
                    temperature=temperature,
                    max_tokens=max_tokens
                )
        return chat.get("choices")[0]["message"]["content"]

if __name__ == "__main__":
    cg = ChatGPT('')
    print(cg.chat("你好"))