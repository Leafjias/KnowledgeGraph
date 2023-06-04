from py2neo import Graph
import os
import json
import csv
# 分词组成词云的头文件
import jieba.analyse
from collections import defaultdict

'''
    功能:该功能是查询数据库
'''


class Neo4jQuery:
    '''初始化函数 self是类自己'''
    '''功能:运行连接neo4j,初始化查询结果保存路径'''
    '''
    参数:
        无
    返回:
        无
    '''

    def __init__(self, url, user, password):
        cur_dir = os.path.dirname(__file__)
        self.price_path = os.path.join(cur_dir, "data\\股价数据")
        self.save_paths = {
            '公司': os.path.join(cur_dir, "data\\results\实体-公司.json"),
            '环节': os.path.join(cur_dir, "data\\results\实体-产业链环节.json"),
            '产品': os.path.join(cur_dir, "data\\results\实体-产品.json"),
            '产业链相关产品': os.path.join(cur_dir, "data\\results\实体-产业链相关产品.json"),
            '新闻': os.path.join(cur_dir, "data\\results\实体-新闻.json"),
            '公司与环节': os.path.join(cur_dir, "data\\results\关系-公司与环节.json"),
            '环节与环节': os.path.join(cur_dir, "data\\results\关系-环节与环节.json"),
            '公司与产品': os.path.join(cur_dir, "data\\results\关系-公司与产品.json"),
            '公司与产业链相关产品': os.path.join(cur_dir, "data\\results\关系-公司与产业链相关产品.json"),
            '产品与产品': os.path.join(cur_dir, "data\\results\关系-产品与产品.json"),
            '产业链相关产品与产业链相关产品': os.path.join(cur_dir, "data\\results\关系-产品与产品.json"),
            '公司与供应商': os.path.join(cur_dir, "data\\results\关系-公司与供应商.json"),
            '公司与客户': os.path.join(cur_dir, "data\\results\关系-公司与客户.json"),
            '公司与新闻': os.path.join(cur_dir, "data\\results\关系-公司与新闻.json"),
            '环节与产品': os.path.join(cur_dir, "data\\results\关系-环节与产品.json"),
            '停用词': os.path.join(cur_dir, "data\\停用词列表\\baidu_stopwords.txt")
        }

        self.search_return = {
            '产品': " RETURN n, id(n)",
            '环节': " RETURN n, id(n)",
            '公司': " RETURN n, id(n)",
            '新闻': " RETURN n, id(n)",
            '产业链相关产品': " RETURN n, id(n)",
            '公司与环节': " RETURN n.name as from,m.name as to,id(n) as id_from,id(m) as id_to,type(r) as rel",
            '环节与环节': " RETURN n.name as from,m.name as to,id(n) as id_from,id(m) as id_to,type(r) as rel",
            '产品与产品': " RETURN n.name as from,m.name as to,id(n) as id_from,id(m) as id_to,type(r) as rel",
            '产业链相关产品与产业链相关产品': " RETURN n.name as from,m.name as to,id(n) as id_from,id(m) as id_to,type(r) as rel",
            '公司与产品': " RETURN n.name as from,m.name as to,r.weight as weight,id(n) as id_from,id(m) as id_to,type(r) as rel",
            '公司与产业链相关产品': " RETURN n.name as from,m.name as to,r.weight as weight,id(n) as id_from,id(m) as id_to,type(r) as rel",
            '公司与供应商': " RETURN n.name as from,m.name as to,r.公开时间 as 公开时间,r.数据来源 as 数据来源,r.采购占比 as 采购占比,r.采购金额万元 as 采购金额万元, id(n) as id_from,id(m) as id_to,type(r) as rel",
            '公司与客户': " RETURN n.name as from,m.name as to,r.公开时间 as 公开时间,r.数据来源 as 数据来源,r.销售占比 as 销售占比,r.销售金额万元 as 销售金额万元, id(n) as id_from,id(m) as id_to,type(r) as rel",
            '公司与新闻': " RETURN n.name as from,m.name as to, id(n) as id_from,id(m) as id_to,type(r) as rel",
            '环节与产品': " RETURN n.name as from,m.name as to, id(n) as id_from,id(m) as id_to,type(r) as rel"
        }

        self.search_match = {
            '产品': "MATCH (n:product) ",
            '环节': "MATCH (n:link) ",
            '公司': "MATCH (n:company) ",
            '新闻': "MATCH (n:news) ",
            '产业链相关产品': "MATCH (n:产业链相关产品) ",
            '公司与环节': "MATCH p = (n:company)-[r]->(m:link) ",
            '环节与环节': "MATCH p = (n:link)-[r]->(m:link) ",
            '产品与产品': "MATCH p = (n:product)-[r]->(m:product) ",
            '产业链相关产品与产业链相关产品': "MATCH p = (n:产业链相关产品)-[r]->(m:产业链相关产品) ",
            '公司与产品': "MATCH p = (n:company)-[r]->(m:product) ",
            '公司与产业链相关产品': "MATCH p = (n:company)-[r]->(m:产业链相关产品) ",
            '公司与供应商': "MATCH p = (n:company)-[r:供应商]-(m:company)  ",
            '公司与客户': "MATCH p = (n:company)-[r:客户]-(m:company) ",
            '公司与新闻': "MATCH p = (n:news)-[r]-(m:company) ",
            '环节与产品': "MATCH p = (n:link)-[r:相关产品]->(m:product) "
        }
        self.search_label = {
            '产品': "product",
            '环节': "link",
            '公司': "company",
            '产业链相关产品': "产业链相关产品",
            '新闻': "news"
        }
        self.graph = Graph(url, user=user, password=password, name="neo4j")

    '''查找实体'''
    '''功能:根据键值查找实体'''
    '''
    参数:
        "label": "实体类型"
        "property_key"="属性名称", 
        "property_value"="值"
    返回:
        成功:返回查询结果的数组
        失败:返回Flase
    '''

    def search_entities(self, label=None, property_key=None, property_value=None):
        if property_value and not label:
            query = f"MATCH (n) WHERE n.name  CONTAINS '{property_value}' AND NOT 'news' IN LABELS(n) RETURN n"
        else:
            query = self.search_match[label]
            if property_key and property_value:
                query += "WHERE n.{} =~ '(?i).*{}.*' ".format(property_key, property_value)
            elif property_value:
                query += "WHERE n.name =~ '(?i).*{}.*' ".format(property_value)
            query = query + self.search_return[label]
        query = query + ",labels(n)[0]"
        print(query)
        try:
            nodes = self.graph.run(query)
            # print(nodes)
            # 将节点对象转换为字典数组
            result = []
            for node in nodes:
                # 获取节点的标签和属性labels(n)
                properties = dict(node["n"])
                properties["type"] = node["labels(n)[0]"]
                properties["id"] = node["id(n)"]
                # 构建字典
                result.append(properties)
            # with open(self.save_paths[label], "w", encoding="utf-8") as f:
            #     json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
            return result
        except:
            print("查询失败")
            return False

    '''查找实体'''
    '''功能:根据n-[r]->根据关系查找实体m，比如查找与n相连的公司信息'''
    '''
    参数:
        "label": "实体类型"
        "property_key"="属性名称", 
        "property_value"="值",
        "rel"="关系"
    返回:
        成功:返回查询结果的数组
        失败:返回Flase
    '''

    def search_entities_m(self, n_label=None, property_key=None, property_value=None, m_label=None):
        if property_value and n_label and property_key and m_label:
            query = f"MATCH (n:{self.search_label[n_label]})-[r]-(m:{self.search_label[m_label]}) WHERE n.{property_key} = '{property_value}' "
        else:
            print("查询条件不满足")
            return False
        query = query + "return m,id(m),labels(m)[0]"
        if(m_label=='新闻'):
            query+=",m.时间 as time"
        print(query)
        try:
            nodes = self.graph.run(query)
            # print(nodes)
            # 将节点对象转换为字典数组
            result = []
            for node in nodes:
                # 获取节点的标签和属性labels(n)
                properties = dict(node["m"])
                properties["id"] = node["id(m)"]
                properties["type"] = node["labels(m)[0]"]
                # 构建字典
                result.append(properties)
            # with open(self.save_paths[label], "w", encoding="utf-8") as f:
            #     json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
            return result
        except:
            print("查询失败")
            return False

    '''查找关系'''
    '''功能:根据键值查找关系或拿出所有关系'''
    '''
    参数:
        "rel_type": "关系类型"
        "property_key"="关系属性名称", 
        "property_value"="值"
    返回:
        查询结果的数组
    '''

    def search_relationships(self, rel_type=None, property_key=None, property_value=None):
        query = self.search_match[rel_type]
        if property_key and property_value:
            query += "WHERE r.{} =~ '(?i).*{}.*' ".format(property_key, property_value)
        query = query + self.search_return[
            rel_type] + ",labels(STARTNODE(r))[0] as from_type,labels(ENDNODE(r))[0] as to_type"
        print(query)
        try:
            nodes = self.graph.run(query)
            # 将节点对象转换为字典数组
            result = []
            for node in nodes:
                # 获取节点的标签和属性
                properties = dict(node)
                # 构建字典
                result.append(properties)
            with open(self.save_paths[rel_type], "w", encoding="utf-8") as f:
                json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
            return result
        except:
            print("查询失败")
            return False

    '''查找关系'''
    '''功能:根据查询某个结点的所关系信息'''
    '''
    参数:
        "rel_type": "关系类型"
        "property_key"="关系属性名称", 
        "property_value"="值"
    返回:
        查询结果的数组
    '''

    def search_relationships_n(self, rel_type=None, n_key=None, n_value=None):
        query = self.search_match[rel_type]
        if n_key and n_value:
            if rel_type !='公司与新闻':
                query += "WHERE n.{} =~ '(?i).*{}.*' ".format(n_key, n_value)
            else:
                query += "WHERE m.{} =~ '(?i).*{}.*' ".format(n_key, n_value)
        query = query + self.search_return[
            rel_type] + ",labels(STARTNODE(r))[0] as from_type,labels(ENDNODE(r))[0] as to_type"
        print(query)
        try:
            nodes = self.graph.run(query)
            # 将节点对象转换为字典数组
            result = []
            for node in nodes:
                # 获取节点的标签和属性
                properties = dict(node)
                # 构建字典
                result.append(properties)
            with open(self.save_paths[rel_type], "w", encoding="utf-8") as f:
                json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
            return result
        except:
            print("查询失败")
            return False

    def search_time(self, type, yy_s, mm_s, dd_s, yy_e, mm_e, dd_e):

        time_s = {
            "公司": f"{yy_s}/{mm_s}/{dd_s}",
            "新闻": f"{yy_s}-{mm_s}-{dd_s}",
            "公司与供应商": f"{yy_s}-{mm_s}",
            "公司与客户": f"{yy_s}-{mm_s}"
        }
        time_e = {
            "公司": f"{yy_e}/{mm_e}/{dd_e}",
            "新闻": f"{yy_e}-{mm_e}-{dd_e}",
            "公司与供应商": f"{yy_e}-{mm_e}",
            "公司与客户": f"{yy_e}-{mm_e}"
        }
        where = {
            "公司": f" where n.成立日期 >= '{time_s[type]}' and n.成立日期 <= '{time_e[type]}'",
            "新闻": f" where n.时间 >= '{time_s[type]}' and n.时间 <= '{time_e[type]}'",
            "公司与供应商": f" where r.公开时间 >= '{time_s[type]}' and r.公开时间 <= '{time_e[type]}'",
            "公司与客户": f" where r.公开时间 >= '{time_s[type]}' and r.公开时间 <= '{time_e[type]}'"
        }
        query = self.search_match[type] + where[type] + self.search_return[type]
        # print(query)
        try:
            nodes = self.graph.run(query)
            # 将节点对象转换为字典数组
            result = []
            for node in nodes:
                # 获取节点的标签和属性
                if type == "公司" or type == "新闻":
                    properties = dict(node["n"])
                else:
                    properties = dict(node)
                # if type== "公司与供应商" or type== "公司与客户" :
                #     properties["rel"] = rel
                # 构建字典
                result.append(properties)
            with open(self.save_paths[type], "w", encoding="utf-8") as f:
                json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
            return result
        except:
            print(type, "查询为空")
            return False

    def search_time(self, type, time):
        yy_e, mm_e, dd_e = time.split("-")
        time_e = {
            "公司": f"{yy_e}/{mm_e}/{dd_e}",
            "新闻": f"{yy_e}-{mm_e}-{dd_e}",
            "公司与供应商": f"{yy_e}-{mm_e}",
            "公司与客户": f"{yy_e}-{mm_e}"
        }
        where = {
            "公司": f" where n.成立日期 <= '{time_e[type]}'",
            "新闻": f" where n.时间 <= '{time_e[type]}'",
            "公司与供应商": f" where r.公开时间 <= '{time_e[type]}'",
            "公司与客户": f" where r.公开时间 <= '{time_e[type]}'"
        }
        query = self.search_match[type] + where[type] + self.search_return[type]
        # print(query)
        try:
            nodes = self.graph.run(query)
            # 将节点对象转换为字典数组
            result = []
            for node in nodes:
                # 获取节点的标签和属性
                if type == "公司" or type == "新闻":
                    properties = dict(node["n"])
                else:
                    properties = dict(node)
                # 构建字典
                result.append(properties)
            with open(self.save_paths[type], "w", encoding="utf-8") as f:
                json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
            return result
        except:
            print(type, "查询为空")
            return False

    def search_time(self, type, start_time, end_time):

        yy_s, mm_s, dd_s = start_time.split("-")
        yy_e, mm_e, dd_e = end_time.split("-")
        time_s = {
            "公司": f"{yy_s}/{mm_s}/{dd_s}",
            "新闻": f"{yy_s}-{mm_s}-{dd_s}",
            "公司与供应商": f"{yy_s}-{mm_s}",
            "公司与客户": f"{yy_s}-{mm_s}"
        }
        time_e = {
            "公司": f"{yy_e}/{mm_e}/{dd_e}",
            "新闻": f"{yy_e}-{mm_e}-{dd_e}",
            "公司与供应商": f"{yy_e}-{mm_e}",
            "公司与客户": f"{yy_e}-{mm_e}"
        }
        where = {
            "公司": f" where n.成立日期 >= '{time_s[type]}' and n.成立日期 <= '{time_e[type]}'",
            "新闻": f" where n.时间 >= '{time_s[type]}' and n.时间 <= '{time_e[type]}'",
            "公司与供应商": f" where r.公开时间 >= '{time_s[type]}' and r.公开时间 <= '{time_e[type]}'",
            "公司与客户": f" where r.公开时间 >= '{time_s[type]}' and r.公开时间 <= '{time_e[type]}'"
        }
        query = self.search_match[type] + where[type] + self.search_return[type]
        print(query)
        try:
            nodes = self.graph.run(query)
            # 将节点对象转换为字典数组
            result = []
            for node in nodes:
                # 获取节点的标签和属性
                if type == "公司" or type == "新闻":
                    properties = dict(node["n"])
                    properties["id"] = node["id(n)"]
                else:
                    properties = dict(node)
                # 构建字典
                result.append(properties)
            with open(self.save_paths[type], "w", encoding="utf-8") as f:
                json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
            return result
        except:
            print(type, "查询为空")
            return False

    # 查询公司股价信息
    def get_stock_info(self, code):

        file_path = os.path.join(self.price_path, f"{code}.csv")

        # 打开csv文件并读取数据
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # 用列表推导式生成包含trade_date和open的字典列表
            data = [{"trade_date": row["trade_date"], "open": row["open"]} for row in reader]

        # 用列表推导式生成以trade_date为键，以open为值的字典
        result = {d["trade_date"]: d["open"] for d in data}
        return result

    # 提取新闻关键字并祖成词云
    # 加载停用词
    def load_stopwords(self, stopwords_path):
        with open(stopwords_path, "r", encoding="utf-8") as f:
            stopwords = f.readlines()
        stopwords = set([word.strip() for word in stopwords])
        return stopwords

    def generate_wordcloud_data(self, news_data, topK=20):
        # 使用 defaultdict 初始化关键字计数字典
        keywords_count = defaultdict(int)

        # 加载停用词
        stopwords_path = self.save_paths["停用词"]
        stopwords = self.load_stopwords(stopwords_path)

        # 遍历新闻标题，提取关键字并计数
        for news_item in news_data:
            title = news_item['name']
            keywords = jieba.analyse.extract_tags(title, withWeight=False)

            # 过滤停用词
            filtered_keywords = [keyword for keyword in keywords if keyword not in stopwords]

            for keyword in filtered_keywords:
                keywords_count[keyword] += 1

        # 对关键字计数进行排序
        sorted_keywords = sorted(keywords_count.items(), key=lambda x: x[1], reverse=True)

        # 取数量最多的前topK个词
        top_keywords = sorted_keywords[:topK]

        # 将关键字计数字典转换为所需的格式
        result = [{"name": keyword, "value": count} for keyword, count in top_keywords]

        return result

    def search_company(self, search_key, search_value):
        results = {
            "环节": [],
            "公司": [],
            "产品": [],
            "新闻": [],
            "环节与环节": [],
            "环节与公司": [],
            "环节与产品": [],
            "公司与供应商": [],
            "公司与产品": [],
            "公司与新闻": [],
            "产品与产品": []
        }
        # 1.查询公司的基本信息
        results['查找的结点'] = self.search_entities(label="公司", property_key=search_key, property_value=search_value)
        # 2.查询公司的主营产品的信息
        results['公司与产品'] = self.search_relationships_n(rel_type="公司与产品", n_key=search_key,
                                                            n_value=search_value)
        # 3.查询公司的客户的信息
        results['公司与客户'] = self.search_relationships_n(rel_type="公司与客户", n_key=search_key,
                                                            n_value=search_value)
        # 4.查询公司和供应商的信息
        results['公司与供应商'] = self.search_relationships_n(rel_type="公司与供应商", n_key=search_key,
                                                              n_value=search_value)
        # 5.查询公司和环节的信息
        results['环节与公司'] = self.search_relationships_n(rel_type="公司与环节", n_key=search_key,
                                                            n_value=search_value)
        # 5.查询公司和新闻的信息
        results['公司与新闻'] = self.search_relationships_n(rel_type="公司与新闻", n_key=search_key,
                                                            n_value=search_value)
        # 1.查询公司的主营产品的信息
        results['产品'] = self.search_entities_m(n_label="公司", property_key=search_key, property_value=search_value,
                                                 m_label="产品")
        # 2.查询公司相关公司的信息
        results['公司'] = self.search_entities_m(n_label="公司", property_key=search_key, property_value=search_value,
                                                 m_label="公司")
        # 3.查询公司相关新闻的信息
        results['新闻'] = self.search_entities_m(n_label="公司", property_key=search_key, property_value=search_value,
                                                 m_label="新闻")
        # 4.查询公司相关环节的信息
        results['环节'] = self.search_entities_m(n_label="公司", property_key=search_key, property_value=search_value,
                                                 m_label="环节")
        # 查询股价信息
        results['股价信息'] = self.get_stock_info(results['查找的结点'][0]['code'])

        # 查询词云
        results['词云'] = self.generate_wordcloud_data(results['新闻'], topK=100)

        results['公司'].append(results['查找的结点'][0])
        return results

    def convert_to_list(self, dic):
        result_list = []
        for key, value in dic.items():
            result_list.append({"name": key, "value": value})
        return result_list

    # 查询某个环节地理信息的值
    def location_search(self, link, start_time, end_time):
        link_name = {
            "up": "上游（原材料）",
            "mid": "中游（四大材料+设备）",
            "down": "下游（电池制造）"
        }
        yy_s, mm_s, dd_s = start_time.split("-")
        yy_e, mm_e, dd_e = end_time.split("-")
        time_s = f"{yy_s}/{mm_s}/{dd_s}"
        time_e = f"{yy_e}/{mm_e}/{dd_e}"
        CQL = f'''MATCH p=(start {{name: '{link_name[link]}'}})-[r*1..3]-(c:company)
    WHERE NONE (rel IN r WHERE type(rel) = '上游') AND
          c.成立日期 >= '{time_s}' and c.成立日期 <= '{time_e}'
    WITH DISTINCT c.所属地区 AS 地区, c
    RETURN 地区, COUNT(c) AS 公司数量, SUM(toFloat(c.注册资本万元)) AS 注册资本总额,SUM(toFloat(c.pagerank)) AS 重要度
    ORDER BY 重要度 DESC
    '''
        print(CQL)
        results = self.graph.run(CQL)

        result_template = {
            '北京': 0,
            '天津': 0,
            '上海': 0,
            '重庆': 0,
            '河北': 0,
            '河南': 0,
            '云南': 0,
            '辽宁': 0,
            '黑龙江': 0,
            '湖南': 0,
            '安徽': 0,
            '山东': 0,
            '新疆': 0,
            '江苏': 0,
            '浙江': 0,
            '江西': 0,
            '湖北': 0,
            '广西': 0,
            '甘肃': 0,
            '山西': 0,
            '内蒙古': 0,
            '陕西': 0,
            '吉林': 0,
            '福建': 0,
            '贵州': 0,
            '广东': 0,
            '青海': 0,
            '西藏': 0,
            '四川': 0,
            '宁夏': 0,
            '海南': 0,
            '台湾': 0,
            '香港': 0,
            '澳门': 0
        }

        final_result = {
            "公司数量": result_template.copy(),
            "注册资本": result_template.copy(),
            "重要度": result_template.copy()
        }

        for record in results:
            if "——" in record["地区"]:
                continue
            province = record["地区"].split("-")[1][:-1]  # 提取省份名称
            if province == "内蒙古自治":
                province = "内蒙古"
            if province == "西藏自治":
                province = "西藏"
            if province in final_result["公司数量"]:
                final_result["公司数量"][province] += record["公司数量"]
                final_result["注册资本"][province] += record["注册资本总额"]
                final_result["重要度"][province] += record["重要度"]
        for key in final_result:
            final_result[key] = self.convert_to_list(final_result[key])
        with open("location.json", "w", encoding="utf-8") as f:
            json.dump(final_result, f, sort_keys=False, indent=4, ensure_ascii=False)
        return final_result

    def search_all(self):
        self.search_entities(label="公司")
        self.search_entities(label="产品")
        self.search_entities(label="新闻")
        self.search_entities(label="环节")
        self.search_relationships(rel_type="公司与环节")
        self.search_relationships(rel_type="环节与环节")
        self.search_relationships(rel_type="产品与产品")
        self.search_relationships(rel_type="公司与产品")
        self.search_relationships(rel_type="公司与供应商")
        self.search_relationships(rel_type="公司与客户")
        self.search_relationships(rel_type="公司与新闻")
        self.search_relationships(rel_type="环节与产品")


if __name__ == '__main__':
    # 数据库的用户名
    url = 'http://localhost:7474/browser/'
    user = "neo4j"
    password = "123456"
    test = Neo4jQuery(url, user, password)
    # test.search_company("name", "宁德时代")
    print(test.location_search(link="down", start_time="1970-10-10", end_time="2025-10-10"))
