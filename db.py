#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
import sqlalchemy.types
import logging
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class FB_ARTICLE(Base):
    __tablename__ = "FB_ARTICLE"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    AUTHOR = Column(String)
    VIEW = Column(Integer)
    DATE = Column(String)
    CMT_NUM = Column(Integer)
    COMMENTS = Column(String)
    HTML = Column(String)
    LINKS = Column(String)
    TAGS = Column(String)
    ADDR = Column(String)
    TITLE = Column(String)
    FAV = Column(Integer)

class FB_LINK(Base):
    __tablename__ = "FB_LINK"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    URL = Column(String)
    NOTE = Column(String)
    FAV = Column(Integer)


class MyDB(object):
    def __init__(self):
        logging.info("database init")
        self.engine = create_engine("sqlite:///freebuf.db", pool_recycle=3600, echo=False)
        self.make_session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        logging.info("create database tables")

if __name__ == "__main__":
    '''直接运行此文件来创建数据库'''
    mydb = MyDB()
    mydb.create_tables()
    print "DONE"