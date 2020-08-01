"""Hollow module

This module is the parser for the CA scraping bot.
"""

__version__ = '1'
__author__ = 'Abhijit Acharya'

import sys
import string
import mysql.connector
from newspaper import Article

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


class Hollow(object):
    """This class provides methods for parsing data from links"""

    def __init__(self):
        super(Hollow, self).__init__()
        # escapes = ''.join([chr(char) for char in range(1, 32)])
        # self.translator = str.maketrans('', '', escapes)
        self.companies = list(dict.fromkeys(['farm', 'sind', 'alfa', 'radico', 'petrochemicals', 'gujarat', 'hans', 'atlas', 'stainless', 'parry', 'karnataka', 'google', 'pallonji', 'dr.', 'airtel', 'gruh', 'snapdeal', 'sakthi', 'fincorp', 'pentamedia', 'dynamatic', 'cmc', 'healthcare', 'ratnamani', 'mastek', 'finolex', 'aban', 'mahanagar', 'asia', 'icim', 'idbi', 'xolo', 'hdfc', 'computer', 'fortis', 'tvs', 'hero', 'air', 'india', 'hcl', 'kotak', 'clays', 'havell', 'perigreen', 'nbcc', 'pharmaceutical', 'provogue', 'nippon', 'chrysler', 'associates', 'birla', 'baer', 'infrastructures', 'mahindra', 'optical', 'paramount', 'ocl', 'inds.', 'iron', 'etc', 'jain', 'silk', 'lever', 'bata', 'pantaloons', 'ksk', 'larsen', 'bosch', 'boltt', 'graphics', 'abp', 'fertilisers', 'suashish', 'star', 'lakshmi', 'ltd', 'jawa', 'surya', 'aftek', 'allsec', 'aeronautics', 'fertilizer', 'and', 'properties', 'ballarpur', 'asahi', 'finance', 'everest', 'strides', 'global', 'karur', 'hinduja', 'exports', 'ceat', 'raymond', 'thermax', 'tramways', 'offshore', 'oswald', 'ramsarup', 'icici', 'canara', 'kennametal', 'dabur', 'software', 'moser', 'infratech', 'cellular', 'gateway', 'mrpl', 'toubro', 'cesc', 'developers', 'mazda', 'microland', 'laval', 'raymond', 'torrent', 'rpg', 'kudremukh', 'clariant', 'laboratories', 'colgate', 'earth', 'forge', 'jaiprakash', 'telecom', 'surana', 'geodesic', 'consultancy', 'engineers', 'aftek', 'nicholas', 'wadia', 'fag', 'enterprises', 'gamble', 'bijlee', 'organosys', 'interactive', 'elgitread', 'kemrock', 'crompton', 'technologies', 'ingersoll-rand', 'renuka', 'shipping', 'simplex', 'refinery', 'fresh', 'mineral', 'distribution', 'dalmia', 'news', 'tmt', 'flipkart', 'mcleod', 'lti', 'jm', 'enfield', 'shipyard', 'sanchar', 'va', 'greaves', 'development', 'hindustan', 'donear', 'bos', 'ambuja', 'sangam', 'jindal', 'crisil', 'mrf', 'factories', 'chemicals', 'leyland', 'fujitsu', 'nava', 'retail', 'persistent', 'baer', 'moser', 'r', 'indraprastha', 'aluminium', 'crop', 'ranbaxy', 'shipyard', 'himalaya', 'balrampur', 'vip', 'ht', 'jewellery', 'sky', 'lifesciences', 'tata', 'delhi', 'elecon', 'bharat', 'cipla', 'plastics', 'rural', 'shoppers', 'siemens', 'the', 'motorworks', 'chennai', 'punjab', 'sasken', 'apollo', 'visaka', 'limited', 'maruti', 'coal', 'nerolac', 'iball', 'dyeing', 'fashions', 'asian', 'srei', 'ugine', 'lg', 'mastek', 'shoes', 'works', 'investmart', 'educomp', 'railway', 'il&fs', 'leela', 'paints', 'ador', 'hll', 'cyient', 'waymo', 'ittiam', 'mindtree', 'strips', 'lumax', 'ambuja', 'galva', 'tessolve', 'electrolux', 'unitech', 'cotton', 'nigam', 'ltd', 'vaibhav', 'airlines', 'nuclear', 'tech', 'papers', 'electrification', 'mahindra', 'goldman', 'kulkarni', 'cola', 'cements', 'circuits', 'geometric', 'mundra', 'micromax', 'norton', 'blue', 'authority', 'ashok', 'biocon', 'nigam', 'tvs', 'real', 'dena', 'hindustan', 'travancore', 'arcolab', 'mmtc', 'genus', 'exide', 'gas', 'dart', 'glenmark', 'suzlon', 'indigo', '18', 'niit', 'aditya', 'essar', 'indo', 'axles', 'coca', 'indusind', 'mahanagar', 'ig', 'pariwar', 'ntpc', 'bpcl', 'petrochina', 'rksv', 'acc', 'hindalco', 'electrosteel', 'amman', 'machine', 'cycles', 'hawkins', 'national', 'penpol', 'force', 'infotek', 'frontier', 'city', 'synthite', 'marg', 'geojit', 'marine', 'leasing', 'vadilal', 'baffin', 'newsprint', 'hcl', 'chemplast', 'rites', 'lloyds', 'adlabs', 'itd', 'mphasis', 'electric', 'avantha', 'ms', 'cochin', 'power', 'pharmaceuticals', 'yes', 'container', 'syrian', 'kajaria', 'onmobile', 'organic', 'muthoot', 'wabag', 'plyboards', 'ashok', 'inkfruit', 'zee', 'megasoft', 'sachs', 'petronet', 'nadu', 'eveready', 'day', 't-series', 'intelenet', 'martin', 'movers', 'bonn', 'mrf', 'ganesh', 'zerodha', 'irrigation', 'insurance', 'corporation', 'yebhi', 'spacex', 'endurance', 'coffee', 'chini', 'glaxosmithkline', 'sea6', 'diamonds', 'zensar', 'grasim', 'escorts', 'posco', 'bajaj', 'idea', 'zomato', 'intex', 'lloyd', 'machine', 'beverages', 'abg', 'hero', 'flex', 'petronet', 'nilkamal', 'il&fs', 'sas', 'inds', 'intel', 'konkan', 'singareni', 'elico', 'jmc', 'jsw', 'eskay', 'tv', 'gail', 'dempo', 'jaypee', 'punj', 'varun', 'metro', 'balmer', 'nrb', 'nahar', 'reliance', 'informatics', 'emcure', 'manugraph', 'tamil', 'fertiliser', 'greenply', 'malabar', 'bongaigaon', 'honda', 'sahara', 'chambal', 'amul', 'bharati', 'indian', 'systems', 'distriparks', 'equipment', 'earth', 'abbott', 'media', 'air', 'cadila', 'essel', 'hdfc', 'plant', 'jio', 'copco', 'coromandel', 'eye', 'allied', 'indiabulls', 'opto', 'lodha', 'adani', 'marico', 'inmobi', 'amtek', 'motors', 'oil', 'electricals', 'matheson', 'amazon', 'parle', 'vilas', 'axis', 'godrej', 'rajshree', 'services', 'sanitaryware', 'graphite', 'foods', 'gmr', 'bharat', 'ballarpur', "haldiram's", 'health', 'defence', 'rajesh', 'fiat', 'emami', 'snapdeal', 'kirloskar', 'living', 'cesc', 'gesco', 'bengal', 'ksl', 'russel', 'rayon', 'drug', 'engineering', 'lawrie', 'aventis', 'zoho', 'shriram', 'toubro', 'dewan', 'ndtv', 'dishman', 'mercator', 'times', 'ideal', 'lava', 'samsung', 'eicher', 'hygiene', 'bsel', 'sanmar', 'amrutanjan', 'amara', 'tea', 'nlc', 'lnt', 'gspc', 'rohren', 'travancore', 'communications', 'ccl', 'lanco', 'airways', 'cinevista', 'arvind', 'federal', 'construction', 'shipping', 'rashtriya', 'aptech', 'wilmar', 'eureka', 'kerala', 'jyoti', 'jaybharat', 'celkon', 'energy', 'yatra', 'k', 'kashmir', 'usha', 'bpo', 'igate', 'south', 'electricals', 'divi', 'nirma', 'britannia', 'ranbaxy', 'corp', 'kotak', 'hindalco', 'satyam', 'welspun', 'forbes', 'leyland', 'jb', 'jbf', 'movers', 'forbes', 'udyog', 'hotels', 'propack', 'steel', 'atcom', 'larsen', 'suzuki', 'pepsi', 'business', 'overseas', 'entertainment', 'vakrangee', 'gokak', 'realty', 'visakhapatnam', 'jubilant', 'welspun', 'offshore', 'arise', 'titanium', 'group', 'fertilizers', 'jetlite', 'infosys', 'natural', 'videocon', 'dlf', 'donohoe', 'jubilant', 'pawan', 'english', 'housing', 'infosys', 'kalpataru', 'nestle', 'ongc', 'infrastructure', 'breweries', 'board', 'gems', 'cummins', 'sterlite', 'emami', 'ansal', 'ventures', 'gvk', 'birla', 'nhpc', 'kirloskar', 'himadri', 'makemytrip', 'railways', 'aluminium', 'biocon', 'fdc', 'jet', 'coop', 'flipkart', 'solectron', 'ruchi', 'express', 'gillette', 'ultratech', 'raj', 'aia', 'triveni', 'jain', 'mediaworks', 'industry', 'corporation', 'dabur', 'greaves', 'fertilizers', 'techno', 'sumi', 'sanghi', 'atn', 'transmission', 'capital', 'centum', 'lng', "reddy's", 'paints', 'jsw', 'spice', 'crompton', 'infrastructure', 'azure', 'engg', 'moil', 'eveready', 'airbus', 'tcs', 'ipca', 'britannia', 'container', 'systems', 'overseas', 'mecon', 'jabong.com', 'motors', 'bp', 'torrent', 'pneumatic', 'costa', 'nagarjuna', 'port', 'maharashtra', 'international', 'company', 'apollo', 'wipro', 'myntra', 'pepsico', 'sugars', 'lic', 'alembic', 'godrej', 'spicejet', 'bajaj', 'coromandel', 'wockhardt', 'dish', 'sun', 'authority', 'eastern', 'refinery', 'satyam', 'nectar', 'skipper', 'gmr', 'state', 'fashion', 'videsh', 'kokuyo', 'anant', 'kfc', 'future', 'camlin', 'spirits', 'realty', 'nuvo', 'consumers', 'ntpc', 'knowlarity', 'sonata', 'roshni', 'hdil', 'lakshmi', 'praj', 'chemicals', 'framatome', 'cyberspace', 'yes', 'solutions', 'products', 'grid', 'itc', 'chassis', 'telephone', 'circuits', 'paytm', 'tradeindia', 'films', 'maruti', 'union', 'bpl', 'vedanta', 'apple', 'titan', 'batteries', 'royal', 'shapoorji', 'engines', 'financial', 'cybermate', 'subhash', 'deccan', 'parry', 'aban', 'structures', 'gramin', 'life', 'cylinder', 'liberty', 'videocon', 'ore', 'terumo', 'essar', 'goair', 'walchandnagar', 'motocorp', 'mangalore', 'jk', 'century', 'united', 'balaji', 'ordnance', 'telesystems', 'castings', 'zandu', 'ispat', 'hexaware', 'digital', 'bombay', 'tractors', 'action', 'boeing', 'creative', 'organics', 'suminter', 'catholic', 'geojit', 'honeywell', 'v-guard', 'auto', 'transmission', 'nvidia', 'swaraj', 'exports', 'brothers', 'berger', 'tyres', 'amartex', 'elder', 'soya', 'piramal', 'rediff.com', 'palmolive', 'central', 'hmt', 'motherson', 'express', 'vijaya', 'great', 'prithvi', 'kelvinator', 'havells', 'spanco', '&', 'crest', 'copper', 'voonik', 'café', 'yepme', 'castrol', 'damodar', 'stahl', 'uco', 'electrical', 'tamilnad', 'zinc', 'mukand', 'nissan', 'madras', 'bank', 'piramal', 'electronics', 'classic', 'hospitals', 'cookers', 'bearings', 'universal', 'firstsource', 'syntex', 'airtel', 'india', 'forge', 'subex', 'west', 'idfc', 'ramco', 'mcnally', 'ksb', 'gulf', 'cementation', 'aurobindo', 'gammon', 'odisha', 'procter', 'bhushan', 'grindwell', 'nucleus', 'abg', 'mangalam', 'tesla', 'alstom', 'acc', 'platinum', 'bharti', 'jammu', 'mitsubishi', 'nbc', 'merck', 'aditya', 'industries', 'uttam', 'sun', 'dredging', 'spinning', 'hindu', 'esab', 'airways', 'bsl', 'infibeam', 'kanto', 'support', 'voltas', 'works', 'bombay', 'iron', 'carborundum', 'kei', 'alok', 'atco', 'house', 'wipro', 'cosmic', 'plant', 'heavy', 'eid', 'gemini', 'mistral', 'adani', 'sterlite', 'sobha', 'rashtriya', 'force', 'heavy', 'valley', 'vst', 'elxsi', 'calcutta', 'tata', 'corp', 'tyre', 'essel', 'walmart', 'khaitan', 'volkswagen', 'fcl', 'agro', 'thirdware', 'bearings', 'mills', 'onida', 'datamatics', 'titan', 'raja', 'karbonn', 'stop', 'register', 'labs', 'zinc', 'collieries', 'daimler', 'exide', 'vysya', 'jindal', 'helios', 'niit', 'lifecare', 'kochi', 'suzuki', 'rolta', 'foodworks', 'sugars', 'petroleum', 'hitachi', 'motor', 'tulip', 'voltas', 'gail', 'archies', 'petrochemicals', 'ltd.', 'vicco', 'glenmark', 'pidilite', 'charters', 'enterprises', 'electricity', 'telefilms', 'sujana', 'baroda', 'walchandnagar', 'glass', 'bannari', 'shopclues', 'binani', 'cadila', 'gulf', 'astrazeneca', 'jet', 'abb', 'kansai', 'of', 'mobiles', 'cement', 'mercantile', 'shree', 'reliance', 'ivrcl', 'eicher', 'sanchar', 'kesoram']))
        print(text_color.HEADER_COLOR + "Initialized hollow object" + text_color.ENDC)

    # Remove punctuations
    def preprocessing(self, line):
        # line = line.translate(self.translator)

        puncts = ""
        for i in string.punctuation:
            if i != "%" and i != "$" and i != "/" and i != ":":
                puncts += i
        spaces = "".join([" "]*28)
        line = line.translate(str.maketrans(puncts, spaces))
        line = line.lower().split(' ')

        if "copyright" in line:
            return "NONE"

        if "subscriber" in line:
            return "NONE"

        return " ".join(line)

    # Get company names in keywords
    def get_company(self, keywords):
        spaces = "".join([" "]*32)
        keywords = keywords.translate(str.maketrans(string.punctuation
                                                    , spaces)).lower()
        company = []
        for j in self.companies:
            if j in keywords.split(" "):
                company.append(j)
        if company == []:
            return "NULL"
        return list(dict.fromkeys(company))

    # Connect to table or create tables if not already done
    def connect_to_existing_table_or_create(self):
        try:
            # Connect to database
            self.connection = mysql.connector.connect(
                     host="database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com",
                     user="admin",
                     password="SIH_2020",
                     database="pythanos_main"
                   )

            self.cursor = self.connection.cursor(buffered=True)
            print(text_color.GREEN_COLOR + "Connected to database " + 'tenderfoot' + text_color.ENDC)

        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format("", ex) + text_color.ENDC)
            sys.exit(0)

    # Check to see if we are already in progress...
    def check_if_already_in_progress(self):
        try:
            # Get id and url of empty keywords' rows
            self.cursor.execute('''INSERT INTO articles(id, url, keywords, filename) SELECT pages_id, url, keywords, filename FROM pages WHERE keywords is NOT NULL and keywords != "NULL" and keywords != "" and moved = 0;''')
            self.cursor.execute('''UPDATE pages SET moved=%s WHERE keywords is NOT NULL and keywords != "NULL" and keywords != ""''', (1,))
            self.connection.commit()
        except Exception as ex:
            print(text_color.FAILED_COLOR + error_string.format("", ex) + text_color.ENDC)

    # get link and parse html
    def get_link_and_drain(self):
        try:
            counter = 0
            s = '\|/-'
            t = iter(s)
            l = 0
            while True:
                l += 1
                # Get id and url of empty html
                self.cursor.execute('''SELECT id,url,keywords,filename
                                      FROM articles WHERE content is NULL and
                                      error is NULL ORDER BY ranks LIMIT 1''')
                try:
                    if counter == 4:
                        counter = 0
                        t = iter(s)
                    counter += 1
                    row = self.cursor.fetchone()
                    company_names = self.get_company(row[2])

                    # Get one article and hollow it
                    article = Article(row[1])
                    # Get html from dump
                    with open('output/dumps/'+row[3],'r', encoding='utf-8') as f:
                        try:
                            # data = json.load(f)
                            # html_str = data[str(row[0])]
                            html_str = f.read()
                        except Exception as ex:
                            print(ex)
                        finally:
                            f.close()

                    try:
                        # html from file
                        article.download(html_str)
                    except:
                        # download the article
                        article.download()
                    article.parse()

                    content_text = self.preprocessing(str(article.text))
                    # print(content_text)
                    if content_text == "NONE":
                        self.cursor.execute('''UPDATE articles SET error=%s WHERE url=%s''', (-1, row[1]))
                        continue

                    # Remove anythong less than 50 chars...
                    if len(article.text) > 50:
                        self.cursor.execute('''UPDATE articles SET authors=%s,
                                            publish_date=%s, title=%s,
                                            content=%s, company_name=%s
                                            WHERE url=%s''', (str(article.authors), article.publish_date, article.title, content_text[:9999], str(company_names), row[1]))
                    else:
                        self.cursor.execute('''UPDATE articles SET error=%s WHERE url=%s''', (-1, row[1]))

                    sys.stdout.write('\rloading {} {}'.format(next(t), l))
                except Exception as ex:
                    # All done for today
                    sys.stdout.write('\rDone!!      ')
                    print(ex)
                    print(text_color.FAILED_COLOR
                          + 'No undrained HTML articles found'
                          + text_color.ENDC)
                    break
                self.connection.commit()

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
    def drain(self):
        self.connect_to_existing_table_or_create()
        self.check_if_already_in_progress()
        self.get_link_and_drain()
        self.close_cur()
