from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length,Email



class Profile(FlaskForm):
    name = StringField(
        label="name",
        validators=[DataRequired(),Length(3,40)],
        render_kw={
            "placeholder":"name",
            "id":"name",
            "class":"name"
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

    update = SubmitField(label="сохранить")


class CreateProject(FlaskForm):
    title = StringField(
        label="title",
        validators=[DataRequired(),Length(1,40)],
        render_kw={
            "placeholder":"название",
            "id":"title",
            "class":"title"
        }
    )

    description = TextAreaField(
        label="description",
        validators=[],
        render_kw={
            "placeholder":"описание",
            "id":"description",
            "class":"description"
        }
    )

    create = SubmitField(
        label="Добавить проект"
    )