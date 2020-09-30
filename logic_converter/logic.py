'''



from forex_python.converter import CurrencyRates

# Documentation: https://forex-python.readthedocs.io/en/latest/usage.html

c = CurrencyRates()
rate = c.get_rates('USD')
# c.convert('USD', 'INR', Decimal('10.45'))
# c = CurrencyRates(force_decimal=True)
# c.convert('USD', 'INR', Decimal('10.45'))
print (rate ['INR'])


from datetime import datetime
from pytz import timezone
import pytz

fmt = "%Y-%m-%d %H:%M:%S %Z%z"
# https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568




for tz in pytz.all_timezones:
    print (tz)

now_time = datetime.now(timezone('US/Samoa'))
print (now_time.strftime(fmt))
# timezonelist = ['UTC','US/Pacific','Europe/Berlin', 'Asia/Kolkata']
# for zone in timezonelist:

#     now_time = datetime.now(timezone(zone))
#     print (now_time.strftime(fmt))

'''



from datetime import datetime
from pytz import timezone
import pytz

fmt = "%Y-%m-%d %H:%M:%S %Z%z"
# https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568

# tz = timezone('US/Pacific')

print (datetime.now())
now_time = "2020-07-28 19:21:45"(timezone('UTC'))#'Asia/Kolkata'))
print (now_time.strftime(fmt))
# tz.normalize(tz.localize(now_time)).astimezone(pytz.utc)

price = 100 # From Aishu

