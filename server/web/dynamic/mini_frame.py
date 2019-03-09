from pymysql import connect
import re
import urllib.parse

url_path = dict()


def route(url):
    def set_func(func):
        url_path[url] = func

        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func


def sql_exe(sql, *args):
    con = connect(host='localhost', port=3306, user='root', password='mysql', database='stock_db', charset='utf8')
    cursor = con.cursor()
    cursor.execute(sql, args)
    con.commit()
    ret = cursor.fetchall()
    cursor.close()
    con.close()
    return ret


def application(env, start_set):
    start_set("200 OK", [("Content-Type", "text/html;charset=utf8")])
    file_name = env["path"]
    try:

        for url, func in url_path.items():
            name = re.match(url, file_name)
            print(name)
            if name:
                ret = func(name)
                return ret
        else:
            ret = "%s没有这个函数" % file_name
    except:
        ret = "%s错误" % func
        return ret
    else:
        return ret


@route(r"/center\.html")
def center(ret):
    with open("./templates/center.html", "r") as f:
        content = f.read()
    module_info = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
            </td>
            <td>
                <input type="button" value="删除" id="toDel" name="toDel" systemidvaule=%s>
            </td>
        </tr>
    """
    sql="select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info as i inner join focus as f on i.id=f.info_id"
    infos = sql_exe(sql)
    html = ""
    for temp in infos:
        html += module_info % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[0], temp[0])
    ret = re.sub(r"\{%content%\}", html, content)
    return ret


@route(r"/index\.html")
def index(ret):
    with open("./templates/index.html", "r") as f:
        content = f.read()
    module_info = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule=%s>
        </td>
        </tr>
    """
    sql = "select * from info;"
    infos = sql_exe(sql)
    html = ""
    for temp in infos:
        html += module_info % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6],temp[7], temp[1])
    ret = re.sub(r"\{%content%\}", html, content)
    return ret


@route(r"/add/(\d+)\.html")
def add_focus(ret):
    stock_code = ret.group(1)
    sql = "select * from info where code=%s;"
    ret = sql_exe(sql, stock_code)
    if not ret:
        return "没有这只股票"
    sql = "select * from focus as f inner join info as i on i.id=f.info_id where code=%s;"
    ret = sql_exe(sql, stock_code)
    if ret:
        return "请勿重复关注"
    sql = "insert into focus (info_id) select id from info where code=%s;"
    sql_exe(sql, stock_code)
    return "关注成功"


@route(r"/del/(\d+)\.html")
def del_focus(ret):
    stock_code = ret.group(1)
    sql = "select * from info where code=%s;"
    ret = sql_exe(sql, stock_code)
    if not ret:
        return "没有这只股票"
    sql = "select * from focus as f inner join info as i on i.id=f.info_id where code=%s;"
    ret = sql_exe(sql, stock_code)
    if not ret:
        return "未关注"
    sql = "delete from focus where info_id=(select id from info where code=%s);"
    sql_exe(sql, stock_code)
    return "成功取消关注"


@route(r"/update/(\d+)\.html")
def update_focus(ret):
    stock_code = ret.group(1)
    sql = "select * from info where code=%s;"
    ret = sql_exe(sql, stock_code)
    if not ret:
        return "没有这只股票"
    sql = "select * from focus as f inner join info as i on i.id=f.info_id where code=%s;"
    ret = sql_exe(sql, stock_code)
    if not ret:
        return "未关注"
    with open("./templates/update.html", "r") as f:
        content = f.read()
    content = re.sub(r"{%code%}", stock_code, content)
    sql = "select note_info from focus as f inner join info as i on i.id=f.info_id where code=%s;"
    ret = sql_exe(sql, stock_code)
    for temp in ret:
        stock_info = temp[0]
    content = re.sub(r"{%note_info%}",stock_info, content)
    return content


@route(r"/update/(\d+)/(.*)\.html")
def update_focus_save(ret):
    stock_code = ret.group(1)
    stock_info = ret.group(2)
    stock_info = urllib.parse.unquote(stock_info)
    sql = "select * from info where code=%s;"
    ret = sql_exe(sql, stock_code)
    if not ret:
        return "没有这只股票"
    sql = "select * from focus as f inner join info as i on i.id=f.info_id where code=%s;"
    ret = sql_exe(sql, stock_code)
    if not ret:
        return "未关注"
    sql = "update focus set note_info=%s where info_id = (select id from info where code=%s);"
    sql_exe(sql, stock_info, stock_code)
    return "修改成功"
