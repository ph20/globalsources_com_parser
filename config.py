#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEFAULT_DIR = ''
INITIAL_URLS = ['http://www.globalsources.com/']

SQLITE_DB = 'company_db.sqlite'
TOKYO_CABINET_DB = '/root/pars/cache_globalsources.db'
MYSQL_USER = 'grab'
MYSQL_DATABASE = 'grab'
MYSQL_PASSWORD = 'grab777'

PROXY_LIST = '/root/proxylist.txt'

DEBUG = True
LOG_DIR = 'log_dir'
GRAB_LOG = 'grab.log'
NETWORK_LOG = 'grab.network.log'
FATAL_ERROR_DUMP = 'fatal_errors.txt'
THREAD_NUMBER = 30
IMG_MAIL_DIR = 'img_dir'

if DEBUG:
    LOG_TASKNAME = True
else:
    LOG_TASKNAME = False