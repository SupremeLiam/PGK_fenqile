#coding=utf-8

#coding:utf-8

#-*- coding:utf-8 -*-
import requests
import json
import base64
from urllib.parse import quote,unquote
##改下面的cookie start end  不用我说吧，验证码自己获取。
##start0是第一单，end15一共报15张，从0到14。
cookie=''
start=48
end=50

offset=5#这个不要乱改
orderurl='https://order.m.fenqile.com/route0001/order/getOrderInfoDetail.json'
smsurl='https://trade.m.fenqile.com/order/query_send_sms.json'
kmurl='https://trade.m.fenqile.com/order/query_verify_fulu_and_coupon_sms.json'
smsi=int(5)
print('Powered by 杨大师')
print('感谢饲养员爸爸赞助')
import time
sj=int(time.time())-60
if cookie=='':
    cookie=input('请填入cookie：')

def getsms():
    global smsi
    global sms
    global sj
    if smsi==5:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print(unquote(
            '%e6%84%9f%e8%b0%a2%e4%b8%80%e4%bd%8d%e4%b8%8d%e6%84%bf%e9%80%8f%e9%9c%b2%e5%a7%93%e5%90%8d%e7%9a%84FGH%e5%85%88%e7%94%9f',
            'utf-8'))
        print(unquote(
            'FGH%e5%85%88%e7%94%9f%e7%9a%84%e8%8b%b9%e6%9e%9c%e5%8d%a1%e4%bb%b7%e6%a0%bc%e9%ab%98%e5%9b%9e%e6%ac%be%e5%bf%ab%ef%bc%8c%e6%ac%a2%e8%bf%8e%e6%94%af%e6%8c%81%ef%bc%8cVx%ef%bc%9aappstoremall',
            'utf-8'))

        if input('是否自动发马？温馨提示：60秒间隔哦。是就回复1，不是你随意，请回复：')=='1':
            print('等待%d秒'%(0-int(time.time())+sj+60))
            while int(time.time())<=sj+61:
                time.sleep(1)
            sj=int(time.time())
            requests.post(smsurl,'{"send_type":8,"is_weex":1}',headers={'Cookie':cookie})
        sms=input('输入验证码：')
        smsi=0
    smsi=smsi+1
    return sms
inde=0
#sms=getsms()
while start<end:
    od=requests.post(orderurl,data='{"system":{"controller":""},"data":{"state_filter":"","offset":%d,"limit":%d}}'%(start,offset),headers={'Cookie':cookie})
    js=json.loads(od.text)

    try:
        fout = open('km.txt', 'a+', encoding='utf8')
        for i in js['data']['result_rows']:

            if i['order_info']['order_state']!=430:
                continue
            otype=i['order_info']['sale_type']
            id=i['order_info']['order_id']
            name=i['template_content'][1]['order_goods_info']['goods_info']['product_info']
            km=requests.post(kmurl,'{"send_type":8,"sms_code":"%s","order_id":"%s","sale_type":%d,"is_weex":1}'%(getsms(),id,otype),headers={'Cookie':cookie})
            kmj=json.loads(km.text)
            timeStamp = int(i['order_info']['create_time'])/1000
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)

            if 'virtual_info' in kmj:
                kmjg=kmj['virtual_info']['fulu_info'][0]
                inde = inde + 1
                if otype==800:
                    print("%s\t%s\t%s\t%s"%(kmjg['card_number']['value'],kmjg['passwd']['value'],name,otherStyleTime))
                    fout.write("%s\t%s\n"%(kmjg['card_number']['value'],kmjg['passwd']['value']))
                if otype==400:
                    print("%s\t%s\t%s"%(kmjg['passwd']['value'],name,otherStyleTime))
                    fout.write("%s\n"%(kmjg['passwd']['value']))
            else:
                print('订单异常第%d个订单，订单地址： https://trade.m.fenqile.com/order/detail/%s.html'%(inde,id))
                print('接口返回：%s'%json.dumps(json.loads(km.text),ensure_ascii=False))
            pass
        start=start+offset
        fout.close()
    except Exception as e:
        print(f"Unexpected error: {e}")
        print('订单异常第%d个订单，订单地址： https://trade.m.fenqile.com/order/detail/%s.html' % (inde, id))
print('一共获取了%d个订单，自动跳过了关闭等等状态的订单'%inde)
