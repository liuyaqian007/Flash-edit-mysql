#!C:\programs\Python3\python3.exe
# _*_ coding:utf-8 _*_
#参考
#https://blog.csdn.net/reblue520/article/details/80553373
#https://blog.csdn.net/yudiyanwang/article/details/72956903

from flask import Flask,render_template,request,redirect
import pymysql
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/loginaction/', methods=["POST", "GET"])
def login():
    error_msg = ''

    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    print('username:%s,password:%s' % (username, password))

    if username and password:
        #用户名密码为文件形式，可以采用验证模式，大牛可以自行改动
        if username == "admin" and password == "admin":
            return redirect('/list')
        else:
            error_msg = "username or password is wrong"
    else:
        error_msg = 'need username and password'

    return render_template('login.html', error_msg=error_msg)

@app.route('/list/')
def userlist():
    conn = pymysql.connect(host='mysql_ip地址', user='mysql用户名', password='mysql密码', db='库名', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id,app_type,version,remark,update_time FROM app_version where app_type='IOS'"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('list.html',u=u)

@app.route('/update/')
def update():
    conn = pymysql.connect(host='mysql_ip地址', user='mysql用户名', password='mysql密码', db='库名', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id,app_type,version,remark,update_time FROM app_version where app_type='IOS'"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('update.html',u=u)

@app.route('/updateaction/', methods=['POST'])
def updateaction():
    error_msg = ''
    params = request.args if request.method == 'GET' else request.form

    version = params.get('version')
    remark = params.get('remark')
    update_time = params.get('update_time')

    if all([version,remark,update_time]):
        conn = pymysql.connect(host='mysql_ip地址', user='mysql用户名', password='mysql密码', db='库名', charset='utf8')
        cur = conn.cursor()
        sql = "update app_version set version=%s,remark=%s,update_time=%s where app_type='IOS'"
        cur.execute(sql,(version,remark,update_time))
        conn.commit()
        conn.close()
        return redirect('/list')
    else:
        error_msg = u'参数不能为空'
    return render_template('update.html', error_msg=error_msg)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True)