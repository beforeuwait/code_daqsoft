# coding=utf8
from __future__ import absolute_import

__author__ = 'wangjiawei'
__version__ = '0.1'

"""
先开发，暂不优化
2018-02-24 开始开发请求模块，配合错误处理
2018-02-26 各模块编写
2018-03-05 继续编写模块
2018-03-06 编辑模块， 关于 headers中referer的带法是个难题
2018-03-08 预期今天完成0.1版本开发
2018-03-12 预期需要一个 TODO
2018-03-21 娘的，很久没碰了，今天算开发完一个demo
"""
import requests
from faker import Faker
import time
# from request_unit.deal_error import


# TODO 主逻辑模块， 03-12开发

class RequestMainModel(object):

    """作为请求模块的的父类
    主逻辑模块，调度headers cookie等各模块的逻辑
    从request_api 获取任务，然后执行相应的逻辑
    """

    def __init__(self):
        self.headers_api = HeadersAPI()
        self.requests_api = RequestsAPI()

    def normal_main(self, req_seed):
        """
        这个作为通用请求模块主逻辑的主模块
        在没有出现新的逻辑部分
        讲使用该方法作为主逻辑

        :param req_seed: 传入的参数，请求用
        :return:
        """
        req_seed['headers'] = self.headers_api.headers_api(domain=req_seed.get('domain'),
                                                           data_type=req_seed.get('data_type', ''),
                                                           referer=req_seed.get('referer', ''))
        result = self.requests_api.request_api(req_seed)
        # todo:需要解决的事status_code的问题,来判断执行主逻辑
        # for k, v in result.items():
        #     print(k, '=====', v)
        return result

class HeadersAPI(object):
    """作为请求头处理的模块
    同时提供api，针对不同的请求拿出不同的headers
    从基础headers中提封装供相应的headers
    """

    def headers_api(self, **kwargs):
        """作为外部接口，知道调用谁的headers
        然后并封装返回
        * 针对，以后的可能出现 http/2.0 的headers，在api这里做分流，配置不同的engine来达到效果
        :return:
        """
        headers = {}
        headers = self._headers_engine(kwargs.get('domain'), kwargs.get('data_type'), kwargs.get('referer'))
        # 也可以先返回一个dict再去封装，减少内存的利用
        return headers

    def _headers_engine(self, domain, data_type, referer):
        """headers引擎，作用是封装好一个可提供给爬虫执行的headers
        :param domain:
        :return:
        """

        #获取最初的headers
        headers = self._base_headers()
        # 搭建好基类的 base headers，（也可以设计到定制），然后按照定制化请求头
        if data_type == 'str':
            """
            字符串类型的数据定制的头,通常没有需要额外添加的部分
            """
            pass
        elif data_type == 'json':
            """
            json类型定制的头
            * 调用字典的update方法，这样的好处就是，更新自己的数据
            """
            headers.update(self._json_headers())
        elif data_type == 'xml':
            """
            xml类型的定制头，
            现阶段暂时未遇到，单纯一个json格式可以满足需求
            """
            pass

        # 2.拼接一个host字段
        headers['Host'] = self._headers_host(domain)
        # 3. 定制请求头,针对不同的网站，定制不同的头

        # 4. 是否需要多个UA
        headers['User-Agent'] = self._ua_maker()
        # 5. 关于referer
        if referer:
            headers['Referer'] = referer
        return headers

    def _base_headers(self):
        """把headers基类返回给headers
        :return:
        """
        base = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return base

    def _headers_host(self, domain):
        """这里返回一个 host字段
        ** 具体怎么实现，有的website需要的host字段有变化

        ** 03.07更行此处逻辑,domain这里需要一个list，针对统一网站不同项目的host不同，需要定制
           domain_list = {
                'ctrip_hotel': 'hotels.ctrip.com',
                'ctrip_scenic': 'piao.ctrip.com',
                ........
           }
        ** 至于http/2.0 的请求头又如何定制
        :param domain:
        :return:
        """
        domain_list = {
            'ctrip_hotel': 'hotels.ctrip.com',
            'ctrip_scenic': 'piao.ctrip.com',
            'dianping_food': 'www.dianping.com',
            'dianping_shopping': 'www.dianping.com',
            'ly_hotel': 'www.ly.com',
            'baidu': 'www.baidu.com',
            'dianping': 'www.dianping.com',
        }
        host = '{0}'.format(domain_list.get(domain))
        return host

    def _headers_referer(self):
        """添加 referer 这个字段
        针对有的网站的反爬虫认证有关于确认referer这个字段
        因此我们需要定制一个添加referer的方法

        * 至于referer的带法，
        :return:
        """
        pass

    def _ua_maker(self):
        return Faker().user_agent()

    def _json_headers(self):
        """请求头关于json格式数据请求

        :return:
        """
        json_headers = {
            'Accept': 'application/json, text/javascript',
            'X-Request': 'JSON',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/64.0.3282.186 Safari/537.36'),
        }
        return json_headers

    def _xx_maker(self):
        """针对不同的网站或者网页，定制请求头
        与其是定制，其实是把提前设置好的请求头找到，并放进去
        :return:
        """
        pass

class CookieAPI(object):
    """执行cookie处理的模块
    提供api，完成cookie处理/加载的动作
    """

    def cookie_switch(self, cookie_info):
        """
        作为筛选器，就是为其装备各种所需的cookie
        :param cookie_info:
        :return:
        """
        if cookie_info == 'baidu_tieba':
            return self.baidu_tieba()
        elif cookie_info == 'dianping_cmt':
            return None
        elif cookie_info == 'dianping_info':
            return None
        elif cookie_info == 'dianping_food_list':
            return self.dianping_food_list()

    def baidu_tieba(self):
        cookie = {'Cookie': ('BAIDUID=00FDDFB865205E569DFB828760CE2DDE:'
                             'FG=1;'
                             ' BIDUPSID=00FDDFB865205E569DFB828760CE2DDE;'
                             ' PSTM=1519116523;'
                             ' BDUSS=DBXLWdUUHBUV2pOc0RpdDlyOE83QkJtcjNRUXRkM3pu'
                             'QzU2SWYzT1RpMXhZcmhhQVFBQUFBJCQAAAAAAAAAAAEAAADzyq'
                             'AYsK6z1LzQyfq3uQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHVkFpx1ZBaT;'
                             ' TIEBA_USERTYPE=59831fa6e4e4c0875d0a49ab;'
                             ' STOKEN=8243706d62f9ba145342902ddecef4783d20e15e8616590c1bc77d10b91497ca;'
                             ' TIEBAUID=69b534f8e3a2ecdf0c852a15;'
                             ' bdshare_firstime=1519450995355;'
                             ' BDORZ=B490B5EBF6F3CD402E515D22BCDA1598;'
                             ' H_PS_PSSID=1444_21094;'
                             ' Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1519896519,1519956045,1520211218,1520387111;'
                             ' BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0;'
                             ' PSINO=3;'
                             ' Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1520405011')
                  }
        return cookie

    def dianping_food_list(self):
        cookie = {
            'Cookie': ('_lxsdk_cuid=162422c252dc8-0fcacc5ef594bc-33627805-13c680-162422c252ec8;'
                       ' _lxsdk=162422c252dc8-0fcacc5ef594bc-33627805-13c680-162422c252ec8;'
                       ' _hc.v=d5577e34-76fc-368f-4031-71cdbdcfe638.1521528612;'
                       ' dper=668d1f13c70683432c25a44d18614673879dea2f3c2c030adc1c685ac6298b8e;'
                       ' ua=_%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E4%B8%AD%E5%80%BC%E5%AE%9A%E7%90%86;'
                       ' ctu=a91d9076090ffb8fe11e3982711567ed049a427fb68f247a21e59c84a4ed9fac;'
                       ' s_ViewType=10;'
                       ' aburl=1;'
                       ' __mta=189209876.1521528632529.1521528632529.1521528632534.2;'
                       ' ll=7fd06e815b796be3df069dec7836c3df;'
                       ' cy=8;'
                       ' cye=chengdu;'
                       ' _lxsdk_s=162475393e8-06-9fa-9c%7C%7C25')
        }
        return cookie

class ProxyPoolAPI(object):
    """代理池开关
    针对请求中是否需要代理，从而机动的判断
    """

    @staticmethod
    def proxy():
        proxies = {
            "http": "http://HY3JE71Z6CDS782P:CE68530DAD880F3B@proxy.abuyun.com:9010",
            "https": "http://HY3JE71Z6CDS782P:CE68530DAD880F3B@proxy.abuyun.com:9010",
        }
        return proxies

class StatusCodeHandle(object):
    """作为一个控制模块，通过处理状态码，告诉主模块流程执行状态
    code：200 则进行下一步
    code：300 相应处理
    code：4xx 相应处理
    """
    pass

class ErrorHandlerAPI(object):
    """错误处理的
    集合可能出现的错误，并提供相应的API
    """
    pass

class RequestsAPI(CookieAPI, StatusCodeHandle, ErrorHandlerAPI, ProxyPoolAPI):
    """执行请求的模块
    提供api，完成请求这个动作
    """

    def request_api(self, req_seed):
        """外部接口
        接受请求，同时调用引擎，最后返回结果
        * 暂时叫 data，想好了新的名字再确认
        *
        :param req_seed: 种子信息
        :return:
        """

        # 1. 接口被调用，找到引擎，告诉引擎执行类型
        # 2. 接受返回结果，该接口调用结束

        # 传入的数据结构也要确定

        # for k, v in data.items():
        #     print(k, v)
        result = self._request_engine(req_seed)
        return result

    def _request_engine(self, req_seed):
        """request引擎
        负责从request_api那获取请求任务，并解析，执行任务
        :param req_seed: 种子信息
        :return:
        """
        # 1.先解析是GET任务还是POST任务
        method = req_seed.get('method')
        # 2.根据解析的任务结果选择相应的请求处理方式
        # 在处理get/post 请求时候，除了登录等个别的对post要求严格的请求方式中
        # get/post是互通的
        if method == 'GET':
            # get请求的处理逻辑
            data = self._get_method(req_seed)
        elif method == 'POST':
            # post请求的处理逻辑
            data = self._post_method(req_seed)
        else:
            # 针对 option/put/delete的处理逻辑
            pass
        return req_seed

    def _deal_request_method(self):
        """选择器，调用不同的方法

        这个模块暂时不需要，取消掉， 通过 engine就可以完成，后续需要封装，再启用
        :return:
        """
        pass

    def _get_method(self, req_seed):
        """GET请求模块
        因为继承自 cookie ，status， error模块，这里就要有相应的cookie处理，反馈机制的status处理机制
        :return:
        """
        # cookie 的 switch
        cookies = {}
        if not req_seed.get('cookie_info', '') == '':
            # 需要装载cookie
            cookies = self.cookie_switch(req_seed.get('cookie_info'))
        # # 带参数和不带参数的处理方法
        if not req_seed.get('params', '') == '' and cookies == {}:
            response = requests.get(req_seed.get('url'), headers=req_seed.get('headers'), params=req_seed.get('params'), proxies=self.proxy())
        elif not req_seed.get('params', '') == '' and cookies != {}:
            response = requests.get(req_seed.get('url'), headers=req_seed.get('headers'), cookies=cookies, params=req_seed.get('params'), proxies=self.proxy())
        elif req_seed.get('params', '') == '' and cookies == {}:
            response = requests.get(req_seed.get('url'), headers=req_seed.get('headers'), proxies=self.proxy())
        else:
            response = requests.get(req_seed.get('url'), headers=req_seed.get('headers'), cookies=cookies, proxies=self.proxy())
        try:
            req_seed['html'] = response.content.decode('utf8')
        except:
            # 编码出错的情况下
            req_seed['html'] = response.content.decode('gbk')
        # 开始对status_code 处理， 这里的原则就是，200 通过，300无视，400/500处理
        req_seed['status_code'] = response.status_code
        # req_seed['cookies'] = response.cookies
        return req_seed

    def _post_method(self, data):
        """POST请求模块
        因为继承自 cookie ，status， error模块，这里就要有相应的cookie处理，反馈机制的status处理机制
        :return:
        """
        # cookie 的 switch
        cookies = {}
        if not data.get('cookie_info', '') == '':
            # 需要装载cookie
            cookies = self.cookie_switch(data.get('cookie_info'))
        # 涉及到，这个payloads 是str 还是 {} 还是 json
        # 选择器

        # 带参数和不带参数的处理方法
        if not cookies == {}:
            response = requests.post(data.get('url'), headers=data.get('headers'), data=data.get('payloads'))
        else:
            response = requests.post(data.get('url'), headers=data.get('headers'), cookies=cookies, data=data.get('payloads'))
        try:
            data['html'] = response.content.decode('utf8')
        except:
            # 编码出错的情况下
            data['html'] = response.content.decode('gbk')
        # 开始对status_code 处理， 这里的原则就是，200 通过，300无视，400/500处理
        data['status_code'] = response.status_code
        # data['cookies'] = response.cookies
        return data

# TODO 03-12 模块，需要编写开发

class RequestModelAPI(object):
    """向外部提供的一个api,作为对这个模块的条用，接收参数，预处理
    1. 判断是什么请求
    2. 处理参数 不仅是 params和payloads
    3. 对于处理调用main model
    """

    def execute(self, seed):
        # 获取种子，准备抓取
        request_seed = self.construct_request_seed(seed)
        req_mm = RequestMainModel()
        # 普通的抓取
        result = req_mm.normal_main(request_seed)
        # 判断是否要重抓
        result.update({'retry': self.status_handler(result.get('status_code'))})
        return result

    def status_handler(self, status_code):
        if status_code >= 200 and status_code < 300:
            # 正常访问，通过
            return 'no'
        elif status_code >= 300 and status_code < 400:
            # 转跳，这个出现可能性不高，暂不处理
            return 'no'
        elif status_code >= 400 and status_code <600:
            # 把4xx 和 5 xx 都放在一起，重新请求
            return 'yes'

    def construct_request_seed(self, seed):
        request_seed = {
            'method': '',
            'domain': '',
            'data_type': '',
            'headers': '',
            'referer': '',
            'url': '',
            'params': '',
            'payloads': '',
            'payloads_type': '',
            'html': '',
            'status_code': '',
            'error_info': '',
            'cookie_info': '',
            'retry': 'no',
            'next_page': 'no',
            'data': '',
            # 需要topic，针对反爬虫，不同的topic对于的cookie不同
        }
        # 装载url
        request_seed.update({'url': seed.get('url')})
        # 装载方法
        request_seed.update({'method': seed.get('method')})
        # 装载domian
        request_seed.update({'domain': seed.get('domain')})
        # 装载referer
        request_seed.update({'referer': seed.get('referer')})
        # 装载topic/cookie_info
        request_seed.update({'cookie_info': seed.get('topic')})
        return request_seed

