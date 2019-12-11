# coding=utf-8
import os
from flask import Flask,request,render_template,redirect,url_for,flash,jsonify,session,Markup
from datetime import datetime

from flask_login import LoginManager,login_user,current_user,login_required,logout_user

from wtforms.validators import DataRequired
from flask_wtf import Form

from flask_sqlalchemy import SQLAlchemy

from config import Config
from form import LoginForm,RegisterForm,ArticleForm
from models import smile_user,Article,categories


	
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app,use_native_unicode='utf8')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '你必须登陆后才能访问该页面'
login_manager.login_message_category = "info"


#主页路由
@app.route('/')
def index():
	return render_template('index/index.html')

#关于我们
@app.route('/about')
def about():
	return render_template('index/about.html')

#联系我们
@app.route('/contact')
def contact():
	return render_template('index/contact.html')

#个人主页
@app.route('/main', methods=['POST', 'GET'])
@login_required
def main():
	cates_1 = categories.query.filter_by(prefix_code="0").all()
	cates_2 = categories.query.filter(categories.prefix_code!="0").all()
	articles = Article.query.all()
	return render_template('index/main.html', title="主页",cates_1=cates_1,cates_2=cates_2,articles=articles)


#文章api
@app.route('/article', methods=['POST'])
@login_required
def article():
	post_id = request.values.get("id")
	print(post_id)
	article = Article.query.filter_by(id=post_id).first()
	if article:
		content_html = Markup(article.content_html)
		return jsonify({
			"success": 200,
			"article":{
				'title' : article.title,
				'content' : content_html,
				'addtime' : article.addtime,
				'user' : article.userid
			}
			})
	else:
		return jsonify({"error": 404})


@login_manager.user_loader
def load_user(user_id):
	curr_user = smile_user.query.get(user_id)
	return curr_user

#登录
@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		name = form.username.data
		pwd = form.password.data
		user = smile_user.query.filter_by(username=name).first()
		if user and user.password == pwd:
			login_user(user,remember=True)
			return redirect(url_for('main'))
		else:
			flash("密码或账户错误。", category='error')
	return render_template('index/login.html', title='登录', form=form)

#注销
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('再见！')
	return redirect(url_for('login'))

#注册
@app.route('/register', methods=['POST', 'GET'])
def register():
	form = RegisterForm()	
	if form.validate_on_submit():
		username = form.username.data
		user = smile_user.query.filter_by(username=username).first()
		
		if user:
			flash('用户名已存在',category='error')
			return redirect(url_for('register'))

		email = form.email.data
		mail = smile_user.query.filter_by(email=email).first()

		if mail:
			flash('邮箱已存在',category='error')
			return redirect(url_for('register'))


		passwd1 = form.password1.data
		passwd2 = form.password2.data

		if passwd1 != passwd2:
			flash('两次密码不一致，请从新输入！',category='error')
			return redirect(url_for('register'))
		#头像地址，先设一个默认值
		image = 'a.jpg'
		#注册日期
		addtime = str(datetime.now().date())
		#手机号，后续可能会用到
		phone = "18888888888"
		#注册时ip地址
		ip = request.remote_addr
		#'权限判断, 1为普通会员 2为团队成员'
		level = 1
		#'账号状态 1为正常 2为禁止登录'
		status = 1
		#会员积分
		cash = 0
		#最后一次登录时间
		lastlogintime = str(datetime.now())
		user = smile_user(username=username,password=passwd1,image=image,addtime=addtime,email=email,phone=phone,ip=ip,level=level,status=status
			,cash=cash,lastlogintime=lastlogintime)
		db.session.add(user)
		db.session.commit()
		flash('注册成功', category='info')
	return render_template('index/register.html', title='注册', form=form)


#投稿功能
@app.route('/add', methods=['GET', 'POST'])
def add():
	form = ArticleForm()
	cates = categories.query.filter_by(prefix_code="0").all()
	if form.validate_on_submit():
		cate_name = form.category.data
		cate = categories.query.filter_by(name=cate_name).first()
		if cate:
			category = cate.code
		else:
			category = cate_name
		title = form.title.data
		content = form.body.data
		addtime = str(datetime.now())
		ip = request.remote_addr
		price = 0
		display = 1
		status = 1
		#basepath = os.path.dirname(__file__)  # 当前文件所在路径
		#fileGet='uploads/assignment{}'.format(HOMEWORK_TIME)
		#upload_path = os.path.join(basepath,fileGet,secure_filename(fpy.filename))
		#savepic_path = 'app/static/assets/img/'+form.file.data.filename
		#cate=Category.query.filter_by(name=dict(form.categories.choices).get(form.categories.data)).first_or_404()  #处理类别
		#cate.number=cate.number+1
		article=Article(
					title=title,
					content=content,
					addtime=addtime,
					ip=ip,
					price=price,
					display=display,
					status=status,
					category=category)  #新建文章
		db.session.add(article)
		db.session.commit()
		flash('上传成功！')
		return redirect(url_for('add'))
	#if request.method=='POST':
	#   fpic=request.files['editormd-image-file']
	#   bodypic_path='app/static/pic/'+fpic.filename
	#   fpic.save(bodypic_path)
	# return render_template('/admin/post.html',title=title, form=form,category=category)
	return render_template('index/add.html', title="投稿", form=form, cates=cates)

#文章图片上传功能
@app.route('/upload/',methods=['GET','POST'])
def upload():
	file=request.files.get('editormd-image-file')
	if not file:
		res={
			'success':0,
			'message':'上传失败'
		}
	else:
		ex=os.path.splitext(file.filename)[1]
		filename=datetime.now().strftime('%H%M%S')+ex
		bodypic_path='./static/file/' + datetime.now().strftime('%Y/%m/%d/')
		isExists=os.path.exists(bodypic_path)
		if not isExists:
			os.makedirs(bodypic_path)
		save_path='./static/file/' + datetime.now().strftime('%Y/%m/%d/') + filename
		file.save(save_path)
		res={
			'success':1,
			'message':'上传成功',
			'url':save_path
		}
	return jsonify(res)

if __name__ == '__main__':
	app.debug = True
	app.run()