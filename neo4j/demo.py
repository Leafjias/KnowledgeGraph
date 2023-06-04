import os
import csv
import csv

class DemoQuery:
    '''初始化函数 self是类自己'''
    '''功能:运行连接neo4j,初始化查询结果保存路径'''
    '''
    参数:
        无
    返回:
        无
    '''

    def __init__(self):
        cur_dir = os.path.dirname(__file__)
        self.price_path = os.path.join(cur_dir, "data\\股价数据")
        self.news_company_path = os.path.join(cur_dir, "data\\demo\关系-公司与新闻.csv")
        self.news_path = os.path.join(cur_dir, "data\\demo\实体-新闻.csv")
        self.find_paths = {
            '公司': os.path.join(cur_dir, "data\\demo\实体-公司.csv"),
            '环节': os.path.join(cur_dir, "data\\demo\实体-环节.csv"),
            '产品': os.path.join(cur_dir, "data\\demo\实体-产品.csv"),
            '环节与环节': os.path.join(cur_dir, "data\\demo\关系-环节与环节.csv"),
            '公司与产品': os.path.join(cur_dir, "data\\demo\关系-公司与产品.csv"),
            '公司与供应商': os.path.join(cur_dir, "data\\demo\关系-公司与公司.csv"),
            '环节与产品': os.path.join(cur_dir, "data\\demo\关系-环节与产品.csv"),
        }

    def search_all(self):
        results = {'环节': [], '公司': [], '产品': [], '新闻': [],
                  '环节与环节': [], '环节与公司': [],
                  '环节与产品': [], '公司与供应商': [], '公司与新闻': [],
                  '公司与产品': [], '产品与产品': []}
        for key, path in self.find_paths.items():
            results[key] = []
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    results[key].append(row)
        return results

if __name__ == '__main__':
    demo = DemoQuery()
    print(demo.search_all())