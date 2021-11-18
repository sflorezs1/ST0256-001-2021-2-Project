from typing import Callable
from sympy.core.symbol import symbols
from sympy.core.sympify import SympifyError
from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,IntegerField,SubmitField,DecimalField
from wtforms.validators import InputRequired, ValidationError
from sympy import sympify, lambdify


def _validate_eq(form, field):
        try:
            sympify(field.data, convert_xor=True, evaluate=False)
        except SympifyError as se:
            print(se)
            raise ValidationError

# Non-Linear Methods

class IncrementalSearchesForm(FlaskForm):
    eq = StringField(label='Equation', validators=[InputRequired(), _validate_eq])
    x0 = FloatField(label='Initial Value (X0)', validators=[InputRequired()])
    h = FloatField(label='Increments', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class BisectionForm(FlaskForm):
    eq = StringField(label='Equation', validators=[InputRequired(), _validate_eq])
    a = FloatField(label='A Value', validators=[InputRequired()])
    b = FloatField(label='B Value', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class FakeRuleForm(FlaskForm):
    eq = StringField(label='Equation', validators=[InputRequired(), _validate_eq])
    a = FloatField(label='A Value', validators=[InputRequired()])
    b = FloatField(label='B Value', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class FixedPointForm(FlaskForm):
    eq = StringField(label='Equation - G(x)', validators=[InputRequired(), _validate_eq])
    x0 = FloatField(label='Initial Value (X0)', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class NewtonForm(FlaskForm):
    eq = StringField(label='Equation', validators=[InputRequired(), _validate_eq])
    deq = StringField(label='Derivative of Equation', validators=[InputRequired(), _validate_eq])
    x0 = FloatField(label='Initial Value (X0)', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class SecantForm(FlaskForm):
    eq = StringField(label='Equation', validators=[InputRequired(), _validate_eq])
    x0 = FloatField(label='Initial Value (X0)', validators=[InputRequired()])
    x1 = FloatField(label='Initial Value (X1)', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class MultipleRootsForm(FlaskForm):
    eq = StringField(label='Equation', validators=[InputRequired(), _validate_eq])
    deq = StringField(label='Derivative of Equation', validators=[InputRequired(), _validate_eq])
    d2eq = StringField(label='Second Derivative of Equation', validators=[InputRequired(), _validate_eq])
    x0 = FloatField(label='Initial Value (X0)', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

# Linear Methods

class GaussForm(FlaskForm):
    a = StringField(label='Matrix A', validators=[InputRequired()])
    b = StringField(label='Vector B', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class GaussTotForm(FlaskForm):
    a = StringField(label='Matrix A', validators=[InputRequired()])
    b = StringField(label='Vector B', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class GaussParForm(FlaskForm):
    a = StringField(label='Matrix A', validators=[InputRequired()])
    b = StringField(label='Vector B', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class LUForm(FlaskForm):
    a = StringField(label='Matrix A', validators=[InputRequired()])
    b = StringField(label='Vector B', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class LUPPForm(FlaskForm):
    a = StringField(label='Matrix A', validators=[InputRequired()])
    b = StringField(label='Vector B', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class JacobiForm(FlaskForm):
    a = StringField(label='Matrix A', validators=[InputRequired()])
    b = StringField(label='Vector B', validators=[InputRequired()])
    x0 = FloatField(label='Initial Value (X0)', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class GSeidelForm(FlaskForm):
    a = StringField(label='Matrix A', validators=[InputRequired()])
    b = StringField(label='Vector B', validators=[InputRequired()])
    x0 = FloatField(label='Initial Value (X0)', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class SORForm(FlaskForm):
    a = StringField(label='Matrix A', validators=[InputRequired()])
    b = StringField(label='Vector B', validators=[InputRequired()])
    x0 = FloatField(label='Initial Value (X0)', validators=[InputRequired()])
    w = FloatField(label='W', validators=[InputRequired()])
    tol = FloatField(label='Tolerance', validators=[InputRequired()])
    n_max = IntegerField(label='Max number of iterations', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

#Interpolation

class VandermondeForm(FlaskForm):
    x = StringField(label='Vector X', validators=[InputRequired()])
    y = StringField(label='Vector Y', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class DivDifForm(FlaskForm):
    x = StringField(label='Vector X', validators=[InputRequired()])
    y = StringField(label='Vector Y', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class LagrangeForm(FlaskForm):
    x = StringField(label='Vector X', validators=[InputRequired()])
    y = StringField(label='Vector Y', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class LinearSplineForm(FlaskForm):
    x = StringField(label='Vector X', validators=[InputRequired()])
    y = StringField(label='Vector Y', validators=[InputRequired()])
    submit = SubmitField(label='Go!')

class QuadraticSplineForm(FlaskForm):
    x = StringField(label='Vector X', validators=[InputRequired()])
    y = StringField(label='Vector Y', validators=[InputRequired()])
    submit = SubmitField(label='Go!')