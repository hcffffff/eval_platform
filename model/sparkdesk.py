import base64
import hmac
import json
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from websocket import create_connection, WebSocketConnectionClosedException

'''
该代码参考 https://github.com/HildaM/sparkdesk-api
'''

def get_prompt(query: str, history: list):
    use_message = {"role": "user", "content": query}
    if history is None:
        history = []
    history.append(use_message)
    message = {"text": history}
    return message

def process_response(response_str: str, history: list):
    res_dict: dict = json.loads(response_str)
    code = res_dict.get("header", {}).get("code")
    status = res_dict.get("header", {}).get("status", 2)

    if code == 0:
        res_dict = res_dict.get("payload", {}).get("choices", {}).get("text", [{}])[0]
        res_content = res_dict.get("content", "")

        if len(res_dict) > 0 and len(res_content) > 0:
            # Ignore the unnecessary data
            if "index" in res_dict:
                del res_dict["index"]
            response = res_content

            if status == 0:
                history.append(res_dict)
            else:
                history[-1]["content"] += response
                response = history[-1]["content"]

            return response, history, status
        else:
            return "", history, status
    else:
        print("error code ", code)
        print("you can see this website to know code detail")
        print("https://www.xfyun.cn/doc/spark/%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E.html")
        return "", history, status


class SparkAPI:
    __api_url = 'wss://spark-api.xf-yun.com/v1.1/chat'
    __max_token = 2048

    def __init__(self, app_id, api_key, api_secret):
        self.__app_id = app_id
        self.__api_key= api_key
        self.__api_secret = api_secret

    def __set_max_tokens(self, token):
        if isinstance(token, int) is False or token < 0:
            print("set_max_tokens() error: tokens should be a positive integer!")
            return
        self.__max_token = token

    """
    doc url: https://www.xfyun.cn/doc/spark/general_url_authentication.html
    """

    def __get_authorization_url(self):
        authorize_url = urlparse(self.__api_url)
        # 1. generate data
        date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %Z')

        """
        Generation rule of Authorization parameters
            1) Obtain the APIKey and APISecret parameters from the console.
            2) Use the aforementioned date to dynamically concatenate a string tmp. Here we take Huobi's URL as an example, 
                the actual usage requires replacing the host and path with the specific request URL.
        """
        signature_origin = "host: {}\ndate: {}\nGET {} HTTP/1.1".format(
            authorize_url.netloc, date, authorize_url.path
        )
        signature = base64.b64encode(
            hmac.new(
                self.__api_secret.encode(),
                signature_origin.encode(),
                digestmod='sha256'
            ).digest()
        ).decode()
        authorization_origin = \
            'api_key="{}",algorithm="{}",headers="{}",signature="{}"'.format(
                self.__api_key, "hmac-sha256", "host date request-line", signature
            )
        authorization = base64.b64encode(authorization_origin.encode()).decode()
        params = {
            "authorization": authorization,
            "date": date,
            "host": authorize_url.netloc
        }

        ws_url = self.__api_url + "?" + urlencode(params)
        return ws_url

    def __build_inputs(
            self,
            message: dict,
            user_id: str = "001",
            domain: str = "general",
            temperature: float = 0.5,
            max_tokens: int = 2048
    ):
        input_dict = {
            "header": {
                "app_id": self.__app_id,
                "uid": user_id,
            },
            "parameter": {
                "chat": {
                    "domain": domain,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
            },
            "payload": {
                "message": message
            }
        }
        return json.dumps(input_dict)

    def chat(
            self,
            query: str,
            history: list = None,  # store the conversation history
            user_id: str = "001",
            domain: str = "general",
            max_tokens: int = 2048,
            temperature: float = 0.5,
    ):
        if history is None:
            history = []

        # the max of max_length is 4096
        max_tokens = min(max_tokens, 4096)
        url = self.__get_authorization_url()
        ws = create_connection(url)
        message = get_prompt(query, history)
        input_str = self.__build_inputs(
            message=message,
            user_id=user_id,
            domain=domain,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        ws.send(input_str)
        response_str = ws.recv()
        try:
            while True:
                response, history, status = process_response(response_str, history)
                """
                The final return result, which means a complete conversation.
                doc url: https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E
                """
                if len(response) == 0 or status == 2:
                    break
                response_str = ws.recv()
            return response

        except WebSocketConnectionClosedException:
            print("Connection closed")
        finally:
            ws.close()

    # Stream output statement, used for terminal chat.
    def __streaming_output(
            self,
            query: str,
            history: list = None,  # store the conversation history
            user_id: str = "001",
            domain: str = "general",
            max_tokens: int = 2048,
            temperature: float = 0.5,
    ):
        if history is None:
            history = []

        # the max of max_length is 4096
        max_tokens = min(max_tokens, 4096)
        url = self.__get_authorization_url()
        ws = create_connection(url)

        message = get_prompt(query, history)
        input_str = self.__build_inputs(
            message=message,
            user_id=user_id,
            domain=domain,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # send question or prompt to url, and receive the answer
        ws.send(input_str)
        response_str = ws.recv()

        # Continuous conversation
        try:
            while True:
                response, history, status = process_response(response_str, history)
                yield response, history
                if len(response) == 0 or status == 2:
                    break
                response_str = ws.recv()

        except WebSocketConnectionClosedException:
            print("Connection closed")
        finally:
            ws.close()

    def chat_stream(self):
        history = []
        print("Enter exit or stop to end the converation.\n")
        try:
            while True:
                query = input("Ask: ")
                if query == "exit" or query == "stop":
                    break
                for response, _ in self.__streaming_output(query, history):
                    print("\r" + response, end="")
                print("\n")
        finally:
            print("\nThank you for using the SparkDesk AI. Welcome to use it again!")


if __name__ == "__main__":
    sd = SparkAPI("a303d825", "0340f6686a6b5f494e308074b4313c8f", "OTE4MmYzZjY2YWRkOTE3ZjM3MjdmNDU3")
    print(sd.chat(query="你好？"))