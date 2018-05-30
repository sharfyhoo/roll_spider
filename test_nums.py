
#coding=utf-8

from selenium import webdriver
import time
import random
import requests
import json
import Queue
import csv
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class QZone():
    u'''qq空间类'''

    def __init__(self):
        u'''初始化'''

        self.username = '2634378274'
        self.password = 'admin111111'
        self.ssion = requests.session()
        self.headers = {
            'host': 'user.qzone.qq.com',  
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Referer': 'https://user.qzone.qq.com/2634378274/main'
            }
        self.queue = Queue.Queue()
        self.queue.put('346426523')
        self.csvfile = open('qq_msg.csv', 'w')
        self.writer = csv.writer(self.csvfile)
        self.writer.writerow(['qq', 'name'])
        self.filter_list = ['346426523']
        self.proxies = { "http": "http://192.168.2.229:8888", "https": "http://192.168.2.229:8888", }

    def text_include(self, src, start, end):
        startIndex = src.find(start)
        endIndex = src[startIndex:].find(end)

        if startIndex > 0 and endIndex > 0:
            return src[startIndex: startIndex + endIndex+len(end)]
        return ''


    def text_between(self, src, start, end):
        startIndex = src.find(start) + len(start)
        endIndex = src[startIndex:].find(end)

        if startIndex - len(start) >= 0 and endIndex > 0:
            return src[startIndex: startIndex + endIndex]
        return ''
        
    def login(self):
        u'''phantomjs模拟登录，获取cookie'''

        driver = webdriver.PhantomJS()
        driver.get('https://qzone.qq.com/')
        driver.switch_to_frame('login_frame')
        driver.find_element_by_id("switcher_plogin").click()
        driver.find_element_by_id("u").clear()
        driver.find_element_by_id("p").clear()
        driver.find_element_by_id("u").send_keys(self.username)
        driver.find_element_by_id("p").send_keys(self.password)
        driver.find_element_by_id("login_button").click()
        time.sleep(3)
        driver.save_screenshot("1.png")
        data = driver.page_source
        print data
        if u'spider_man' in data:
            print(u'【login success】:登陆成功')
        else:
            print(u'【login faild】:登陆失败')


        #main_url = driver.current_url
        cookies = [item['name']+'='+item['value'] for item in driver.get_cookies()]
        print cookies
        self.skey = ''
        for i in driver.get_cookies():
            if i['name'] == 'skey':
                self.skey = i['value']
        driver.quit()
        if self.skey:
            self.g_tk = self.getGTK(self.skey)
        else:
            self.g_tk = '@r6qRXgEd5'
        self.cookiestr = '; '.join(item for item in cookies)
        print self.cookiestr
        self.headers['cookie'] = self.cookiestr
        print 'haha'
        self.main()
        #m = self.get_album_list()
        #self.parse_index()
        # proxies = { "http": "http://192.168.199.171:8888", "https": "http://192.168.199.171:8888", }
        # headers = {
        #   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        #   #'referer':'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
        #   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #   'upgrade-insecure-requests': '1',
        # }
        # headers['cookie'] = str(cookiestr)
        # resp = ssion.get(url=main_url, headers=headers, verify=False)
        # print main_url
    def utf8_unicode(self, c):
        u"""对应js中的charCodeAt方法"""

        if len(c)==1:
            return ord(c)
        elif len(c)==2:
            n = (ord(c[0]) & 0x3f) << 6
            n += ord(c[1]) & 0x3f
            return n
        elif len(c)==3:
            n = (ord(c[0]) & 0x1f) << 12
            n += (ord(c[1]) & 0x3f) << 6
            n += ord(c[2]) & 0x3f
            return n
        else:
            n = (ord(c[0]) & 0x0f) << 18
            n += (ord(c[1]) & 0x3f) << 12
            n += (ord(c[2]) & 0x3f) << 6
            n += ord(c[3]) & 0x3f
            return n

    def getGTK(self, skey):
        u'''js里可以看到'''
        hash = 5381
        for i in range(0,len(skey)):
            hash += (hash << 5) + self.utf8_unicode(skey[i])
        return hash & 0x7fffffff

    def get_album_list(self):
        u'''获取相册列表'''
        self.username = '346426523'
        t = random.Random().random()
        url = "https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?g_tk={}&callback=shine0_Callback&t={}&hostUin={}&uin={}&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=4&callbackFun=shine0&_=1527559058314".format(self.g_tk, t, self.username, self.username)
        self.headers['cookie'] = self.cookiestr  
        resp = self.ssion.get(url=url, headers=self.headers)
        print resp.text
        result = resp.text.replace('shine0_Callback(', '').replace(');', '')
        album_dic = json.loads(result)
        assert isinstance(album_dic, dict)
        album_list = album_dic['data']['albumListModeSort']
        #assert isinstance(album_list, list)
        return album_list

    def get_picture_list(self):
        u'''获取每个相册的图片的列表'''
        album_list = self.get_album_list()
        t = random.Random().random()
        for album in album_list:
            album_id = album['id']
            album_name = album['name']
            album_total = album['total']    # 相册里照片的数量，
            # todo: 判断相片数量是不是符合要求

            url = "https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?g_tk={}&callback=shine0_Callback&t={}&mode=0&idcNum=4&hostUin={}&topicId={}&noTopic=0&uin={}&pageStart=0&pageNum=1000&skipCmtCount=0&singleurl=1&batchId=&notice=0&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&outstyle=json&format=jsonp&json_esc=1&question=&answer=&callbackFun=shine0&_=1527561201896".format(self.g_tk, t, self.username, album_id, self.username)
            resp = self.ssion.get(url=url, headers=self.headers)
            print resp.text
            # result = resp.text.replace('shine0_Callback(', '').replace(')', '')
            # main_dic = json.loads(result)

    def parse_index(self, qqid):
        u'''访问好友主页 获取关键参数'''
        url = 'https://user.qzone.qq.com/{}'.format(qqid)
        #url = "https://i.qq.com/?s_url=http%3A%2F%2Fuser.qzone.qq.com%2F346426523&rd=1"
        resp = self.ssion.get(url, headers=self.headers, allow_redirects=True)
        # print resp.request.headers
        # print resp.request.url
        print "【访问qq】*** {} ***".format(qqid)
        #print resp.text
        #print url
        if u"主人设置了权限" in resp.text:
            qzonetoken = None
        else:
            qzonetoken = self.text_between(resp.text, 'window.g_qzonetoken = (function(){ try{return "', '";} catch(e)')
        return qzonetoken

    def get_friend_list(self, qqid):
        qzonetoken = self.parse_index(qqid)
        #print ('【qzonetoken】= {}'.format(qzonetoken))
        if qzonetoken:
            url = "https://user.qzone.qq.com/proxy/domain/g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_simple?uin={}&mask=2&mod=2&fupdate=1&g_tk={}&qzonetoken={}&g_tk={}".format(qqid, self.g_tk, qzonetoken, self.g_tk)
            resp = self.ssion.get(url=url, headers=self.headers)
            #print resp.text
            if u'抱歉，您没有权限访问' not in resp.text:  # 相册好友没有访问权限
                result = resp.text.replace('_Callback(', '').replace(');', '')
                friends_dic = json.loads(result)
                #print result
                friends_list = friends_dic['data']['items']
                if len(friends_list) > 0:
                    for friend in friends_list:
                        qqid = friend['uin']
                        name = friend['name']
                        if qqid not in self.filter_list:
                            self.queue.put(qqid)
                            self.filter_list.append(qqid)
                            self.writer.writerow([qqid, name])

    def main(self):
        self.headers['cookie'] = "pgv_pvi=5701770240; pgv_pvid=9484171904; ptui_loginuin=346426523; RK=jHq1TXnwQk; ptcz=a197b335814ce371e543f9d0b981ba43ce11e29ba77826805d4d8b052667e62f; QZ_FE_WEBP_SUPPORT=1; __Q_w_s__QZN_TodoMsgCnt=1; o_cookie=346426523; pac_uid=1_346426523; pt2gguin=o0346426523; ptisp=cnc; pgv_si=s4975732736; pgv_info=ssid=s3842306356; uin=o0346426523; skey=@sqJbd8Cer; p_uin=o0346426523; pt4_token=OXFoQWE5SBk6LnCXm4ghhrd0lagjfNK-KraOqwa8raY_; p_skey=7FOLr2a6qG90KOmTD6lbWVF9kFKfO92L5DamkjR7IhY_; Loading=Yes; qz_screen=1920x1080; 346426523_todaycount=4; 346426523_totalcount=125959; cpu_performance_v8=21; rv2=8023350C488C8EBC814D4169CA0279E5E6376AE9FB8DC38500; property20=2FCD4EDD1A827C94E525EAFF67EA3856D98D658EAB4EED33FAF61E08DC5A0AA02598C7A39E5CA37C; __Q_w_s_hat_seed=1"
        self.skey = '@sqJbd8Cer'
        self.g_tk = self.getGTK(self.skey)
        while not self.queue.empty():
            qqid = self.queue.get()
            # try:
            #     print(u'\n【start】开始访问qq:{}\n'.format(qqid))
            #     self.get_friend_list(qqid)
            # except Exception as e:
            #     print(u'【wrong】目前访问的qq号为:{}出错\n{}'.format(qqid, e))
            self.get_friend_list(qqid)
        self.csvfile.close()

if __name__ == '__main__':
    qzone = QZone()
    qzone.main()
    #qzone.get_picture_list()
