# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
import logging

logger = logging.getLogger()
handler = logging.FileHandler("/home/pyt/log/scrapy.log")
handler.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class BasePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # 获取url的md5编码
    def _get_linkmd5id(self, item):
        # url进行md5处理，为避免重复采集设计
        return md5(item['link']).hexdigest()

    # 异常处理
    def _handle_error(self, failue, item, spider):
        logger.err("err %s" % failue)


class OfficialImagePipeline(BasePipeline):

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        linkmd5id = self._get_linkmd5id(item)
        conn.execute("select 1 from officialimage WHERE urlmd5 = %s", linkmd5id)
        ret = conn.fetchone()
        if ret:
            conn.execute("update officialimage set name = %s, url = %s, urlmd5 = %s",
                         (item['name'], item['link'], linkmd5id))
        else:
            conn.execute("insert into officialimage(name, url, urlmd5) values (%s, %s, %s)",
                         (item['name'], item['link'], linkmd5id))
            print "insert into officialimage(name, url, urlmd5) values (%s, %s, %s)", \
                (item['name'], item['link'], linkmd5id)


class ClassifiedImagePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    def _do_upinsert(self, conn, item, spider):
        linkmd5id = self._get_linkmd5id(item)
        print linkmd5id
        conn.execute("select 1 from classifiedimage WHERE linkmd5 = %r", linkmd5id)
        ret = conn.fetchone()
        logger.warn("select 1 from classifiedimage WHERE linkmd5 = %r and ret is: %r" % (linkmd5id, ret))
        if not ret:
            # conn.execute("""
            # update classifiedimage set name = %s, star = %s, pull = %s, description = %s,
            #  automated = %s, official = %s, link = %s, linkmd5 = %s, category = %s
            # """, (item['repo_name'], item['star_count'], item['pull_count'], item['short_description'],
            #       item['is_automated'], item['is_official'], item['link'], linkmd5id, item['category']))
        # else:
            logger.warn("inserting one entry")
            try:
	            conn.execute("""
	            insert into classifiedimage(name, star, pull, description, automated,
	             official, link, linkmd5, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
	            """, (item['repo_name'], item['star_count'], item['pull_count'], item['short_description'],
	                  item['is_automated'], item['is_official'], item['link'], linkmd5id, item['category']))
	            logger.warn("insert successfully")
            except Exception, e:
            	logger.error("insert into mysql error: %r", e)

    # 获取url的md5编码
    def _get_linkmd5id(self, item):
        # url进行md5处理，为避免重复采集设计
        return md5(item['link']).hexdigest()

    # 异常处理
    def _handle_error(self, failue, item, spider):
        logger.error(failue)
