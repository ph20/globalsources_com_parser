#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

sql_path = "sqlite:///{0}".format(os.path.join(config.DEFAULT_DIR, config.SQLITE_DB))
# mysql://username:password@server/db
#sql_path = "mysql://{username}:{password}@localhost/{database}".format(username=config.MYSQL_USER,
#                                                                       password=config.MYSQL_PASSWORD,
#
#                                                                        database=config.MYSQL_DATABASE)
engine = create_engine(sql_path, echo=False)

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    about = Column(String)
    url_card = Column(String)
    site = Column(String)
    country = Column(String)
    address_index = Column(String)
    city = Column(String)
    province = Column(String)
    address = Column(String)
    tel = Column(String)
    fax = Column(String)
    person = Column(String)
    stars = Column(String)
    exporter = Column(Boolean)
    importer = Column(Boolean)
    email = Column(String)
    email_img_url = Column(String)

    def __init__(self,
                 name='',
                 about='',
                 url_card='',
                 site='',
                 country='',
                 index='',
                 city='',
                 province='',
                 address='',
                 tel='',
                 fax='',
                 person='',
                 stars='',
                 exporter=False,
                 importer=False,
                 email='',
                 email_img_url=''
    ):
        self.name = name
        self.about = about
        self.url_card = url_card
        self.site = site
        self.country = country
        self.address_index = index
        self.city = city
        self.province = province
        self.address = address

        self.tel = tel
        self.fax = fax
        self.person = person
        self.stars = stars
        self.exporter = exporter
        self.importer = importer
        self.email = email
        self.email_img_url = email_img_url

    def __repr__(self):
        return "<Company('%s','%s', '%s')>" % (self.name,
                                               self.url_card,
                                               self.city,
                                               self.address_index
        )

metadata = Base.metadata
metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_company(company):
    session.add(company)



