#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os.path
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import db
import json
from urlparse import urlparse

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/page", PageHandler),
            (r"/links", LinksHandler)


        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret="603550C2-DB60-4518-BC98-819F0A206DCC",
            login_url="/auth/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")



DB = db.MyDB()
SES = DB.make_session()
class PageHandler(BaseHandler):

    def get(self):
        p = self.get_argument('p', default=0)
        p = int(p)
        # d = SES.query(db.FB_ARTICLE).order_by(db.FB_ARTICLE.CMT_NUM.desc()).offset(p).limit(1)
        d = SES.query(db.FB_ARTICLE).filter_by(ID=p)
        for i in d:
            self.write(u'<h3>{},F={},{}</h3>'.format(i.DATE, i.FAV, i.TITLE))
            self.write(i.HTML)
            for c in  json.loads(i.COMMENTS):
                self.write(u'<p>{}:{}</p>'.format(c[1], c[2]))

            self.write('''
            <style>
            pre{
                 white-space: pre-wrap;       /* css-3 */
            }
            </style>
            ''')
            
            self.write(u'<script src="/static/jquery.js" > </script>')
            self.write(u'<script src="/static/page.js" ></script>')

    def post(self):
        
        p = self.get_argument('p', default=0)
        p = int(p)
        v = int(self.get_argument('v'))
        d = SES.query(db.FB_ARTICLE).filter_by(ID=p)
        for i in d:
            i.FAV = v
        SES.commit()
        self.write('good')

class LinksHandler(BaseHandler):
    def get(self):
        p = self.get_argument('p', default=0)
        p = int(p)
        p = p*10
        d = SES.query(db.FB_ARTICLE). offset(p).limit(10)
        for i in d:
            self.write(u'<div><h5>{}</h5></div>'.format(i.TITLE))
            for l in  json.loads(i.LINKS):
                self.write(u'<div><a href="{}" target="_blank">{}</a></div>'.format(l, l))

def main():
    define("port", default=4444, help="run on the given port", type=int)

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

def links():
    d = SES.query(db.FB_ARTICLE).all()
    ll = set()
    for i in d:
            for l in  json.loads(i.LINKS):
                if l:
                    u = urlparse(l)
                    print u.scheme, u.netloc
                    if 'http' in u.scheme:
                        ll.add(u.scheme + '://'  + u.netloc)
                        if 'github' in u.netloc:
                            ll.add(l)
    
    with open('fb_links.txt', 'w') as fp:
        for l in ll:
            line = u'{}\n'.format(l).encode('utf-8')
            print line
            fp.write(line)
        


if __name__ == "__main__":
    links()
