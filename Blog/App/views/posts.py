from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify

from App.extensions import cache
from App.forms import Posts
from App.models import Posts as MPosts
from flask_login import current_user

posts = Blueprint('posts',__name__)

# 发表博客
@posts.route('/send_posts/',methods=['GET','POST'])
def send_posts():
    form = Posts()
    if not current_user.is_authenticated:
        flash('您还没有登录,请先登录再发表')
    elif form.validate_on_submit():
        p = MPosts(title=form.title.data,content=form.content.data,user=current_user)
        p.save()
        flash('发表成功! 去首页查看')
        return redirect(url_for('posts.send_posts'))
    return render_template('posts/send_posts.html',form=form)


# 博客详情
@posts.route('/posts_detail/<int:pid>/')
def posts_detail(pid):
    form = Posts()
    data = MPosts.query.get(pid)
    comment = MPosts.query.filter(MPosts.path.contains(str(pid))
            ).order_by(MPosts.path.concat(MPosts.id))
    # 访问量
    data.visit = data.visit+1
    data.save()
    cache.clear()
    return render_template('posts/posts_detail.html',data=data,form=form,comment=comment)

# 发表评论
@posts.route('/comment/',methods=['GET','POST'])
def comment():
    pid = int(request.form.get('pid'))  # 博客的自增id
    if request.form.get('rid'):
        rid = int(request.form.get('rid'))  # 回复评论人的id
    else:
        rid = None
    if current_user.is_authenticated:
        if rid:
            ppid = rid
        else:
            ppid = pid
        p = MPosts.query.get(ppid)
        MPosts(content=request.form.get('content'),pid=p.id,path=p.path+str(p.id)+',',user=current_user).save()

    else:
        flash('请先登录再发表评论!!!')
    return redirect(url_for('posts.posts_detail',pid=pid))

#收藏操作
@posts.route('/dofavorite/')
def dofavorite():
    try:
        pid = int(request.args.get('pid'))
        if current_user.is_favorite(pid):
            current_user.remove_favorite(pid)
        else:
            current_user.add_favorite(pid)
        return jsonify({'code': 200})
    except:
        return jsonify({'code':500})



