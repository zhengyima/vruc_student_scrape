import requests
import re
import time
from time import strftime, localtime
import json
from tqdm import tqdm
def get_id(id):
    url = "http://app.ruc.edu.cn/idccw/finance/StudentAction.do"

    querystring = {"method":"enterStudent","q_xh":str(id),"q_xm":""}

    headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'cache-control': "no-cache",
        'postman-token': "524d22a5-6f66-096b-08df-ccef375e8ebc"
        }

    cookies={'JSESSIONID':'91BCf25FvvySZK7g8LZpM8Slfw9HNGrQTywNSsf1G2svBKrtvntg!2065617623',\
        'username':'2019101404',
        'J_SSO_ACCESS_TOKEN':'q4F9-u-3TGOEjzJeLWdxXQ',
        'J_SSO_CSRF_TOKEN':'0.6914097749375056:0.665423603731992',
        'access_token':'Qu-RiSzLQDC1CXZLyWgcMA',
        'BIGipServer970B/Mnpho7o/QN2Pp1UeA':'!NsbL5r0L7oBDderT4LUAbIdkXavJAmXioCHYvQqyu897Qbe/p1hWw75xfKOz5y1lY6Y1kdwrNm2dpHc='
        }

    response = requests.request("GET", url, headers=headers, params=querystring, cookies=cookies)
    rtxt = response.text

    # print(response.text)
    mystr_list = re.findall(r"[(](.*?)[)]",rtxt)
    mystr = mystr_list[0]
    return mystr
    # print(mystr)
    # cols = mystr.split(",")


with open("ids.csv",'r') as af:
    alines = af.readlines()
asnos_dict = {}
for aline in alines:
    aline = aline.strip()
    asno = aline.split(",")[0].replace("\'","")
    # print(asno)
    asnos_dict[asno] = 1


f = open("users2.tsv")
lines = f.readlines()
sno_list = []
for line in lines:
    # print(line.strip().split("\t"))
    _, iden, _, _, _, _, _, _ = line.strip().split("\t")
    arr = json.loads(iden)
    for a in arr:
        if ( a['idno'].startswith('201700')) and a['idno'] not in asnos_dict and a['idno'] not in sno_list:
            sno_list.append(a['idno'])
# sno_list = [2019101404]

# new_sno_list = [for sno in sno_list]
    
# print("the num of sno list:", len(sno_list))
# print(sno_list[0:50])

for sno in tqdm(sno_list):
    print(sno)
    txt = get_id(sno)
    print(txt)
    if len(txt.strip())>3:
        f = open("./ids_new.csv","a")
        f.write(txt+"\n")
        f.close()
    # print(sno,strftime("%Y-%m-%d %H:%M:%S", localtime()))
    time.sleep(1)

