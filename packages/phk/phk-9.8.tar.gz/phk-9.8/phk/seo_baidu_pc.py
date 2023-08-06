# -!- coding: utf-8 -!-
import requests, re, json, time
import pandas as pd
from copy import deepcopy
from math import ceil
from lxml import etree
from sqlalchemy import create_engine
# 同文件夹模块
from .req_base import req_base
from .req_baidu_pc import req_baidu_pc
from .deco import 失败重试



class seo_baidu_pc(req_baidu_pc):

    去除www匹配排名 = True
    网站内页排名有效 = True
    psino = False
    psino有效值 = (6, 1, 2)
    无排名报错 = False  # 查询没有排名时报错
    无排名返回 = 'rn+1'  # 无排名时的返回值
    打印查询结果 = True

    results最低占比 = False
    if type(results最低占比) is int: results最低占比 = float(results最低占比)
    # 接收False或浮点数, 范围为0-1, len(results) < rn 时报错, False表示关闭此功能

    def __init__(self):
        req_baidu_pc.__init__(self)

    def get(self, *vs, **kvs):
        r = req_baidu_pc.get(self, *vs, **kvs)
        if self.psino:
            psino = int(r.cookies.get('PSINO') or -1)
            if psino in self.psino有效值:
                if self.打印查询结果: print(f"psino: {psino}")
            else:
                if self.打印查询结果: print(f"psino: {psino}, 不符合要求")
                raise Exception("psino值不符合要求")
        return r

    # json查排名
    def kw_get_json排名(self, kw, domain, rn=None):
        rn = rn or self.rn
        r = self.json搜索(kw=kw, rn=rn)
        ranking = self.rjson_get_ranking(rjson=r, domain=domain)
        if not ranking:
            if self.无排名报错: raise Exception("self.无排名报错")
            elif self.无排名返回 == 'rn+1': return rn + 1
            else: return self.无排名返回
        if self.打印查询结果: print(f'{kw} - {domain} - {ranking}')
        return ranking

    # 传入 关键词 和 域名 和 熊掌号, 获取pc排名
    def kw_get_ranking(self, kw, domain=None, 熊掌号=None, rn=None, **kvs):
        rn = rn or self.rn
        if domain and domain.count('.') >= 3:
            # 分发到json
            r = self.json搜索(kw=kw, rn=rn)
            ranking = self.rjson_get_ranking(rjson=r, domain=domain)
        else:
            # 分发到普通html
            r = self.搜索(kw=kw, rn=rn)
            results = self.html_get_results(html=self.r_get_html(r=r))
            if type(self.results最低占比) is float:
                if len(results) < rn * self.results最低占比:
                    raise Exception("self.results最低占比")
            ranking = self.results_get_ranking(results=results, domain=domain, 熊掌号=熊掌号)
        if not ranking:
            if self.无排名报错: raise Exception("self.无排名报错")
            elif self.无排名返回 == 'rn+1': return rn + 1
            else: return self.无排名返回
        if self.打印查询结果: print(f'{kw} - {domain} - {熊掌号} - {ranking}')
        return ranking

    # 传入json类型的r和domain, 传出排名
    def rjson_get_ranking(self, rjson, domain):
        domain = self.url_get_domain(url=domain)
        if self.去除www匹配排名: domain = re.sub('^www\.', '', domain)
        rjson = rjson.json()["feed"]["entry"][:-1]
        result = [(x['pn'], re.sub(' |https:|http:|\.shtml|\.html', '', x['url'], 0)) for x in rjson]
        result = [(x[0], re.sub('/+', '/', '/' + x[1] + '/', 0)[1:-1]) for x in result]
        domain = re.sub('/+', '/', '/' + re.sub(' |https:|http:', '', domain, 0) + '/', 0)[1:-1]
        for i in result:
            if domain in i[1]: return int(i[0])
        return None


    #  传入 以排名为key的字典 和 domain, 传出排名
    def results_get_ranking(self, results, domain=None, 熊掌号=None):
        if domain:
            domain = self.url_get_domain(url=domain)
            if self.去除www匹配排名: domain = re.sub('^www\.', '', domain)
        for id, item in results.items():
            底部文字 = item.get('底部文字') or ''
            if domain and domain in self.url_get_domain(url=底部文字):
                if self.网站内页排名有效: return id
                elif not re.findall('/(.+)', re.sub('https?://| ', '', 底部文字)):
                    return id  # 不存在内页, 说明是首页
            if 熊掌号 and 熊掌号 in 底部文字: return id
        return None



class 百度关键词(seo_baidu_pc):

    def __init__(self):
        seo_baidu_pc.__init__(self)

    def domain_get_jsons(self, domain):
        retry = 失败重试(最高次数=30, 重试间隔=0, 每次失败执行=self.update_proxies)
        domain = self.url_get_domain(domain)
        res = []
        msg, 收录量 = retry(self.kw_get_num)(f"site:{domain}")
        if msg:
            totalpage = ceil(收录量 / 50)
            rn = 50
            for i in range(1, totalpage+1):
                print(f"\r{domain} 正在获取第{i}/{totalpage}页", end='    ')
                pn = (i - 1) * rn # 代表从哪个索引开始, 百度的索引是从0开始的
                url = f"https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=json&wd=site:{domain}&fenlei=256&rsv_pq=8fd634a100049b6a&rsv_t=cf61DU8FFmN%2FwF8kfppQ6QTCVzs%2Bo5IVb6YOJ5TOhOVo8ZEYyOlLvBO0ggE&rqlang=cn&rsv_dl=ib&rsv_sug3=6&rsv_sug2=0&rsv_btype=i&inputT=706&rsv_sug4=706&pn={pn}&rn={rn}"
                for i2 in range(30):
                    try:
                        ires = []
                        rj = self.get(url).json()
                        for x in rj['feed']['entry'][:-1]:
                            ires.append(dict(标题=x.get('title'), 网址=x.get('url')))
                        res += ires
                        break
                    except Exception as err:
                        print(err)
                        self.update_proxies()
        df = pd.DataFrame(res or dict(标题=[], 网址=[]))
        df['域名'] = domain
        return df
    
    def url_get_keywords(self, url):
        html = self.r_get_html(self.get(url, headers=self.base_headers))
        tree = etree.HTML(html)
        tags = set(x.attrib.get('content') for x in tree.xpath("//*[@name = 'keywords']"))
        return ','.join(x for x in tags if x) or '-'
    
    def df_set_tags(self, df, 标题字段='标题', 网址字段='网址', 源码关键词字段='源码关键词', 标题关键词字段='标题关键词'):
        retry = 失败重试(最高次数=30, 重试间隔=0, 每次失败执行=self.update_proxies)
        allkw = df.to_dict('records')
        kws = [x for x in allkw if not ((type(x.get(源码关键词字段)) is str) and x and (x.get(源码关键词字段) != '-'))]
        total = len(kws)
        for i, kw in enumerate(kws):
            print(f"\r{i}/{total}", end='    ')
            msg, kw[源码关键词字段] = retry(self.url_get_keywords)(kw[网址字段])
            if not msg: kw[源码关键词字段] = None
            kw[标题关键词字段] = self.标题_get_关键词(kw.get(标题字段, ''))
        return pd.DataFrame(kws)
    
    def 标题_get_关键词(self, 标题):
        分隔符 = ' _,|-'
        ts = re.findall(f"[^{分隔符}]+", 标题.replace('.', ''))
        return ','.join(x for x in set(ts) if x) or '-'
    
    def df_关键词拆分(self, df, 拆分字段=('源码关键词', '标题关键词')):
        res = []
        for kw in df.to_dict('records'):
            for cn in 拆分字段:
                text = kw.get(cn)
                if (type(text) is str) and text and (text != '-'):
                    res += [{**kw, cn:k, '关键词':k, '关键词长度':len(k), '关键词来源':cn} for k in text.split(',')]
                    break
            else: res.append(kw)
        df = pd.DataFrame(res)
        for cn in 拆分字段: df.drop(cn, axis=1, inplace=True)
        return df
    
    def df_字段修正(self, df):
        # 字段修正
        df = df.rename(columns=dict(关键词长度='长度'))
        df = pd.DataFrame(df, columns=['域名', '网址', '关键词', '长度', '关键词来源'])
        df['关键词来源'] = df['关键词来源'].replace('源码关键词', 'keywords').replace('标题关键词', 'title')
        # 去重
        dfs = [df for x,df in df.groupby(['网址', '关键词'])]
        df = pd.concat(dfs).sort_index()
        return df
    
    def df_导入数据库(self, df, sql, sheet):
        engine = create_engine(sql)
        df.to_sql(sheet, engine, index=False, if_exists='replace') #用append的话,就是追加
        return True
    
    def main(self, domains, save_path=False, sql=None, sheet=None, 最高次数=30):
        total_domains = len(domains)
        dfs = []
        for idomain,domain in enumerate(domains):
            print(f"\r{idomain}/{total_domains} {domain} 正在请求json", end='    ')
            df1 = self.domain_get_jsons(domain)
            print(f"\r{idomain}/{total_domains} {domain} 正在从源码获取keyword关键词", end='    ')
            df2 = self.df_set_tags(df1)
            print(f"\r{idomain}/{total_domains} {domain} 正在拆分关键词", end='    ')
            df3 = self.df_关键词拆分(df2)
            print(f"\r{idomain}/{total_domains} {domain} 正在修正字段", end='    ')
            df4 = self.df_字段修正(df3)
            dfs.append(df4)
        dfs = pd.concat(dfs)
        if save_path:
            print(f"\r正在保存到文件", end='    ')
            if save_path[-4:] == '.csv': dfs.to_csv(save_path, index=False)
            else: dfs.to_excel(save_path, index=False)
        if sql:
            print(f"\r正在导入到数据库", end='    ')
            retry = 失败重试(最高次数=30, 重试间隔=0)
            retry(self.df_导入数据库)(dfs, sql, sheet)
        return True
