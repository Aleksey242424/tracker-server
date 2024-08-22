from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,FileField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length



class ProfileWorker(FlaskForm):
    name = StringField(
        label="name",
        validators=[DataRequired(),Length(3,40)],
        render_kw={
            "placeholder":"name",
            "id":"name",
            "class":"name"
            }
    )
    update = SubmitField(label="update")


class CreateProject(FlaskForm):
    title = StringField(
        label="title",
        validators=[DataRequired(),Length(1,40)],
        render_kw={
            "placeholder":"title",
            "id":"title",
            "class":"title"
        }
    )

    description = TextAreaField(
        label="description",
        validators=[Length(0,800)]
    )

    create = SubmitField(
        label="create"
    )