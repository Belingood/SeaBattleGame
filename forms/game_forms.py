from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired


# The form of index page
class StartForm(FlaskForm):
    name = StringField('Name / Имя: ', validators=[DataRequired()])
    language = SelectField(u'Language / Язык: ',
                           choices=[('rus', 'Русский'),
                                    ('eng', 'English')]
                           )
    rand = SelectField('Ship placement method / Способ расстановки кораблей: ',
                       choices=[('auto', 'Auto / Автоматическая'),
                                ('manual', 'Manual / Ручная')]
                       )


# The form of review
class ReviewForm(FlaskForm):
    review = TextAreaField('Text of review', render_kw={"rows": 10, "cols": 50}, validators=[DataRequired()])
