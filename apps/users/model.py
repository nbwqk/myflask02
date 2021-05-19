
# class User(object):
#     def __init__(self,username,password,phone=None):
#         self.username=username
#         self.password=password
#         self.phone=phone
#
#     def __str__(self):
#         return self.username
from datetime import datetime

from exts import db


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(11),unique=True)
    email=db.Column(db.String(30))
    icon=db.Column(db.String(100))
    isdelete=db.Column(db.Boolean,default=False)
    rdatetime=db.Column(db.DateTime,default=datetime.now)
    articles=db.relationship('Article',backref='user')
    photos=db.relationship('Photo',backref='user')
    comments=db.relationship('Comment',backref='user')
    aboutme=db.relationship('Aboutme',backref='user')
    message=db.relationship('Messageboard',backref='user')

    def __str__(self):
        return self.username

class Photo(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    photo_name=db.Column(db.String(50),nullable=False)
    photo_path=db.Column(db.String(50),nullable=False)
    photo_datetime=db.Column(db.DateTime,default=datetime.now)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __str__(self):
        return self.photo_name

class Aboutme(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.BLOB,nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    pdatetime=db.Column(db.DateTime,default=datetime.now)

    def __str__(self):
        return self.content

class Messageboard(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.String(255),nullable=False)
    mdatetime=db.Column(db.DateTime,default=datetime.now)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),default=0)