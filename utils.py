import json

def getAllSubject():
    with open('./data/knowledge_node.json', 'r', encoding='utf-8') as f:
        knJson = json.load(f)
    return list(knJson.keys())

def getKnowledgeNode(subject):
    if subject == None:
        return []
    with open('./data/knowledge_node.json', 'r', encoding='utf-8') as f:
        knJson = json.load(f)
    return knJson[subject]

def getModelLabel():
    with open('./data/model_label.json', 'r', encoding='utf-8') as f:
        mlJson = json.load(f)
    return list(mlJson)

if __name__ == "__main__":
    print(getAllSubject())