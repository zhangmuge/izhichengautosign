# -*- coding: utf-8 -*-
from urllib.parse import quote
import requests
import time
import re
import os

students = []
pattern = re.compile(r'[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}')  # 找session的正则表达式

# 如果检测到程序在 github actions 内运行，那么读取环境变量中的登录信息
if os.environ.get('GITHUB_RUN_ID', None):
    try:
        if not students:
            tmp_students = os.environ.get('students', '').split('\n')
            if "".join(tmp_students) == '':
                students = []
            else:
                students = tmp_students
            del tmp_students
    except:
        print('err: environment config error')
else:  # 如果不在github里面则读取本地文件去打卡
    with open('student.txt', encoding='utf-8', errors='ignore') as s:
        students = s.read().split('\n')


# 在服务器还可以连接数据库打卡，我没有服务器，略

def tianbao(id, sheng, shi, qu):
    try:
        url = 'http://dw10.fdzcxy.edu.cn/datawarn/ReportServer?formlet=app/sjkrb.frm&op=h5&userno=' + id + '#/form'  # 主页面url，在获取的页面h5里面有session
        headers = {  # 构造请求头，我这里是自己浏览器复制的
            'Host': 'dw10.fdzcxy.edu.cn',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Edg/97.0.1072.55',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        # 获取sessionID
        res = requests.get(url=url, headers=headers)  # get拿到主页h5
        sessionID = pattern.search(res.text)[0]  # 正则表达式找到session
        cookie = 'JSESSIONID=' + requests.utils.dict_from_cookiejar(res.cookies)['JSESSIONID']  # 记录cookie
        headers = {
            'Host': 'dw10.fdzcxy.edu.cn',
            'Connection': 'keep-alive',
            'responseType': 'json',
            'terminal': 'H5',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Edg/97.0.1072.55',
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'clientType': 'mobile/h5_5.0',
            'deviceType': 'android',
            'Referer': 'http://dw10.fdzcxy.edu.cn/datawarn/ReportServer?formlet=app/sjkrb.frm&op=h5&userno=211906149',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'

        }
        url = 'http://dw10.fdzcxy.edu.cn/datawarn/decision/view/form?sessionID=' + sessionID + '&op=fr_form&cmd=load_content&toVanCharts=true&fine_api_v_json=3&widgetVersion=1'
        res = requests.get(url=url, headers=headers)
        items = res.json()['items'][0]['el']['items']
        name = items[2]['value']  # 这里拿到姓名
        for i in items:
            if i['widgetName'] == 'SUBMIT':
                submit = i['listeners'][0]['action']
                break
        # print(submit)
        jsConfId = pattern.findall(submit)[0]  # 拿到两个验证码
        callbackConfId = pattern.findall(submit)[1]
        # print(jsConfId, callbackConfId)

        # 提交打卡信息
        url = 'http://dw10.fdzcxy.edu.cn/datawarn/decision/view/form'  # 提交表单地址
        headers = {
            'Host': 'dw10.fdzcxy.edu.cn',
            'Connection': 'keep-alive',
            'terminal': 'H5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            '__device__': 'unknown',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'sessionID': sessionID,
            'clientType': 'mobile/h5_5.0',
            'deviceType': 'unknown',
            'Origin': 'http://dw10.fdzcxy.edu.cn',
            'Referer': 'http://dw10.fdzcxy.edu.cn/datawarn/ReportServer?formlet=app/sjkrb.frm&op=h5&userno=' + id,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': cookie,
        }  # 构造请求头时加入session和cookie
        data = {  # 构造提交表单项
            'op': 'dbcommit',
            '__parameters__': quote(
                '{"jsConfId":"' + jsConfId + '","callbackConfId":"' + callbackConfId + '","LABEL2":"  每日健康上报","XH":"' + id + '","XM":"' + name + '","LABEL12":"","LABEL0":"1. 目前所在位置:","SHENG":"' + sheng + '","SHI":"' + shi + '","QU":"' + qu + '","LABEL11":"2.填报时间:","SJ":"' + time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime()) + '","LABEL1":"3. 今日体温是否正常？(体温小于37.3为正常)","TWZC":"正常","LABEL6":"目前体温为：","TW":"0","TXWZ":"' +
                sheng + shi + qu + '","LABEL9":"4. 昨日午检体温:","WUJ":"36.4","LABEL8":"5. 昨日晚检体温:","WJ":"36.5","LABEL10":"6. 今日晨检体温:","CJ":"36.4","LABEL3":"7. 今日健康状况？","JK":["健康"],"JKZK":"","QTB":"请输入具体症状：","QT":" ","LABEL4":"8. 近14日你和你的共同居住者(包括家庭成员、共同租住的人员)是否存在确诊、疑似、无症状新冠感染者？","WTSQK":["无以下特殊情况"],"SFXG":"","LABEL5":"9. 今日隔离情况？","GLQK":"无需隔离","LABEL7":"* 本人承诺以上所填报的内容全部真实，并愿意承担相应责任。","CHECK":true,"DWWZ":{},"SUBMIT":"提交信息"}'),
        }
        # print(data)
    except:
        print(id + '打卡失败')
        return
    try:
        res = requests.post(url=url, headers=headers, data=data)
        if res.text:
            print(name + '打卡成功')
    except:
        print(name + '打卡失败')
        return


if __name__ == '__main__':
    for stu in students:
        stu_temp = stu.split(' ')
        id = stu_temp[0]  # 如果只输入学号则默认地址打卡
        if len(stu_temp) > 1:  # 如果有输入地址则使用自己输入的地址进行打卡
            sheng = stu_temp[1]
            shi = stu_temp[2]
            qu = stu_temp[3]
        else:
            sheng = '福建省'
            shi = '福州市'  # 默认学校地址
            qu = '鼓楼区'
        tianbao(id, sheng, shi, qu)
        del id
        time.sleep(2)

    print('全部打卡完成！')
