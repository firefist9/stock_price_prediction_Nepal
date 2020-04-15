from check_and_scrape import check_symbol_in_web, check_file_exist, scrape
from prediction import predict_stock
from datetime import date, timedelta



def main():
    print("Input the stock symbol: ")
    symbol = input()
    textfile = str(symbol)+".txt"
    print(textfile)
    if check_file_exist(symbol) == 2:
        #check_symbol_in_web(symbol)
        with open(textfile, 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            x = int(last_line[:4])
            y = int(last_line[5:7])
            z = int(last_line[8:10])
        ldate = date(x, y, z)
        edate = date.today()
        if (edate.year + edate.month *30 + edate.day) - (ldate.year + ldate.month*30 + ldate.day) <= 5:
            predict_stock(symbol)
            #print("ok")
        else:
            scrape(symbol, ldate)
            predict_stock(symbol)
            #print("not ok")



    elif check_file_exist(symbol) == "yes":
        #check_symbol_in_web(symbol)
        ldate = date(2016, 1, 1)   # start date
        edate = date.today()
        scrape(symbol, ldate)
        predict_stock(symbol)

    elif check_file_exist(symbol) == "no":
        exit()
    else:
        exit()



if __name__ == '__main__':
    main()