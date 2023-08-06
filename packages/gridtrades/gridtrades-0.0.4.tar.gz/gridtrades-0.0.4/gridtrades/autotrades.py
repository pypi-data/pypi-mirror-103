# !/usr/bin/env python
# coding: utf-8

class autotrades:
    # 针对一些特殊情况，比如直接暴跌，暴涨，如果变化率超过多少，比如说不买，或者不卖，操作单位严格控制在1份网格单位数量上。
    # 连续上涨时，如果空仓怎么应对？
    # 连续上涨时，如果临近价格没有存货，怎么处理？
    # 连续上涨时，如果涨势过快，暂停卖出，
    # 连续下跌时，比市价高的存货仓位怎么处理？
    # 连续下跌时，判断趋势，如果下跌动能过强，则停止网格买入逻辑

    # 实际成交价格比触发交割低了，处理的逻辑如何设置？如果连续走低，自动调整触发价格？还是创建新的策略？
    # 触发价格如何评估？ 按照成交最低，最高的平均值？或者取成交量中位值，对应的价格。。。

    # 网格数量的评估：前后两次的差值，形成一个差值序列，计算差值的可信区间
    # 如何计算最小平均价格间距？0.002的费率，买入+卖出=0.004， (卖出费用-买入费用) >= (卖出费用+买入费用)*0.002
    # 以中枢价格为初始买入价格，求最小利润卖出价格；
    # sellprice - (4.363+2.92)/2> = (sellprice + (4.363+2.92)/2)*0.002
    # sellprice-3.6415 >= 0.002 * sellprice + 3.6415*0.002
    # 0.998 * sellprice >= 3.6415 * 1.002
    # sellprice >= 3.6415 * 1.002 / 0.998
    # sellprice >= 3.6560951904 ~= 3.6561
    # interprice >= 3.6561-3.6415 = 0.0136
    # bug: 靠近买入点多少的比例的时候，触发买入，直接用前后两次成交价格，来判断挂单，预算资金很快就会用玩
    # bug: 靠近卖出点多少的比例的时候，触发卖出，直接用前后两次成交价格，来判断挂吃单。
    # 总体逻辑正确的，需要有一个方法定期输出 网格收益、现货市场价格、总投入，浮动盈亏

    # 逻辑梳理：
    # 1、买入时，手续费扣除的是现货，因此以usdt计价时，没有手续费，但是可卖现货少了0.2%，卖出数量也需要记录交易对中。。。
    # 2、卖出时，手续费扣除的是USDT，卖出数量为买入数量的0.998，手续费为成交价格的0.2%
    # 重新梳理收益平衡表----修正
    # bug：如果卖单，分多次成交，卖出状态更新出错。。。 修正。。。
    # 长时间使用，系统会自动断开，需要有一个守候进程
    # 每次动态调整购买数量？使一次投资保持在最小投入量1USDT？

    import datetime
    import math
    import os
    import time
    import hashlib
    import hmac
    import random

    import requests
    import json
    import logging
    import sys

    # pip install -U websocket_client
    from websocket import WebSocketApp

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s",
                        handlers=[
                            logging.FileHandler(filename='/opt/xoenmap/gateio/log/run.log'),
                            logging.StreamHandler(sys.stdout)
                        ])
    logger = logging.getLogger(__name__)
    # 只读api_key
    readonly_api_key = ''
    # 只读api_secret
    readonly_api_secret = ''
    # 可写api_key
    write_api_key = ''
    # 可写api_secret
    write_api_secret = ''

    # 文本的false和python的布尔类型的False不一致，需要这里替换下
    false = False
    # 文本的true和python的布尔类型的True不一致，需要这里替换下
    true = True

    # 计算七天最小值，最大值
    minValue = 0
    maxValue = 0

    # 买入费
    taker_fee = 0.002
    # 卖出费
    maker_fee = 0.002
    # 最后一条交易价格
    lasttradeprice = 0
    # 倒数第二条交易价格
    lasttwotradeprice = 0

    # 当前货币对
    currencypair = 'DOGE_USDT'

    # 触发价格与成交价格的比例，小于该比例值，开始挂单
    trade_grid_rate = 0.001

    # 触发价格
    beginprice = 3.425
    # 止损价格
    stoplossprice = 2.92
    # 止盈价格
    stopgainprice = 4.50

    # 网格价差
    pricepercell = 0.04

    # 总预算
    totalmoney = 0.6

    # 已支出金额
    totaloutcoming = 0
    # 可用金额
    canusemoney = 0

    # 初始投入比例
    firstinvestradio = 0.2

    # 每单元投资额
    invpercell = 1
    # 网格价格序列
    gridprices = [2.92,
                  2.96,
                  3,
                  3.04,
                  3.08,
                  3.12,
                  3.16,
                  3.2,
                  3.24,
                  3.28,
                  3.32,
                  3.36,
                  3.4,
                  3.44,
                  3.48,
                  3.52,
                  3.56,
                  3.6,
                  3.64,
                  3.8,
                  3.72,
                  3.76,
                  3.8,
                  3.84,
                  3.88,
                  3.92,
                  3.96,
                  4,
                  4.04,
                  4.08,
                  4.12,
                  4.16,
                  4.2,
                  4.24,
                  4.28,
                  4.32,
                  4.36,
                  4.4,
                  4.44
                  ]

    # 网格成交列表
    gridtradelist = {}
    # 网格交易是否启动
    gridbuyandcellstart = 0

    # 日志输出地址
    logoutpath = ''


    class GateWebSocketApp(WebSocketApp):

        def __init__(self, url, api_key, api_secret, **kwargs):
            super(GateWebSocketApp, self).__init__(url, **kwargs)
            self._api_key = api_key
            self._api_secret = api_secret

        def _send_ping(self, interval, event):
            while not event.wait(interval):
                self.last_ping_tm = time.time()
                if self.sock:
                    try:
                        self.sock.ping()
                    except Exception as ex:
                        # logger.warning("send_ping routine terminated: {}".format(ex))
                        break
                    try:
                        self._request("spot.ping", auth_required=False)
                    except Exception as e:
                        raise e

        def _request(self, channel, event=None, payload=None, auth_required=True):
            current_time = int(time.time())
            data = {
                "time": current_time,
                "channel": channel,
                "event": event,
                "payload": payload,
            }
            if auth_required:
                message = 'channel=%s&event=%s&time=%d' % (channel, event, current_time)
                data['auth'] = {
                    "method": "api_key",
                    "KEY": self._api_key,
                    "SIGN": self.get_sign(message),
                }
            data = json.dumps(data)
            # logger.info('request: %s', data)
            self.send(data)

        def get_sign(self, message):
            h = hmac.new(self._api_secret.encode("utf8"), message.encode("utf8"), hashlib.sha512)
            return h.hexdigest()

        def subscribe(self, channel, payload=None, auth_required=True):
            self._request(channel, "subscribe", payload, auth_required)

        def unsubscribe(self, channel, payload=None, auth_required=True):
            self._request(channel, "unsubscribe", payload, auth_required)


    # 有写权限的签名
    def gen_trade_sign(method, url, query_string=None, payload_string=None):
        key = write_api_key  # api_key
        secret = write_api_secret  # api_secret

        t = time.time()
        m = hashlib.sha512()
        m.update((payload_string or "").encode('utf-8'))
        hashed_payload = m.hexdigest()
        s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
        sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
        return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}


    def gen_sign(method, url, query_string=None, payload_string=None):
        key = readonly_api_key  # api_key
        secret = readonly_api_secret  # api_secret

        t = time.time()
        m = hashlib.sha512()
        m.update((payload_string or "").encode('utf-8'))
        hashed_payload = m.hexdigest()
        s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
        sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
        return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}


    def timestamp_datetime(value):
        format = '%Y-%m-%d %H:%M:%S'
        # value为传入的值为时间戳(整形)，如：1332888820
        value = time.localtime(value)
        ## 经过localtime转换后变成
        ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
        # 最后再经过strftime函数转换为正常日期格式。
        dt = time.strftime(format, value)
        return dt


    def datetime_timestamp(dt):
        # dt为字符串
        # 中间过程，一般都需要将字符串转化为时间数组
        time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
        # 将"2012-03-28 06:53:40"转化为时间戳
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return int(s)


    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


    # # 查询订单列表
    # url = '/spot/orders'
    # query_param = 'currency_pair=' + currencypair + '&status=open'
    # # `gen_sign` 的实现参考认证一章
    # sign_headers = gen_sign('GET', prefix + url, query_param)
    # headers.update(sign_headers)
    # r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    # print(r.json())
    #
    # query_param = 'currency_pair=' + currencypair + '&status=finished'
    # # `gen_sign` 的实现参考认证一章
    # sign_headers = gen_sign('GET', prefix + url, query_param)
    # headers.update(sign_headers)
    # r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    # print(r.json())


    # cancelled 不支持查询
    # query_param = 'currency_pair='+currencypair+'&status=canceled'
    # # `gen_sign` 的实现参考认证一章
    # sign_headers = gen_sign('GET', prefix + url, query_param)
    # headers.update(sign_headers)
    # r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    # print(r.json())

    # 获取所有货币
    # url = '/spot/currencies'
    # query_param = ''
    # r = requests.request('GET', host + prefix + url, headers=headers)
    # print(r.json())

    # 获取所有交易对
    # url = '/spot/currency_pairs'
    # query_param = ''
    # r = requests.request('GET', host + prefix + url, headers=headers)
    # print(r.json())

    # 获取市场深度信息（实时的）
    # url = '/spot/order_book'
    # query_param = 'currency_pair='+currencypair+'&interval=0.05&limit=20&with_id=true'
    # r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    # print(r.json())

    # 市场k线图
    def getcandlesticks(interval, fromtime, totime, currencypair):
        url = '/spot/candlesticks'
        query_param = 'currency_pair=' + currencypair + '&interval=' + interval + '&from=' + str(fromtime) + '&to=' + str(
            totime)
        r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
        print(r.json())

        global minValue
        global maxValue
        # 计算每天平均价格
        for item in r.json()[0:]:
            print(item[0] + ":" + str((float(item[3]) + float(item[4])) / 2))

        for item in r.json()[0:]:
            if minValue == 0:
                minValue = float(item[4])
            else:
                minValue = min(minValue, float(item[4]))

            if maxValue == 0:
                maxValue = float(item[3])
            else:
                maxValue = max(maxValue, float(item[3]))

        print("最高：" + str(maxValue) + "; 最低: " + str(minValue))


    # 获取交易费率
    url = '/wallet/fee'
    query_param = ''
    # `gen_sign` 的实现参考认证一章
    sign_headers = gen_sign('GET', prefix + url, query_param)
    headers.update(sign_headers)
    print('signature headers: %s' % sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    print(r.json())

    # jsonobj = gettrades(0)
    # print(jsonobj)
    # print(jsonobj[-1])
    # # 获取最后一条成交价格,不管买单，还是卖单
    # lasttradeprice = float(jsonobj[-1]['price'])
    # print(lasttradeprice)
    # # 获取最后二条成交价格,不管买单，还是卖单
    # lasttwotradeprice = float(jsonobj[-2]['price'])
    # print(lasttwotradeprice)
    taker_fee = float(r.json()['taker_fee'])
    # 卖出费
    maker_fee = float(r.json()['maker_fee'])


    # 获取实时交易明细
    def gettrades(lastid):
        tradeapiurl = '/spot/trades'
        if lastid == 0:
            trade_query_param = 'currency_pair=' + currencypair + '&limit=100&reverse=false'
        else:
            trade_query_param = 'currency_pair=' + currencypair + '&limit=100&reverse=false&' + 'last_id=' + str(lastid)

        r = requests.request('GET', host + prefix + tradeapiurl + "?" + trade_query_param, headers=headers)
        return r.json()


    # 获取订单详情
    def getorderdetail(orderid):
        url = '/spot/orders/' + str(orderid)
        query_param = 'currency_pair=' + currencypair
        # `gen_sign` 的实现参考认证一章
        sign_headers = gen_sign('GET', prefix + url, query_param)
        headers.update(sign_headers)
        r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
        # print(r.json())
        return r.json()


    # 获取最近的网格价格
    def getfitgridprice(lastprice):
        # 找到最接近的价格
        global gridprices
        fitprice = min(gridprices, key=lambda x: abs(x - lastprice))
        return fitprice


    # 获取网格索引
    def closest(mylist, Number):
        answer = []
        for i in mylist:
            answer.append(abs(Number - i))
        return answer.index(min(answer))


    # 计算最小间距, 以中枢价格买入，卖出的最低价格,最小下单单位1usdt
    def calmingridprice(lowprice, highprice, feeratio):
        # sellprice - (lowprice + highprice) / 2 > = (sellprice + (lowprice + highprice) / 2) * feeratio
        # sellprice*(1-feeratio)>=(lowprice + highprice) / 2 * (1+feeratio)
        sellprice = (((lowprice + highprice) / 2) * (1 + feeratio)) / (1 - feeratio)
        return sellprice - (lowprice + highprice) / 2


    # 初始化参数
    def initSysParas(m_totalmoney,
                     m_firstinvestradio,
                     m_pricepercell,
                     m_trade_grid_rate,
                     m_beginprice,
                     m_stoplossprice,
                     m_stopgainprice,
                     m_currencypair,
                     m_invpercell,
                     m_logoutpath
                     ):
        global currencypair
        currencypair = m_currencypair
        # 触发价格与成交价格的比例，小于该比例值，开始挂单
        global trade_grid_rate
        trade_grid_rate = m_trade_grid_rate
        # 触发价格
        global beginprice
        beginprice = m_beginprice
        # 止损价格
        global stoplossprice
        stoplossprice = m_stoplossprice
        # 止盈价格
        global stopgainprice
        stopgainprice = m_stopgainprice
        # 网格价差
        global pricepercell
        pricepercell = m_pricepercell

        # 总预算
        global totalmoney
        totalmoney = m_totalmoney
        # 初始投入比例
        global firstinvestradio
        firstinvestradio = m_firstinvestradio
        # 没单元投资额
        global invpercell
        invpercell = m_invpercell
        # 没单元投资额
        global logoutpath
        logoutpath = m_logoutpath


    # 创建价格网格
    def creategrids(lowprice, highprice, pricepercell):
        global gridprices
        gridprices = []
        length = math.ceil((highprice - lowprice) / pricepercell)
        count = 0
        while count < length:
            gridprices.append(count * pricepercell + lowprice)
            count = count + 1


    # 初始持仓,批量提交不能超过10个订单
    def initposition(price, amount, batchcnt, type):
        global gridtradelist
        if type == 0:
            # 在初始价格买多份，承担往下的风险，以换取可能的收益，暂时无法确定
            # 根据数量，买下一级的价格
            texts = []
            levelprice = 0
            for num in range(0, batchcnt):
                # time.sleep(1.5)
                # if levelprice==0:
                #     levelprice=price
                text = 't-b-' + str(int(price * 1000000)) + '-' + str(int(time.time()))
                texts.append(text)
                # levelprice = gridprices[closest(gridprices, levelprice) - 1]

            batchlis = batchorders('buy', amount, price, texts)
            # 输出批量提交成果
            logger.info('批量提交:' + repr(batchlis))
            for item in batchlis:
                if item['succeeded'] == True:
                    if item['status'] == 'open' or item['status'] == 'closed':
                        key = item['text']
                        logger.info("{} 加入持仓。".format(key))
                        item['samount'] = str(amount * (1 - taker_fee))
                        gridtradelist[key] = item

            outgridtradestotxt(gridtradelist, lasttradeprice)
        elif type == 1:
            print('1')
        else:
            print('2')
        logger.info("初始化持仓")
        return 1


    # 计划卖出
    def plansell(gridprice, realprice):
        # 如果
        if realprice is None:
            realprice = gridprice
        if realprice == 0:
            realprice = gridprice

        # 严格按照网格的订单
        order = {}

        # 从takelist获取网格价格的低一档的买单
        mindex = gridprices.index(gridprice)
        mlowerprice = gridprices[mindex - 1]

        # btext = 't-b-' + str(int(gridprice * 1000000))
        btext = 't-b-' + str(int(mlowerprice * 1000000))
        for k in gridtradelist:
            # 已经卖掉/挂单的过滤
            if 'sid' in gridtradelist[k].keys():
                if gridtradelist[k]['sid'] is not None:
                    if gridtradelist[k]['sstatus'] == 'closed':
                        continue
                    elif gridtradelist[k]['sstatus'] == 'open':
                        continue

            # 网格价格之买单
            if k.find(btext) >= 0:
                order = gridtradelist[k]
                btext = k
                break

        # 提取买单的id
        bid = -1

        # 库存是空的时候，不挂卖单
        if 'id' in order.keys():
            if order['id'] is not None:
                bid = order['id']
            else:
                return 0

            # 判断订单是否已经卖出
            if 'sstatus' in order.keys():
                if order['sstatus'] == 'open' or order['sstatus'] == 'closed':
                    return 0

            # 构造卖单
            text = 't-s-' + str(int(mlowerprice * 1000000)) + '-' + str(bid)
            logger.info("相关卖出网格：{}".format(repr(order)))

            cansellamount = float(order['samount'])

            # 挂单时，用实际成交价格+买入时损失0.2%现货的价格
            realprice = realprice + ((cansellamount / 0.998) * 0.002 * realprice)
            order = orders("sell", cansellamount, realprice, text)
            logger.info("挂单卖出,挂单卖出价" + str(realprice) + "，卖出数量：" + str(cansellamount))
            logger.info("返回结果 {}".format(repr(order)))
            # {'label': 'BALANCE_NOT_ENOUGH', 'message': 'Not enough balance'}
            if 'label' in order.keys():
                if str.upper(order['label']) == str.upper('BALANCE_NOT_ENOUGH'):
                    return 0

            if order['status'] == 'open':
                # 卖了之后，更新买单记录对应的买单记录
                gridtradelist[btext]['sid'] = order['id']
                # 更新买单的卖单价
                gridtradelist[btext]['sprice'] = realprice
                # 更新买单的卖单状态
                gridtradelist[btext]['sstatus'] = order['status']
                # 卖出数量
                gridtradelist[btext]['samount'] = str(cansellamount)
            if order['status'] == 'closed':
                # 卖了之后，更新买单记录对应的买单记录
                gridtradelist[btext]['sid'] = order['id']
                # 更新买单的卖单价
                gridtradelist[btext]['sprice'] = realprice
                # 更新买单的卖单状态
                gridtradelist[btext]['sstatus'] = order['status']
                # 卖出数量
                gridtradelist[btext]['samount'] = str(cansellamount)
                # 移走已关闭的交易
                removefinishedtrade(gridtradelist[btext])
            if order['status'] == 'cancelled':
                logger.info("交易未成交")
            # 输出到文件
            outgridtradestotxt(gridtradelist, lasttradeprice)
            return 1
        else:
            logger.info("下一网格{}没有现货，无法卖出.".format(mlowerprice))
            return 0


    # 计划买入
    def planbuy(price, amount):
        # 提交订单返回记录集
        # {
        #     "text": "t-123456",
        #     "currency_pair": "ETH_BTC",
        #     "type": "limit",
        #     "account": "spot",
        #     "side": "buy",
        #     "iceberg": "0",
        #     "amount": "1",
        #     "price": "5.00032",
        #     "timeinforce": "gtc",
        #     "autoborrow": false
        # }

        # 买入处增加一道防御，可用金额是否足够本次购买，避免造成总账户开口
        if price * amount > canusemoney:
            logger.info("可用余额不足此次买入。买入成本：{},可用余额:{}".format(str(price * amount), str(canusemoney)))
            return 0

        order = {}
        # 从takelist获取最近一次b
        cantake = 0;
        btext = 't-b-' + str(int(price * 1000000))
        for k in gridtradelist:
            if k.find(btext) >= 0:
                order = gridtradelist[k]
                if 'sid' in order.keys():
                    if order['sid'] is not None:
                        if order['sstatus'] == 'open':
                            cantake = 0
                        else:
                            cantake = 1
                    else:
                        # sid不为null，说明该记录以卖出，先标识为1
                        cantake = 1
                else:
                    # 没有卖出标记，则认为有存货，不买入
                    cantake = 0
                    break
            else:
                # 不在存货中，需要全部循环完毕
                cantake = 1

        if cantake == 1:
            # 提交买入挂单
            text = 't-b-' + str(int(price * 1000000)) + '-' + str(int(time.time()))
            order = orders("buy", amount, price, text)
            order['samount'] = str(amount * (1 - taker_fee))
            logger.info("挂单买入,挂单买入价" + str(price) + "，买入数量：" + str(amount))
            logger.info("返回结果 {}".format(repr(order)))
            # 根据status判断，处理订单状态
            if order['status'] == 'cancelled':
                # 不加入持仓表
                return 0
            elif order['status'] == 'closed':
                logger.info("加入持仓。")
                # 加入持仓表
                text = text + '-' + str(order['id'])
                gridtradelist[text] = order
                # 输出到文件
                outgridtradestotxt(gridtradelist, lasttradeprice)
            elif order['status'] == 'open':
                logger.info("加入持仓。")
                # 加入持仓表
                text = text + '-' + str(order['id'])
                gridtradelist[text] = order
                # 输出到文件
                outgridtradestotxt(gridtradelist, lasttradeprice)
                # 挂单中
                return 0
            else:
                return 0
        else:
            logger.info("买入网格未卖出，不需要再买入。" + str(price) + "，买入数量：" + str(amount))
            return 1


    # 移走已关闭的交易
    def removefinishedtrade(trade):
        logger.info("后续需要以走，尚未完成。记录为：" + repr(trade))


    # 输出到磁盘文件
    def outgridtradestotxt(gridtradelist, curprice):
        # 打开一个文件
        f = open(logoutpath + currencypair + str(int(time.time())) + ".txt", "w")
        # 网络收益，卖出
        sellprofit = 0
        # 卖出手续费
        sellfee = 0
        # 买入手续费
        buyfee = 0
        # 总投入
        buycost = 0
        # 持仓价格
        positionprofit = 0
        # 浮动盈余
        floatprofit = 0

        cp_gridtradelist = {}
        for k in gridtradelist:
            # buy单如果撤单的跳过
            if gridtradelist[k]['side'] == 'buy' and gridtradelist[k]['status'] == 'cancelled':
                continue

            # 计算网格总收益
            if 'sstatus' in gridtradelist[k].keys():
                if gridtradelist[k]['sstatus'] is not None:
                    if gridtradelist[k]['sstatus'] == 'finished' or gridtradelist[k]['sstatus'] == 'closed':
                        sellprofit = sellprofit + float(gridtradelist[k]['sprice']) * float(gridtradelist[k]['samount'])
                        # 卖出总费用
                        sellfee = sellfee + float(gridtradelist[k]['sprice']) * float(
                            gridtradelist[k]['samount']) * maker_fee

            # 计算总投入，买单总价格
            buycost = buycost + float(gridtradelist[k]['price']) * float(gridtradelist[k]['amount'])
            # 买入总费用
            # buyfee = buyfee + float(gridtradelist[k]['price']) * float(gridtradelist[k]['amount']) * taker_fee
            buyfee = buyfee + 0

            # 计算持仓价值
            if 'sstatus' in gridtradelist[k].keys():
                if gridtradelist[k]['sstatus'] is None:
                    positionprofit = positionprofit + float(curprice) * float(gridtradelist[k]['samount'])
                else:
                    if gridtradelist[k]['sstatus'] == 'open':
                        positionprofit = positionprofit + float(curprice) * float(gridtradelist[k]['samount'])
                    elif gridtradelist[k]['sstatus'] == 'cancelled':
                        positionprofit = positionprofit + float(curprice) * float(gridtradelist[k]['samount'])
            else:
                positionprofit = positionprofit + float(curprice) * float(gridtradelist[k]['samount'])

            if 'sstatus' in gridtradelist[k].keys():
                if gridtradelist[k]['sstatus'] == 'finished' or gridtradelist[k]['sstatus'] == 'closed':
                    output = {
                        'id': gridtradelist[k]['id'],
                        'amount': gridtradelist[k]['amount'],
                        'price': gridtradelist[k]['price'],
                        'buyfee': '0',
                        'status': gridtradelist[k]['status'],
                        'sid': gridtradelist[k]['sid'],
                        'sprice': gridtradelist[k]['sprice'],
                        'samount': gridtradelist[k]['samount'],
                        'sstatus': gridtradelist[k]['sstatus'],
                        'sellfee': str(float(gridtradelist[k]['samount']) * float(gridtradelist[k]['sprice']) * maker_fee),
                    }
                elif gridtradelist[k]['sstatus'] == 'cancelled':
                    output = {
                        'id': gridtradelist[k]['id'],
                        'amount': gridtradelist[k]['amount'],
                        'price': gridtradelist[k]['price'],
                        'buyfee': '0',
                        'status': gridtradelist[k]['status'],
                        'sid': None,
                        'sprice': None,
                        'samount': None,
                        'sstatus': None,
                        'sellfee': None,
                    }
                else:
                    output = {
                        'id': gridtradelist[k]['id'],
                        'amount': gridtradelist[k]['amount'],
                        'price': gridtradelist[k]['price'],
                        'buyfee': '0',
                        'status': gridtradelist[k]['status'],
                        'sid': gridtradelist[k]['sid'],
                        'sprice': gridtradelist[k]['sprice'],
                        'sstatus': gridtradelist[k]['sstatus'],
                        'samount': gridtradelist[k]['samount'],
                        'sellfee': None,
                    }
            else:
                output = {
                    'id': gridtradelist[k]['id'],
                    'amount': gridtradelist[k]['amount'],
                    'price': gridtradelist[k]['price'],
                    'buyfee': '0',
                    'status': gridtradelist[k]['status'],
                    'sid': None,
                    'sprice': None,
                    'samount': None,
                    'sstatus': None,
                    'sellfee': None
                }
            cp_gridtradelist[k] = output

        # 已支出金额
        global totaloutcoming
        totaloutcoming = buycost + buyfee + sellfee

        # 可用金额
        global canusemoney
        global totalmoney
        canusemoney = totalmoney - totaloutcoming + sellprofit

        # 浮动盈余
        floatprofit = sellprofit + positionprofit - buycost - sellfee - buyfee
        cp_gridtradelist['summry'] = {
            'floatprofit': floatprofit,
            'sellprofit': sellprofit,
            'sellfee': sellfee,
            'positionprofit': positionprofit,
            'positionprice': curprice,
            'buycost': buycost,
            'buyfee': buyfee,
            'canusemoney': canusemoney
        }
        value = repr(cp_gridtradelist)
        s = str(value)
        f.writelines(s)

        # value = '浮动盈亏:{}, 卖出收入：{},卖出手续费：{},持仓价值：{},投入成本：{},买入手续费：{}'.format(floatprofit, sellprofit, sellfee,
        #                                                                     positionprofit, buycost, buyfee)
        #
        # s = str(value)
        # f.writelines(s)

        # 关闭打开的文件，必须关闭不然电脑能炸裂
        f.close()


    # 单条提交订单
    def orders(side, amount, price, text):
        m_time_in_force = ''
        if side == 'buy':
            m_time_in_force = 'gtc'
        elif side == 'sell':
            m_time_in_force = 'gtc'

        # 持仓判断已经在计划买入，卖出中做了，此地只管提交
        orders_url = '/spot/orders'
        orders_query_param = ''
        body = '{"text":"' + text + '","currency_pair":"' + currencypair + '","type":"limit","account":"spot","side":"' + side + '","iceberg":"0","amount":"' + str(
            amount) + '","price":"' + str(price) + '","time_in_force":"' + m_time_in_force + '","auto_borrow":false} '
        # `gen_sign` 的实现参考认证一章
        orders_sign_headers = gen_trade_sign('POST', prefix + orders_url, orders_query_param, body)
        headers.update(orders_sign_headers)
        r = requests.request('POST', host + prefix + orders_url, headers=headers, data=body)
        return r.json()

        status = ''
        rnd = random.randint(0, 9)
        if rnd <= 3:
            status = 'open'
        elif 3 < rnd <= 8:
            status = 'closed'
        else:
            status = 'cancelled'

        return {
            "id": str(int(time.time())),
            "text": text,
            "create_time": "1548000000",
            "update_time": "1548000100",
            "currency_pair": currencypair,
            "status": status,
            "type": "limit",
            "account": "spot",
            "side": side,
            "iceberg": "0",
            "amount": str(amount),
            "price": str(price),
            "time_in_force": "ioc",
            "left": "0.5",
            "filled_total": "2.50016",
            "fee": "0.002",
            "fee_currency": "USDT",
            "point_fee": "0",
            "gt_fee": "0",
            "gt_discount": false,
            "rebated_fee": "0",
            "rebated_fee_currency": "BTC"
        }


    # 单条提交订单
    def batchorders(side, amount, price, texts):
        m_time_in_force = ''
        if side == 'buy':
            m_time_in_force = 'gtc'
        elif side == 'sell':
            m_time_in_force = 'gtc'

        orders_url = '/spot/batch_orders'
        orders_query_param = ''
        batchsbody = ''
        # 遍历texts
        for text in texts:
            singlebody = '{"text":"' + text + '","currency_pair":"' + currencypair + '","type":"limit","account":"spot","side":"' + side + '","iceberg":"0","amount":"' + str(
                amount) + '","price":"' + str(price) + '","time_in_force":"' + m_time_in_force + '","auto_borrow":false} '
            # singlebody = {
            #     "text": text,
            #     "currency_pair": "GT_USDT",
            #     "type": "limit",
            #     "account": "spot",
            #     "side": side,
            #     "iceberg": "0",
            #     "amount": str(amount),
            #     "price": str(price),
            #     "time_in_force": "ioc",
            #     "auto_borrow": false
            # }
            if len(batchsbody) == 0:
                batchsbody = singlebody
            else:
                batchsbody = batchsbody + ',' + singlebody

        batchsbody = '[' + batchsbody + ']'

        # `gen_sign` 的实现参考认证一章
        batch_sign_headers = gen_trade_sign('POST', prefix + orders_url, orders_query_param, batchsbody)
        headers.update(batch_sign_headers)
        r = requests.request('POST', host + prefix + orders_url, headers=headers, data=batchsbody)
        return r.json()

        batchsbody = []
        for text in texts:
            time.sleep(1.5)
            status = ''
            rnd = random.randint(0, 9)
            if rnd <= 3:
                status = 'open'
            elif 3 < rnd <= 8:
                status = 'closed'
            else:
                status = 'cancelled'
            singlebody = {
                "id": str(int(time.time())),
                "text": text,
                "create_time": "1548000000",
                "update_time": "1548000100",
                "currency_pair": currencypair,
                "status": status,
                "type": "limit",
                "account": "spot",
                "side": side,
                "iceberg": "0",
                "amount": str(amount),
                "price": str(price),
                "time_in_force": "ioc",
                "left": "0.5",
                "filled_total": "2.50016",
                "fee": "0.002",
                "fee_currency": "USDT",
                "point_fee": "0",
                "gt_fee": "0",
                "gt_discount": false,
                "rebated_fee": "0",
                "rebated_fee_currency": "BTC"
            }
            batchsbody.append(singlebody)
        return batchsbody


    # websocket获取实时交易信息
    def on_message(ws, message):
        # type: (GateWebSocketApp, str) -> None
        # handle whatever message you received
        # logger.info("message received from server: {}".format(message))
        try:
            data = json.loads(message)
            if data['result'] is None:
                return
            if data['channel'] == "spot.trades":
                # 第一次返回的是订阅成功的消息，跳出即可
                if data['result']['price'] is None:
                    return
                # 根据接受回来的数据，记录last，lasttwo两个价格
                global lasttradeprice
                global lasttwotradeprice
                global gridbuyandcellstart
                global stoplossprice
                global stopgainprice

                if lasttradeprice == 0:
                    lasttradeprice = float(data['result']['price'])
                else:
                    lasttwotradeprice = lasttradeprice
                    lasttradeprice = float(data['result']['price'])

                if lasttradeprice == 0 or lasttwotradeprice == 0:
                    return

                # 判断上行，还是下行
                direction = ''
                if lasttradeprice > lasttwotradeprice:
                    direction = '上行'
                elif lasttradeprice < lasttwotradeprice:
                    direction = '下行'
                else:
                    direction = '横盘'

                logger.info(
                    "当前时间: {} ,上一成交价：{} ,当前成交价格: {}，触发价格：{}，方向：{}".format(timestamp_datetime(int(time.time())),
                                                                          lasttwotradeprice, lasttradeprice, beginprice,
                                                                          direction))

                # 成交价低于止损价，网格停止
                if stoplossprice >= lasttradeprice:
                    logger.info("停止网格")
                    return
                if stopgainprice <= lasttradeprice:
                    logger.info("停止网格")
                    return

                # 启动网格策略
                if beginprice >= lasttradeprice:

                    # 初始化持仓时，先等待一段3分钟秒时间，看是否连续下行，如果连续下行区，则不做初始化
                    # 通过初始化比例来规避套牢的风险

                    if gridbuyandcellstart == 0:
                        logger.info("启动网格")
                        gridbuyandcellstart = 1
                        # 批量挂单买入初始仓位
                        buyprice = getfitgridprice(lasttradeprice)
                        # 计算批量下单数量
                        batchcnt = math.ceil(totalmoney * firstinvestradio)
                        # 批量挂单买入初始仓位

                        # 保证每个网格投入相同
                        initposition(buyprice, invpercell / buyprice, batchcnt, 0)
                # 下行
                if lasttradeprice < lasttwotradeprice:
                    if gridbuyandcellstart == 1:
                        # 根据两个成交区获取合适网格下限价格
                        buyprice = getfitgridprice(lasttradeprice)
                        if lasttwotradeprice > buyprice > lasttradeprice:
                            logger.warning("买入触发: 最新成交价 {}，计划卖出价（最近网格价格）{}，容差；{}".format(lasttradeprice, buyprice,
                                                                                         round(
                                                                                             abs(buyprice - lasttradeprice),
                                                                                             4)))
                            # 防御1：靠近买入价格,防止在网格中间部分买入，除非具备构建新网格的能力。。。。
                            if round(abs(buyprice - lasttradeprice), 4) <= trade_grid_rate:
                                # 是否还要判断是否对应网格价格，已经存在未卖的单子???
                                # 挂单买入

                                # 保证每次投入总额都是一致的
                                planbuy(buyprice, invpercell / buyprice)
                            else:
                                logger.warning(
                                    "与网格最近价格超出容差{},差值为{}。".format(trade_grid_rate, abs(buyprice - lasttradeprice)))

                # 上行
                else:
                    if gridbuyandcellstart == 1:
                        # 根据两个成交区获取合适网格价格
                        sellprice = getfitgridprice(lasttradeprice)
                        if lasttwotradeprice < sellprice < lasttradeprice:
                            logger.warning("卖出触发: 最新成交价 {}，计划卖出价（最近网格价格）{}，容差；{}".format(lasttradeprice, sellprice,
                                                                                         round(abs(
                                                                                             sellprice - lasttradeprice),
                                                                                             4)))
                            # 防御1：靠近买出价格，减少频饭挂单，要产生交易费用的
                            if round(abs(sellprice - lasttradeprice), 4) < trade_grid_rate:
                                # 挂单，卖出
                                plansell(sellprice, sellprice)
                            else:
                                logger.warning(
                                    "与网格最近价格超出容差{},差值为{}。以最新成交价{}卖出。".format(trade_grid_rate,
                                                                             round(abs(sellprice - lasttradeprice), 4),
                                                                             lasttradeprice))
                                # 买入时，扣除的现货的比例
                                plansell(sellprice, lasttradeprice)

            elif data['channel'] == "spot.orders":
                # {
                #     "time": 1605175506,
                #     "channel": "spot.orders",
                #     "event": "update",
                #     "result": [
                #         {
                #             "id": "30784435",
                #             "user": 123456,
                #             "text": "t-abc",
                #             "create_time": "1605175506",
                #             "update_time": "1605175506",
                #             "event": "put",
                #             "currency_pair": "BTC_USDT",
                #             "type": "limit",
                #             "account": "spot",
                #             "side": "sell",
                #             "amount": "1",
                #             "price": "10001",
                #             "time_in_force": "gtc",
                #             "left": "1",
                #             "filled_total": "0",
                #             "fee": "0",
                #             "fee_currency": "USDT",
                #             "point_fee": "0",
                #             "gt_fee": "0",
                #             "gt_discount": true,
                #             "rebated_fee": "0",
                #             "rebated_fee_currency": "USDT"
                #         }
                #     ]
                # }
                # 订阅用户交易频道
                logger.warning("on_message: orders {}".format(message))
                userorders = data['result']

                if not isinstance(userorders, list):
                    if 'status' in userorders.keys():
                        return

                # 同步订单状态,rest api 高频请求会被断开
                for userorder in userorders:
                    # 针对买单状态
                    if 'event' in userorder.keys():
                        if userorder['event'] is not None:
                            if userorder['side'] == 'sell':
                                if userorder['event'] == 'finish':
                                    # 更新sid对应的sstatus
                                    for key in gridtradelist:
                                        if gridtradelist[key]['sid'] == userorder['id']:
                                            if userorder['left'] == userorder['amount']:
                                                gridtradelist[key]['sstatus'] = 'canceled'
                                                gridtradelist[key]['samount'] = '0'
                                            else:
                                                gridtradelist[key]['sstatus'] = 'closed'
                                                gridtradelist[key]['samount'] = str(
                                                    float(userorder['amount']) * (1 - taker_fee))
                                            break
                                if userorder['event'] == 'put':
                                    print('卖单创建')
                                if userorder['event'] == 'update':
                                    print('卖单部分成交')
                            elif userorder['side'] == 'buy':
                                if userorder['event'] == 'finish':
                                    # 更新id对应的status
                                    for key in gridtradelist:
                                        if gridtradelist[key]['id'] == userorder['id']:
                                            if userorder['left'] == userorder['amount']:
                                                gridtradelist[key]['status'] = 'canceled'
                                            else:
                                                gridtradelist[key]['status'] = 'closed'
                                            break
                                if userorder['event'] == 'put':
                                    print('买单创建')
                                if userorder['event'] == 'update':
                                    print('买单部分成交')
                            else:
                                print('do nothing')

                # 更新持仓信息和浮动盈亏等统计数据
                outgridtradestotxt(gridtradelist, lasttradeprice)
            elif data['channel'] == "spot.usertrades":
                # 订阅用户交易频道
                logger.warning("on_message:usertrades {}".format(message))
                # usertrades = data['result']
                # for i in range(len(usertrades)):
                #     # {
                #     #     "id": 5736713,
                #     #     "user_id": 1000001,
                #     #     "order_id": "30784428",
                #     #     "currency_pair": "BTC_USDT",
                #     #     "create_time": 1605176741,
                #     #     "create_time_ms": "1605176741123.456",
                #     #     "side": "sell",
                #     #     "amount": "1.00000000",
                #     #     "role": "taker",
                #     #     "price": "10000.00000000",
                #     #     "fee": "0.00200000000000",
                #     #     "point_fee": "0",
                #     #     "gt_fee": "0"
                #     # }
                #     orderid = usertrades[i]['order_id']
                # 卖单和买单，如果量过大，还会存在分批成交的情况，因此会有多条记录过来
            else:
                print('bbbbb')
        except Exception as ex:
            logger.warning("on_message: {}".format(ex))


    def on_open(ws):
        # type: (GateWebSocketApp) -> None
        # subscribe to channels interested
        # logger.info('websocket connected')
        # ws.subscribe("spot.trades", ['BTC_USDT'], False)
        # 订阅GT_USDT实时交易信息
        ws.subscribe("spot.trades", [currencypair], False)
        # 订阅所有订单信息？
        ws.subscribe("spot.orders", [currencypair], True)
        # # 订阅用户订单信息
        # ws.subscribe("spot.usertrades", [currencypair], True)
        # ws.subscribe("spot.tickers", ['GT_USDT'], False)
        # ws.subscribe("spot.candlesticks", ['1m', 'BTC_USDT'], False)


    def on_error(ws, error):
        print("####### on_error #######")
        print(ws)
        print(error)


    def on_close(ws):
        print("####### on_close #######")
        print(ws)
        print("####### closed #######")
        print("####### 等待30秒后重连 #######")
        time.sleep(30)

        start()


    # 初始化
    def start(m_currencypair,
              m_logoutpath,
              m_readonly_api_key,
              m_readonly_api_secret,
              m_write_api_key,
              m_write_api_secret,
              m_interval,
              m_timedelta,
              ):
        # 接收外部参数
        m_currencypair = ''
        # 日志输出地址
        m_logoutpath = ''
        #
        if m_currencypair == '':
            m_currencypair = 'GT_USDT'
        logging.info("货币对：" + str(m_currencypair))
        if m_logoutpath == '':
            os.mkdir('/opt/xoenmap/gateio/log/')
            m_logoutpath = '/opt/xoenmap/gateio/log/'

        logging.info("日志地址：" + str(m_logoutpath))
        m_runlogpath = '/opt/xoenmap/gateio/log/run_' + m_currencypair + '.log'
        # 日志基础配置
        logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO,
                            handlers=[
                                logging.FileHandler(filename=m_runlogpath),
                                logging.StreamHandler(sys.stdout)
                            ])
        # 获取市场k线图，计算最大最小价格
        getcandlesticks(m_interval, datetime_timestamp(
            (datetime.datetime.now() - datetime.timedelta(hours=m_timedelta)).strftime('%Y-%m-%d %H:%M:%S')),
                        datetime_timestamp(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), m_currencypair)

        # 计算最小间距
        m_mininterval_price = round((maxValue - minValue) / 5, 4)

        logging.info("最小单元价差" + str(m_mininterval_price))
        # 初始建仓比例
        m_firstratio = 0.2
        # 总投入预算
        m_allmoney = 2 / m_firstratio
        # 初始化参数
        initSysParas(m_allmoney, m_firstratio, m_mininterval_price, 0.0001, (minValue + maxValue) / 2,
                     minValue * 0.95, maxValue * 1.05, m_currencypair, 1, m_logoutpath)

        # initSysParas(m_allmoney, m_firstratio, m_mininterval_price, 0.0001, 0.272422,
        #              minValue * 0.95, maxValue * 1.05, 'GT_USDT',1)

        # 初始网格
        creategrids(minValue, maxValue, m_mininterval_price)
        logging.info(','.join(str(i) for i in gridprices))
        try:
            app = GateWebSocketApp("wss://api.gateio.ws/ws/v4/",
                                   m_readonly_api_key,
                                   m_readonly_api_secret,
                                   on_open=on_open,
                                   on_message=on_message,
                                   on_error=on_error,
                                   on_close=on_close)
            app.run_forever(ping_interval=5)
        except Exception as ex:
            logger.warning("startapp terminated: {}".format(ex))


    # 测试
    def test():
        start('GT_USDT',
              '/opt/xoenmap/gateio/log/',
              '497747c410ee1ef279285c3e9b40e803',
              '47a71e8c9de54ff620fa6a214926c01154d617e606cdd1c5e0d87c3bbfe0062f',
              '45adfb0ba3705fa72107d304c1b959f4',
              '100d5909ee761b5c957ff11de1ffe4368a3b3e9b341ed7e50d514630242852a6',
              '1h',
              12)
