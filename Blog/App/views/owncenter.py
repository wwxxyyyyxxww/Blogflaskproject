from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
# current_app:表示当前运行程序文件的程序实例。
from flask_login import login_required, current_user
from sqlalchemy import or_, and_

from App.extensions import cache
from App.models import Posts as MPosts
from App.forms import Posts

center = Blueprint('center',__name__)

# 博客管理
@center.route('/blog_manage/',methods=['GET','POST'])
@login_required
def blog_manage():
    # 获取页码
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1
    pagination = current_user.posts.filter_by(pid=0).order_by(MPosts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
    data = pagination.items  # 获取当前页面的数据
    print(data)
    return render_template('owncenter/blogmanage.html',data=data,pagination=pagination)

# 博客编辑
@center.route('/edit_blog/<int:pid>/',methods=['GET','POST'])
def edit_blog(pid):
    form = Posts()
    posts = MPosts.query.get(pid)
    if form.validate_on_submit():
        posts.title = request.form.get('title')
        posts.content = request.form.get('content')
        posts.timestamp = datetime.utcnow()
        posts.save()
        flash('博客更新成功')
        cache.clear()
        return redirect(url_for('center.blog_manage'))
    # 给表单添加默认值
    form.title.data = posts.title
    form.content.data = posts.content
    return render_template('owncenter/edit_blog.html',form=form,posts=posts,pid=pid)

# 设置为自己查看
@center.route('/see_myself/<int:pid>/')
def see_myself(pid):
    posts = MPosts.query.get(pid)
    posts.state = not posts.state
    posts.save()
    flash('设置成功!')
    return redirect(url_for('center.blog_manage'))

# 删除
@center.route('/del_posts/<int:pid>/')
def del_posts(pid):
    posts = MPosts.query.get(pid)
    posts.delete()
    flash('删除成功!')
    return redirect(url_for('center.blog_manage'))


# 博客搜索
@center.route('/blog_search/',methods=['POST','GET'])
def blog_search():
    # 获取页码
    try:
        page=int(request.args.get('page',1))
    except:
        page=1
    #获取搜索的内容
    if request.method =='POST':
        word = request.form.get('search', '')
    else:
        word = request.args.get('search', '')
    pagination = MPosts.query.filter(MPosts.title.contains(word),and_(MPosts.pid==0,MPosts.state==True)
        ).order_by(MPosts.timestamp.desc()
        ).paginate(page,current_app.config['PAGE_NUM'],False)
    print(pagination)
    data = pagination.items  # 获取当前页面的数据
    print(data)
    return render_template('owncenter/search_blog.html',data=data,pagination=pagination,word=word)

@center.route('/collections/')
@login_required
def collections():
    try:
        pid = int(request.args.get('pid'))
        if pid and current_user.is_favorite(pid):
            current_user.remove_favorite(pid)
            flash('取消收藏成功!')
            # return redirect(url_for('center.collections'))
    except:
        pass
    data = current_user.favorites.all()  # 查询所有的收藏
    return render_template('owncenter/collections.html',data=data)
