import gradio as gr
from model.model import Model
from utils import *
from eval_metric import *
'''
这是构成前端交互页面的组件文件
'''

scripts = '''
## 规则

这里说明该系统的规则

## 使用条款

这里说明该系统的使用条款

## 使用方法

这里说明该系统的使用方法
'''
apikey = {}
def singleModelEval(model, question, answer, reason):
    '''
    单模型自动测评
    input:
        model: str 使用的模型
        question: str 问题
        answer: str 标准答案
        reason: str 答案解析
    output:
        response: str 模型回答
        accuracy: float 准确性
        robustness: float 鲁棒性
        Interpretability: float 可解释性
    '''
    Md = Model(apikey)
    response = Md.chat(model, question)
    return response, check_choice(answer, reason, response), "鲁棒性自动测评TODO", "可解释性自动测评TODO"

def multiModelEval(model_1, model_2, question):
    '''
    多模型对比测评
    input:
        model_1: str 模型1
        model_2: str 模型2
        question 问题
    output:
        model_1_response: str 模型1回答
        model_2_response: str 模型2回答
    '''
    Md = Model(apikey)
    model_1_response = Md.chat(model_1, question)
    model_2_response = Md.chat(model_2, question)
    return model_1_response, model_2_response

def verifyUser(uid):
    '''
    初步的用户登录验证
    '''
    global apikey
    apikey = getAPIKey()
    return True
    if uid=='chaofan': # TODO 修改为验证测评人身份的判断条件
        return True
    else:
        return False

def setInteractiveForSingleEval(uid):
    '''
    通过用户验证后将登录框设置为不可见，并将单模型自动测评中的交互文本框和各种按钮设置为可交互
    '''
    if verifyUser(uid):
        return gr.update(value=f'''
            ## 登录

            已登录为 {uid}
        '''), gr.update(visible=False), gr.update(visible=False), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)
    else:
        return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update()

def setInteractiveForMultiEval(uid):
    '''
    通过用户验证后将登录框设置为不可见，并将两模型人工对比中的交互文本框和各种按钮设置为可交互
    '''
    if verifyUser(uid):
        return gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)
    else:
        return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update()

def changeKnowledgeNode(subject):
    '''
    根据学科选择知识点多选框更新
    '''
    return gr.update(choices=getKnowledgeNode(subject), interactive=True)

def changeModelListForMultiEval(model_choose):
    '''
    防止两模型人工对比时选择了两个一样的模型
    '''
    model_list = getModelLabel()
    return gr.update(choices=model_list) ## TODO 待模型API可用后修改回来
    if model_choose == None or model_choose not in model_list:
        return gr.update(choices=model_list)
    else:
        model_list.remove(model_choose)
        return gr.update(choices=model_list)

def changeSubmitButtonForMultiEval(human_option, output_1, output_2):
    '''
    防止两模型人工对比时提交空评价，等待两个模型的output都有结果再进行提交
    '''
    if human_option != None and output_1 != "" and output_2 != "":
        return gr.update(interactive=True)
    else:
        return gr.update()

def main():
    with gr.Blocks() as demo:
        gr.Markdown('''
            # 教育大模型测试系统
            
            请选择单模型测试或两模型对比
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
        with gr.Tab("单模型自动测评"):
            gr.Markdown(
                '''
                ## 单模型自动测评

                请选择模型和参数
                '''
            )
            # 用于选择指定模型进行测评 根据具体实现的模型修改
            input_model = gr.Dropdown(getModelLabel(), label="模型", interactive=False)
            with gr.Row():
                input_subject = gr.Radio(choices=getAllSubject(), label="学科", interactive=False)
                input_knowledge_node = gr.CheckboxGroup([], label="请选择该题所涉及知识点", interactive=False)
                input_subject.change(changeKnowledgeNode, inputs=input_subject, outputs=input_knowledge_node)
            with gr.Row():
                input_knowledge_level = gr.Dropdown(["初级", "中级", "高级"], label="知识点分级", interactive=False)
                input_type = gr.Dropdown(["选择题", "填空题", "解答题"], label="题目类型", interactive=False)
            input_question = gr.Textbox(label="题目", interactive=False)
            # 根据具体需求确定是否需要该选项
            # 这里知识点和核心素养分级起到的作用可能得问申老师,包括这里是”知识点多选+分级单选 如 有理数*二次根式+初级“ 还是 ”知识点+分级多选 如 有理数初级+二次根式中级“
            # 知识点待补全
            input_answer = gr.Textbox(label="答案", info="请给出最终答案", interactive=False)
            input_reason = gr.Textbox(label="答案解析", info="请给出完整解析", interactive=False)
            """
            应能提取出模型输出的最终答案和答案解析，并于输入进行对比
            input：（标准答案，模型答案）/三次模型答案/（标准解析，模型解析）
            准确度：字符串比较
            鲁棒性：让模型回答同样的问题三次观察答案是否相同，借助字典
            可解释性：选用现成的文本相似度计算的库
            output：单道题测试直接输出正误、是否鲁棒、相似度分数/多道题测试算平均（取决于是否实现批量输入）
            """
            output_response = gr.Textbox(label="模型回答", interactive=False)
            with gr.Row():
                metric_correct = gr.Textbox(label="准确度", interactive=False)
                metric_robust = gr.Textbox(label="鲁棒性", interactive=False)
                metric_explain = gr.Textbox(label="可解释性", interactive=False)
            with gr.Row():
                do_button = gr.Button("测评", interactive=False)
                clear_button = gr.ClearButton([input_model, input_question, input_subject, input_type, input_knowledge_node, input_knowledge_level, input_reason, input_answer, metric_correct, metric_robust, metric_explain], interactive=False)
            upload_button = gr.Button("上传", interactive=False)
            check_button.click(
                setInteractiveForSingleEval,
                inputs=[
                    input_user_info
                ],
                outputs=[
                    login_md, 
                    input_user_info, 
                    check_button, 
                    do_button, 
                    clear_button, 
                    input_model, 
                    input_subject, 
                    input_type, 
                    input_question, 
                    input_knowledge_level, 
                    input_answer, 
                    input_reason, 
                    upload_button
                ]
            )
            do_button.click(
                singleModelEval,
                inputs=[
                    input_model, 
                    input_question, 
                    input_answer, 
                    input_reason
                ],
                outputs=[
                    output_response, 
                    metric_correct,
                    metric_robust,
                    metric_explain
                ]
            )
            upload_button.click(
                saveSingleEval, 
                inputs=[
                    input_question, 
                    input_answer, 
                    input_reason, 
                    input_type, 
                    input_subject, 
                    input_knowledge_node, 
                    input_knowledge_level, 
                    input_model, 
                    output_response, 
                    input_user_info
                ], 
                outputs=[
                    upload_button
                ]
            )
        with gr.Tab("两模型人工对比"):
            gr.Markdown(
                '''
                ## 两模型人工对比

                请选择模型
                '''
            )
            with gr.Row():
                input_model_1 = gr.Dropdown(choices=getModelLabel(), label="模型1", interactive=False)
                input_model_2 = gr.Dropdown(choices=getModelLabel(), label="模型2", interactive=False)
                input_model_1.change(changeModelListForMultiEval, inputs=input_model_1, outputs=input_model_2)
                input_model_2.change(changeModelListForMultiEval, inputs=input_model_2, outputs=input_model_1)
            with gr.Row():
                input_subject = gr.Radio(choices=getAllSubject(), label="学科", interactive=False)
                input_knowledge_node = gr.CheckboxGroup([], label="请选择该题所涉及知识点", interactive=False)
                input_subject.change(changeKnowledgeNode, inputs=input_subject, outputs=input_knowledge_node)
            with gr.Row():
                input_knowledge_level = gr.Dropdown(["初级", "中级", "高级"], label="知识点分级", interactive=False)
                input_type = gr.Dropdown(["选择题", "填空题", "解答题"], label="题目类型", interactive=False)
            input_question = gr.Textbox(label="题目", interactive=False)
            input_answer = gr.Textbox(label="答案", info="请给出最终答案", interactive=False)
            input_reason = gr.Textbox(label="答案解析", info="请给出完整解析", interactive=False)

            with gr.Row():
                output_response_1 = gr.Textbox(label="模型 1 回答", interactive=False)
                output_response_2 = gr.Textbox(label="模型 2 回答", interactive=False)
            with gr.Row():
                do_button = gr.Button("模型对比测评", interactive=False)
            with gr.Row():
                user_opinion = gr.Radio(["模型1更好", "模型2更好", "平手","都很差"], label="请给出你的评价", interactive=False)
                submit_button = gr.Button("提交", interactive=False)
            with gr.Row():
                clear_button = gr.ClearButton(
                    [input_model_1, input_model_2, input_question, input_subject, input_type, input_knowledge_node, input_knowledge_level, input_answer, 
                    input_reason, output_response_1, output_response_2, user_opinion], interactive=False)
            check_button.click(
                setInteractiveForMultiEval,
                inputs=[
                    input_user_info
                ],
                outputs=[
                    do_button,
                    clear_button, 
                    user_opinion, 
                    input_model_1, 
                    input_model_2, 
                    input_question, 
                    input_type, 
                    input_subject, 
                    input_knowledge_level, 
                    input_answer, 
                    input_reason
                ]
            )
            do_button.click(
                multiModelEval,
                inputs=[
                    input_model_1, 
                    input_model_2, 
                    input_question
                ],
                outputs=[
                    output_response_1,
                    output_response_2
                ]
            )
            user_opinion.change(changeSubmitButtonForMultiEval, inputs=[user_opinion, output_response_1, output_response_2], outputs=submit_button)
            submit_button.click(
                saveMultiEval, 
                inputs=[
                    input_question, 
                    input_answer, 
                    input_reason, 
                    input_type, 
                    input_subject, 
                    input_knowledge_node, 
                    input_knowledge_level, 
                    input_model_1, 
                    input_model_2, 
                    output_response_1, 
                    output_response_2, 
                    input_user_info, 
                    user_opinion
                ], 
                outputs=[
                    submit_button
                ]
            )
    demo.launch()

if __name__ == "__main__":
    main()