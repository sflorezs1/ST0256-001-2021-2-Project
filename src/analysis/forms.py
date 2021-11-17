from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class NonLinearForm(FlaskForm):
    eq = StringField(label='Equation',validators=[DataRequired()])
    submit = SubmitField(label='Go!')