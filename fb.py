#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import requests
from pyquery import PyQuery as pq
import urllib
import db
import json

def list_routine(n):
    url = "http://www.freebuf.com/page/" + str(n)

    headers = {
        'accept': "*/*",
        'origin': "http://www.freebuf.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'referer': "http://www.freebuf.com/",
        'accept-encoding': "gzip, deflate",
        'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7,la;q=0.6",
        'cookie': "comment_author_e7382aacd190d171a15486ff88d472d4=%E8%BF%99%E7%A7%8D%E6%83%85%E5%86%B5; comment_author_email_e7382aacd190d171a15486ff88d472d4=sdfdsf%40dsdsfd.csdf; wordpress_logged_in_e7382aacd190d171a15486ff88d472d4=majres%7C1524143815%7C3cacf4702c78804bee8f7270233d0ce9; _ga=GA1.2.321412073.1521551827; subject=1; 3cb185a485c81b23211eb80b75a406fd=1522653022; Hm_lvt_cc53db168808048541c6735ce30421f5=1522400870,1522469855,1522653024,1522730965; Hm_lpvt_cc53db168808048541c6735ce30421f5=1522744591",
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "8d7ef050-5e55-9983-3aeb-18efebf4e3b9"
        }

    response = requests.request("POST", url, headers=headers)

    d = pq(response.text)
    d = d('#timeline')
    lt = d('.news-img')
    ret = []
    for l in lt:
        l = pq(l)
        addr = l('a').attr.href
        img = l('img').attr.src
        tlt = l('img').attr.alt
        print addr, tlt, img
        ret.append([addr, tlt, img])
    return ret

def gen_list():
    '''获得文章列表'''
    f = open('freebuf-list.txt', 'a')
    for i in xrange(0, 1000):
        print 'page', i
        ret = list_routine(i)
        if len(ret) == 0:
            print 'DONE'
        else:
            ret = map(lambda x: u"{}[=]{}[=]{}\n".format(x[0],x[1],x[2]), ret)
            for l in ret:
                f.write(l.encode('utf-8'))

def download_img(src_url, save_path):
    data = urllib.urlopen(src_url).read()  
    f = file(save_path,"wb")  
    f.write(data)  
    f.close() 

def download_all_imgs():
    '''下载所有封面图片'''
    count = 0
    with open('freebuf-list.txt', 'r') as fp:
        for l in fp.readlines()[200:]:
            ww = l.split('-|-')
            img = ww[2]
            if len(img) < 10:
                continue
            img = img[:-9]
            save_path = "img/fb_{}_{}.png".format(count, ww[1].strip().replace('/',''))
            count += 1
            print count, img, save_path
            download_img(img, save_path)



def download_article_routine(url):
    headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "http://www.freebuf.com/",
        'accept-encoding': "gzip, deflate",
        'accept-language': "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7,la;q=0.6",
        'cookie': "comment_author_e7382aacd190d171a15486ff88d472d4=%E8%BF%99%E7%A7%8D%E6%83%85%E5%86%B5; comment_author_email_e7382aacd190d171a15486ff88d472d4=sdfdsf%40dsdsfd.csdf; _ga=GA1.2.321412073.1521551827; subject=1; 3cb185a485c81b23211eb80b75a406fd=1522653022; Hm_lvt_cc53db168808048541c6735ce30421f5=1522400870,1522469855,1522653024,1522730965; new_prompt=0; PHPSESSID=fv5s101m7dqbtu2sc545qbtrl4; _gid=GA1.2.2044358967.1522805299; Key_auth=SrMS1CrAeioOCivwX%2FIGrWM%2FmnvUSP%2Bz6K4hNDu59oE%3D; Hm_lpvt_cc53db168808048541c6735ce30421f5=1522827484",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers)

    d = pq(response.text)
    title = d('.title>h2').text()
    da = d('.article-wrap')
    tags = da('.tags>a').text()

    look = da('.look>strong').text()
    see = look.split(' ')
    cmt_n = 0
    if len(see) > 1:
        cmt_n = see[1]
    look = see[0]
    author = da('.name>a').text()
    date = da('.time').text()
    html = d('#contenttxt').html()
    dc = d('#contenttxt')
    links = []
    for a in dc('a'):
        links.append(pq(a).attr.href)

    cmts = d('.comment')
    cmt = []
    for c in cmts:
        c = pq(c)
        p_ava = c('img').attr.src
        p_name = c('.tit').text()
        p_name = p_name.split(' ')[0]
        p_text = c('.txt>p').text()
        # print p_ava, p_name, p_text
        cmt.append([p_ava, p_name, p_text])
    
    # print url, title, look, author, date, len(html), len(links), len(cmt), tags
    return [url, title, look, cmt_n, author, date, html, links, cmt, tags]



def download_all_content():
    DB = db.MyDB()
    ses = DB.make_session()

    count = 0
    with open('freebuf-list.txt', 'r') as fp:
        for l in fp.readlines()[1951+397+7045:]:
            l = l.decode('utf-8')
            ww = l.split('-|-')
            url = ww[0]
            crt = download_article_routine(url)
            count += 1
            # for i, v in enumerate(crt):
            #     print i, v

            at = db.FB_ARTICLE()
            at.AUTHOR = crt[4]
            at.CMT_NUM = int(crt[3])
            at.COMMENTS = json.dumps(crt[8])
            at.DATE = crt[5]
            at.HTML = crt[6]
            at.LINKS = json.dumps(crt[7])
            at.TAGS = crt[9]
            at.VIEW = crt[2]
            at.TITLE = ww[1]
            at.ADDR = crt[0]

            ses.add(at)
            print count, at.TITLE

            ses.commit()

g_map = {}
def download_avatars():

    DB = db.MyDB()
    ses = DB.make_session()
    cnt = 0

    for a in ses.query(db.FB_ARTICLE):
        cmts = json.loads(a.COMMENTS)
        for c in  cmts:
            u = c[0]
            if u == None:
                continue
            if 'headimg' in u:
                pass
            elif 'user-avatar' in u:
                pass
            else:
                if g_map.has_key(u):
                    pass
                else:
                    print cnt, c[1]
                    g_map[u] = 1
                    try:
                        download_img(u, u'head/{}.png'.format(c[1]))
                    except Exception:
                        print 'ERROR'
                    cnt += 1

download_avatars()