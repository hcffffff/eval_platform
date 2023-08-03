import json
import uuid
from datetime import datetime
import os

def getAllSubject():
    with open('data/knowledge_node.json', 'r', encoding='utf-8') as f:
        knJson = json.load(f)
    return list(knJson.keys())

def getKnowledgeNode(subject):
    if subject == None:
        return []
    with open('data/knowledge_node.json', 'r', encoding='utf-8') as f:
        knJson = json.load(f)
    return knJson[subject]

def getModelLabel():
    with open('data/model_label.json', 'r', encoding='utf-8') as f:
        mlJson = json.load(f)
    return list(mlJson)

def getAPIKey():
    with open('keys/mine.json', 'r', encoding='utf-8') as f:
        apikey = json.load(f)
    return apikey

def getSubjectsEN():
    with open('data/subjects_en.json', 'r', encoding='utf-8') as f:
        subjects_en = json.load(f)
    return subjects_en

def saveSingleEval(question, answer, reason, question_type, subject, knowledge_node, knowledge_level, model, model_response, user):
    eval_id = str(uuid.uuid4())
    question_id = str(uuid.uuid4())
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    subjects_en = getSubjectsEN()
    evalDict = {
        "eval_id": eval_id, 
        "question_id": question_id, 
        "question": question, 
        "answer": answer, 
        "model": model, 
        "model_response": model_response, 
        "eval_user": user, 
        "eval_time": now
    }
    questionDict = {
        "question_id": question_id, 
        "question": question, 
        "answer": answer, 
        "reason": reason, 
        "question_type": question_type, 
        'subject': subject, 
        "knowledge_node": knowledge_node, 
        "knowledge_level": knowledge_level, 
        "update_user": user, 
        "update_time": now
    }
    subject = subjects_en[subject]
    if not os.path.exists(f'data/single_eval/{subject}'):
        os.mkdir(f'data/single_eval/{subject}')
    if not os.path.exists(f'data/question_collect/{subject}'):
        os.mkdir(f'data/question_collect/{subject}')
    with open(f'data/single_eval/{subject}/{eval_id}.json', 'w', encoding='utf-8') as evalF:
        json.dump(evalDict, evalF, ensure_ascii=False, indent=4)
    evalF.close()
    with open(f'data/question_collect/{subject}/{question_id}.json', 'w', encoding='utf-8') as questionF:
        json.dump(questionDict, questionF, ensure_ascii=False, indent=4)
    questionF.close()

if __name__ == "__main__":
    print(getAllSubject())