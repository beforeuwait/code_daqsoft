# coding=utf8

__author__ = 'WangJiaWei'
"""
日志：
    2017-12-11： 开始开发正式版
    2017-12-12： 完成第一版开发
        测试过程中遇到的问题：比如某个关键词有 100 页，跑到第60页时候就可能中断掉了
    2017-12-15： 遇到的问题有，程序运行时间过长
                通过反复登录的方式，或者多进程来简短抓取时间
                封装了逻辑，将数据结构清洗模块进行封装
"""

import re
import os
import json
import random
import datetime
import time
import logging
import multiprocessing
import requests
from faker import Faker
from lxml import etree
from hdfs3 import HDFileSystem
import config

class LinkIpEngine(object):
    """作为linkip的引擎模块

    一是 登录逻辑
    二是 抓取逻辑
    """

    def __init__(self):
        self.down = LinkIpDownloader()
        self.spider = LinkIpSpider()
        self.pipe = LinkIpPipeline()

    def login_system(self):
        """
        登录模块
        """
        # 获取第一个response，主要是拿到jessionid
        home_page = self.down.get_home_page()
        # 处理并获取jessionid
        setting.cookie_dict['Cookies'] = setting.cookies_text % home_page['cookies'].get('JSESSIONID')
        login = self.down.login()

    def get_news_types(self):
        """根据不同的分类，抓取不同的关键词的舆情新闻

        每次获取列表都要对id_list进行清空
        以及 news_list进行清空
        """
        self.do_clear_list_id_file()
        # 这里提供3个进程，共用同一个session
        pool = multiprocessing.Pool(3)
        id_set = set(i.strip()for i in open(setting.news_list_ids_history_file, 'r', encoding=setting.encode))
        for key_word in setting.key_words:
            # self.get_data(key_word, id_set)
            pool.apply_async(self.get_data, (key_word, id_set,))
        pool.close()
        pool.join()

    def do_clear_list_id_file(self):
        """每次运行时候，都将把list以及id文件进行重置"""
        f = open(setting.news_list_ids_file, 'w+')
        f.close()

        f = open(setting.news_list_file, 'w+')
        f.close()

    def get_data(self, key_word, id_set):
        """
        每次都是请求 1个月前到当前请求的数据，如果id一旦重复，则停止
        """
        page, num, next_page = 1, 1, True
        while num <= page:
            response = setting.request_result
            response = self.down.get_data(num, key_word[1], response)
            # 处理cookie，出现新的jessionid则顺势添加
            cookie = response['cookies'].get('JSESSIONID', 'none')
            if cookie is not 'none':
                setting.cookie_dict['Cookies'] = setting.cookies_text % response['cookies'].get('JSESSIONID')
            news_list = setting.news_list
            news_list = self.spider.news_list(response['response'], news_list)
            page = news_list['page']
            if not news_list['list'] == []:
                next_page = self.pipe.save_news_list(news_list['list'], key_word[0], id_set)
            else:
                next_page = False
            #清理
            self.do_clear_data_struct(response=response, news_list=news_list)
            num += 1
            # 遇到已采集就停止
            if not next_page:
                break

    def get_info(self):
        """抓取每天舆情的快照

        每次开始前要将 news_info 清空
        """
        f = open(setting.news_info_file, 'w+')
        f.close()

        id_list = (i.strip() for i in open(setting.news_list_ids_file, 'r', encoding=setting.encode))
        for id in id_list:
            self.get_info_logic(id)


    def get_info_logic(self, id):
        response = setting.request_result
        response = self.down.get_info(id, response)
        info = setting.news_info_content
        if response['response'] is not 'bad_request':
            info = self.spider.news_info_content(response['response'], info)
            self.pipe.save_news_info(id, info)
        self.do_clear_data_struct(response=response, info=info)


    def do_clear_data_struct(self, **kwargs):
        # 清空字典
        response = kwargs.get('response', {})
        info = kwargs.get('info', {})
        news_list = kwargs.get('news_list', {})
        if not response == {}:
            response['response'] = 'bad_requests'
            response['url'] = ''
            response['cookies'] = ''
            response['data'] = ''
            response['status_code'] = ''
            response['error'] = ''
        elif not info == {}:
            info['content'] = ''
            info['source'] = ''
            info['author'] = ''
            info['time'] = ''
        elif not news_list == {}:
            news_list['list'].clear()
            news_list['page'] = 1
            news_list['json_error'] = False

    def load_2_hdfs(self):
        news_list = setting.news_list_file
        hdfs_news_list = setting.hdfs % (os.path.split(news_list)[1])
        news_info = setting.news_info_file
        hdfs_news_info = setting.hdfs % (os.path.split(news_info)[1])
        try:
            hdfs = HDFileSystem(host='192.168.100.178', port=8020)
            hdfs.put(news_list, hdfs_news_list)
            hdfs.put(news_info, hdfs_news_info)
        except:
            print('集群挂了')

class LinkIpDownloader(object):
    """sessin 模块

    """
    session = requests.session()

    def GET_request(self, *args):
        ''' GET请求模块 '''
        retry = 10
        response = args[2]
        response['url'] = args[0]
        response['params'] = args[3] if (len(args) == 4) else ''
        while retry > 0:
            args[1]['User-Agent'] = Faker().user_agent()
            # 休息0-1秒间的随机数
            time.sleep(random.random())
            try:
                if len(args) == 2:
                    res = self.session.get(args[0], headers=args[1], proxies=setting.proxy, timeout=30)
                else:
                    res = self.session.get(args[0], headers=args[1], params=args[3], proxies=setting.proxy, timeout=30)
                # 这里暂时只对 2xx和4xx做处理
                response['status_code'] = res.status_code
                if repr(res.status_code).startswith('2'):
                    response['response'] = res.content.decode(setting.encode)
                    response['cookies'] = res.cookies
                    break
                elif repr(res.status_code).startswith('4'):
                    args[1]['Proxy-Switch-Ip'] = 'yes'
                    continue
                else:
                    # 其他情况，继续请求
                    #
                    # 继续完善后续情况
                    args[1]['Proxy-Switch-Ip'] = 'yes'
                    continue
            except Exception as e:
                response['error'] = e
            retry -= 1
        return response

    def POST_request(self, *args):
        ''' POST请求模块 '''
        retry = 10
        response = args[2]
        response['url'] = args[0]
        response['data'] = args[3] if (len(args) == 4) else ''
        while retry > 0:
            args[1]['User-Agent'] = Faker().user_agent()
            try:
                res = self.session.post(args[0], headers=args[1], data=args[3],
                                        cookies=setting.cookie_dict, proxies=setting.proxy, timeout=30)
                # 这里暂时只对 2xx和4xx做处理
                response['status_code'] = res.status_code
                if repr(res.status_code).startswith('2'):
                    response['response'] = res.content.decode(setting.encode)
                    response['cookies'] = res.cookies
                    break
                elif repr(res.status_code).startswith('4'):
                    args[1]['Proxy-Switch-Ip'] = 'yes'
                    continue
                else:
                    # 其他情况，继续请求
                    #
                    # 继续完善后续情况
                    args[1]['Proxy-Switch-Ip'] = 'yes'
                    continue
            except Exception as e:
                response['error'] = e
            retry -= 1
        return response

    def get_home_page(self):
        url = setting.url_home
        headers = setting.headers
        response = self.GET_request(url, headers)
        return response

    def login(self):
        url = setting.url_login
        headers = setting.headers
        data = setting.login_data
        response = self.POST_request(url, headers, data)
        return response

    def get_data(self, num, theme_id, response):
        url = setting.url_data
        headers = setting.headers_xml
        data = setting.request_data
        data['currPage'] = num
        data['themeId'] = theme_id
        data['startDay'] = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M')
        data['endDay'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
        response = self.POST_request(url, headers, response, data)
        return response

    def get_info(self, id, response):
        url = setting.url_yq % id
        headers = setting.headers
        response = self.GET_request(url, headers, response)
        return response

class LinkIpSpider(object):
    """作为spider的存在

    各种解析规则
    """

    def news_list(self, html, news_list):
        js_dict = {}
        try:
            js_dict = json.loads(html)
        except Exception as e:
            news_list['error'] = e
        if not js_dict == {}:
            list_element = setting.list_elements
            news_list['page'] = js_dict.get('pageNum', 0)
            result_list = js_dict.get('result', [])
            for result in result_list:
                news_list['list'].append([str(result.get(i, ''))for i in list_element])
        return news_list

    def news_info_content(self, html, info):
        selector = etree.HTML(html)
        parse = setting.info_parse
        try:
            info['content'] = selector.xpath(parse['content'])[0].xpath('string(.)')
        except:
            info['content'] = ''
        info['source'] = selector.xpath(parse['source'])[0] if selector.xpath(parse['source']) else ''
        info['author'] = selector.xpath(parse['author'])[0] if selector.xpath(parse['author']) else ''
        info['time'] = selector.xpath(parse['time'])[0] if selector.xpath(parse['time']) else ''
        return info


class LinkIpPipeline(object):
    """管道

    作为数据存储清洗的地方
    """

    def save_news_list(self, news_list, type, id_set):
        """作为保存列表的存在

        同时保存一份 id 的列表用来避免重复录入
        :param news_list:
        """
        next_page = True
        text = ''
        record_id = ''
        for news in news_list:
            if news[0] not in id_set:
                news.append(type)
                text += re.sub('\r|\n| ', '', setting.blank.join(news)) + '\n'
                record_id += news[0] + '\n'
                next_page = True
            else:
                next_page = False

        with open(setting.news_list_file, 'a', encoding=setting.encode) as f:
            f.write(text)
        with open(setting.news_list_history_file, 'a', encoding=setting.encode) as f:
            f.write(text)
        with open(setting.news_list_ids_file, 'a', encoding=setting.encode) as f:
            f.write(record_id)
        with open(setting.news_list_ids_history_file, 'a', encoding=setting.encode) as f:
            f.write(record_id)
        return next_page

    def save_news_info(self, id, info):
        text = setting.blank.join([id, info['author'], info['time'], info['source'], info['content']])
        text = re.sub('\r|\n', '', text)
        with open(setting.news_info_file, 'a', encoding=setting.encode) as f:
            f.write(text + '\n')

        with open(setting.news_info_history_file, 'a', encoding=setting.encode) as f:
            f.write(text + '\n')

class setting:
    encode = config.ENCODE
    blank = config.BLANK
    url_home = config.URL_HOME
    url_login = config.URL_LOGIN
    request_result = config.REQUESTS_RESULT
    proxy = config.PROXIES
    headers = config.HEADERS
    headers_xml = config.HEADERS_XML
    cookies_text = config.COOKIE_TEXT
    login_data = config.USER_INFO
    request_data = config.REQUEST_DATA
    url_data = config.URL_DATA
    cookie_dict = config.COOKIE_DICT
    news_list = config.NEWS_LIST
    list_elements = config.LIST_ELEMENTS
    news_list_file = config.NEWS_LIST_FILE
    news_list_history_file = config.NEWS_LIST_HISTORY_FILE
    news_list_ids_file = config.NEWS_LIST_IDS_FILE
    news_list_ids_history_file = config.NEWS_LIST_IDS_HISTORY_FILE
    news_info_file = config.NEWS_INFO_FILE
    news_info_history_file = config.NEWS_INFO_HISTORY_FILE
    url_yq = config.URL_YQ
    news_info_content = config.NEWS_INFO_CONTENT
    info_parse = config.INFO_PARSE
    key_words = config.KEYWORDS
    hdfs = config.HDFS


class LinkIpSchedule(object):
    """这是一个简单的调度

    每小时，重复，反复的执行
    """
    def main(self):
        while True:
            start = time.time()
            lie = LinkIpEngine()
            lie.login_system()
            lie.get_news_types()
            lie.get_info()
            lie.load_2_hdfs()
            del lie
            end = time.time()
            rest_time = int(end-start)
            if rest_time < 3600:
                time.sleep(3600 - rest_time)


if __name__ == '__main__':
    lis = LinkIpSchedule()
    lis.main()