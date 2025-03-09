import json
import os

def load_keywords():
    """从配置文件中加载关键词配置"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'resume_filter_rules.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config['keywords']

def getMatchScore(text):
    keywords = load_keywords()
    weight = 0
    fullScore = 0
    score = 0.0
    
    for keyword in keywords:
        fullScore += keyword['weight']
        if keyword['code'] in text:
            weight += keyword['weight']
    
    score = weight / fullScore
    formatScore = "%.2f%%" % (score * 100)
    return formatScore