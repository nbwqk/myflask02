import hashlib
import os
import time
from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session, g
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps.article.model import Article_type
from apps.users.model import User, Photo, Aboutme, Messageboard
from exts import db
from settings import Config

user_bp = Blueprint('user', __name__, url_prefix='/user')

required_login_list = ['/user/user_center',
                       '/user/add_photo',
                       '/user/myphoto',
                       '/photo_detail',
                       '/user/aboutme',
                       '/user/display_me',
                       '/manage_message',]

allowed_suffix = ['bmp', 'jpg', 'jpeg', 'png']


@user_bp.before_app_request
def before_request():
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            return redirect(url_for('user.login'))
        else:
            user = User.query.get(id)
            g.user = user
    else:
        id = session.get('uid')
        if not id:
            g.user = None
        else:
            user = User.query.get(id)
            g.user = user

@user_bp.app_template_filter('udecode')
def aboutme_decode(content):
    content=content.decode('utf-8')
    return content

@user_bp.route('/center')
def center():
    users = User.query.filter(User.isdelete == False).all()
    return render_template('user/center.html', users=users)


@user_bp.route('/user_center', methods=['GET', 'POST'])
def user_center():
    types = Article_type.query.all()
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        icon1 = request.form.get('icon1')  # 隐藏字段，是原来数据库里的头像地址
        icon = request.files.get('icon')
        user = User.query.filter(User.phone == phone).first()
        if (not user) or (user.id == g.user.id):  # 如果手机号码没被注册或者是本用户手机号码
            suffix = icon.filename.rsplit('.')[-1]  # 获取上传的文件后缀名
            if suffix == '':
                user = g.user
                user.username = username
                user.phone = phone
                user.email = email
                user.icon = icon1
                db.session.commit()
                return render_template('user/modify_user.html', user=g.user, types=types)
            else:
                if suffix in allowed_suffix:
                    # 保证文件名符合pathon规则
                    icon_name = secure_filename(icon.filename)
                    icon_name = str(time.time()) + icon_name
                    file_path = os.path.join(Config.UPLOAD_ICON_DIR, icon_name)
                    icon.save(file_path)  # 保存成功
                    user = g.user
                    user.username = username
                    user.phone = phone
                    user.email = email
                    path = 'upload/icon'
                    user.icon = path + '/' + icon_name
                    db.session.commit()
                    return render_template('user/modify_user.html', user=g.user, types=types)
                else:
                    msg = '图像后缀名必须是bmp,jpg,jpeg,png'
                    render_template('user/modify_user.html', user=g.user, msg=msg, types=types)
        else:
            msg = '此号码已被注册'
            return render_template('user/modify_user.html', user=g.user, msg=msg, types=types)
    return render_template('user/modify_user.html', user=g.user, types=types)


@user_bp.route('/del', endpoint='delete')
def del_user():
    id = request.args.get('id')
    user = User.query.get(id)
    user.isdelete = True
    db.session.commit()
    return redirect(url_for('user.center'))


@user_bp.route('/update', methods=['POST', 'GET'], endpoint='update')
def update_user():
    if request.method == 'POST':
        id = request.form.get('id')
        username = request.form.get('username')
        phone = request.form.get('phone')
        user = User.query.get(id)
        user.username = username
        user.phone = phone
        db.session.commit()
        return redirect(url_for('user.center'))
    id = request.args.get('id')
    user = User.query.get(id)
    return render_template('/user/update.html', user=user)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    # uid=session.get('uid',None)
    # uid=request.cookies.get('uid',None)
    # user=User.query.get(uid)
    types = Article_type.query.all()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if username:
            u = User.query.filter(User.username == username).all()
            if not u:
                if password == repassword:
                    u = User.query.filter(User.phone == phone).all()
                    if not u:
                        user = User()
                        user.username = username
                        # user.password=hashlib.sha256(password.encode('utf-8')).hexdigest()
                        user.password = generate_password_hash(password)
                        user.phone = phone
                        user.email = email
                        db.session.add(user)
                        db.session.commit()
                        session['uid'] = user.id
                        return redirect(url_for('article.detail'))
                        # response=redirect(url_for('article.detail'))
                        # response.set_cookie('uid',str(user.id),max_age=3600)
                        # return response
                    else:
                        msg = '电话已经被注册'
                        return render_template('user/register.html', msg=msg, user=g.user, types=types)
                else:
                    msg = '两次输入的密码不正确'
                    return render_template('user/register.html', msg=msg, user=g.user, types=types)
            else:
                msg = '用户名已被使用！'
                return render_template('user/register.html', msg=msg, user=g.user, types=types)
        else:
            msg = '用户名不能为空'
            return render_template('user/register.html', msg=msg, user=g.user, types=types)
    return render_template('user/register.html', user=g.user, types=types)


@user_bp.route('/check_phone')
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    # code:400 不能用  code:200 能用
    if user:
        return jsonify(code=400, msg='此号码已经被注册')
    else:
        return jsonify(code=200, msg='此号码可用')


@user_bp.route('/check_u')
def check_u():
    usename = request.args.get('username')
    user = User.query.filter(User.username == usename).all()
    if user:
        return jsonify(code=400, msg='用户已存在，请更换')
    else:
        return jsonify(code=200, msg='此用户名可用')


@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    # session方式获取用户id
    # uid=session.get('uid',None)
    # cookie方式获取用户id
    # uid=request.cookies.get('uid',None)
    # user=User.query.get(uid)
    types = Article_type.query.all()
    if request.method == 'POST':
        f = request.args.get('f')
        if f == '1':
            username = request.form.get('username')
            password = request.form.get('password')
            # new_password=hashlib.sha256(password.encode('utf-8')).hexdigest()
            u = User.query.filter(User.username == username).first()
            if u:
                flag = check_password_hash(u.password, password)
                if flag:
                    # session方式记录用户状态
                    session['uid'] = u.id
                    # cookie方式记录用户状态
                    # response=redirect(url_for('article.detail'))
                    # response.set_cookie('uid',str(u.id),max_age=3600)
                    # return response
                    return redirect(url_for('user.user_center'))
                else:
                    msg = '用户名或者密码错误，请重新输入'
                    return render_template('user/login.html', msg=msg, user=g.user, types=types)
            else:
                msg = '用户名或者密码错误，请重新输入'
                return render_template('user/login.html', msg=msg, user=g.user, types=types)
        elif f == '2':
            phone = request.form.get('phone')
            u = User.query.filter(User.phone == phone).first()
            code = request.form.get('code')
            valid_code = session.get(phone, None)
            if code == valid_code:
                session['uid'] = u.id
                del session[phone]
                return redirect(url_for('user.user_center'))
            else:
                msg = '验证码不正确'
                return render_template('user/login.html', msg=msg, user=g.user, types=types)
    return render_template('user/login.html', user=g.user, types=types)


@user_bp.route('/logout')
def logout():
    # 删除session
    session.clear()
    return redirect(url_for('article.detail'))
    # cookie方式删除用户状态
    # response=redirect(url_for('article.detail'))
    # response.delete_cookie('uid')
    # return response


@user_bp.route(('/search'))
def search():
    content = request.args.get('search')
    users = User.query.filter(or_(User.username.contains(content), User.phone.contains(content))).all()
    return render_template('user/center.html', users=users)


@user_bp.route('/send_message')
def send_message():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone, User.isdelete == False).first()
    if user:
        session[phone] = '146389'  # 假设验证码
        return jsonify(code=200, msg='验证码发送成功')
    else:
        return jsonify(code=400, msg='手机没有注册')


@user_bp.route('/add_photo', methods=['GET', 'POST'])
def add_photo():
    user = g.user
    types = Article_type.query.all()
    page = int(request.args.get('page',1))
    photos = Photo.query.filter(Photo.user_id==user.id).paginate(page=page,per_page=5)
    if request.method == 'POST':
        photo = request.files.get('photo')
        p_name = request.form.get('p_name')
        suffix = photo.filename.rsplit('.')[-1]
        if suffix in allowed_suffix:
            photo_name = secure_filename(photo.filename)  # 上传的图片文件名安全化
            photo_name = str(time.time()) + photo_name
            file_path = os.path.join(Config.UPLOAD_PHOTO_DIR, photo_name)
            photo.save(file_path)

            photo = Photo()
            photo.photo_name = p_name
            photo.user_id = user.id
            path = 'upload/photo'
            photo_path = path + '/' + photo_name
            photo.photo_path = photo_path
            db.session.add(photo)
            db.session.commit()
            return redirect(url_for('user.add_photo'))
        else:
            msg = '图片格式错误！'
            return render_template('user/add_photo.html', user=user, types=types, msg=msg, photos=photos)
    return render_template('user/add_photo.html', user=user, types=types, photos=photos)

@user_bp.route('/myphoto')
def myphoto():
    types=Article_type.query.all()
    user=g.user
    page=int(request.args.get('page',1))
    photos=Photo.query.filter(Photo.user_id==user.id).paginate(page=page,per_page=8)
    return render_template('user/myphoto.html',user=user,types=types,photos=photos)

@user_bp.route('/photo_detail')
def photo_detail():
    types=Article_type.query.all()
    user=g.user
    p_id=request.args.get('p_id')
    photo=Photo.query.get(p_id)
    return render_template('user/photo_detail.html',types=types,user=user,photo=photo)

@user_bp.route('/photo_del')
def photo_del():
    pid=request.args.get('pid')
    photo=Photo.query.get(pid)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('user.add_photo'))

@user_bp.route('/aboutme',methods=['GET','POST'])
def aboutme():
    user=g.user
    types=Article_type.query.all()
    if request.method=='POST':
        content=request.form.get('content')
        user_id=g.user.id
        about_me=Aboutme()
        about_me.content=content.encode('utf-8')
        about_me.user_id=user_id
        db.session.add(about_me)
        db.session.commit()
        return redirect(url_for('user.display_me'))
    return render_template('user/aboutme.html',user=user,types=types)

@user_bp.route('/display_me')
def display_me():
    user=g.user
    types=Article_type.query.all()
    aboutme=Aboutme.query.filter(Aboutme.user_id==user.id).first()
    return render_template('user/display_me.html',user=user,types=types,aboutme=aboutme)

@user_bp.route('/message',methods=['POST','GET'])
def message():
    user=g.user
    types=Article_type.query.all()
    page=int(request.args.get('page',1))
    messages=Messageboard.query.order_by(-Messageboard.mdatetime).paginate(page=page,per_page=8)
    if request.method=='POST':
        content=request.form.get('content')
        if content=='':
            msg='必须填写留言板内容哦。'
            return render_template('user/message.html',user=user,types=types,messages=messages,msg=msg)
        if user:
            user_id=user.id
        else:
            user_id=0
        m=Messageboard()
        m.content=content
        m.user_id=user_id
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('user.message'))
    return render_template('user/message.html',user=user,types=types,messages=messages)

@user_bp.route('/manage_message')
def manage_message():
    user=g.user
    types=Article_type.query.all()
    page=int(request.args.get('page',1))
    messages=Messageboard.query.filter(Messageboard.user_id==user.id).order_by(-Messageboard.mdatetime).paginate(page=page,per_page=7)
    return render_template('user/manage_message.html',user=user,types=types,messages=messages)

@user_bp.route('/del_message')
def del_message():
    m_id=request.args.get('m_id')
    message=Messageboard.query.get(m_id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('user.manage_message'))


