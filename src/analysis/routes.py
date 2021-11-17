from analysis import app
from flask import render_template, url_for, redirect
from analysis.forms import NonLinearForm

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html',title="Analysis")

@app.route('/methods')
def methods():
    return render_template('methods.html',title="Choose a Method")

@app.route('/about')
def about():
    return render_template('about.html',title="About")

#Method Menus

@app.route('/interpolation')
def interpolation():
    return render_template('interpolation.html',title="Interpolation")

@app.route('/linear')
def linear():
    return render_template('linear.html',title="Linear Equations")

@app.route('/nonlinear',methods=['POST','GET'])
def nonlinear():
    form=NonLinearForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    else:
        print('Not Working')
        return render_template('nonlinear.html',title="Non-Linear Equations",form=form)