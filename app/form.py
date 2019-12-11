# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField,FileField,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired,FileAllowed

from models import smile_user

#登录表单
class LoginForm(FlaskForm):
	username = StringField('用户名：', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('密码：', validators=[DataRequired()])
	submit = SubmitField('登陆')

#注册表单
class RegisterForm(FlaskForm):
	username = StringField('用户名：', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('邮箱：', validators=[DataRequired()])
	password1 = PasswordField('密码：', validators=[DataRequired(), Length(min=3, max=120)])
	password2 = PasswordField('确认密码：', validators=[DataRequired()])
	submit = SubmitField('提交')


	# def validate_username(self, username):
	#		 user = smile_user.query.filter_by(username=username.data).first()
	#		 if user:
	#			 raise ValidationError("用户昵称已存在。")

	# def validate_email(self, email):
	#	 user = smile_user.query.filter_by(email=email.data).first()
	#	 if user:
	#		 raise ValidationError('邮箱已存在.')

#文章表单

class ArticleForm(FlaskForm):

	title = StringField('标题', [DataRequired(), Length(max=255)])
	body = TextAreaField('内容', [DataRequired()])
	#categories = SelectMultipleField('Categories', coerce=int)
	#categories=SelectField('文章种类', choices=[],coerce=int )
	category = StringField('文章分类', [DataRequired(), Length(max=255)])
	body_html = HiddenField()
	submit = SubmitField('提交')
	#submit=SubmitField(render_kw={'value': "提交",'class': 'btn btn-success pull-right'})
	#file = FileField(label="文章封面",validators=[FileRequired(),FileAllowed(['png', 'jpg'], '只接收.png和.jpg的图片')])

	#保证数据与数据库同步
	# def __init__(self):
	# 	super(PostForm, self).__init__()
	# 	self.categories.choices = [(c.id, c.name) for c in Category.query.order_by('id')]






































