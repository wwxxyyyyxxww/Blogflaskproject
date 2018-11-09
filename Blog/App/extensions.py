from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
# pip3 install flask-login
from flask_login import LoginManager
from flask_cache import Cache  # 缓存

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate(db=db)
mail = Mail()
cache = Cache(config={'CACHE_TYPE':'simple'})
# cache = Cache(config={'CACHE_TYPE':'redis'})
login_manager = LoginManager()

#初始化所有第三方扩展库加载
def ext_init(app):
    bootstrap.init_app(app)  # bootstrap
    moment.init_app(app)  # 格式化时间的扩展库
    db.init_app(app)  # 模型的对象
    migrate.init_app(app)  # 模型迁移命令
    mail.init_app(app)
    cache.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'  # 指定登录的端口
    login_manager.login_message = '请登录后再进行访问'  # 跳到登录页面的提示
    login_manager.session_protection = 'strong'  # 设置session保护级别,有任何异常都会进行账户退出







