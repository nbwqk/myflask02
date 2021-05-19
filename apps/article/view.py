from base64 import decode

from flask import Blueprint, request, render_template, session, g, redirect, url_for, jsonify

from apps.article.model import Article, Article_type, Comment
from apps.users.model import User
from exts import db
from settings import DevelopmentConfig

article_bp=Blueprint('article',__name__,url_prefix='/article')

required_login_list=['/article/publish']
@article_bp.before_app_request
def before_request():
    if request.path in required_login_list:
        id=session.get('uid')
        if not id:
            return redirect(url_for('user.login'))
        else:
            user=User.query.get(id)
            g.user=user
    else:
        id = session.get('uid')
        if not id:
            g.user=None
        else:
            user = User.query.get(id)
            g.user = user

 # 添加模板过滤器，把二进制转换成字符
@article_bp.app_template_filter('cdecode')
def content_decode(content):
    content=content.decode('utf-8')
    if len(content)>100:
        return content[:100]+'......'
    else:
        return content

@article_bp.app_template_filter('wdecode')
def wenzhang_decode(content):
    content=content.decode('utf-8')
    return content

@article_bp.route('/publish',methods=['GET','POST'])
def publish():
    user=g.user
    types=Article_type.query.all()
    if request.method=='POST':
        title=request.form.get('title')
        type_id=request.form.get('type')
        content=request.form.get('content')
        article=Article()
        article.title=title
        article.content=content
        article.user_id=g.user.id
        article.type_id=type_id
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('article.detail'))
    else:
        return  render_template('article/add_article.html',user=user,types=types)

@article_bp.route('/detail')
def detail():
    types=Article_type.query.all()
    page=int(request.args.get('page',1))
    pagination = Article.query.order_by(-Article.pdatetime).paginate(page=page,per_page=DevelopmentConfig.PER_PAGE)
    # uid=request.cookies.get('uid',None)
    return render_template('article/detail.html',pagination=pagination,user=g.user,types=types)

@article_bp.route('/wenzhang')
def wenzhang():
    aid=request.args.get('aid')
    page=request.args.get('page',type=int)
    article=Article.query.get(aid)
    types=Article_type.query.all()
    comments=Comment.query.filter(Comment.article_id==aid).order_by(-Comment.cdatetime).paginate(page=page,per_page=5)
    return render_template('article/wenzhang.html',article=article,user=g.user,types=types,comments=comments)

@article_bp.route('/article_love')
def article_love():
    aid=request.args.get('aid')
    tag=request.args.get('tag')
    article=Article.query.get(aid)
    if tag=='0':
        article.love_num+=1
    elif tag=='1':
        article.love_num-=1
    db.session.commit()
    return jsonify(num=article.love_num)

@article_bp.route('/article_save')
def article_save():
    aid=request.args.get('aid')
    tag=request.args.get('tag')
    article=Article.query.get(aid)
    if tag=='0':
        article.save_num+=1
    elif tag=='1':
        article.save_num-=1
    db.session.commit()
    return jsonify(num=article.save_num)

@article_bp.route('/add_comment',methods=['GET','POST'])
def add_comment():
    user=g.user
    if request.method=='POST':
        a_id=request.form.get('a_id')
        c=request.form.get('comment')
        comment=Comment()
        comment.comment=c
        comment.user_id=user.id
        comment.article_id=a_id
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article.wenzhang')+'?aid='+a_id)
    return redirect(url_for('article.detail'))

@article_bp.route('/type_detail')
def type_detail():
    user=g.user
    types=Article_type.query.all()
    t_id=request.args.get('t_id')
    type=Article_type.query.get(t_id)
    page=int(request.args.get('page',1))
    articles=Article.query.filter(Article.type_id==t_id).order_by(-Article.pdatetime).paginate(page=page,per_page=DevelopmentConfig.PER_PAGE)
    return render_template('article/type_detail.html',user=user,types=types,articles=articles,t_id=t_id,type=type)

@article_bp.route('/search_article',methods=['GET','POST'])
def search_article():
    user=g.user
    types=Article_type.query.all()
    if request.method=='POST':
        c=request.form.get('content')
    else:
        c=request.args.get('content')
    page=int(request.args.get('page',1))
    articles=Article.query.filter(Article.title.contains(c)).order_by(-Article.pdatetime).paginate(page=page,per_page=DevelopmentConfig.PER_PAGE)
    return render_template('article/search_article.html',user=user,types=types,articles=articles,content=c)