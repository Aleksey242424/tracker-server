from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email


class RegisterForm(FlaskForm):
    name = StringField(
        label="name",
        validators=[DataRequired(),Length(3,40)],
        render_kw={
            "placeholder":"имя",
            "id":"name",
            "class":"name"
        }
    )
    password = PasswordField(
        label="password",
        validators=[DataRequired(),Length(6,20)],
        render_kw={
            "placeholder":"пароль",
            "id":"password",
            "class":"password"
            }
    )
    confirm_password = PasswordField(
        label="confirm_password",
        validators=[EqualTo('password')],
        render_kw={
            "placeholder":"повторить пароль",
            "id":"password",
            "class":"password"
            }
    )
    email = EmailField(
        label="email",
        validators=[DataRequired(),Length(6,90),Email()],
        render_kw={
            "placeholder":"email",
            "id":"email",
            "class":"email"
            }
    )

    is_owner = BooleanField(
        label="is_owner",
        render_kw={
            "id":"is_owner",
            "class":"is_owner"
        }
    )

    sign_up = SubmitField(label="регистрация")


class LoginForm(FlaskForm):
    name = StringField(
        label="name",
        validators=[DataRequired(),Length(3,40)],
        render_kw={
            "placeholder":"имя",
            "id":"name",
            "class":"name"
        }
    )
    password = PasswordField(
        label="password",
        validators=[DataRequired(),Length(6,20)],
        render_kw={
            "placeholder":"пароль",
            "id":"password",
            "class":"password"
            }
    )
    sign_in = SubmitField(label="Войти")