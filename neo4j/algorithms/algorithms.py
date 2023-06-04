from py2neo import Graph
import json


class Neo4jGDS:
    '''初始化函数 self是类自己'''
    '''功能:运行连接neo4j,初始化查询结果保存路径'''
    '''
    参数:
        无
    返回:
        无
    '''

    def __init__(self, url, user, password):
        self.g = Graph(url, user=user, password=password, name="neo4j")
        self.created_graphs = set()
        self.get_all_graphs()
        self.node_tlist = {
            '上游': '环节与环节',
            '属于': '环节与环节',
            '提炼': '环节与环节',
            '构成': '环节与环节',
            '发展趋势': '环节与环节',
            '相关': '环节与公司',
            '相关产品': '环节与产品',
            '供应商': '公司与供应商',
            '客户': '公司与供应商',
            '主营产品': '公司与产品',
            '关联': '公司与新闻',
            '产品小类': '产品与产品',
            '上游材料': '产品与产品',
            '下游产品': '产品与产品'
        }

    def create_graph_name(self, ll=False, lc=False, lp=False, cc=False, cp=False, cn=False, pp=False):
        return f"graph{int(ll)}{int(lc)}{int(lp)}{int(cc)}{int(cp)}{int(cn)}{int(pp)}"

    def create_graph_cql(self, ll, lc, lp, cc, cp, cn, pp):
        graph_name = self.create_graph_name(ll, lc, lp, cc, cp, cn, pp)

        relationship_mapping = {
            "link_link": {
                "上游": "UNDIRECTED",
                "属于": "UNDIRECTED",
                "提炼": "UNDIRECTED",
                "构成": "UNDIRECTED",
                "发展趋势": "UNDIRECTED",
            },
            "link_company": {
                "相关": "UNDIRECTED",
            },
            "link_product": {
                "相关产品": "UNDIRECTED",
            },
            "company_company": {
                "供应商": "UNDIRECTED",
            },
            "company_product": {
                "主营产品": "UNDIRECTED",
            },
            "company_new": {
                "关联": "UNDIRECTED",
            },
            "product_product": {
                "产品小类": "UNDIRECTED",
                "上游材料": "UNDIRECTED",
                "下游产品": "UNDIRECTED",
            },
        }

        selected_relationships = {}
        if ll:
            selected_relationships.update(relationship_mapping["link_link"])
        if lc:
            selected_relationships.update(relationship_mapping["link_company"])
        if lp:
            selected_relationships.update(relationship_mapping["link_product"])
        if cc:
            selected_relationships.update(relationship_mapping["company_company"])
        if cp:
            selected_relationships.update(relationship_mapping["company_product"])
        if cn:
            selected_relationships.update(relationship_mapping["company_new"])
        if pp:
            selected_relationships.update(relationship_mapping["product_product"])

        relationships_str = ",\n    ".join(
            [f"{k}: {{type: '{k}',orientation: '{v}' }}" for k, v in selected_relationships.items()]
        )

        cql = f"""CALL gds.graph.project('{graph_name}',
        ['link', 'company', '产业链相关产品', 'news'],
        {{
        {relationships_str}
        }}
    )"""

        return cql

    '''
    删除图投影
    '''

    def drop_graph_cql(self, ll, lc, lp, cc, cp, cn, pp):
        graph_name = self.create_graph_name(ll, lc, lp, cc, cp, cn, pp)
        cql = f'CALL gds.graph.drop("{graph_name}")'
        return cql

    def get_all_graphs(self):
        try:
            result = self.g.run("CALL gds.graph.list() YIELD graphName")
            graph_names = [record["graphName"] for record in result]
            for graph_name in graph_names:
                self.created_graphs.add(graph_name)
        except KeyError:
            # 如果不存在图投影，不执行删除操作
            pass

    def find_path_cql(self, start_node_name, end_node_name, ll, lc, lp, cc, cp, cn, pp):
        graph_name = self.create_graph_name(ll, lc, lp, cc, cp, cn, pp)
        cql = f"""MATCH (a), (b)
WHERE a.name ='{start_node_name}' AND b.name = '{end_node_name}'
WITH id(a) AS sourceNodeId, id(b) AS targetNodeId
CALL gds.shortestPath.dijkstra.stream('{graph_name}', {{sourceNode: sourceNodeId, targetNode: targetNodeId}})
YIELD sourceNode, targetNode, path
WITH nodes(path) as nodes, relationships(path) as rels
UNWIND range(0, size(nodes) - 2) as idx
MATCH (src)-[originalRel]->(dst)
WHERE src = nodes[idx] AND dst = nodes[idx + 1]
WITH nodes, rels, originalRel, idx
RETURN [node in nodes | {{name: node.name, type: labels(node)[0], id: id(node)}}] as nodes,
       [i in range(0, size(rels) - 1) | {{
           from: nodes[i].name,
           to: nodes[i+1].name,
           id_from: id(nodes[i]),
           id_to: id(nodes[i+1]),
           rel: type(originalRel),
           from_type: labels(nodes[i])[0],
           to_type: labels(nodes[i+1])[0]
       }}] as relationships
"""

        return cql

    def data(self, nodes, relationships):
        formatted_result = {
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
        # Process nodes
        for node in nodes:
            if node['type'] == 'company':
                formatted_result['公司'].append(node)
            elif node['type'] == 'link':
                formatted_result['环节'].append(node)
            elif node['type'] == 'product':
                formatted_result['产品'].append(node)
            elif node['type'] == 'news':
                formatted_result['新闻'].append(node)

        # Process relationships
        for relationship in relationships:
            rel_key = self.node_tlist[relationship["rel"]]
            if rel_key in formatted_result:
                formatted_result[rel_key].append(relationship)
        return formatted_result

    def find_path(self, start_node_name, end_node_name, ll, lc, lp, cc, cp, cn, pp):
        graph_name = self.create_graph_name(ll, lc, lp, cc, cp, cn, pp)
        # 查看表是否创建，如果没有则创建
        if graph_name not in self.created_graphs:
            self.g.run(self.create_graph_cql(ll, lc, lp, cc, cp, cn, pp))
            self.created_graphs.add(graph_name)
        print(self.create_graph_cql(ll, lc, lp, cc, cp, cn, pp))
        print(self.find_path_cql(start_node_name, end_node_name, ll, lc, lp, cc, cp, cn, pp))
        result = self.g.run(self.find_path_cql(start_node_name, end_node_name, ll, lc, lp, cc, cp, cn, pp))
        try:
            nodes = [record["nodes"] for record in result][0]
            relationships = result["relationships"]
            print(nodes)
            print(relationships)
            # 将JSON字符串写入到response.json文件中
            result = self.data(nodes, relationships)
            with open('path.json', 'w', encoding="utf-8") as f:
                json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
        except:
            print("结果为空")
            result = {"环节": [],
                      "公司": [],
                      "产品": [],
                      "新闻": [],
                      "环节与环节": [],
                      "环节与公司": [],
                      "环节与产品": [],
                      "公司与供应商": [],
                      "公司与产品": [],
                      "公司与新闻": [],
                      "产品与产品": []}  # 返回一个空字典
        return result

    # 将计算后的pagerank值写入属性
    def pagerank(self):
        ll, lc, lp, cc, cp, cn, pp = True, True, True, True, True, False, True
        graph_name = self.create_graph_name(ll, lc, lp, cc, cp, cn, pp)
        # 查看表是否创建，如果没有则创建
        if graph_name not in self.created_graphs:
            self.g.run(self.create_graph_cql(ll, lc, lp, cc, cp, cn, pp))
            self.created_graphs.add(graph_name)
        # print(self.create_graph_cql(ll, lc, lp, cc, cp, cn, pp))
        # 计算pagerank并写会结点
        CQL1 = f'''CALL gds.pageRank.write('{graph_name}', {{
  maxIterations: 50,
  writeProperty: 'pagerank'
}})
YIELD nodePropertiesWritten;'''
        CQL2 = '''MATCH (n)
SET n.pagerank_sqrt = toFloat(round(1000 * sqrt(n.pagerank_raw))) / 1000;'''
        print(CQL1)
        try:
            # 计算pagerank值写回属性pagerank
            self.g.run(CQL1)
            # 保留三位小数
            self.g.run(CQL2)
            print("pagerank成功了！！！")
        except:
            print("pagerank失败了！！！")

    # 将计算后的社群id值再写入属性
    def Louvain(self):
        ll, lc, lp, cc, cp, cn, pp = True, True, True, True, True, True, True
        graph_name = self.create_graph_name(ll, lc, lp, cc, cp, cn, pp)
        # 查看表是否创建，如果没有则创建
        if graph_name not in self.created_graphs:
            self.g.run(self.create_graph_cql(ll, lc, lp, cc, cp, cn, pp))
            self.created_graphs.add(graph_name)
        CQL1 = f'''CALL gds.louvain.mutate('{graph_name}', {{mutateProperty:'communityId'}})'''
        CQL2 = f'''CALL gds.graph.streamNodeProperty('{graph_name}', 'communityId', ['link', 'company', '产业链相关产品', 'news'])
YIELD nodeId, propertyValue
WITH gds.util.asNode(nodeId) AS n, propertyValue AS communityId
SET n.communityId = communityId
'''
        try:
            # 计算communityId
            self.g.run(CQL1)
            # 将communityId写回属性
            self.g.run(CQL2)
            print("Louvain成功了！！！")
        except:
            print("Louvain失败了！！！")

    def community_find(self, comunity_id):
        CQL = f'''MATCH (n)-[r]-(m)
    WHERE n.communityId = {comunity_id} AND labels(n)[0] <> "news"
    AND m.communityId = {comunity_id} AND labels(m)[0] <> "news"
    WITH COLLECT(DISTINCT {{type: labels(n)[0], name: n.name, id: id(n), pagerank: n.pagerank}}) as nodes,
         COLLECT(DISTINCT {{from_type: labels(n)[0], id_from: id(n), to_type: labels(m)[0], rel: type(r),id_to: id(m),to: m.name, from: n.name}}) as relationships
    RETURN nodes, relationships'''
        result = self.g.run(CQL)
        print(CQL)

        # 添加额外的查询来获取所有具有n.communityId = 553的节点
        CQL_additional_nodes = f'''MATCH (n)
    WHERE n.communityId = {comunity_id} AND labels(n)[0] <> "news"
    WITH COLLECT(DISTINCT {{type: labels(n)[0], name: n.name, id: id(n), pagerank: n.pagerank}}) as additional_nodes
    RETURN additional_nodes'''

        additional_nodes_result = self.g.run(CQL_additional_nodes)

        try:
            nodes = [record["nodes"] for record in result][0]
            additional_nodes = [record["additional_nodes"] for record in additional_nodes_result][0]

            # 将额外查询的节点添加到nodes中，确保不会有重复
            for additional_node in additional_nodes:
                if additional_node not in nodes:
                    nodes.append(additional_node)

            relationships = result["relationships"]
            print(nodes)
            print(relationships)
            # 将JSON字符串写入到response.json文件中
            result = self.data(nodes, relationships)
            with open('path.json', 'w', encoding="utf-8") as f:
                json.dump(result, f, sort_keys=False, indent=4, ensure_ascii=False)
        except:
            print("结果为空")
            result = {"环节": [],
                      "公司": [],
                      "产品": [],
                      "新闻": [],
                      "环节与环节": [],
                      "环节与公司": [],
                      "环节与产品": [],
                      "公司与供应商": [],
                      "公司与产品": [],
                      "公司与新闻": [],
                      "产品与产品": []}  # 返回一个空字典
        return result


if __name__ == '__main__':
    # 数据库的用户名
    url = 'http://localhost:7474/browser/'
    user = "neo4j"
    password = "123456"
    test = Neo4jGDS(url, user, password)
    test.community_find(400)
