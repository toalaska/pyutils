# coding=utf-8
import calendar
import random
import sys
import time
import uuid




import subprocess
import json
import platform
from urllib.parse import parse_qs
import urllib.request, urllib.parse, urllib.error

import datetime


def is_linux():
    return 'Linux' in platform.system()
def parse_form_data(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    res = {}
    for k, v in list(parse_qs(request_body).items()):
        res[k] = v[0] if len(v) > 0 else ""
    return res


# 分解query_string为一个map
def query_string_parse(environ):
    url = environ['fc.request_uri']
    result = {}
    if "?" in url:
        url = url.split("?")[-1]
    for x in url.split("&"):
        if x.strip(" ") == "":
            continue
        r = x.strip().split("=")
        if len(r) != 2:
            continue
        result[r[0]] = urllib.parse.unquote(r[1].strip())
    return result


def request_data(environ):
    get_data = query_string_parse(environ)
    post_data = parse_form_data(environ)
    return dict(get_data, **post_data)


def result(start_response, msg, info, err_msg, result):
    status = '200 OK'
    response_headers = [('Content-type', 'application/json;charset=utf-8')]
    start_response(status, response_headers)
    return json.dumps({
        "msg": msg,
        "info": info,
        "err_msg": err_msg,
        "result": result
    })


''''
返回msg,info,err_msg,result
'''


def exec_cmd(cmd):
    status, out = subprocess.getstatusoutput(cmd)
    if status != 0:
        return "sys_err", "系统异常", "", None
    try:
        arr = json.loads(out)
        return arr.get("msg", ""), arr.get("info", ""), arr.get("err_msg", ""), arr.get("result", ""),
    except Exception as e:
        return "sys_err", "系统异常", "json_err:%s;%s;%s" % (out, e, cmd), None


''''
返回msg,info,err_msg
'''


def chk_params_empty(arr, post_data):
    for en, cn in list(arr.items()):
        if not post_data.get(en, ""):
            r = 'params_empty', "%s不能为空" % cn, ""
            print(r)
            return r
    return "ok", "参数正确", ""


def get_time_offset(t):
    if IS_LINUX:
        return t + 8 * 3600
    else:
        return t


def get_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", get_localtime())


def get_datetime_offset(d):
    if IS_LINUX:
        return d+ datetime.timedelta(hours=8)
    else:
        return d

def get_now_date():
    return get_datetime_offset(datetime.datetime.now())

def get_bak_filename():
    return time.strftime("%Y%m%d_%H%M%S", get_localtime())

def get_time_str_by_format(fmt):
    return time.strftime(fmt, get_localtime())


def format_time(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(get_time_offset(timestamp)))


def get_localtime():
    # 差8小时
    time1 = time.time()
    return time.localtime(get_time_offset(time1))


def get_timestamp_str():
    return str(get_timestamp())


def get_timestamp():
    return int(time.time())


def get_micro_timestamp():
    return int(time.time() * 1000)


'''20180718163706987'''


def get_ymd_micro_time_str():
    ct = time.time()
    # 差8小时
    local_time = time.localtime(get_time_offset(ct))
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s%03d" % (data_head, data_secs)
    return time_stamp


def urlencode(txt):
    if not txt:
        return ""
    try:
        return urllib.parse.quote(txt.encode("utf-8"), "").replace("-", "___")
    except Exception as e:
        print(("URLENCODE_ERR", e))
        return e.message


def get_list_params(post_data):
    page_size_default = 10
    page_size = post_data.get("page_size", '10')
    try:
        page_size = int(page_size)
        if page_size <= 0:
            page_size = page_size_default
    except:
        page_size = page_size_default

    return page_size, post_data.get("marker", "")


def get_rand_int(num):
    start = 10 ** (num - 1)
    end = 10 ** num - 1
    # range[a, b]
    return random.randint(start, end)


'''guid'''


def get_my_guid():
    return get_ymd_micro_time_str() + str(get_rand_int(8))


def get_today_str():
    time1 = time.time()
    return time.strftime("%Y-%m-%d", time.localtime(time1))


def arr_to_json(arr):
    return json.dumps(arr, ensure_ascii=False, indent=4)


def cal_time_use(funcs):
    start_time = get_timestamp()
    funcs()
    end_time = get_timestamp()
    return end_time - start_time


def get_page_and_size(post_data):
    try:
        page_size = int(post_data.get("page_size", "10"))
    except:
        page_size = 10

    try:
        page = int(post_data.get("page", "1"))
    except:
        page = 1
    return page, page_size


def warp_face(face):
    if not face:
        return "https://pucheng-main.oss-cn-hangzhou.aliyuncs.com/weixin-img/def_face.jpg"
    if not face.endswith(".jpg"):
        return face + "?a=jpg"
    return face


# 2018073117100223796488296
def my_guid_to_time_str(guid):
    if len(guid) < 14:
        return "-"
    time_str = guid[:14]
    return "%s-%s-%s %s:%s:%s" % (
    time_str[:4], time_str[4:6], time_str[6:8], time_str[8:10], time_str[10:12], time_str[12:14])


def guid():
    return str(uuid.uuid4()).replace("-", "")


def intval(v,default_val=0):
    try:
        return int(v)
    except:
        return default_val

def md5(txt):
    import hashlib
    m = hashlib.md5()
    m.update(txt.encode("utf-8"))
    return m.hexdigest()


def get_page(arr):
    if not arr:
        return 1, 10
    return intval(arr.get("page"), 1), intval(arr.get("page_size"), 10)


def format_datetime(d):
    return d.strftime("%Y-%m-%d %H:%M:%S")

def get_zero(d):
    return datetime.datetime.combine(d, datetime.datetime.min.time())
def get_datetime_range(t):
    if t=="all":
        return "1997-01-01 00:00:00","3000-01-01 00:00:00"
    if t=="today":
        start=get_datetime_offset(get_zero(datetime.date.today()))
        end= start + datetime.timedelta(hours=23, minutes=59, seconds=59)
        return format_datetime(start),format_datetime(end)
    
    if t=="this_month":
        today =datetime.date.today()
        _, last_day_num = calendar.monthrange(today.year, today.month)
        first_day = datetime.datetime(today.year, today.month, 1)
        #最后一天的23:59:59
        last_day = datetime.datetime(today.year, today.month, last_day_num) + datetime.timedelta(hours=23, minutes=59, seconds=59)
        return format_datetime(get_datetime_offset(first_day)),format_datetime(get_datetime_offset(last_day))


def get_time_range(duration_type, arr):
    lists=[]
    if duration_type=="y":
        for y in range(arr.get("start_year"),arr.get("end_year")+1):
            start=datetime.datetime(y,1,1,0,0,0)
            end=datetime.datetime(y,12,31,23,59,59)
            lists.append((start,end))
    elif duration_type=="m":
        start=datetime.datetime(arr.get("start_year"),arr.get("start_month"),1,0,0,0)
        while start.timestamp() <= datetime.datetime(arr.get("end_year"),arr.get("end_month"),1,0,0,0).timestamp():
            _, last_day_num = calendar.monthrange(start.year, start.month)
            delta=datetime.timedelta(days=last_day_num)-datetime.timedelta(seconds=1)
            # prints
            # print("del",delta)

            end=start+delta
            # print("end",end)
            lists.append((start,end))
            start=end+datetime.timedelta(seconds=1)
    elif duration_type=="d":
        start = datetime.datetime(arr.get("start_year"), arr.get("start_month"), arr.get("start_day"), 0, 0, 0)
        while start.timestamp() <= datetime.datetime(arr.get("end_year"), arr.get("end_month"),arr.get("end_day"), 0, 0, 0).timestamp():
            _, last_day_num = calendar.monthrange(start.year, start.month)
            delta = datetime.timedelta(days=1)-datetime.timedelta(seconds=1)
            end = start + delta
            lists.append((start, end))
            start = end + datetime.timedelta(seconds=1)
    else:
        return []

    lists=[(format_datetime(get_datetime_offset(start)), format_datetime(get_datetime_offset(end))) for (start,end) in lists]
    return lists
def get_price_txt(fen):
    return "%.2f"%(fen/100)
