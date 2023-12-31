# eval_platform

## requirements

```
python >= 3.8.0
gradio >= 3.39.0
openai
websocket-client >= 1.6.1
tiktoken >= 0.4.0
```

## Run
首先，将`keys/example.json`中的内容复制到`keys/mine.json`中，写入自己的ChatGPT API-Key，讯飞key以及其他大模型api-key，如果同一个大模型有多个key请以逗号分隔，注意json格式只支持双引号否则会报错。如下所示：
```
{
    "ChatGPT": [
        "sk-aklsjdfa", 
        "sk-akljsdfa"
    ], 
    "sparkDesk": [
        {
            "appid": "asdfadf",
            "api_secret": "asdfasdfasdfafa", 
            "api_key": "sadfgsdfgsdfg"
        }, 
        {
            "appid": "asdfasd",
            "api_secret": "asdfasdfasdfa", 
            "api_key": "wsedthwrethw"
        }
    ], 
    "ErnieBot": [
        {
            "api_key": "xx", 
            "secret_key": "xx"
        }, 
        {
            "api_key": "xx", 
            "secret_key": "xx"
        }
    ]
}
```

运行：
```
python launch.py
```
visit `http://localhost:7860` for inspect.



## TODO
- [x] 两个模型对比，一个选中了，则不能选另一个
- [x] 试题上传和文件管理后端
- [x] 收集问题时分学科和等级
- [x] 两个模型比较时的按钮逻辑，参照单模型测评
- [ ] 模型测评的自动测评指标
- [ ] 模型限制token输入长度，计算问题token数量
- [ ] 设置模型回复等待时间

## 模型API：
- [x] ChatGPT
- [x] 讯飞星火
- [x] 百度文心一言
- [x] 百度文心一言-turbo
- [ ] 
- [ ] ...