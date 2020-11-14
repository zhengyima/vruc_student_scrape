import requests
import re
import time
from time import strftime, localtime
import json
from tqdm import tqdm

def get_from_page(classid):
    # url = "http://app.ruc.edu.cn/idccw/finance/StudentAction.do"
    # url = "https://v.ruc.edu.cn/educenter/api/courses?offset="+str(page_idx)+"&limit=10&name=&year=2019-2020&term=%E6%98%A5%E5%AD%A3%E5%AD%A6%E6%9C%9F&school_domain=v.ruc.edu.cn&timespan=1605343936876"

    url = 'https://v.ruc.edu.cn/educenter/api/classes/'+classid+'/users?limit=65536&school_domain=v.ruc.edu.cn'
    querystring = {}

    headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'cache-control': "no-cache",
        'postman-token': "524d22a5-6f66-096b-08df-ccef375e8ebc"
        }

    cookies={
        "UM_distinctid":'17516e41de896f-03105bc472b838-5e1a3f18-1fa400-17516e41de9c43',
        'PHPSESSID':'jktid141a40ck81t4d7bgnots5',
        'is_simple':'0',
        'session':'448de480803f419390ec0680cec0d902.798cc262b1274a9791ae99d5b4d5886d',
        'access_token':'ZvSWYQg1Sc2ca6jRjh0fZQ',
        'tiup_uid':'11774323',
        'lang':'%22zh-cn%22'
        }

    response = requests.request("GET", url, headers=headers, params=querystring, cookies=cookies)
    rtxt = response.text

    # print(response.text)
    # mystr_list = re.findall(r"[(](.*?)[)]",rtxt)
    # mystr = mystr_list[0]
    # return mystr
    # print(mystr)
    # cols = mystr.split(",")
    return rtxt

class_file = "classes_600.txt"
f = open(class_file)
has_scraped_classes = {}
has_scraped_students = {}

student_file = "users_600c.txt"


def get_students_from_class(cid):

    content = get_from_page(cid)
    data = json.loads(content)
    users = data['data']['users']
    cnt_u = 0
    for u in users:
        if u['id'] in has_scraped_students:
            continue
        else:
            has_scraped_students[u['id']] = 1
        fsw = open(student_file,'a')
        line_w = [u['id'], json.dumps(u,ensure_ascii=False), u['name'], u['photo'], u['description']]
        line_w = '\t'.join(line_w)
        fsw.write(line_w+'\n')
        fsw.close()
        cnt_u += 1
    # return len(user)
    return cnt_u






def main():
    cnt_class= 0 
    for line in f:
        class_data = json.loads(line.strip())
        classes = class_data['classes']
        for c in classes:
            
            # print(cid)
            cid = c['id']

            if cid not in has_scraped_classes:
                has_scraped_classes[cid] = 1
            else:
                continue
            cnt_u = get_students_from_class(cid)
            cnt_class += 1
            print("from %s get %d users, total %d users, class idx %d" % (cid, cnt_u, len(has_scraped_students), cnt_class))
            time.sleep(0.1)
main()
# page_start = 0
# page_end = 4100
# fout = "classes.txt"
# f = open(fout,'w')
# f.close()
# len_courses = 0
# len_classes = 0
# for page_i in range(page_start, page_end):
#     # print(get_from_page(page_i))
#     content = get_from_page(page_i*10)
#     data =  json.loads(content)['data']
#     len_courses += len(data['courses'])
#     len_classes += len(data['classes'])
#     data_str = json.dumps(data,ensure_ascii=False)
#     f = open(fout,'a')
#     f.write(data_str+"\n")
#     f.close()    
#     print("page %d, %d courses, %d classes" % (page_i, len_courses, len_classes))

