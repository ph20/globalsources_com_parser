#!/usr/bin/env python
# -*- coding: utf-8 -*-

from grab.spider import Spider, Task, Data
from grab.tools.logs import default_logging
import urlparse
import re
import sys
import os
import company as comp_db

import ocr.mailimg_to_str
import config

INDEX_PATTERN = re.compile('(.*) (\d{3,6})')

def chek_loading(html='', slogan='Trade Media Holdings Ltd.'):
    """
    Функция для проверки коректности загрузки страницы
    подстраховка если прокси сервер вместо страницы передал чтото другое
    проверяетса посредством присутствия некой последовательности в странице
    """
    is_ok = slogan in html
    return is_ok

class GlobalsourcesCrawler(Spider):


    initial_urls = config.INITIAL_URLS
    parsed_url = [] ## масив ссылок на карточки компаний для предотвращения повторного парсинга

    def task_initial(self, grab, task):
        """
        Извлекаим ссылку на страницу с категориями компаний
        """
        if not chek_loading(grab.response.body):
            yield Task('initial', url=task.url, priority=100)
            return

        category_url = grab.doc.select('//a[contains(text(), "Browse Categories")]').attr('href')
        yield Task('level_1', url=category_url, priority=95)


    def task_level_1(self, grab, task):
        """
        Получаем ссылки на категории
        """
        if not chek_loading(grab.response.body):
            yield Task('level_1', url=task.url, refresh_cache=True, priority=90)
            return

        for url_level_2 in grab.doc.select('//div[@class="browse-ttl"]/a').attr_list('href'):
            yield Task('level_2', url=grab.make_url_absolute(url_level_2), priority=85)

    def task_level_2(self, grab, task):
        """
        Получаем ссылки на подкатегории
        """
        if not chek_loading(grab.response.body):
            yield Task('level_2', url=task.url, refresh_cache=True, priority=80)
            return

        for url_level_3 in grab.doc.select('//div[@class="category-top"]/a').attr_list('href'):
            yield Task('level_3', url=grab.make_url_absolute(url_level_3), priority=75)

    def task_level_3(self, grab, task):
        """
        Получаем ссылки на подкатегории
        """
        if not chek_loading(grab.response.body):
            yield Task('level_3', url=task.url, refresh_cache=True, priority=70)
            return

        for url_level_4 in grab.doc.select('//div[@class="category-top"]/a').attr_list('href'):
            url_level_4 = grab.make_url_absolute(url_level_4)
            yield Task('level_4', url=url_level_4, priority=65)
            print """add url yield Task('level_4', url=url_level_4, priority=65):""", task.url
            self.parsed_url.append(url_level_4)


    def task_level_4(self, grab, task):
        """
        Наконец то список продукции где также есть ссылки на карточку компании
        """
        if not chek_loading(grab.response.body):
            yield Task('level_4', url=task.url, refresh_cache=True, priority=50)
            return

        url_level_5_list = grab.doc.select('//a[@class="supplierTit"]').attr_list('href')
        for url_level_5 in url_level_5_list:
            url_level_5 = grab.make_url_absolute(url_level_5)


            if not url_level_5 in self.parsed_url:  ## проверям не извлекали ли уже ссылку на карточку компании
                yield Task('level_5', url=url_level_5, priority=45)


        for next_page_url in grab.doc.select('//p[@class="pagination mt5"]/a').attr_list('href'):
            next_page_url = grab.make_url_absolute(next_page_url)
            if not next_page_url in self.parsed_url:
                yield Task('level_4', url=next_page_url, priority=55)
                self.parsed_url.append(next_page_url)


    def task_level_5(self, grab, task):
        """
        Парсим карточку компании
        """
        if not chek_loading(grab.response.body, 'manufacturers'):
            yield Task('level_5', url=task.url, refresh_cache=True, priority=80)
            return

        company_info = grab.doc.select('//div[@class="companyInfo"]').one()
        company = comp_db.Company()
        try:
            company.name = company_info.select('//*[@class="mt10"]').text()
        except:
            yield Task('level_5', url=task.url, priority=80)
            return

        company.url_card = task.url

        try:
            company.site = '; '.join(company_info.select('p[contains(text(), "Homepage Address")]/following-sibling::p[1]').text_list())
        except:
            pass

        #try:
        #    country = grab.doc.select('//p[@class="supplierInfo_main"]/*').text_list()[-1]
        #    country = country.replace('(mainland)', '').strip()
        #    company.country = country
        #except:
        #    pass

        try:
            country_and_index = ''.join(company_info.select('text()').text_list())
        except:
            country_and_index = ''
        try:
            company.country, company.address_index = INDEX_PATTERN.search(country_and_index).group(1, 2)
        except:
            company.country = country_and_index

        try:
            company.city = company_info.select('p[contains(text(), "Tel")]/preceding-sibling::p[2]').text()
        except:
            pass

        try:
            company.province = company_info.select('p[contains(text(), "Tel")]/preceding-sibling::p[1]').text()
        except:
            pass

        try:
            company.address = company_info.select('p[2]').text()
        except:
            pass

        try:
            company.fax = company_info.select('p[contains(text(), "Fax")]').text().replace('Fax:', '').strip()
        except:
            pass

        try:
            company.tel = company_info.select('p[contains(text(), "Tel")]').text().replace('Tel:', '').strip()
        except:
            pass

        try:
            company.about = grab.doc.select('//div[@class="commonBox userContent"]').text().replace('... more >>', '')
        except:
            pass

        try:
            company.email_img_url = company_info.select('p[contains(text(), "-mail")]/img').attr('src')
            company.email_img_url = grab.make_url_absolute(company.email_img_url)
        except:
            pass

        try:
            company.person = grab.doc.select('//div[@class="companyInfo"][2]/p[2]').text()
        except:
            pass

        try:
            company.stars = grab.doc.select('//p[@class="supplierInfo_main"]/a').text()
        except:
            pass

        company.importer = 'Import' in grab.doc.select('//div[@class="CoProfile"]').text(smart=True)
        company.exporter = 'Export' in grab.doc.select('//div[@class="CoProfile"]').text(smart=True)

        comp_db.session.add(company)
        comp_db.session.commit()

        yield Task('ocr_image', url=company.email_img_url, priority=35)



    def task_ocr_image(self, grab, task):
        """
        Собствено процес распознания
        """
        email_for_ocr_path = os.path.join(config.IMG_MAIL_DIR, 'email_for_ocr')
        grab.response.save(email_for_ocr_path)
        comp = comp_db.session.query(comp_db.Company).filter_by(email_img_url=task.url)[0]
        comp.email = ocr.mailimg_to_str.tesser_engine(email_for_ocr_path)
        comp_db.session.add(comp)
        comp_db.session.commit()

def start_parsing():
    default_logging(grab_log=config.GRAB_LOG, network_log=config.NETWORK_LOG)
    bot = GlobalsourcesCrawler(thread_number=config.THREAD_NUMBER)
    #bot.setup_cache(engine='tokyo_cabinet', database=config.TOKYO_CABINET_DB)
    #bot.setup_queue('mysql', database='grab', use_compression=True, user='grab', passwd='grab777')
    bot.setup_cache('mysql', database=config.MYSQL_DATABASE, use_compression=True, user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD)
    #if config.DEBUG:
    #     bot.setup_grab(log_dir=config.LOG_DIR)
    bot.load_proxylist(config.PROXY_LIST, 'text_file', proxy_type='http')
    try:
        bot.run()
    except KeyboardInterrupt:
        pass
    if config.DEBUG:
        bot.save_list('fatal', config.FATAL_ERROR_DUMP)
    comp_db.session.commit()
    print bot.render_stats()
    sys.exit()

if __name__ == '__main__':
    start_parsing()





