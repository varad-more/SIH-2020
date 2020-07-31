import sys
sys.path.insert(0, '')
import mysql.connector
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
    ["moneycontrol1", "https://www.moneycontrol.com/news/business", "15"],
    ["newindianexpress", "https://www.newindianexpress.com/business", "15"],
    ["timesnownews", "https://www.timesnownews.com/business-economy/companies", "12"],
    ["capitalmarket2", "http://www.capitalmarket.com", "5"],
    ["economictimes", "https://www.economictimes.indiatimes.com", "10"],
    ["livemint1", "https://www.livemint.com/companies/news", "15"],
    ["livemint2", "https://www.livemint.com", "5"],
    ["businessinsider1", "https://www.businessinsider.in/business/news", "15"],
    ["businessinsider2", "https://www.businessinsider.in", "5"],
    ["stockinforce", "https://www.stockinforce.com", "5"],
    ["hindustantimes1", "https://www.hindustantimes.com/business-news", "15"],#
    ["hindustantimes2", "https://www.hindustantimes.com", "5"],
    ["thehindubusinessline1", "https://www.thehindubusinessline.com/companies/announcements", "15"],
    ["thehindubusinessline2", "https://www.thehindubusinessline.com", "5"],
    ["gadgetsnow1", "https://www.gadgetsnow.com/latest-news", "15"],
    ["gadgetsnow2", "https://www.gadgetsnow.com", "5"],
    ["thenewsminute1", "https://www.thenewsminute.com/section/News", "15"],
    ["thenewsminute2", "https://www.thenewsminute.com", "5"],
    ["outlookindia1", "https://www.outlookindia.com/newsscroll", "15"],
    ["outlookindia2", "https://www.outlookindia.com", "5"],
    ["business-standard1", "https://www.business-standard.com/sector/display-article/Financials", "25"],
    ["business-standard2", "https://www.business-standard.com/markets-news", "25"],
    ["business-standard3", "https://www.business-standard.com", "5"],
    ["businesstoday", "https://www.businesstoday.in/current/corporate", "15"],
    ["newskube", "https://www.newskube.com", "5"],
    ["moneycontrol2", "https://www.moneycontrol.com/news/business/markets", "30"],
    ["moneycontrol3", "https://www.moneycontrol.com", "5"],
    ["republicworld1", "https://www.freepressjournal.in/business", "10"],
    ["republicworld2", "https://www.freepressjournal.in", "5"],
    ["republicworld3", "https://www.republicworld.com/business-news/india-business", "10"],
    ["republicworld4", "https://www.republicworld.com/business-news", "10"],
    ["republicworld5", "https://www.republicworld.com", "5"],
    ["ndtv1", "https://www.ndtv.com/business", "10"],
    ["ndtv2", "https://www.ndtv.com", "5"],
    ["ndtv3", "https://www.ndtv.com/business/corporates", "10"],
    ["firstpost1", "https://www.firstpost.com/category/business", "10"],
    ["firstpost2", "https://www.firstpost.com", "5"],
    ["businessworld1", "http://www.businessworld.in", "5"],
    ["businessworld2", "http://www.businessworld.in/business-news", "10"],
    ["equitybulls", "http://www.equitybulls.com", "5"],
    ["newsjournals", "https://www.newsjournals.in", "5"],
    ["bloombergquint1", "https://www.bloombergquint.com/business", "10"],
    ["bloombergquint2", "https://www.bloombergquint.com", "5"],
    ["businesstimes1", "https://www.businesstimes.com.sg/keywords/agm", "30"],
    ["businesstimes2", "https://www.businesstimes.com.sg/keywords/buyback", "20"],
    ["businesstimes3", "https://www.businesstimes.com.sg/keywords/dividend", "40"],
    ["businesstimes4", "https://www.businesstimes.com.sg/keywords/merger", "20"],
    ["businesstimes5", "https://www.businesstimes.com.sg/keywords/takeover", "20"],
    ["businesstimes6", "https://www.businesstimes.com.sg", "8"],
    ["financialexpress1", "https://www.financialexpress.com/industry", "30"],
    ["financialexpress2", "https://www.financialexpress.com", "30"],
    ["financialexpress3", "https://www.financialexpress.com/market/stock-market", "40"],
    ["bing", "https://www.bing.com/search?q=agm", "10"],
    ["news18", "https://www.news18.com", "5"]
]


def deadpan_and_hollow(i, sum_rank):
    deadpan = Deadpan(i[0], i[1], round(int(i[2])*100/sum_rank))
    deadpan.spider()


if __name__ == "__main__":
    # add webs table if not existing
    # deadpan_and_hollow(["moneycontrol", "https://www.moneycontrol.com/news/business", "5"], 100)

    for i in init_web_list:
        deadpan_and_hollow(i, 100)

    while True:
        connection = mysql.connector.connect(
                 host="database-1.chm9rhozwggi.us-east-1.rds.amazonaws.com",
                 user="admin",
                 password="SIH_2020",
                 database="pythanos_main"
        )

        cursor = connection.cursor(buffered=True)
        web_list = cursor.execute('SELECT * from webs ORDER BY RAND()')
        row = cursor.fetchall()
        cursor.close()
        web_rank_list = []
        for i in row:
            web_rank_list.append(i[2])

        sum_rank = sum(web_rank_list)

        try:
            hollow = Hollow()
            hollow.drain()

            loathe = Loathe()
            loathe.loathe()

            for i in row:
                deadpan_and_hollow(i, sum_rank)

                reaper = Reaper("5")
                reaper.reap()

        except KeyboardInterrupt:
            print(text_color.FAILED_COLOR + 'Program interrupted by user...' + text_color.ENDC)
            break

        except Exception as ex:
            continue
