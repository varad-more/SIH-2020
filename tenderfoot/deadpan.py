"""Deadpan module

This module is the initial crawler for the SIH 2020 CA scraping bot.
"""

__version__ = '2'
__author__ = 'Abhijit Acharya'

import gc
import sys
import ssl
import requests
import mysql.connector
from datetime import datetime
from bs4 import BeautifulSoup
from requests.compat import urljoin

error_string = """
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n
ERROR in {} : {}\n
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

    def get_filename(self):
        filename = str(datetime.timestamp(datetime.now()))
        open('output/dumps/'+filename, 'a', encoding='utf-8').close()
        return filename

    def dump_html(self, row, soup, filename):
        # Insert html
        with open('output/dumps/'+filename, 'w', encoding='utf-8') as f:
            try:
                f.write(str(soup))
            except Exception as ex:
                print(text_color.FAILED_COLOR
                      + error_string.format("", ex)
                      + text_color.ENDC)
            finally:
                f.close()

    def get_keyword(self, soup):
        try:
            header = soup.find('head')
            html_str = header.find('meta', attrs={'name': 'news_keywords'})
            meta_keyword_str = html_str.get('content')
            if meta_keyword_str == '[]':
                return 'NULL'
            return meta_keyword_str
        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format("", ex)
                  + text_color.ENDC)
            return 'NULL'

    def __del__(self):
        pass


class Deadpan(object):
    """
        This class provides methods for obtaining
        links from different news websites
    """

    def __init__(self, website_name, website_url, many):
        self.website_name = website_name
        self.website_url = website_url
        self.many = str(many)
        self.starturl = website_url
        self.POSITIVE = 0.5
        self.NEGATIVE = 0.3
        super(Deadpan, self).__init__()

        self.filename = ""
        print(text_color.HEADER_COLOR
              + "Initialized deadpan object"
              + text_color.ENDC)

    # Ignore SSL certificate errors
    def ignore_ssl_error(self, state=False):
        try:
            if state:
                print(text_color.GREEN_COLOR
                      + "Ignoring SSL errors"
                      + text_color.ENDC)
                self.SSL_CONTEXT = ssl.create_default_context()
                self.SSL_CONTEXT.check_hostname = False
                self.SSL_CONTEXT.verify_mode = ssl.CERT_NONE
            else:
                print(text_color.WARNING_COLOR
                      + "Not ignoring SSL errors"
                      + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format("", ex)
                  + text_color.ENDC)

    # Create table if not already created
    def create_table_if_not_exists(self):
        try:
            # Connect to database
            self.connection = mysql.connector.connect(
                     host="database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com",
                     user="admin",
                     password="SIH_2020",
                     database="pythanos_main"
            )

            # self.connection = sqlite3.connect('output/tenderfoot.sqlite')
            self.cursor = self.connection.cursor(buffered=True)
            print(text_color.GREEN_COLOR
                  + "Connected to database "
                  + 'tenderfoot' + text_color.ENDC)

        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format("", ex)
                  + text_color.ENDC)
            sys.exit(0)

    # Check to see if we are already in progress...
    def check_if_already_in_progress(self):
        try:
            # Get id and url of empty html
            self.cursor.execute('''
                SELECT pages_id,url FROM pages WHERE keywords is NULL
                and website=%s and error is NULL
                ORDER BY RAND() LIMIT 1''', (self.website_name,))
            row = self.cursor.fetchone()

            if row is not None:
                print(text_color.BLUE_COLOR
                      + """Restarting existing crawl.
                      Remove tenderfoot.sqlite to start a fresh crawl."""
                      + text_color.ENDC)
            else:
                self.starturl = self.website_url
                if(self.starturl.endswith('/')):
                    self.starturl = self.starturl[:-1]
                web = self.starturl
                if(self.starturl.endswith('.htm')
                        or self.starturl.endswith('.html')):
                    pos = self.starturl.rfind('/')
                    web = self.starturl[:pos]

                if(len(web) > 1):
                    self.cursor.execute('''INSERT IGNORE INTO
                        webs(name, url, web_rank) VALUES(%s, %s, %s)'''
                                        , (self.website_name, web,
                                            int(self.many)))
                    self.cursor.execute('''INSERT IGNORE INTO
                        pages(url, website, keywords, new_rank)
                            VALUES(%s, %s, NULL, 1.0)'''
                                        , (self.starturl, self.website_name))
                    self.connection.commit()
        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format("", ex)
                  + text_color.ENDC)

    # get current website and start crawling
    def get_current_webs_and_deadpan(self):
        try:
            # Get current website
            self.cursor.execute('''SELECT url FROM webs''')
            webs = list()
            for row in self.cursor:
                webs.append(str(row[0]))

            # Counter
            many = int(self.many)
            while True:
                gc.collect()
                self.cursor.execute('''SELECT web_rank from webs WHERE url=%s
                    LIMIT 1''', (self.starturl,))
                row = self.cursor.fetchone()
                self.web_rank = row[0]
                # For first iteration...
                if(many < 1):
                    print(text_color.GREEN_COLOR + 'Done!!' + text_color.ENDC)
                    break
                many = many - 1
                # Again get unchecked page
                self.cursor.execute('''SELECT pages_id, url FROM pages
                                    WHERE keywords is NULL and website=%s
                                    and error is NULL ORDER BY new_rank DESC
                                    LIMIT 1''', (self.website_name,))
                try:
                    # Gets id and url
                    row = self.cursor.fetchone()
                    fromid = row[0]
                    url = row[1]
                    print("url : ", url)
                except Exception as ex:
                    # All done for today
                    print(text_color.FAILED_COLOR
                          + 'No unretrieved HTML pages found'
                          + text_color.ENDC)
                    self.connection.commit()
                    many = 0
                    break

                # If we are retrieving this page,
                # there should be no links from it, just verifying
                self.cursor.execute('''DELETE from links
                                    WHERE from_id=%s''', (fromid,))
                try:
                    headers = {
                                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','referrer':'https://google.com'}
                    try:
                        # document = urlopen(req, context=self.SSL_CONTEXT,timeout = 1)
                        document = requests.get(url, headers=headers, timeout=3, verify=False)
                        # print("Obtained document")
                    except Exception as ex:
                        print(text_color.FAILED_COLOR
                              + "Timeout"
                              + text_color.ENDC)
                        self.cursor.execute('''INSERT IGNORE INTO
                                            errors(url, exception) VALUES(%s, %s)''',
                                            (url, str(document.status_code)))

                    # html_doc = document.read()
                    html_doc = document.text.strip()
                    # print("html extracted")
                    # if document.getcode() != 200:
                    if document.status_code != 200:
                        print(text_color.FAILED_COLOR
                              + "Error on page: "
                              + str(document.status_code)
                              + text_color.ENDC)
                        self.cursor.execute('''INSERT IGNORE INTO
                                            errors(url, exception) VALUES(%s, %s)''',
                                            (url, str(document.status_code)))
                        self.cursor.execute('UPDATE webs SET web_rank=%s WHERE url=%s',
                                            (int(self.web_rank)-self.NEGATIVE, self.starturl))
                        self.cursor.execute('UPDATE pages SET error=%s WHERE url=%s', (document.status_code, url))

                    if 'text/html' != document.headers['content-type'].split(";")[0]:
                        print(text_color.FAILED_COLOR + "Non text/html page" + text_color.ENDC)
                        self.cursor.execute('DELETE FROM pages WHERE url=%s', (url,))
                        self.connection.commit()
                        continue

                    soup = BeautifulSoup(html_doc, "html.parser")
                    # print("Obtained soup")
                except KeyboardInterrupt:
                    print(text_color.FAILED_COLOR + 'Deadpan interrupted by user...' + text_color.ENDC)
                    break
                except Exception as ex:
                    print(text_color.FAILED_COLOR + "Unable to retrieve or parse page : " + str(ex) + text_color.ENDC)
                    self.cursor.execute('UPDATE pages SET error=-1 WHERE url=%s', (url,))
                    self.cursor.execute('INSERT IGNORE INTO errors(url, exception) VALUES(%s, %s)',(url, str(ex)))
                    self.cursor.execute('UPDATE webs SET web_rank=%s WHERE url=%s', (int(self.web_rank)-self.NEGATIVE, self.starturl))
                    self.connection.commit()
                    continue

                # Create helper object and get keywords
                helper = Helper()
                meta_keyword_str = helper.get_keyword(soup)
                self.filename = helper.get_filename()

                # Insert url and keywords
                # Seperate statements make sure that error in first does not end up not inserting the keywords
                self.cursor.execute('INSERT IGNORE INTO pages(url, website, keywords, moved, new_rank, filename) VALUES(%s, NULL, NULL, NULL, 1.0, NULL)', (url,))
                self.cursor.execute('UPDATE pages SET website=%s, keywords=%s, moved=%s, filename=%s WHERE url=%s', (self.website_name, meta_keyword_str, 0, self.filename, url))
                self.cursor.execute('UPDATE webs SET web_rank=%s WHERE url=%s',(int(self.web_rank)+self.POSITIVE, self.starturl))

                # Dump html to 'dumps/'
                helper.dump_html(row, soup, self.filename)
                del helper, row

                # Retrieve all of the anchor tags
                tags = soup('a')
                for tag in tags:
                    href = tag.get('href', None)
                    if(href is None):
                        continue
                    # Resolve common link issues and remove tags for images
                    # parsed_url = urlparse(href)
                    parsed_url = requests.utils.urlparse(href)

                    # If http or https is empty, add the domain url before href
                    if(len(parsed_url.scheme) < 1):
                        href = urljoin(url, href)

                    hashpos = href.find('#')
                    if(hashpos > 1):
                        href = href[:hashpos]
                    if(href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') or href.endswith('.jpeg')):
                        continue
                    if(href.endswith('/')):
                        href = href[:-1]

                    if(len(href) < 1):
                        continue

                    # Check if the URL belongs to specified domains
                    found = False
                    for web in webs:
                        if(href.startswith(web)):
                            found = True
                            break
                    if not found:
                        # go to next loop if it links off the required website
                        continue

                    # Else insert
                    self.cursor.execute('''INSERT IGNORE INTO pages(url, website
                                        , keywords, new_rank)
                                        VALUES(%s, %s, NULL, 1.0)'''
                                        , (href, self.website_name))
                    self.cursor.execute('''SELECT pages_id FROM pages WHERE
                                          url=%s LIMIT 1''', (href,))
                    try:
                        row = self.cursor.fetchone()
                        toid = row[0]
                    except Exception as ex:
                        print(text_color.FAILED_COLOR
                              + 'Could not retrieve id'
                              + text_color.ENDC)
                        continue
                    self.cursor.execute('''INSERT IGNORE INTO
                        links(from_id, to_id) VALUES(%s, %s)''', (fromid, toid))
                self.connection.commit()

        except KeyboardInterrupt:
            print(text_color.FAILED_COLOR
                  + "Deadpan interrupted by user..."
                  + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format("", ex)
                  + text_color.ENDC)

    # Close connection
    def close_cur(self):
        try:
            self.cursor.close()
            print(text_color.GREEN_COLOR
                  + "Connection closed"
                  + text_color.ENDC)
        except Exception as ex:
            print(text_color.FAILED_COLOR
                  + error_string.format("", ex)
                  + text_color.ENDC)

    # Main spider
    def spider(self):
        self.ignore_ssl_error(True)
        self.create_table_if_not_exists()
        self.check_if_already_in_progress()
        self.get_current_webs_and_deadpan()
        self.close_cur()
