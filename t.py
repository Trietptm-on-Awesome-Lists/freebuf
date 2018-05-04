import db


DB = db.MyDB()
SES = DB.make_session()

def put_links():
    with open('fb_links_common.txt', 'r') as fp:
        ll = fp.readlines()
        for l in ll:
            l = l.decode('utf-8')
            l = l.strip()
            ww = l.split(' ')
            link = db.FB_LINK()
            link.URL = ww[0]
            left = l[len(ww[0]):]
            left = left.strip()
            ww = left.split('*')
            if len(ww)>0:
                link.NOTE = ww[0]
            
            link.FAV = len(l.split('*')) - 1

            SES.add(link)
            SES.commit()
            

