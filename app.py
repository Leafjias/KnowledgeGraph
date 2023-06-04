from flask import Flask
import neo4j
from neo4j import algorithms
from flask.views import MethodView  # Flask提供的视图基类，方便处理HTTP请求
from flask import Flask, request, jsonify
from flask_cors import CORS  # 处理跨域问题

app = Flask(__name__)

# 跨域处理初始化
CORS().init_app(app)

# 数据库的用户名
url = 'http://localhost:7474/browser/'
user = "neo4j"
password = "123456"

'''
    参数:
        传入两个实体类别，和一个关系列表
    功能:去除relationships中没有实体对应的项
'''


def clean_relationships(entitie_from, entitie_to, relationships):
    valid_from = set([entity['id'] for entity in entitie_from])
    valid_to = set([entity['id'] for entity in entitie_to])

    cleaned_relationships = []
    for relationship in relationships:
        if relationship['id_from'] in valid_from and relationship['id_to'] in valid_to:
            cleaned_relationships.append(relationship)

    return cleaned_relationships


# 定义一个自定义命令create，用于创建数据库
@app.cli.command()
def create():
    # 连接数据库
    handler = neo4j.init_db.MedicalGraph(url, user, password)
    # 删除所有的表
    handler.drop_graph()
    # 创建所有的表
    handler.build_graph()
    # 计算社群关系
    algo = neo4j.algorithms.algorithms.Neo4jGDS(url, user, password)
    algo.Louvain()
    algo.pagerank()
    print('666')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# 首页图谱请求
# 定义一个类首页Api，继承自MethodView，用于处理GET请求
# 将情况编码比如link=true,company=true,product=true就是情况111
class NodesApi(MethodView):
    # 各种情况
    # 显示实体:环节，产品，公司，
    def query_case_111(self, export, start_time, end_time, result):
        # 实体
        result['环节'] = export.search_entities("环节")
        result['公司'] = export.search_time("公司", start_time, end_time)
        result['产品'] = export.search_entities("产业链相关产品")
        # 关系
        result['环节与环节'] = export.search_relationships(rel_type="环节与环节")
        result['环节与公司'] = export.search_relationships(rel_type="公司与环节")
        result['环节与产品'] = export.search_relationships(rel_type="环节与产品")
        result['产品与产品'] = export.search_relationships(rel_type="产业链相关产品与产业链相关产品")
        result['公司与产品'] = export.search_relationships(rel_type="公司与产业链相关产品")
        result['公司与供应商'] = export.search_time("公司与供应商", start_time, end_time)
        # 需要清理的关系：和公司相关的
        result['环节与公司'] = clean_relationships(result['公司'], result['环节'], result['环节与公司'])
        result['公司与产品'] = clean_relationships(result['公司'], result['产品'], result['公司与产品'])
        result['公司与供应商'] = clean_relationships(result['公司'], result['公司'], result['公司与供应商'])
        return result

    def query_case_110(self, export, start_time, end_time, result):
        # 实体
        result['环节'] = export.search_entities("环节")
        result['公司'] = export.search_time("公司", start_time, end_time)
        # 关系
        result['环节与环节'] = export.search_relationships(rel_type="环节与环节")
        result['环节与公司'] = export.search_relationships(rel_type="公司与环节")
        result['公司与供应商'] = export.search_time("公司与供应商", start_time, end_time)
        # 需要清理的关系：和公司相关的
        result['环节与公司'] = clean_relationships(result['公司'], result['环节'], result['环节与公司'])
        result['公司与供应商'] = clean_relationships(result['公司'], result['公司'], result['公司与供应商'])
        return result

    def query_case_101(self, export, start_time, end_time, result):
        # 实体
        result['环节'] = export.search_entities("环节")
        result['产品'] = export.search_entities("产业链相关产品")
        # 关系
        result['环节与环节'] = export.search_relationships(rel_type="环节与环节")
        result['环节与产品'] = export.search_relationships(rel_type="环节与产品")
        result['产品与产品'] = export.search_relationships(rel_type="产业链相关产品与产业链相关产品")
        return result

    def query_case_011(self, export, start_time, end_time, result):
        # 实体
        result['公司'] = export.search_time("公司", start_time, end_time)
        result['产品'] = export.search_entities(label="产业链相关产品")
        # 关系
        result['产品与产品'] = export.search_relationships(rel_type="产业链相关产品与产业链相关产品")
        result['公司与产品'] = export.search_relationships(rel_type="公司与产品")
        result['公司与供应商'] = export.search_time("公司与供应商", start_time, end_time)
        # 需要清理的关系：和公司相关的
        result['公司与产品'] = clean_relationships(result['公司'], result['产品'], result['公司与产品'])
        result['公司与供应商'] = clean_relationships(result['公司'], result['公司'], result['公司与供应商'])
        return result

    def query_case_100(self, export, start_time, end_time, result):
        # 实体
        result['环节'] = export.search_entities("环节")
        # 关系
        result['环节与环节'] = export.search_relationships(rel_type="环节与环节")
        return result

    def query_case_010(self, export, start_time, end_time, result):
        # 实体
        result['公司'] = export.search_time("公司", start_time, end_time)
        # 关系
        result['公司与供应商'] = export.search_time("公司与供应商", start_time, end_time)
        # 需要清理的关系：和公司相关的
        result['公司与供应商'] = clean_relationships(result['公司'], result['公司'], result['公司与供应商'])
        return result

    def query_case_001(self, export, start_time, end_time, result):
        # 实体
        result['产品'] = export.search_entities(label="产业链相关产品")
        # 关系
        result['产品与产品'] = export.search_relationships(rel_type="产业链相关产品与产业链相关产品")
        return result

    def query_other_cases(self, result):
        # 其他剩余情况
        return result

    # def query_case_111(self):
    def get(self, link, company, product, start_time, end_time):
        # 1.连接数据库
        export = neo4j.export_data.Neo4jQuery(url, user, password)
        # 2.创建结果的词典
        result = {'环节': [], '公司': [], '产品': [], '新闻': [],
                  '环节与环节': [], '环节与公司': [],
                  '环节与产品': [], '公司与供应商': [], '公司与新闻': [],
                  '公司与产品': [], '产品与产品': []}
        # 3.根据情况调用不同的函数
        query_map = {
            (True, True, True): self.query_case_111,
            (False, True, True): self.query_case_011,
            (True, False, True): self.query_case_101,
            (True, True, False): self.query_case_110,
            (True, False, False): self.query_case_100,
            (False, True, False): self.query_case_010,
            (False, False, True): self.query_case_001
        }
        # 4.拿取结果
        print((link, company, product))
        try:
            query_func = query_map.get((link, company, product), self.query_other_cases)
            results = query_func(export, start_time, end_time, result)  # 调用查询方法时传递参数
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
        # 5.判断返回值
        except:
            print(results)
            return {
                'status': 'failed',
                'message': '数据查询失败',
                'results': results
            }


# 请求格式http://192.168.31.221:5000/datas/?link=true&product=true&company=true&start_time=2010-10-10&end_time=2020-10-10
import json


@app.route('/datas', methods=['GET'])
def get_data():
    link = request.args.get('link') == 'true'
    product = request.args.get('product') == 'true'
    company = request.args.get('company') == 'true'
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    if not start_time:
        start_time = "1970-01-01"
    print(link, product, company, start_time, end_time)
    nodes_api = NodesApi()
    response = nodes_api.get(link, company, product, start_time, end_time)
    # response_json = json.dumps(response)

    # 将JSON字符串写入到response.json文件中
    with open('response.json', 'w', encoding="utf-8") as f:
        json.dump(response, f, sort_keys=False, indent=4, ensure_ascii=False)
    return response


# 查询地理位置信息
class LocationApi(MethodView):
    def merge_results(self, result, new_data):
        # 遍历 new_data 中的每个类别（如"公司数量"，"注册资本"等）
        for category in new_data:
            # 如果 result 字典中不存在此类别，则在 result 中创建一个空列表
            if category not in result:
                result[category] = []

            # 遍历 new_data 中该类别下的每个项目（如 {"name": "北京", "value": 0}）
            for item in new_data[category]:
                # 遍历 result 中该类别下的现有项目
                for existing_item in result[category]:
                    # 如果项目的 "name" 与现有项目的 "name" 相同
                    if item["name"] == existing_item["name"]:
                        # 将项目的 "value" 添加到现有项目的 "value"
                        existing_item["value"] += item["value"]
                        # 结束遍历现有项目的循环
                        break
                # 如果没有找到具有相同 "name" 的现有项目（即 "break" 未执行）
                else:
                    # 将新项目添加到 result 中的相应类别下
                    result[category].append(item)


    # 查询锂电池上中下游
    def get(self, up, mid, down, start_time, end_time):
        # 1.连接数据库
        export = neo4j.export_data.Neo4jQuery(url, user, password)

        result = {
            "公司数量": [],
            "注册资本": [],
            "重要度": []
        }

        if up:
            up_result = export.location_search("up", start_time, end_time)
            print(up_result)
            self.merge_results(result, up_result)

        if mid:
            mid_result = export.location_search("mid", start_time, end_time)
            self.merge_results(result, mid_result)

        if down:
            down_result = export.location_search("down", start_time, end_time)
            self.merge_results(result, down_result)

        # final_result = []
        # for key, value in result.items():
        #     final_result.extend([{"name": k, "value": v} for k, v in value.items()])

        with open("location.json", "w", encoding="utf-8") as f:
            json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
        return result

#http://192.168.153.221:5000/datas/location?up=true&mid=true&down=true&start_time=1970-10-10&end_time=2023-10-10
@app.route('/datas/location', methods=['GET'])
def get_location():
    up = request.args.get('up') == 'true'
    mid = request.args.get('mid') == 'true'
    down = request.args.get('down') == 'true'
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    if not start_time:
        start_time = "1970-01-01"
    print(up, mid, down, start_time, end_time)
    test = LocationApi()
    try:
        results = test.get(up=up, mid=mid, down=down, start_time=start_time, end_time=end_time)
        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': results
        }
    except:
        return {
            'status': 'success',
            'message': '数据查询失败',
            'results': results
        }


# 功能结点查找的api
class NodesFindApi(MethodView):
    # 根据关键字查找，返回一堆的结点
    def get_by_value(self, search_value):
        # 1.连接数据库
        export = neo4j.export_data.Neo4jQuery(url, user, password)
        results = export.search_entities(property_value=search_value)  # 调用查询方法时传递参数
        try:
            print()
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
            # 5.判断返回值
        except:
            return {
                'status': 'failed',
                'message': '数据查询失败',
                'results': ''
            }

    # 根据类型和值去查找，返回唯一的结点
    # 公司的使用公司代码
    # 需要查询的信息:公司的基本信息，公司和客户，公司和供应商，公司和主营产品，公司的股价信息，公司和新闻
    # 产品的使用产品名：产品基本信息，公司和产品，
    # 环节使用环节名：环节和公司
    def get_by_type(self, search_type, search_key, search_value):
        # 1.连接数据库
        export = neo4j.export_data.Neo4jQuery(url, user, password)
        # 2.根据类型和值去查找，返回唯一的结点
        if search_type == 'company':
            results = export.search_company(search_key, search_value)
        elif search_type == 'product':
            results = export.search_product(search_key, search_value)
        elif search_type == 'link':
            results = export.search_link(search_key, search_value)
        else:
            return {
                'status': 'failed',
                'message': '未知的查询类型',
                'results': ''
            }
        try:
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
            # 5.判断返回值
        except:
            return {
                'status': 'failed',
                'message': '数据查询失败',
                'results': ''
            }


# http://192.168.212.221:5000/datas/find/?value=宁德时代
# http://192.168.212.221:5000/datas/find/?value=宁德时代&type=company
@app.route('/datas/find/', methods=['GET'])
def find_data():
    search_value = request.args.get('value')
    search_type = request.args.get('type')
    search_key = request.args.get('key')
    # 没有指明类型
    if not search_type:
        print(search_value)
        nodes_api = NodesFindApi()
        response = nodes_api.get_by_value(search_value)
    # 指明类型精确查找
    else:
        print(search_value)
        print(search_type)
        print(search_key)
        if not search_key:
            search_key = "name"
        nodes_api = NodesFindApi()
        response = nodes_api.get_by_type(search_type, search_key, search_value)
    return response


# 最短路径查找查找的api
class PathFindApi(MethodView):
    # 根据起点终点名称去查，放回一堆结点
    # ll lc lp cc cp cn pp
    def get_by_name(self, start_node_name, end_node_name, ll=False, lc=False, lp=False, cc=False, cp=False, cn=False,
                    pp=False):
        # 1.连接数据库
        export = neo4j.algorithms.algorithms.Neo4jGDS(url, user, password)
        results = export.find_path(start_node_name, end_node_name, ll, lc, lp, cc, cp, cn, pp)
        try:
            print(results)
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results

            }
            # 5.判断返回值
        except:
            return {
                'status': 'failed',
                'message': '数据查询失败',
                'results': ''
            }


# /datas/find_path?start=&end=&ll=&lc&lp&cc&cp&cn&pp
@app.route('/datas/find_path', methods=['GET'])
def find_path():
    start_node_name = request.args.get('start')
    end_node_name = request.args.get('end')
    ll = request.args.get('ll', 'False') == 'true'
    lc = request.args.get('lc', 'False') == 'true'
    lp = request.args.get('lp', 'False') == 'true'
    cc = request.args.get('cc', 'False') == 'true'
    cp = request.args.get('cp', 'False') == 'true'
    cn = request.args.get('cn', 'False') == 'true'
    pp = request.args.get('pp', 'False') == 'true'
    print(ll, lc, lp, cc, cp, cn, pp)
    # 信息不全
    if not start_node_name or not end_node_name:
        print("信息不全，查找失败！")
        response = {
            'status': 'failed',
            'message': '信息不全，查找失败！',
            'results': ''
        }

    # 找到了
    else:
        print(start_node_name)
        print(end_node_name)
        nodes_api = PathFindApi()
        response = nodes_api.get_by_name(start_node_name, end_node_name, ll, lc, lp, cc, cp, cn, pp)
    return response


# 社群查找的api
class communityFindApi(MethodView):
    # 根据起点终点名称去查，放回一堆结点
    # ll lc lp cc cp cn pp
    def get_by_name(self, name, type):
        # 1.连接数据库
        find_id = neo4j.export_data.Neo4jQuery(url, user, password)
        # 获取社群名称
        communityid = find_id.search_entities(label=type, property_key="name", property_value=name)[0]["communityId"]
        print(communityid)
        export = neo4j.algorithms.algorithms.Neo4jGDS(url, user, password)
        # 2.获取社群编号
        results = export.community_find(communityid)
        try:
            print(results)
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results

            }
            # 5.判断返回值
        except:
            return {
                'status': 'failed',
                'message': '数据查询失败',
                'results': ''
            }


# 根据名字查询相关社群
# http://192.168.124.5:5000/datas/community?type=company&name=宁德时代
@app.route('/datas/community', methods=['GET'])
def find_community():
    type_list = {
        "company": "公司",
        "link": "环节",
        "product": "产品",
        "news": "环节"
    }
    type = type_list[request.args.get('type')]
    name = request.args.get('name')
    print(type, name)
    # 信息不全
    if not type or not name:
        print("信息不全，查找失败！")
        response = {
            'status': 'failed',
            'message': '信息不全，查找失败！',
            'results': ''
        }

    # 找到了
    else:
        nodes_api = communityFindApi()
        response = nodes_api.get_by_name(type=type, name=name)
    return response

# 首页demo请求
# 定义一个类首页Api，继承自MethodView，用于处理GET请求
# 将情况编码比如就是情况

@app.route('/datas/search_all', methods=['GET'])
def search_all():
    try:
        find = neo4j.demo.DemoQuery()
        results = find.search_all()
        return jsonify({
            'status': 'success',
            'message': '数据查询成功',
            'results': results
        })  # Flask的jsonify函数可以把Python字典转换成JSON格式
    except Exception as e:  # 捕获所有异常，实际开发中应当更明确异常类型
        return jsonify({
            'status': 'failed',
            'message': '数据查询失败: {}'.format(str(e)),
            'results': ''
        }), 500  # 返回500状态码表示服务器错误

if __name__ == '__main__':
    app.run()
