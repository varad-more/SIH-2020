import sys
sys.path.insert(0, '')
import sqlite3
from tenderfoot.deadpan import Deadpan
from tenderfoot.reap import Reaper
from tenderfoot.hollow import Hollow
from tenderfoot.loathe import Loathe

class text_color:
    HEADER_COLOR = '\033[95m'
    BLUE_COLOR = '\033[94m'
    GREEN_COLOR = '\033[92m'
    WARNING_COLOR = '\033[93m'
    FAILED_COLOR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

init_web_list = [
    ["moneycontrol1",'https://www.moneycontrol.com/news/business',"2"],
]


def deadpan_and_hollow(i,max_rank):
    deadpan = Deadpan(i[0],i[1],round(int(i[2])*100/max_rank))
    deadpan.spider()

# for i in init_web_list:
#     deadpan_and_hollow(i,100)

while True:
    # Connect to database
    connection = sqlite3.connect('output/tenderfoot.sqlite')
    cursor = connection.cursor()
    web_list = cursor.execute('SELECT * from Webs ORDER BY Random()')
    row = cursor.fetchall()
    cursor.close()
    web_rank_list = []
    for i in row:
        web_rank_list.append(i[2])

    max_rank = max(web_rank_list)

    try:
        for i in row:
            deadpan_and_hollow(i,max_rank)

            reaper = Reaper("5")
            reaper.reap()

            hollow = Hollow(i[0],i[1])
            hollow.drain()

        loathe = Loathe()
        loathe.loathe()

    except KeyboardInterrupt:
        print(text_color.FAILED_COLOR + 'Program interrupted by user...' + text_color.ENDC)
        break
