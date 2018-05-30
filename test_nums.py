
#coding=utf-8

from selenium import webdriver
import time
import random
import requests
import json
import Queue
import csv
import re
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class QZone():
    u'''qq空间类'''

    def __init__(self):
        u'''初始化'''

        self.username = '2221639157'
        self.password = 'hu123654'
        self.ssion = requests.session()
        self.headers = {
            'host': 'user.qzone.qq.com',  
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Referer': 'https://user.qzone.qq.com/2634378274/main'
            }
        self.queue = Queue.Queue()
        self.queue.put('862655287')
        self.csvfile = open('qq_msg.csv', 'w')
        self.writer = csv.writer(self.csvfile)
        self.writer.writerow(['qq', 'name'])
        self.filter_list = ['862655287']
        self.proxies = { "http": "http://192.168.2.229:8888", "https": "http://192.168.2.229:8888", }
        self.pic_dir = os.getcwd() + '/qq_pics'

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
        #print data
        if u'demaxiya' in data:
            print(u'【login success】:登陆成功')
        else:
            print(u'【login faild】:登陆失败')


        #main_url = driver.current_url
        cookies = [item['name']+'='+item['value'] for item in driver.get_cookies()]
        #print cookies
        self.skey = ''
        for i in driver.get_cookies():
            if i['name'] == 'skey':
                self.skey = i['value']
        driver.quit()
        if self.skey:
            self.g_tk = self.getGTK(self.skey)
        self.cookiestr = '; '.join(item for item in cookies)
        self.headers['cookie'] = self.cookiestr
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

    def get_album_list(self, qqid):
        u'''获取相册列表'''
        #self.username = '346426523'
        t = random.Random().random()
        url = "https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?g_tk={}&callback=shine0_Callback&t={}&hostUin={}&uin={}&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=4&callbackFun=shine0&_=1527559058314".format(self.g_tk, t, qqid, self.username)
        #self.headers['cookie'] = self.cookiestr  
        resp = self.ssion.get(url=url, headers=self.headers)
        print resp.text
        result = resp.text.replace('shine0_Callback(', '').replace(');', '')
        album_dic = json.loads(result)
        assert isinstance(album_dic, dict)
        album_list = album_dic['data']['albumListModeSort']
        #assert isinstance(album_list, list)
        return album_list

    def get_picture_list(self, qqid):
        u'''获取每个相册的图片的列表'''
        self.headers['cookie']= "_qpsvr_localtk=0.09296240426904356; pgv_pvi=5298276352; pgv_si=s645937152; ptisp=cnc; pgv_pvid=445871590; pgv_info=ssid=s8576858245; ptui_loginuin=2634378274; pt2gguin=o2634378274; RK=xVgV1bFB5M; ptcz=f0325ee2ef78c84144b41f218c3766d4b6872aff7fd4eee0bc7716354004aba0; qqmusic_uin=; qqmusic_key=; qqmusic_fromtag=; midas_openid=2634378274; midas_openkey=@5bNq4zjh8; rv2=80A93B1CFEA49ED8E89172B7686B2EBA3BE53C66F87CF4F2F5; property20=E99D5A2B562BB97BB6A553BFE43F2D9A106DB80936DEF117BCFAF317E62691C5513E3C58DFDE6A6A; uin=o2634378274; skey=@fmiwKjA2J"
        self.skey = '@fmiwKjA2J'
        self.g_tk = self.getGTK(self.skey)

        album_list = self.get_album_list(qqid)
        t = random.Random().random()
        qq_path = self.pic_dir + '/' + qqid + '/'
        if not os.path.exists(qq_path):
            os.mkdir(qq_path)
        for album in album_list:
            album_id = album['id']
            album_name = album['name']
            album_total = int(album['total'])    # 相册里照片的数量，
            # todo: 判断相片数量是不是符合要求
            if album_total > 0 and not album.get('question'):
                album_path = qq_path + album_id
                if not os.path.exists(album_path):
                    os.mkdir(album_path)
                page_list = self.get_pagelist(album_total)
                for page in page_list:
                    url = "https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?g_tk={}&callback=shine0_Callback&t={}&mode=0&idcNum=4&hostUin={}&topicId={}&noTopic=0&uin={}&pageStart={}&pageNum=50&skipCmtCount=0&singleurl=1&batchId=&notice=0&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&outstyle=json&format=jsonp&json_esc=1&question=&answer=&callbackFun=shine0&_=1527561201896".format(self.g_tk, t, qqid, album_id, self.username, page)
                    resp = self.ssion.get(url=url, headers=self.headers)
                    photo_list = json.loads(self.text_between(resp.text, '(', ')'))['data']['photoList']
                    for photo in photo_list:
                        photo_url = photo['url'].replace("\\", '')
                        photo_id = photo['sloc']
                        photo_path = album_path + '/' + photo_id
                        print photo_url
                        photo_content = self.ssion.get(url=photo_url, headers=self.headers).content
                        with open(photo_path+'.jpg', 'wb') as f:
                            f.write(photo_content)

    def parse_index(self, qqid):
        u'''访问好友主页 获取关键参数'''
        self.headers['cookie']= "_qpsvr_localtk=0.09296240426904356; pgv_pvi=5298276352; pgv_si=s645937152; ptisp=cnc; pgv_pvid=445871590; pgv_info=ssid=s8576858245; ptui_loginuin=2634378274; pt2gguin=o2634378274; RK=xVgV1bFB5M; ptcz=f0325ee2ef78c84144b41f218c3766d4b6872aff7fd4eee0bc7716354004aba0; 2634378274_totalcount=1; QZ_FE_WEBP_SUPPORT=1; __Q_w_s__QZN_TodoMsgCnt=1; zzpaneluin=; zzpanelkey=; qz_screen=1920x1080; 2634378274_todaycount=0; qqmusic_uin=; qqmusic_key=; qqmusic_fromtag=; midas_openid=2634378274; midas_openkey=@5bNq4zjh8; cpu_performance_v8=2; qzmusicplayer=qzone_player_2534092499_1527663535388; rv2=80A93B1CFEA49ED8E89172B7686B2EBA3BE53C66F87CF4F2F5; property20=E99D5A2B562BB97BB6A553BFE43F2D9A106DB80936DEF117BCFAF317E62691C5513E3C58DFDE6A6A; uin=o2634378274; skey=@fmiwKjA2J; p_uin=o2634378274; pt4_token=gigNsLyzFJgpzax*M*338c6Dn5xpBWwobf0Z13xJWE8_; p_skey=7bATHacwSygXUdb4CYlSfrf9YGG7ni6mNXmSjG89T5g_"
        self.skey = '@fmiwKjA2J'
        self.g_tk = self.getGTK(self.skey)
        url = 'https://user.qzone.qq.com/{}'.format(qqid)
        #url = "https://i.qq.com/?s_url=http%3A%2F%2Fuser.qzone.qq.com%2F346426523&rd=1"
        resp = self.ssion.get(url, headers=self.headers)
        # print resp.request.headers
        # print resp.request.url
        print "【访问qq】*** {} ***".format(qqid)
        #print resp.text
        #print url
        if u"主人设置了权限" in resp.text:
            qzonetoken = None
        else:
            self.filter_list.append(qqid)
            self.writer.writerow([qqid, name])
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


    def get_pagelist(self, album):
        m = (float(album)/50) - (album/50)
        if m > 0:
            page = (album/50) + 1
        elif m == 0:
            page = album/50

        pagelist = [i*50 for i in range(page)]
        return pagelist

    def main(self):
        # self.headers['cookie'] = "pgv_pvi=5701770240; pgv_pvid=9484171904; ptui_loginuin=346426523; RK=jHq1TXnwQk; ptcz=a197b335814ce371e543f9d0b981ba43ce11e29ba77826805d4d8b052667e62f; QZ_FE_WEBP_SUPPORT=1; __Q_w_s__QZN_TodoMsgCnt=1; o_cookie=346426523; pac_uid=1_346426523; pt2gguin=o0346426523; ptisp=cnc; pgv_si=s4975732736; pgv_info=ssid=s3842306356; uin=o0346426523; skey=@sqJbd8Cer; p_uin=o0346426523; pt4_token=OXFoQWE5SBk6LnCXm4ghhrd0lagjfNK-KraOqwa8raY_; p_skey=7FOLr2a6qG90KOmTD6lbWVF9kFKfO92L5DamkjR7IhY_; Loading=Yes; qz_screen=1920x1080; 346426523_todaycount=4; 346426523_totalcount=125959; cpu_performance_v8=21; rv2=8023350C488C8EBC814D4169CA0279E5E6376AE9FB8DC38500; property20=2FCD4EDD1A827C94E525EAFF67EA3856D98D658EAB4EED33FAF61E08DC5A0AA02598C7A39E5CA37C; __Q_w_s_hat_seed=1"
        # self.skey = '@sqJbd8Cer'
        # self.g_tk = self.getGTK(self.skey)
        while not self.queue.empty():
            qqid = self.queue.get()
            try:
                print(u'\n【start】开始访问qq:{}\n'.format(qqid))
                self.get_friend_list(qqid)
            except Exception as e:
                print(u'【wrong】目前访问的qq号为:{}出错\n{}'.format(qqid, e))
            #self.get_friend_list(qqid)
        self.csvfile.close()

if __name__ == '__main__':
    qzone = QZone()
    qzone.login()
    #qzone.parse_index('346426523')
