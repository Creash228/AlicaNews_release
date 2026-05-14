from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    is_private = BooleanField('Личная новость (видны только вам)')
    photo = FileField('Изображение', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Разрешены только картинки!')
    ])
    submit = SubmitField('Сохранить')