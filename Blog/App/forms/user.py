from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from App.models import User  # 导入User模型类


class Register(FlaskForm):
    username = StringField('用户名',validators=[DataRequired('用户名不能为空!'),
        Length(min=6,max=12,message='用户名6~12位之间')],
        render_kw={'placeholder':'请输入用户名','minlength':6,'maxlength':12})
    password = PasswordField('密码',validators=[DataRequired('密码不能为空!'),
        Length(min=6,max=12,message='用户名6~12位之间')],
        render_kw={'placeholder':'请输入密码','minlength':6,'maxlength':12})
    confirm = PasswordField('确认密码',validators=[DataRequired('确认密码不能为空!'),
        Length(min=6,max=12,message='用户名6~12位之间'),EqualTo('password',message='密码和确认密码不一致')],
        render_kw={'placeholder':'请输入确认密码','minlength':6,'maxlength':12})
    email = StringField('激活邮箱',validators=[DataRequired('邮箱不能为空!'),
        Email('请输入正确的邮箱地址')],
        render_kw={'placeholder':'请输入有效的邮箱地址'})
    submit = SubmitField('注册')

    # 用户名的唯一性
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已存在 请重新输入')
    # 邮箱的唯一性
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在 请重新输入')


# 再一次激活表单类
class AgainActivate(FlaskForm):
    username = StringField('用户名',validators=[DataRequired('用户名不能为空!'),
        Length(min=6,max=12,message='用户名6~12位之间')],
        render_kw={'placeholder':'请输入用户名','minlength':6,'maxlength':12})
    password = PasswordField('密码',validators=[DataRequired('密码不能为空!'),
        Length(min=6,max=12,message='用户名6~12位之间')],
        render_kw={'placeholder':'请输入密码','minlength':6,'maxlength':12})
    submit = SubmitField('激活')

    # 用户名的唯一性
    def validate_username(self,field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户不存在 请重新输入')

# 登录
class Login(FlaskForm):
    username = StringField('用户名',validators=[DataRequired('用户名不能为空!'),
        Length(min=6,max=12,message='用户名6~12位之间')],
        render_kw={'placeholder':'请输入用户名','minlength':6,'maxlength':12})
    password = PasswordField('密码',validators=[DataRequired('密码不能为空!'),
        Length(min=6,max=12,message='用户名6~12位之间')],
        render_kw={'placeholder':'请输入密码','minlength':6,'maxlength':12})
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

    # 用户名的唯一性
    def validate_username(self,field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户不存在 请重新输入')

# 修改密码
class Update_password(FlaskForm):
    oldpassword = PasswordField('旧密码', validators=[DataRequired('密码不能为空!'),
            Length(min=6, max=12, message='用户名6~12位之间')],
            render_kw={'placeholder': '请输入密码', 'minlength': 6, 'maxlength': 12})
    newpassword = PasswordField('新密码', validators=[DataRequired('密码不能为空!'),
        Length(min=6, max=12, message='用户名6~12位之间')],
        render_kw={'placeholder': '请输入密码', 'minlength': 6, 'maxlength': 12})
    confirm = PasswordField('确认密码', validators=[DataRequired('确认密码不能为空!'),
        Length(min=6, max=12, message='用户名6~12位之间'),
        EqualTo('newpassword', message='密码和确认密码不一致')],
        render_kw={'placeholder': '请输入确认密码', 'minlength': 6, 'maxlength': 12})
    submit = SubmitField('修改提交')

# 修改邮箱
class Update_email(FlaskForm):
    email = StringField('激活邮箱', validators=[DataRequired('邮箱不能为空!'),
        Email('请输入正确的邮箱地址')],
        render_kw={'placeholder': '请输入有效的邮箱地址'})
    submit = SubmitField('修改提交')

    # 邮箱的唯一性
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在 请重新输入')


#文件上传表单类
class Update_icon(FlaskForm):
    icon = FileField('选择头像')
    submit = SubmitField('上传')


