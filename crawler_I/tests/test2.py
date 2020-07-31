import sys
sys.path.insert(0, '')
from tenderfoot.hollow import Hollow

hollow = Hollow("moneycontrol",'https://www.moneycontrol.com')
hollow.drain()