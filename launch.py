import gradio as gr

scripts = '''
## 规则

这里说明该系统的规则

## 使用条款

这里说明该系统的使用条款

## 使用方法

这里说明该系统的使用方法
'''
isValidUser = False

def greet(name):
    return "Hello " + name + "!"

def typeInEvalProblem(question, options, correctOPT):
    return 1

def done_by_model_1(question, task):
    return f"{task} done by model 1."

def done_by_model_2(question, task):
    return f"{task} by model 2."

def zhishidian_EVAL(question):
    '''
    知识点测评Gradio函数，需要配置模型到这里
    input:
        question 问题
        模型选择 TODO
    output:
        模型1回答, 模型2回答
    '''
    return "zhishidian done by model 1", "zhishidian done by model 2"

def hexinsuyang_EVAL(question):
    '''
    核心素养测评Gradio函数，需要配置模型到这里
    input:
        question 问题
        模型选择 TODO
    output:
        模型1回答, 模型2回答
    '''
    return "hexinsuyang done by model 1", "hexinsuyang done by model 2"

def verifyUser(uid):
    '''
    初步的用户登录验证
    '''
    if uid=='chaofan': # TODO 修改为验证测评人身份的判断条件
        return gr.update(value=f'''
            ## 登录

            已登录为 {uid}
        '''), gr.update(visible=False), gr.update(visible=False), gr.update(interactive=True), gr.update(interactive=True)


def main():
    with gr.Blocks() as demo:
        gr.Markdown('''
            # 教育大模型测试系统
            
            请选择知识点或核心素养级别测试
        ''')
        with gr.Blocks() as loginBlock:
            login_md = gr.Markdown('''
                ## 登录

                请使用您的uid进行登录
            ''')
            input_user_info = gr.Textbox(label="user ID")
            check_button = gr.Button("登录")
            
        with gr.Blocks() as scripsBlock:
            gr.Markdown(scripts)
        with gr.Tab("知识点测评"):
            gr.Markdown(
                '''
                ## 知识点测评

                请上传习题
                '''
            )
            input_question = gr.Textbox(label="题目", interactive=True)
            input_answer = gr.Textbox(label="答案", info="上传答案可以获得自动测评结果", interactive=True)
            with gr.Row():
                output_model_1 = gr.Textbox(label="模型 1 回答")
                output_model_2 = gr.Textbox(label="模型 2 回答")
            with gr.Row():
                do_button = gr.Button("做这个题", interactive=False)
                clear_button = gr.ClearButton([input_question, input_answer, output_model_1, output_model_2], interactive=False)
            check_button.click(
                verifyUser, 
                inputs=[
                    input_user_info
                ], 
                outputs=[
                    login_md, 
                    input_user_info, 
                    check_button, 
                    do_button, 
                    clear_button
                ]
            )
            do_button.click(
                zhishidian_EVAL,
                inputs=[
                    input_question
                ],
                outputs=[
                    output_model_1,
                    output_model_2
                ]
            )
        with gr.Tab("核心素养测评"):
            gr.Markdown(
                '''
                ## 核心素养测评

                请上传习题
                '''
            )
            input_question = gr.Textbox(label="题目", interactive=True)
            input_answer = gr.Textbox(label="答案", info="上传答案可以获得自动测评结果", interactive=True)
            with gr.Row():
                output_model_1 = gr.Textbox(label="模型 1 回答")
                output_model_2 = gr.Textbox(label="模型 2 回答")
            with gr.Row():
                do_button = gr.Button("做这个题", interactive=False)
                clear_button = gr.ClearButton([input_question, input_answer, output_model_1, output_model_2], interactive=False)
            check_button.click(
                verifyUser, 
                inputs=[
                    input_user_info
                ], 
                outputs=[
                    login_md, 
                    input_user_info, 
                    check_button, 
                    do_button, 
                    clear_button
                ]
            )
            do_button.click(
                hexinsuyang_EVAL,
                inputs=[
                    input_question
                ],
                outputs=[
                    output_model_1,
                    output_model_2
                ]
            )
    demo.launch()

if __name__ == "__main__":
    main()