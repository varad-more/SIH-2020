import feedparser
import json
from datetime import date
import time

url = 'http://feeds.feedburner.com/nseindia/ca'

d = feedparser.parse(url)
l = []

for i,j in enumerate(d.entries):
    company = j.title.split("-")[0]
    exdate = j.title.split(":")[1]

    print({'PK':i+1,'company':company,'exdate':exdate})
    l.append({'PK':i+1,'company':company,'exdate':exdate})

with open("rssDate/" + str(time.time()),'w') as f:
    f.write(str(l))
