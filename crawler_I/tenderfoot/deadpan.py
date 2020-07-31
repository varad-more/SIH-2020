"""Deadpan module

This module is the initial crawler for the SIH 2020 CA scraping bot.
"""

__version__ = '2'
__author__ = 'Abhijit Acharya'

import gc
import os
import sys
import ssl
import json
import sqlite3
import urllib.error
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen

error_string = """
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n
ERROR : {}\n
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n
"""

class text_color:
    HEADER_COLOR = '\033[95m'
    BLUE_COLOR = '\033[94m'
    GREEN_COLOR = '\033[92m'
    WARNING_COLOR = '\033[93m'
    FAILED_COLOR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Helper:
    def __init__(self):
        pass

    def get_filename(self, filename):
        # If current filesize > 200MB then generate new file name
        if os.stat('output/dumps/'+filename).st_size>200000000:
            filename = str(datetime.timestamp(datetime.now()))
            open('output/dumps/'+filename, 'a').close()
            return filename
        return filename

    def dump_html(self, row, soup, filename):
        # Insert html
        with open('output/dumps/'+filename,'r+') as f:
            try:
                data = json.load(f)
                data[row[0]] = str(soup)
                f.seek(0)
                json.dump(data, f)
            except Exception as ex:
                print(ex)
                json.dump({row[0] : str(soup)},f)
            finally:
                f.close()

    def get_keyword(self,soup):
        try:
            header = soup.find('head')
            html_str = header.find('meta',attrs={'name':'news_keywords'})
            meta_keyword_str = html_str.get('content')
            if meta_keyword_str=='[]':
                return 'NULL'
            return meta_keyword_str
        except:
            return 'NULL'

    def __del__(self):
        pass

class Deadpan(object):
    """This class provides methods for obtaining links from different news websites"""

    def __init__(self, website_name, website_url,many):
        self.website_name = website_name
        self.website_url  = website_url
        self.many = str(many)
        self.starturl = website_url
        self.POSITIVE = 0.3
        self.NEGATIVE = 0.3
        super(Deadpan, self).__init__()
        try:
            filesizes = {os.stat('output/dumps/'+filename).st_size:filename for filename in os.listdir('output/dumps/')}
            self.filename = filesizes[min(filesizes.keys())]
        except:
            os.mkdir('output')
            os.mkdir('output/dumps')
            self.filename = str(datetime.timestamp(datetime.now()))
            open('output/dumps/'+self.filename, 'a').close()
        print(text_color.HEADER_COLOR + "Initialized deadpan object" + text_color.ENDC)

    # Ignore SSL certificate errors
    def ignore_ssl_error(self,state=False):
        try:
            if state==True:
                print(text_color.GREEN_COLOR + "Ignoring SSL errors" + text_color.ENDC)
                self.SSL_CONTEXT = ssl.create_default_context()
                self.SSL_CONTEXT.check_hostname = False
                self.SSL_CONTEXT.verify_mode = ssl.CERT_NONE
            else:
                print(text_color.WARNING_COLOR + "Not ignoring SSL errors" + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Create table if not already created
    def create_table_if_not_exists(self):
        try:
            # Connect to database
            self.connection = sqlite3.connect('output/tenderfoot.sqlite')
            self.cursor = self.connection.cursor()
            print(text_color.GREEN_COLOR + "Connected to database " + 'tenderfoot' + text_color.ENDC)

            # Creates the main table
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Pages
               (id INTEGER PRIMARY KEY, url TEXT UNIQUE, keywords TEXT, website TEXT,
                 error INTEGER, old_rank REAL, new_rank REAL, moved INTEGER, filename TEXT)''')

            # Many to many tableId,url,title,keywords,content,author,publish_date,old_rank,new_rank,error
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Links
               (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')

            # Website main links, for site based ranking
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Webs(name TEXT, url TEXT UNIQUE, web_rank REAL)''')

            # Error table, for error logging
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Errors(url TEXT UNIQUE, exception TEXT)''')
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)
            sys.exit(0)

    # Check to see if we are already in progress...
    def check_if_already_in_progress(self):
        try:
            # Get id and url of empty html
            self.cursor.execute('SELECT id,url FROM Pages WHERE keywords is NULL and website is ? and error is NULL ORDER BY RANDOM() LIMIT 1',(self.website_name,))
            row = self.cursor.fetchone()

            if row is not None:
                print(text_color.BLUE_COLOR + "Restarting existing crawl.  Remove tenderfoot.sqlite to start a fresh crawl." + text_color.ENDC)
            else :
                self.starturl = self.website_url
                if(self.starturl.endswith('/')) : self.starturl = self.starturl[:-1]
                web = self.starturl
                if(self.starturl.endswith('.htm') or self.starturl.endswith('.html')) :
                    pos = self.starturl.rfind('/')
                    web = self.starturl[:pos]

                if(len(web) > 1) :
                    self.cursor.execute('INSERT OR IGNORE INTO Webs(name,url,web_rank) VALUES(?, ?, ?)',(self.website_name, web, int(self.many)))
                    self.cursor.execute('INSERT OR IGNORE INTO Pages(url, website, keywords, new_rank) VALUES(?, ?, NULL, 1.0)',(self.starturl, self.website_name))
                    self.connection.commit()
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # get current website and start crawling
    def get_current_webs_and_deadpan(self):
        try:
            # Get current website
            self.cursor.execute('''SELECT url FROM Webs''')
            webs = list()
            for row in self.cursor:
                webs.append(str(row[0]))

            print(text_color.WARNING_COLOR + "Current Websites : " + text_color.ENDC,webs)

            # Counter
            many = int(self.many)
            while True:
                gc.collect()
                self.cursor.execute('SELECT web_rank from Webs WHERE url=? LIMIT 1',(self.starturl,))
                row = self.cursor.fetchone()
                self.web_rank = row[0]
                # For first iteration...
                if(many < 1) :
                    print(text_color.GREEN_COLOR + 'Done!!' + text_color.ENDC)
                    break
                many = many - 1

                # Again get unchecked page
                self.cursor.execute('SELECT id,url FROM Pages WHERE keywords is NULL and website is ? and error is NULL ORDER BY new_rank DESC LIMIT 1',(self.website_name,))
                try:
                    # Gets id and url
                    row = self.cursor.fetchone()
                    fromid = row[0]
                    url = row[1]
                except Exception as ex:
                    # All done for today
                    print(text_color.FAILED_COLOR + 'No unretrieved HTML pages found' + text_color.ENDC)
                    self.connection.commit()
                    many = 0
                    break

                # If we are retrieving this page, there should be no links from it, just verifying
                self.cursor.execute('DELETE from Links WHERE from_id=?',(fromid,))
                try:
                    document = urlopen(url, context=self.SSL_CONTEXT)

                    html = document.read()
                    if document.getcode() != 200 :
                        print(text_color.FAILED_COLOR + "Error on page : ",document.getcode() + text_color.ENDC)
                        self.cursor.execute('INSERT OR IGNORE INTO Errors(url, exception) VALUES(?, ?)',(url, str(document.getcode())))
                        self.cursor.execute('UPDATE Webs SET web_rank=? WHERE url=?',(int(self.web_rank)-self.NEGATIVE,self.starturl))
                        cur.execute('UPDATE Pages SET error=? WHERE url=?',(document.getcode(), url))

                    if 'text/html' != document.info().get_content_type() :
                        print(text_color.FAILED_COLOR + "Non text/html page" + text_color.ENDC)
                        self.cursor.execute('DELETE FROM Pages WHERE url=?',(url,))
                        self.connection.commit()
                        continue

                    soup = BeautifulSoup(html, "html.parser")
                except KeyboardInterrupt:
                    print(text_color.FAILED_COLOR + 'Deadpan interrupted by user...' + text_color.ENDC)
                    break
                except Exception as ex:
                    print(text_color.FAILED_COLOR + "Unable to retrieve or parse page" + text_color.ENDC)
                    self.cursor.execute('UPDATE Pages SET error=-1 WHERE url=?',(url,))
                    self.cursor.execute('INSERT OR IGNORE INTO Errors(url, exception) VALUES(?, ?)',(url, str(ex)))
                    self.cursor.execute('UPDATE Webs SET web_rank=? WHERE url=?',(int(self.web_rank)-self.NEGATIVE,self.starturl))
                    self.connection.commit()
                    continue

                # Create helper object and get keywords 
                helper = Helper()
                meta_keyword_str = helper.get_keyword(soup)
                self.filename = helper.get_filename(self.filename)
                

                # Insert url and keywords
                # Seperate statements make sure that error in first does not end up not inserting the keywords
                self.cursor.execute('INSERT OR IGNORE INTO Pages(url, website, keywords, moved, new_rank, filename) VALUES(?, NULL, NULL, NULL, 1.0, NULL)',(url,))
                self.cursor.execute('UPDATE Pages SET website=?, keywords=?, moved=?, filename=? WHERE url=?',(self.website_name, meta_keyword_str, 0, self.filename, url))
                self.cursor.execute('UPDATE Webs SET web_rank=? WHERE url=?',(int(self.web_rank)+self.POSITIVE,self.starturl))

                # Dump html to 'dumps/'
                helper.dump_html(row,soup,self.filename)
                del helper,row

                # Retrieve all of the anchor tags
                tags = soup('a')
                for tag in tags:
                    href = tag.get('href', None)
                    if(href is None) : continue
                    # Resolve common link issues and remove tags for images
                    parsed_url = urlparse(href)

                    # If http or https is empty, add the domain url before href
                    if(len(parsed_url.scheme)<1):
                        href = urljoin(url, href)

                    hashpos = href.find('#')
                    if(hashpos > 1) : href = href[:hashpos]
                    if(href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') or href.endswith('.jpeg')) : continue
                    if(href.endswith('/')) : href = href[:-1]

                    if(len(href) < 1) : continue

                    # Check if the URL belongs to specified domains
                    found = False
                    for web in webs:
                        if(href.startswith(web)) :
                            found = True
                            break
                    if not found : continue # go to next loop if it links off the required website

                    # Else insert
                    self.cursor.execute('INSERT OR IGNORE INTO Pages(url, website, keywords, new_rank) VALUES(?, ?, NULL, 1.0)',(href, self.website_name))
                    self.cursor.execute('SELECT id FROM Pages WHERE url=? LIMIT 1',(href,))
                    try:
                        row = self.cursor.fetchone()
                        toid = row[0]
                    except:
                        print(text_color.FAILED_COLOR + 'Could not retrieve id' + text_color.ENDC)
                        continue
                    self.cursor.execute('INSERT OR IGNORE INTO Links(from_id, to_id) VALUES(?, ?)',(fromid, toid))
                self.connection.commit()

        except KeyboardInterrupt:
            print(text_color.FAILED_COLOR + "Deadpan interrupted by user..." + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Close connection
    def close_cur(self):
        try:
            self.cursor.close()
            print(text_color.GREEN_COLOR + "Connection closed" + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format(ex) + text_color.ENDC)

    # Main spider
    def spider(self):
        self.ignore_ssl_error(True)
        self.create_table_if_not_exists()
        self.check_if_already_in_progress()
        self.get_current_webs_and_deadpan()
        self.close_cur()
