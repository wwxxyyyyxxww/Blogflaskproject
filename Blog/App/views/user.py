import os
from datetime import datetime

from flask import Blueprint, render_template, flash, url_for, redirect, request

from App.email import send_mail
from App.forms import Register, AgainActivate, Login, Update_password, Update_email,Update_icon  # 导入注册表单类
from App.models import User  # 导入User模型类
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required,login_user,logout_user,current_user
from App.settings import Config

user = Blueprint('user',__name__)
'''
1.接受到数据(用户名和邮箱唯一性)
2.保存到数据库(密码加密后)
3.生成token值
4.配置发送邮件
5.发送激活邮件
6.提示用户注册成功 前去激活
7.跳转到登录页面
8.创建激活视图函数
9.登录
'''


# 注册
@user.route('/register/',methods=['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        u = User(username=form.username.data,
                 password=form.password.data,
                 email=form.email.data)
        u.save()
        token = u.generate_token()  # 生成token值
        send_mail('账户激活',u.email,'activate',username=u.username,endpoint='user.activate',token=token)
        flash('恭喜注册成功 请前去邮箱激活')
        return redirect(url_for('user.login'))

    return render_template('user/register.html',form=form)

# 再次激活
@user.route('/again_activate/',methods=['GET','POST'])
def again_activate():
    form = AgainActivate()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u.check_password(form.password.data):
            flash('请输入正确的密码')
        elif u.confirm:
            flash('该账户已经激活 请前往登录')
        else:
            token = u.generate_token()  # 生成token值
            send_mail('账户激活', u.email, 'again_activate', username=u.username, endpoint='user.activate', token=token)
            flash('激活邮件发送成功 请前去邮箱激活')
            return redirect(url_for('user.login'))

    return render_template('user/again_activate.html',form=form)

# 账户激活
@user.route('/activate/<token>/')
def activate(token):
    if User.check_token(token):
        flash('恭喜你激活成功,请前去登录')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败,请重新再次激活')
        return redirect(url_for('user.register'))


# 登录
@user.route('/login/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u.check_password(form.password.data):
            flash('请输入正确的密码')
        elif not u.confirm:
            flash('该账户未激活 请前往激活')
        else:
            u.lastLogin = datetime.utcnow()
            u.save()
            flash('登录成功!!')
            login_user(u,remember=form.remember.data)
            return redirect(request.args.get('prevpath','/'))  # 返回到上一个页面
    return render_template('user/login.html',form=form)

# 登出
@user.route('logout')
@login_required
def logout():
    logout_user()
    flash('注销成功!!')
    return redirect(url_for('main.index'))

# 修改密码
@user.route('update_password',methods=['GET','POST'])
@login_required
def update_password():
    form = Update_password()
    if form.validate_on_submit():
        u = User.query.filter_by(username=current_user.username).first()
        if not u.check_password(form.oldpassword.data):
            flash('请输入正确的密码')
        else:
            u.password = form.newpassword.data
            u.save()
            flash('修改密码成功!!')
            return redirect(url_for('main.index'))
    return render_template('user/update_password.html', form=form)

# 修改邮箱
@user.route('update_email',methods=['GET','POST'])
@login_required
def update_email():
    form = Update_email()
    if form.validate_on_submit():
        u = User.query.filter_by(username=current_user.username).first()
        u.email = form.email.data
        u.confirm = False
        u.save()
        token = u.generate_token()  # 生成token值
        send_mail('账户激活', u.email, 'again_activate', username=u.username, endpoint='user.activate', token=token)
        flash('修改邮箱成功 激活邮件发送成功 请前去邮箱激活')
        return redirect(url_for('main.index'))
    return render_template('user/update_email.html', form=form)

# 修改头像
@user.route('/update_icon/',methods=['GET','POST'])
@login_required
def update_icon():
    form = Update_icon()
    if form.validate_on_submit():
        u = User.query.filter_by(username=current_user.username).first()
        file = form.icon.data
        print(file)  # 获取文件名称
        u.icon = file.filename
        u.save()
        # file.save(file.filename) #存储上传文件
        path = os.path.join(os.getcwd(), 'App/static/upload')
        file.save(os.path.join(path, file.filename))
        flash('修改头像成功')
        return redirect(url_for('main.index'))
    return render_template('user/update_icon.html',form=form)

# 必须登录才能访问
@user.route('/test/')
@login_required
def test():
    return 'test'









# # 加密
# @user.route('/test/')
# def test():
#     h = generate_password_hash('123456')
#     print(check_password_hash(h,'1234567'))
#     return ''


