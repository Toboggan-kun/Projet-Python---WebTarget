# -*- coding: utf-8 -*-
import scrapy
import csv
import re
from Tkinter import *
class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    mail = []

    def start_requests(self):
        urls = [
            #            'http://quotes.toscrape.com/page/1/',
            #            'http://quotes.toscrape.com/page/2/',
            'http://www.thelin.net/laurent/labo/html/mailto.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global mail
        i = 0

        page = response.url.split("/")[-2]
        filename = 'dyson-%s.html' % page
        #       with open(filename, 'wb') as f:
        #           f.write(response.body)
        #       self.log('Saved file %s' % filename)
        for line in response.body.splitlines():
            line = line.lower()
            if line.find('href="mailto') == -1:
                #                print "%s" % (line)
                print "NO MAIL"
            else:
                print"%s" % (line)
                match = re.search(r'[\w\.-]+@[\w\.-]+', line)
                #                print"%s" % (match.group(0))
                str1 = match.group(0)
                mail.append(str1)
                print "MAIL"
                i += 1

        print(mail)
        with open('test.csv', 'wb') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(mail)
        print "nombre de mail : %d" % (i)

