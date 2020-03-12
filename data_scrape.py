from urllib.request import urlopen
from bs4 import BeautifulSoup as bsup
from datetime import date, timedelta

sdate = date(2019, 5, 3)   # start date
edate = date(2020, 3, 12)   # end date
def scrape(symbol):
    delta = edate - sdate       # as timedelta
    file1 = open(symbol+".txt", "a")
    #file1.write("Date,Open,High,Low,Close,Volume\n")

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        #print(day)
        webpage = "http://nepalstockinfo.com/todaysprice/"+str(day)
        #print(webpage)
        html = urlopen(webpage)
        bs_obj = bsup(html)
        data = bs_obj.find("td", text=symbol).parent
        try:
            data.a["data-high"]
        except KeyError:
            continue
        data_high = data.a["data-high"]
        data_low = data.a["data-low"]
        data_open = data.a["data-open"]
        data_prev_closing = data.a["data-prev_closing"]
        date_n = str(day)
        data_volume = data.a["data-volumn"]
        file1.write(date_n+","+data_open+","+data_high+","+data_low+","+data_prev_closing+","+data_volume+"\n")
        print(date_n, data_high, data_low, data_open, data_prev_closing)
    file1.close()

print("Enter symbol name")
sym = input()
scrape(sym)
