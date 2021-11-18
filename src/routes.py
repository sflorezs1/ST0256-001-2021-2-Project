from flask.json import dump
from sympy import sympify, lambdify
from sympy.core.symbol import symbols
from sympy.utilities.lambdify import lambdify
from __init__ import app
from flask import render_template, url_for, redirect
from forms import *
from util.utilities import plot_png, domain
from methods.one_variable_eqs import *

x_sym = symbols('x')


@app.route('/')
@app.route('/home', methods=['GET'])
def index():
    return render_template('home.html',title="Analysis", color_class="main-menu")

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title="About", color_class="main-menu")

#Method Menus

@app.route('/interpolation', methods=['GET'])
def interpolation():
    return render_template('interpolation.html', title="Interpolation", color_class="interpol")

@app.route('/linear', methods=['GET'])
def linear():
    return render_template('linear.html', title="Linear Equations", color_class="linear")

@app.route('/nonlinear', methods=['GET'])
def nonlinear():
    return render_template('nonlinear.html', title="Non-Linear Equations", color_class="nonlinear")

#Non-Linear Methods

@app.route('/incrementalsearches', methods=['GET', 'POST'])
def incsearch():
    form = IncrementalSearchesForm()
    data = {}
    if form.validate_on_submit():
        eq = (lambda a: lambdify(x_sym, form.eq.data)(a))
        x0 = form.x0.data
        h = form.h.data
        n_max = form.n_max.data
        result = incremental_searches(eq, x0, h, n_max)
        img = plot_png(eq, (x0 - 10, x0 + h * n_max), [result[0], result[1]])
        data['img'] = img
        data['x0'] = result[0]
        data['xf'] = result[1]
        data['iter'] = result[2]
        
    return render_template('incrementalsearches.html', title="Incremental Searches", color_class="nonlinear", form=form, result=data)

@app.route('/bisection', methods=['GET', 'POST'])
def bisect():
    form = BisectionForm()
    data = {}
    if form.validate_on_submit():
        eq = (lambda a: lambdify(x_sym, form.eq.data)(a))
        a = form.a.data
        b = form.b.data
        tol = form.tol.data
        n_max = form.n_max.data
        result = bisection(eq, a, b, tol, n_max)
        # plot_png: function, interval (a, b), points to draw
        img = plot_png(eq, (a - 10, b + 10), [result[0]])
        data['img'] = img
        data['x'] = result[0]
        data['iter'] = result[1]
        data['error'] = result[2]
    return render_template('bisection.html', title="Bisection", color_class="nonlinear",form=form, result=data)

@app.route('/fakerule', methods=['GET', 'POST'])
def frule():
    data = {}
    form = FakeRuleForm()
    if form.validate_on_submit():
        eq = (lambda a: lambdify(x_sym, form.eq.data)(a))
        a = form.a.data
        b = form.b.data
        tol = form.tol.data
        n_max = form.n_max.data
        result = fake_rule(eq, a, b, tol, n_max)
        # plot_png: function, interval (a, b), points to draw
        img = plot_png(eq, (a - 10, b + 10), [result[0]])
        data['img'] = img
        data['x'] = result[0]
        data['iter'] = result[1]
        data['error'] = result[2]
    return render_template('fakerule.html', title="Fake Rule", color_class="nonlinear",form=form,result=data)

@app.route('/fixedpoint', methods=['GET', 'POST'])
def fpoint():
    data = {}
    form = FixedPointForm()
    if form.validate_on_submit():
        eq = (lambda a: lambdify(x_sym, form.eq.data)(a))
        x0 = form.x0.data
        tol = form.tol.data
        n_max = form.n_max.data
        result = fixed_point(eq, x0, tol, n_max)
        # plot_png: function, interval (a, b), points to draw
        img = plot_png(eq, (x0 - 10, result[0] + 10), [result[0]])
        data['img'] = img
        data['x'] = result[0]
        data['iter'] = result[1]
        data['error'] = result[2]
    return render_template('fixedpoint.html', title="Fixed Point", color_class="nonlinear",form=form,result=data)

@app.route('/newton', methods=['GET', 'POST'])
def newt():
    data = {}
    form = NewtonForm()
    if form.validate_on_submit():
        eq = (lambda a: lambdify(x_sym, form.eq.data)(a))
        deq = (lambda a: lambdify(x_sym, form.deq.data)(a))
        x0 = form.x0.data
        tol = form.tol.data
        n_max = form.n_max.data
        result = newton(eq, deq, x0, tol, n_max)
        # plot_png: function, interval (a, b), points to draw
        img = plot_png(eq, domain(x0 - 10, result[0] + 10), [result[0]])
        data['img'] = img
        data['x'] = result[0]
        data['iter'] = result[1]
        data['error'] = result[2]
    return render_template('newton.html', title="Newton Method", color_class="nonlinear",form=form,result=data)
    
@app.route('/secant', methods=['GET', 'POST'])
def sec():
    data = {}
    form = SecantForm()
    if form.validate_on_submit():
        eq = (lambda a: lambdify(x_sym, form.eq.data)(a))
        x0 = form.x0.data
        x1 = form.x1.data
        tol = form.tol.data
        n_max = form.n_max.data
        result = secant(eq, x0, x1, tol, n_max)
        # plot_png: function, interval (a, b), points to draw
        img = plot_png(eq, (x0 - 10, x1 + 10), [result[0]])
        data['img'] = img
        data['x'] = result[0]
        data['iter'] = result[1]
        data['error'] = result[2]
    return render_template('secant.html', title="Secant Method", color_class="nonlinear",form=form,result=data)

@app.route('/mroots', methods=['GET', 'POST'])
def mroots():
    data = {}
    form = MultipleRootsForm()
    if form.validate_on_submit():
        eq = (lambda a: lambdify(x_sym, form.eq.data)(a))
        deq = (lambda a: lambdify(x_sym, form.deq.data)(a))
        d2eq = (lambda a: lambdify(x_sym, form.d2eq.data)(a))
        x0 = form.x0.data
        tol = form.tol.data
        n_max = form.n_max.data
        try:
            result = multiple_roots(eq, deq, d2eq, x0, tol, n_max)
            # plot_png: function, interval (a, b), points to draw
            img = plot_png(eq, domain(x0 - 10, result[0] + 10), [result[0]])
            data['img'] = img
            data['x'] = result[0]
            data['iter'] = result[1]
            data['error'] = result[2]
        except ZeroDivisionError:
            data['fail'] = 'ZeroDivisionError: Check your arguments'
    return render_template('mroots.html', title="Multiple Roots", color_class="nonlinear",form=form,result=data)

#Linear Methods

@app.route('/gauss', methods=['GET', 'POST'])
def gauss():
    data = {}
    form = GaussForm()
    return render_template('gauss.html', title="Gauss Elimination", color_class="linear",form=form,result=data)

@app.route('/gauss_tot', methods=['GET', 'POST'])
def gauss_tot():
    data = {}
    form = GaussTotForm()
    return render_template('gauss_tot.html', title="Gauss Elimination (Total Pivoting)", color_class="linear",form=form,result=data)

@app.route('/gauss_par', methods=['GET', 'POST'])
def gauss_par():
    data = {}
    form = GaussParForm()
    return render_template('gauss_par.html', title="Gauss Elimination (Partial Pivoting)", color_class="linear",form=form,result=data)

@app.route('/lu', methods=['GET', 'POST'])
def lu():
    data = {}
    form = LUForm()
    return render_template('lu.html', title="LU Factorization", color_class="linear",form=form,result=data)

@app.route('/lu_pp', methods=['GET', 'POST'])
def lu_pp():
    data = {}
    form = LUPPForm()
    return render_template('lu_pp.html', title="LU Factorization (Partial Pivoting)", color_class="linear",form=form,result=data)

@app.route('/jacobi', methods=['GET', 'POST'])
def jacobi():
    data = {}
    form = JacobiForm()
    return render_template('jacobi.html', title="Jacobi Method", color_class="linear",form=form,result=data)

@app.route('/gseidel', methods=['GET', 'POST'])
def gseidel():
    data = {}
    form = GSeidelForm()
    return render_template('gseidel.html', title="Gauss-Seidel Method", color_class="linear",form=form,result=data)

@app.route('/sor', methods=['GET', 'POST'])
def sor():
    data = {}
    form = SORForm()
    return render_template('sor.html', title="Successive Over-Relaxation", color_class="linear",form=form,result=data)

#Interpolation Methods

@app.route('/div_dif', methods=['GET', 'POST'])
def div_dif():
    data = {}
    form = DivDifForm()
    return render_template('divided_differences.html', title="Divided Differences", color_class="interpol",form=form,result=data)

@app.route('/lagrange', methods=['GET', 'POST'])
def lagrange():
    data = {}
    form = LagrangeForm()
    return render_template('lagrange.html', title="Lagrange Polynomial", color_class="interpol",form=form,result=data)

@app.route('/linear_spline', methods=['GET', 'POST'])
def linear_spline():
    data = {}
    form = LinearSplineForm()
    return render_template('linear_spline.html', title="Linear Spline", color_class="interpol",form=form,result=data)

@app.route('/quadratic_spline', methods=['GET', 'POST'])
def quadratic_spline():
    data = {}
    form = QuadraticSplineForm()
    return render_template('quadratic_spline.html', title="Quadratic Spline", color_class="interpol",form=form,result=data)

@app.route('/vandermonde', methods=['GET', 'POST'])
def vandermonde():
    data = {}
    form = VandermondeForm()
    return render_template('vandermonde.html', title="Quadratic Spline", color_class="interpol",form=form,result=data)
