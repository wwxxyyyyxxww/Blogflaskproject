from flask import Flask

from App.models import Posts
from .extensions import ext_init
from .settings import configDict
from .views import register_blueprint
#整个项目的加载
def create_app(configName):
    app = Flask(__name__)
    app.config.from_object(configDict[configName]) #配置文件的加载
    ext_init(app)
    register_blueprint(app)
    add_tem_filter(app)
    return app

#内容超出20个字显示 ...
#超出长度范围显示...
def add_tem_filter(app):
    def showpoint(val,myLength=20):
        length = len(val)
        if length>myLength:
            val = val[0:myLength]+'...'
        return val

    def replace_color(con,word):
        con = con.replace(word,'<span style="color:red;font-seze:20px">'+str(word)+'</span>')
        return con

    # 回复用户名的显示
    def replay_username(pid):
        return Posts.query.get(int(pid)).user.username

    app.add_template_filter(replay_username)
    app.add_template_filter(showpoint)
    app.add_template_filter(replace_color)
