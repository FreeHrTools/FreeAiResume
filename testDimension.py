# 前端工程师筛选关键词(React、小程序)



keywords = [
  { 'code': 'github.com', 'weight': 10 },
  { 'code': 'React', 'weight': 1 },
  { 'code': 'Vue', 'weight': 3 },
  { 'code': '前端', 'weight': 1 },
  { 'code': '小程序', 'weight': 3 },
  { 'code': 'Node.js', 'weight': 1 },
  { 'code': '热爱技术', 'weight': 1 },
  { 'code': '@gmail', 'weight': 3 },
  { 'code': '本科', 'weight': 2 },
  { 'code': '大专', 'weight': 1 },
  { 'code': 'CSRF', 'weight': 1 },
  { 'code': 'XSS', 'weight': 1 },
]
# for keyword in keywords:
#     keyword['code'] = keyword['code'].lower()
#     print(keyword['code'])
#     print(keyword['weight'])
def getMatchScore(text):
    filtered_keywords = keywords[:];
    weight = 0
    fullScore = 0
    score = 0.0
    print(filtered_keywords)
    for keyword in keywords:
        fullScore += keyword['weight']
        if keyword['code'] in text:
            weight += keyword['weight']
    score = weight / fullScore
    formatScore = "%.2f%%" % (score * 100)
    # print(formatScore)  # %.2f 表示保留两位小数
    return formatScore