import traceback
from __init__ import app
from flask import render_template
from forms import *
from util.utilities import plot_png, domain, parse_matrix, parse_vector
from methods.one_variable_eqs import *
from methods.linear_equations import *
from methods.interpolation import *
from sympy import *

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
        try:
            eq = lambda a: lambdify(x_sym, sympify(form.eq.data))(a)
            print(form.eq.data)
            x0 = form.x0.data
            h = form.h.data
            n_max = form.n_max.data
            result = incremental_searches(eq, x0, h, n_max)
            img = plot_png(eq, (x0 - 10, x0 + h * n_max), [result[0], result[1]])
            data['img'] = img
            data['x0'] = result[0]
            data['xf'] = result[1]
            data['iter'] = result[2]
        except Exception as e:
            print(traceback.format_exc())
            data['fail'] = str(e)
        
    return render_template('incrementalsearches.html', title="Incremental Searches", color_class="nonlinear", form=form, result=data)

@app.route('/bisection', methods=['GET', 'POST'])
def bisect():
    form = BisectionForm()
    data = {}
    if form.validate_on_submit():
        try:
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
        except Exception as e:
            data['fail'] = str(e)
    return render_template('bisection.html', title="Bisection", color_class="nonlinear",form=form, result=data)

@app.route('/fakerule', methods=['GET', 'POST'])
def frule():
    data = {}
    form = FakeRuleForm()
    if form.validate_on_submit():
        try:
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
        except Exception as e:
            data['fail'] = str(e)
    return render_template('fakerule.html', title="Fake Rule", color_class="nonlinear",form=form,result=data)

@app.route('/fixedpoint', methods=['GET', 'POST'])
def fpoint():
    data = {}
    form = FixedPointForm()
    if form.validate_on_submit():
        try:
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
        except Exception as e:
            data['fail'] = str(e)
    return render_template('fixedpoint.html', title="Fixed Point", color_class="nonlinear",form=form,result=data)

@app.route('/newton', methods=['GET', 'POST'])
def newt():
    data = {}
    form = NewtonForm()
    if form.validate_on_submit():
        try:
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
        except Exception as e:
            data['fail'] = str(e)
    return render_template('newton.html', title="Newton Method", color_class="nonlinear",form=form,result=data)
    
@app.route('/secant', methods=['GET', 'POST'])
def sec():
    data = {}
    form = SecantForm()
    if form.validate_on_submit():
        try:
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
        except Exception as e:
            data['fail'] = str(e)
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
def r_gauss():
    data = {}
    form = GaussForm()
    if form.validate_on_submit():
        try:
            a = parse_matrix(form.a.data)
            b = parse_matrix(form.b.data)
            print(a)
            result = gauss(a,b)
            print(result)
            data['x'] = result
        except Exception as e:
            data['fail'] = str(e)
        
    return render_template('gauss.html', title="Gauss Elimination", color_class="linear",form=form,result=data)

@app.route('/gauss_tot', methods=['GET', 'POST'])
def r_gauss_tot():
    data = {}
    form = GaussTotForm()
    if form.validate_on_submit():
        try:
            a = parse_matrix(form.a.data)
            b = parse_matrix(form.b.data)
            result = gauss_tot(a,b)
            data['x'] = result
        except Exception as e:
            data['fail'] = str(e)
    return render_template('gauss_tot.html', title="Gauss Elimination (Total Pivoting)", color_class="linear",form=form,result=data)

@app.route('/gauss_par', methods=['GET', 'POST'])
def r_gauss_par():
    data = {}
    form = GaussParForm()
    if form.validate_on_submit():
        try:
            a = parse_matrix(form.a.data)
            b = parse_matrix(form.b.data)
            result = gauss_par(a,b)
            data['x'] = result
        except Exception as e:
            data['fail'] = str(e)
    return render_template('gauss_par.html', title="Gauss Elimination (Partial Pivoting)", color_class="linear",form=form,result=data)

@app.route('/lu', methods=['GET', 'POST'])
def r_lu():
    data = {}
    form = LUForm()
    if form.validate_on_submit():
        try:
            a = parse_matrix(form.a.data)
            b = parse_matrix(form.b.data)
            result = lu(a,b)
            data['x'] = result
        except Exception as e:
            data['fail'] = str(e)
    return render_template('lu.html', title="LU Factorization", color_class="linear",form=form,result=data)

@app.route('/lu_pp', methods=['GET', 'POST'])
def r_lu_pp():
    data = {}
    form = LUPPForm()
    if form.validate_on_submit():
        try:
            a = parse_matrix(form.a.data)
            b = parse_matrix(form.b.data)
            result = lu_pp(a,b)
            data['x'] = result
        except Exception as e:
            data['fail'] = str(e)
    return render_template('lu_pp.html', title="LU Factorization (Partial Pivoting)", color_class="linear",form=form,result=data)

@app.route('/jacobi', methods=['GET', 'POST'])
def r_jacobi():
    data = {}
    form = JacobiForm()
    if form.validate_on_submit():
        try:
            a = parse_matrix(form.a.data)
            b = parse_matrix(form.b.data)
            x0 = form.x0.data
            tol = form.tol.data
            nmax = form.n_max.data
            print(a, b, x0, tol, nmax)
            result = gjacobi(a,b,x0,tol,nmax)
            data['x'] = result[0]
            data['iter'] = result[1]
            data['error'] = result[2]
        except Exception as e:
            data['fail'] = str(e)
    return render_template('jacobi.html', title="Jacobi Method", color_class="linear",form=form,result=data)

@app.route('/gseidel', methods=['GET', 'POST'])
def r_gseidel():
    data = {}
    form = GSeidelForm()
    if form.validate_on_submit():
        try:
            a = parse_matrix(form.a.data)
            b = parse_matrix(form.b.data)
            x0 = form.x0.data
            tol = form.tol.data
            nmax = form.n_max.data
            result = gseidel(a,b,x0,tol,nmax)
            data['x'] = result[0]
            data['iter'] = result[1]
            data['error'] = result[2]
        except Exception as e:
            data['fail'] = str(e)
    return render_template('gseidel.html', title="Gauss-Seidel Method", color_class="linear",form=form,result=data)

@app.route('/sor', methods=['GET', 'POST'])
def r_sor():
    data = {}
    form = SORForm()
    if form.validate_on_submit():
        try:
            a = parse_matrix(form.a.data)
            b = parse_matrix(form.b.data)
            x0 = form.x0.data
            w= form.w.data
            tol = form.tol.data
            nmax = form.n_max.data
            result = sor(a,b,x0,w,tol,nmax)
            data['x'] = result[0]
            data['iter'] = result[1]
            data['error'] = result[2]
        except Exception as e:
            data['fail'] = str(e)
    return render_template('sor.html', title="Successive Over-Relaxation", color_class="linear",form=form,result=data)

#Interpolation Methods
@app.route('/interpol/<method>', methods=['GET', 'POST'])
def r_interpol(method):
    data = {}
    form = InterpolForm()
    if form.validate_on_submit():
        try:
            x = parse_vector(form.x.data)
            y = parse_vector(form.y.data)
            val = form.val.data
            result = interpolate(method, x, y)
            data['p'] = result[0](val)
            data['val'] = val
            data['expr'] = latex(result[1])
            points = list(zip(x,y))
            points.append((val, data['p']))
            data['img'] = plot_png(result[0], (min(val, min(x)) - 10, max(val, max(x)) + 10), points)
        except Exception as e:
            import traceback
            traceback.print_exc()
            data['fail'] = str(e)
    return render_template('interpolate.html', title=method, color_class="interpol",form=form,result=data)

@app.route('/lagrange', methods=['GET', 'POST'])
def lagrange():
    data = {}
    form = InterpolForm()
    if form.validate_on_submit():
        try:
            x = parse_vector(form.x.data)
            y = parse_vector(form.y.data)
            val = form.val.data
            result = divided_differences(x, y)
            data['p'] = result[0](val)
            data['val'] = val
            data['expr'] = latex(result[1])
            points = list(zip(x,y))
            points.append((val, data['p']))
            data['img'] = plot_png(result[0], (min(val, min(x)) - 10, max(val, max(x)) + 10), points)
        except Exception as e:
            import traceback
            traceback.print_exc()
            data['fail'] = str(e)
    return render_template('interpolate.html', title="Lagrange Polynomial", color_class="interpol",form=form,result=data)

@app.route('/linear_spline', methods=['GET', 'POST'])
def linear_spline():
    data = {}
    form = InterpolForm()
    if form.validate_on_submit():
        try:
            x = parse_vector(form.x.data)
            y = parse_vector(form.y.data)
            val = form.val.data
            result = divided_differences(x, y)
            data['p'] = result[0](val)
            data['val'] = val
            data['expr'] = latex(result[1])
            points = list(zip(x,y))
            points.append((val, data['p']))
            data['img'] = plot_png(result[0], (min(val, min(x)) - 10, max(val, max(x)) + 10), points)
        except Exception as e:
            import traceback
            traceback.print_exc()
            data['fail'] = str(e)
    return render_template('interpolate.html', title="Linear Spline", color_class="interpol",form=form,result=data)

@app.route('/quadratic_spline', methods=['GET', 'POST'])
def quadratic_spline():
    data = {}
    form = InterpolForm()
    if form.validate_on_submit():
        try:
            x = parse_vector(form.x.data)
            y = parse_vector(form.y.data)
            val = form.val.data
            result = divided_differences(x, y)
            data['p'] = result[0](val)
            data['val'] = val
            data['expr'] = latex(result[1])
            points = list(zip(x,y))
            points.append((val, data['p']))
            data['img'] = plot_png(result[0], (min(val, min(x)) - 10, max(val, max(x)) + 10), points)
        except Exception as e:
            import traceback
            traceback.print_exc()
            data['fail'] = str(e)
    return render_template('interpolate.html', title="Quadratic Spline", color_class="interpol",form=form,result=data)

@app.route('/vandermonde', methods=['GET', 'POST'])
def vandermonde():
    data = {}
    form = InterpolForm()
    if form.validate_on_submit():
        try:
            x = parse_vector(form.x.data)
            y = parse_vector(form.y.data)
            val = form.val.data
            result = divided_differences(x, y)
            data['p'] = result[0](val)
            data['val'] = val
            data['expr'] = latex(result[1])
            points = list(zip(x,y))
            points.append((val, data['p']))
            data['img'] = plot_png(result[0], (min(val, min(x)) - 10, max(val, max(x)) + 10), points)
        except Exception as e:
            import traceback
            traceback.print_exc()
            data['fail'] = str(e)
    return render_template('interpolate.html', title="Vandermonde", color_class="interpol",form=form,result=data)
