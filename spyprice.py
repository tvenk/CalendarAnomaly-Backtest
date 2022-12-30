from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

url ="https://finance.yahoo.com/quote/SPY/"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")

Current_price = ""

tags = doc.find_all("fin-streamer")

for tag in tags:
    if tag["data-symbol"] == "SPY":
        Current_price = tag["value"]
        break

print("Current SPY price: $",Current_price)

year = int(input("Enter year: "))
month = int(input("Enter month: "))
day = int(input("Enter day: "))


input_dt = datetime(year, month, day)
print("Today's date is:", input_dt.date())

next_month = input_dt.replace(day=28) + timedelta(days=4)
res = next_month - timedelta(days=next_month.day)
print(f"Last date of month is:", res.date())

if input_dt.date() == res.date():
    url ="https://finance.yahoo.com/quote/SPY/"

    result = requests.get(url)

    doc = BeautifulSoup(result.text, "html.parser")

    Buy_price = ""

    tags = doc.find_all("fin-streamer")

    for tag in tags:
        if tag["data-symbol"] == "SPY":
             Buy_price = tag["value"]
             break

    print("Buying SPY price: ",Buy_price)

    file1 = open("BuyingSpyPriceEOM.txt", "a") 
    Buying_prices = [Buy_price+"\n"]
    file1.write(Buying_prices)
    file1.close()

endofmonth_date = res.date()

tdl = endofmonth_date + timedelta(3)

print("Three days later from the end of the month:", tdl)


if input_dt.date() == tdl:

    url ="https://finance.yahoo.com/quote/SPY/"

    result = requests.get(url)

    doc = BeautifulSoup(result.text, "html.parser")

    Sell_price = ""

    tags = doc.find_all("fin-streamer")

    for tag in tags:
        if tag["data-symbol"] == "SPY":
             Sell_price = tag["value"]
             break

    print("Selling SPY price: ",Sell_price)

    file2 = open("SellingSpyPriceTDA.txt", "a") 
    Selling_prices = [Sell_price+"\n"]
    file1.write(Selling_prices)
    file1.close()

initialinvestment = 0    

with open("BuyingSpyPriceEOM.txt") as b:
    list1 = [x for x in b.read().split('\n')]
    print("Bought prices for SPY at the end of the months: ",list1)
initialinvestment= float(list1[0]) * 10 #the price for buying 10 shares of SPY
print("Starting amount: $",initialinvestment)

with open("SellingSpyPriceTDA.txt") as s:
    list2 = [y for y in s.read().split('\n')]
    print("Sold prices for SPY three days after end of months: ",list2)

difference =[]
for i,j in zip(list1,list2):
        difference.append(float(j)-float(i))


print("Your net profit on SPY for 10 shares: $",sum(difference))


print("Current amount: $",float(initialinvestment) + (sum(difference))*10)

percentage = (((sum(difference))*10)/initialinvestment)* 100

if (sum(difference))*10 > 0:
    print("Your are up {0}%".format(percentage))
if (sum(difference))*10 < 0:
    print("Your are down {0}%".format(percentage))


