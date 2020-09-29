import sys
sys.path.insert(0, '')
from tenderfoot.deadpan import Deadpan

deadpan = Deadpan("moneycontrol","https://www.moneycontrol.com/news/business","5")
deadpan.spider()