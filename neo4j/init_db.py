import os
import json

from py2neo import Graph, Node


# 类名
class MedicalGraph:
    '''初始化函数 self是类自己'''
    '''功能:初始化导入数据的路径，运行连接neo4j'''
    '''
    参数:
        无
    返回:
        无
    '''

    def __init__(self, url, user, password):
        # 初始化导入数据的路径
        # cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        cur_dir = os.path.dirname(__file__)
        print(cur_dir)
        self.company_path = os.path.join(cur_dir, "data\init_db\实体-公司.json")
        self.link_path = os.path.join(cur_dir, "data\init_db\实体-产业链环节.json")
        self.product_path = os.path.join(cur_dir, "data\init_db\实体-产品.json")
        self.news_path = os.path.join(cur_dir, "data\init_db\实体-新闻.json")
        self.company_link_path = os.path.join(cur_dir, "data\init_db\关系-公司与环节.json")
        self.link_link_path = os.path.join(cur_dir, "data\init_db\关系-环节与环节.json")
        self.link_product_path = os.path.join(cur_dir, "data\init_db\关系-环节与产品.json")
        self.company_product_path = os.path.join(cur_dir, "data\init_db\关系-公司与产品.json")
        self.product_product_path = os.path.join(cur_dir, "data\init_db\关系-产品与产品.json")
        self.company_suppliers_path = os.path.join(cur_dir, "data\init_db\关系-公司与供应商.json")
        self.company_client_path = os.path.join(cur_dir, "data\init_db\关系-公司与客户.json")
        self.company_news_path = os.path.join(cur_dir, "data\init_db\关系-公司与新闻.json")
        # 连接数据库
        # self.g = Graph('http://localhost:7474/browser/', user="neo4j",
        #                password="123456", name="neo4j")
        self.g = Graph(url, user=user, password=password, name="neo4j")
        #相关语句
        self.cql = {
            "产业链相关产品" : "MATCH (p:product)-[:相关产品]-(:link)SET p:产业链相关产品"
        }

    '''加载数据'''
    '''功能:读入用于初始化的json数据文件,并返回数组形式'''
    '''
    参数:
        filepath:文件位置
    返回:
        存有数据的数组
    '''

    def load_data(self, filepath):
        datas = []
        with open(filepath, 'r', encoding="utf-8") as f:
            data = json.load(f)
            for line in data:
                if not line:
                    continue
                datas.append(line)
        return datas

    '''建立节点'''
    '''功能:生成创建实体结点的CQL语言，并用neo4j运行'''
    '''
    参数:
        label:实体结点的类型
        nodes:结点的属性
    返回:
        1
    '''

    def create_node(self, label, nodes):
        count = 0
        for node in nodes:
            bodies = []
            for k, v in node.items():
                body = k + ":" + "'%s'" % v
                bodies.append(body)
            query_body = ', '.join(bodies)
            try:
                sql = "CREATE (:%s{%s})" % (label, query_body)
                # print(sql)
                self.g.run(sql)
                count += 1
            except:
                pass
            # 打印成功了几个，总数是几个
            print(label, count, len(nodes))
        return 1

    '''创建知识图谱实体节点类型'''
    '''功能:第一次初始化时生成所有的实体结点'''
    '''
    参数:
        无
    返回:
        无
    '''

    def create_graphnodes(self):
        # 导入数据
        company = self.load_data(self.company_path)
        link = self.load_data(self.link_path)
        product = self.load_data(self.product_path)
        news = self.load_data(self.news_path)
        # 生成实体结点
        self.create_node('company', company)
        self.create_node('link', link)
        self.create_node('product', product)
        self.create_node('news', news)
        # 结束打印共有多少个
        print("company" + str(len(company)) + "over!!")
        print("link" + str(len(link)) + "over!!")
        print("product" + str(len(product)) + "over!!")
        print("news" + str(len(news)) + "over!!")
        return

    '''创建实体关联边'''
    '''功能:针对普通的三元组，创建没有属性的关系'''
    '''参数:
        start_node:起始结点的类型
        end_node:终止结点的类型
        edges:存储关系的数组
        from_key:起始结点的关键字（依据这个在数据库中查找，一般是name）
        end_key:终止结点的关键字（依据这个在数据库中查找，一般是name）
    '''

    def create_relationship(self, start_node, end_node, edges, from_key, end_key):
        count = 0
        for edge in edges:
            try:
                p = edge[from_key]
                q = edge[end_key]
                rel = edge["rel"]
                query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s]->(q)" % (
                    start_node, end_node, p, q, rel)
                # print(query)
                self.g.run(query)
                count += 1
                print(rel, count, all)
            except Exception as e:
                print(e)
        return

    '''创建实体关联边'''
    '''功能:针对有属性的三元组，创建附带属性的关系'''
    '''参数:
        start_node:起始结点的类型
        end_node:终止结点的类型
        edges:存储关系的数组
        from_key:起始结点的关键字（依据这个在数据库中查找，一般是name）
        end_key:终止结点的关键字（依据这个在数据库中查找，一般是name）
    '''

    def create_relationship_attr(self, start_node, end_node, edges, from_key, end_key):
        count = 0
        for edge in edges:
            # 拿取除了重要结点之外的信息
            bodies = []
            for k, v in edge.items():
                if (k != from_key and k != end_key and k != 'rel'):
                    body = k + ":" + "'%s'" % v
                    bodies.append(body)
            query_body = ', '.join(bodies)
            print(query_body)
            try:
                p = edge[from_key]
                q = edge[end_key]
                rel = edge["rel"]
                if (rel == '主营产品'):
                    query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{%s}]->(q)" % (
                        start_node, end_node, p, q, rel, query_body)
                elif (rel == '相关产品'):
                    query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s]->(q)" % (
                        start_node, end_node, p, q, rel)
                else:
                    query = "match(p:%s),(q:%s) where p.fullname='%s'and q.name='%s' create (p)-[rel:%s{%s}]->(q)" % (
                        start_node, end_node, p, q, rel, query_body)
                #print(query)
                self.g.run(query)
                count += 1
                print(rel, count, len(edges))
            except:
                pass
        return

    '''创建实体关系边'''
    '''功能:第一次初始化时生成所有的关系边'''
    '''
    参数:
        无
    返回:
        无
    '''

    def create_graphrels(self):
        link_link = self.load_data(self.link_link_path)
        self.create_relationship(
            'link', 'link', link_link, "from", "to")
        company_link = self.load_data(self.company_link_path)
        self.create_relationship(
            'company', 'link', company_link, "company", "link")
        company_product = self.load_data(self.company_product_path)
        self.create_relationship_attr(
            'company', 'product', company_product, "company", "product")
        link_product = self.load_data(self.link_product_path)
        self.create_relationship_attr(
            'link', 'product', link_product, "产业链环节", "产品")
        product_product = self.load_data(self.product_product_path)
        self.create_relationship(
            'product', 'product', product_product, "from_entity", "to_entity")
        company_news = self.load_data(self.company_news_path)
        self.create_relationship(
            'news', 'company', company_news, "news", "company")
        company_suppliers = self.load_data(self.company_suppliers_path)
        self.create_relationship_attr(
            'company', 'company', company_suppliers, "from", "to")
        company_client = self.load_data(self.company_client_path)
        self.create_relationship_attr(
            'company', 'company', company_client, "from", "to")

    '''第一次初始化'''
    '''功能:第一次初始化时生成所有的关系边'''
    '''
    参数:
        无
    返回:
        无
    '''

    def build_graph(self):
        self.create_graphnodes()
        self.create_graphrels()
        #创建
        self.g.run(self.cql["产业链相关产品"])
        # link_product = self.load_data(self.link_product_path)
        # self.create_relationship_attr(
        #     'link', 'product', link_product, "产业链环节", "产品")

    def drop_graph(self):
        self.g.run("MATCH (n) DETACH DELETE n")
