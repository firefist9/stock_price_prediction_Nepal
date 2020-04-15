from urllib.request import urlopen
from bs4 import BeautifulSoup as bsup
from datetime import date, timedelta

def check_symbol_in_web(symbol):
    webpage = "http://nepalstockinfo.com/todaysprice/"
    html = urlopen(webpage)
    bs_obj = bsup(html)
    try:
        data = bs_obj.find("td", text=symbol).parent
    except AttributeError:
        print("Sorry, this company symbol doesn't exist in nepalstockinfo db")



def check_file_exist(symbol):
    try:
        f = open(symbol+".txt")
    except IOError:
        print("File not found")
        while 1:
            print("Do you want to scrape the data, it may take 1-2 hrs? \n")
            print("Choice: yes, no")
            x = input()
            value = {1:"yes", 2:"no"}
            if str(x) in value.values():
                return str(x)
                break
            else:
                continue
            
    return 2

def scrape(symbol, sdate):
    edate = date.today()
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

