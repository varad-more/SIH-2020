import sys
sys.path.insert(0, '')
from tenderfoot.deadpan import Deadpan

deadpan = Deadpan("moneycontrol",'https://www.moneycontrol.com',"100")
deadpan.spider()