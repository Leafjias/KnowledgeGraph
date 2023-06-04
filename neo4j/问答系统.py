import ahocorasick
from py2neo import Graph, Node, Relationship

# 初始化Neo4j数据库连接
url = 'http://localhost:7474/browser/'
user = "neo4j"
password = "123456"
graph = Graph(url, user=user, password=password, name="neo4j")

# 初始化Aho-Corasick自动机
keywords = ['负极材料', '宁德时代', '比亚迪', 'CATL', '上市']
A = ahocorasick.Automaton()
for keyword in keywords:
    A.add_word(keyword, keyword)
A.make_automaton()

# 查询模板
query_templates = [
    ("负极材料的环节涉及到哪些公司", "MATCH (n:link)<-[:相关]-(c:company) where n.name = \"三元材料\" RETURN c.name"),
    ("宁德时代在哪里上市的", "MATCH (c:公司{name:'宁德时代'})-[:上市于]->(s:交易所) RETURN s.name"),
    ("宁德时代和比亚迪有什么关系", "MATCH (c1:公司{name:'宁德时代'})-[:合作]->(c2:公司{name:'比亚迪'}) RETURN c1.name, c2.name"),
    ("宁德时代12.1有哪些新闻", "MATCH (c:公司{name:'宁德时代'})-[:发布]->(n:新闻{date:'12.1'}) RETURN n.title")
]

# 根据问题查找查询模板
def find_query_template(question):
    for template in query_templates:
        if all(word in question for word in template[0].split()):
            return template[1]
    return None

# 处理用户输入的问题
def process_question(question):
    # 在Aho-Corasick自动机中查找关键词
    keywords = []
    for end_index, keyword in A.iter(question):
        keywords.append(keyword)
    # 根据关键词查找查询模板
    query_template = find_query_template(question)
    # 如果没有找到匹配的查询模板，则返回错误信息
    if query_template is None:
        return "抱歉，我不知道该怎么回答这个问题"
    # 根据查询模板和关键词生成查询语句
    query = query_template.format(*keywords)
    # 在Neo4j数据库中执行查询
    results = graph.run(query)
    # 生成自然语言回答
    answer = ""
    for record in results:
        answer += str(record[0]) + "\n"
    if answer == "":
        answer = "抱歉，我没有找到相关信息"
    return answer

# 交互式对话
while True:
    question = input("请问您有什么问题吗？\n")
    answer = process_question(question)
    print(answer)
