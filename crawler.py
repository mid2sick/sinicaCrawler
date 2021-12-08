import urllib.request as req
import re
import time
import csv

totalNum = 44585

def getName(str):
    pattern = '<a href="(.*?)">(.*?)</a>'
    substr = re.search(pattern, str).group(2)
    return substr

def getNum(str):
    pattern = '<td>(.*?)</td>'
    substr = re.search(pattern, str).group(1)
    return substr

def findLine(content):
    name="null"
    powerNum = "null"
    cbdb = "null"

    # find 姓名
    search_str = "<tr><th>姓名</th><td id=name>"
    for line in content.splitlines():
        if search_str in line:
            name = line
    if name != "null":
        name = getName(name)
    
    # find 權威號
    search_str = "<th>權威號</th>"
    for line in content.splitlines():
        if search_str in line:
            powerNum = line
    if powerNum != "null":
        powerNum = getNum(powerNum)
    
    # find CBDB
    search_str = "<th>CBDB</th>"
    for line in content.splitlines():
        if search_str in line:
            cbdb = line
    if cbdb != "null":
        cbdb = getNum(cbdb)
    # or something else because the search_str was not found
    return name + "," + powerNum + "," + cbdb

with open('./list.csv', 'a', encoding='UTF-8') as f:
    # f.write("姓名,權威號,CBDB,url\n")
    for i in range(1, totalNum + 1):
        # if i == 4060 or i == 6940 or i == 9400 or i == 9705 or i == 12301:
        #     continue
        SN = format(i, '06d')
        url = "https://newarchive.ihp.sinica.edu.tw/sncaccgi/sncacFtp?ACTION=TQ,sncacFtpqf,SN=" + SN +",2nd,search_simple"
        try:
            with req.urlopen(url) as response:
                data = response.read().decode("utf-8")
            result = findLine(data)
            f.write(result + ',"{}"'.format(url))
            f.write("\n")
            # f.write(result + "," + url)
            # print(result + "," + url)
            if i % 3 == 0:
                time.sleep(0.3)
            # if i % 100 == 0:
                # time.sleep(30)
            print(result)
        except:
            f.write("500 internal server error,," + ',"{}"'.format(url) + "\n")
            print("500 internal server error")
    f.truncate()
