# coding=utf-8
from flask import Flask,Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user
from flask_login import LoginManager
from werkzeug.security import check_password_hash, generate_password_hash

import bleach
from markdown import markdown

app = Flask(__name__)

#设置连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/smile_team'

#设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#设置成 True，SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#实例化SQLAlchemy对象
db = SQLAlchemy(app)

class smile_user(db.Model,UserMixin):
	__tablename__ = 'smile_user'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),unique=True)
	password = db.Column(db.String(50),nullable=False)
	image = db.Column(db.String(50),nullable=False)
	addtime = db.Column(db.Date,nullable=False)
	email = db.Column(db.String(50),unique=True)
	phone = db.Column(db.String(50),nullable=False)
	ip = db.Column(db.String(50),nullable=True)
	level = db.Column(db.Integer,default=1) #'权限判断, 1为普通会员 2为团队成员'
	status = db.Column(db.Integer,default=1)#'账号状态 1为正常 2为禁止登录'
	cash = db.Column(db.Integer,default=0)
	lastlogintime = db.Column(db.DateTime,nullable=False)
	
	# def __repr__(self):
	# 	return "<User %r>" % self.Username

	# def generate_password_hash(self, pwd):
	# 	self.pwd = generate_password_hash(pwd)

	# def check_password_hash(self, pwd):
	# 	return check_password_hash(self.pwd, pwd)


class Article(db.Model):
	__tablename__ = 'article'
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer) #提交者id,0为匿名投稿
	title = db.Column(db.String(128),nullable=False)	   #文章标题
	content=db.Column(db.Text,nullable=False)	 #原本text格式
	content_html = db.Column(db.Text)	  #转化成html代码后的格式
	poc = db.Column(db.Text) 				# 文章poc，可以为空
	file = db.Column(db.String(128)) 		#文章附件，可以为空
	addtime = db.Column(db.DateTime)	   #创建时间
	uptime = db.Column(db.DateTime)		#后台审核时间
	ip = db.Column(db.String(50),nullable=True) #提交时IP
	price = db.Column(db.Integer) 	#文章奖金
	display = db.Column(db.Integer) # 审核状态：审核状态 1审核中 2为待补充 3审核通过 4后台拒绝
	status = db.Column(db.Integer) # 文章状态 1完全公开 2详情公开，poc禁止查看 3团队公开
	category = db.Column(db.String(128))	 #文章类别
	# posts = db.relationship('Post',backref='article',lazy='dynamic')	#一个评论的外键

	#将文本转化为html
	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
					'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
					'h1', 'h2', 'h3', 'p', 'img', 'video', 'div', 'iframe', 'p', 'br', 'span', 'hr', 'src', 'class']
		allowed_attrs = {'*': ['class'],'a': ['href', 'rel'],'img': ['src', 'alt']}
		target.content_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),tags=allowed_tags,attributes=allowed_attrs,strip=True))
		
db.event.listen(Article.content, 'set', Article.on_changed_body)


#文章分类
class categories(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer,primary_key=True)
	code = db.Column(db.String(50),nullable=True)
	prefix_code = db.Column(db.String(50))
	name = db.Column(db.String(50))

# insert into categories(code,prefix_code,name) values('00','0','默认分类');
# insert into categories(code,prefix_code,name) values('01','0','WEB安全');
# insert into categories(code,prefix_code,name) values('02','0','内网渗透');
# insert into categories(code,prefix_code,name) values('03','0','工具使用');
# insert into categories(code,prefix_code,name) values('04','0','编程学习');
# insert into categories(code,prefix_code,name) values('0101','01','SQL注入');
# insert into categories(code,prefix_code,name) values('0102','01','XSS漏洞');
# insert into categories(code,prefix_code,name) values('0201','02','msf使用');
# insert into categories(code,prefix_code,name) values('0202','02','cs使用');

# 	def __init__(self, arg):
# 		super(crs, self).__init__()
# 		self.arg = arg
		




if __name__ == '__main__':
	db.create_all()

