#!/usr/bin/env python3

import jinja2, os, sys, tempfile, shutil, re
from flask import Flask, flash, jsonify, redirect, render_template, request, session, g, Markup, url_for
from flaskext.mysql import MySQL
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from subprocess import Popen


app = Flask(__name__)


""" Constants """
ACCESS_RIGHTS = 0o755
OUT_DIR = 'appDock/tex/' # Where PDF is placed
UPLOAD_FOLDER = OUT_DIR + 'img/' # Where images are uploaded
ALLOWED_EXTENSIONS = {'png'} # Add image extensions
# Escaping tex syntax
LATEX_SUBS = (
    (re.compile(r"\\"), r"\\textbackslash"),
    (re.compile(r"([{}_#%&$])"), r"\\\1"),
    (re.compile(r"~"), r"\~{}"),
    (re.compile(r"\^"), r"\^{}"),
    (re.compile(r'"'), r"''"),
    (re.compile(r"\.\.\.+"), r"\\ldots"),
)
# Set jinja2 environment in latex syntax so that it doesn't conflict with .tex
PATH = os.path.join(os.path.dirname(__file__),'./tex')
TEMPLATELOADER = jinja2.FileSystemLoader(searchpath=PATH)
LATEX_JINJA_ENV = jinja2.Environment(
    block_start_string = '((*',
    block_end_string = '*))',
    variable_start_string = '(((',
    variable_end_string = ')))',
    comment_start_string = '((=',
    comment_end_string = '=))',
    loader = TEMPLATELOADER,
    autoescape = True
)


def escape_tex(value):
    """ Make sure tex syntax is escaped """
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval


LATEX_JINJA_ENV.filters['escape_tex'] = escape_tex
TEXTEMPLATE = LATEX_JINJA_ENV.get_template('template.tex')


""" Configure application """
app.config["SECRET_KEY"] = "helpfulhat@4dollarCREAM" # ONLY FOR LOCAL ENV
app.config["TEMPLATES_AUTO_RELOAD"] = True # Autoreload templates
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # Limit file size
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SESSION_FILE_DIR"] = tempfile.mkdtemp() # Session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#app.config['MYSQL_HOST'] = 'localhost' # Database
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'cv'


""" MySQL """
mysql = MySQL()
mysql.init_app(app)


""" Session """
Session(app)


def allowed_file(filename):
    """ Make sure uploaded files have the correct extension """
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#@app.teardown_appcontext
#def closeConnection(exception):
#    """ In order to close the DB connection """
#    if mysql is not None:
#        mysql.close()


#def queryDB(query, args=(), one=False):
#    """ Make queries to the DB within the app_context()
#    https://flask.palletsprojects.com/en/1.1.x/appcontext/
#    https://sentry.io/answers/working-outside-of-application-context/ """
#    cur = mysql.get_db().cursor()
#    cur.execute(query, args)
#    rv = cur.fetchall()
#    return (rv[0] if rv else None) if one else rv


#def updateDB(update, args=()):
#    """ insert, update or delete DB entries """
#    cur = mysql.get_db().cursor()
#    cur.execute(update, args)
#    mysql.get_db().commit()


@app.after_request
def after_request(response):
    """ Ensure responses aren't cached """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def writeTex(rendered_tex, out_dir):
    """ Render .tex and compile with latexmk """
    cur_dir = os.getcwd()
    os.chdir(out_dir)
    with open('rendered.tex', 'w') as outfile:
        outfile.write(rendered_tex)
    p = Popen(['latexmk', '-pdf', '-recorder', 'rendered.tex'])
    p.communicate()
    q = Popen(['latexmk', '-c', 'rendered.tex'])
    q.communicate()
    os.chdir(cur_dir)


def servePdf(pdf_path):
    """ Send file to user """


def deleteGenFiles(tex):
    """ Delete generated files """
    if (tex != 'default'):
        os.remove(UPLOAD_FOLDER + tex) # Uploaded image
    os.remove(OUT_DIR + 'render.tex') # Rendered TEX
    os.remove(OUT_DIR + 'rendered.pdf') # Rendered PDF

@app.route("/")
def index():
    """ Open index page and show current assignments """
    with app.app_context():
        return render_template("index.html")

@app.route("/addtocv", methods=["GET", "POST"])
def addtoCV():
    """ Add assignment to DB """
    with app.app_context():
        # Get form data
        data = request.form
        msg = {}
        msg['name'] = data['name']
        msg['role'] = data['role']
        msg['unit'] = data['unit']
        msg['unitdetail'] = data['unitdetail']
        msg['phone'] = data['phone']
        msg['email'] = data['email']
        msg['employmentdate'] = data['employmentdate']
        if 'img' in request.files:
            file = request.files['img']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename).replace("_","")
                portraitFilePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(portraitFilePath)
            if file.filename == '':
                filename = 'default.png'
                flash('Ingen bildfil vald, använder "default"')
        else:
            filename = 'default.png'
            flash('Ingen bildfil vald')
        if 'presentation' in data:
            msg['presentation'] = data['presentation']
        if 'edu-title' in data:
            msg['edu'] =  [{'title': i, 'time': j} for i, j in zip(request.form.getlist('edu-title'), request.form.getlist('edu-time'))]
        if 'emp-title' in data:
            msg['emp'] = [{'title': i, 'time': j} for i, j in zip(request.form.getlist('emp-title'), request.form.getlist('emp-time'))]
        if 'cou-title' in data:
            msg['cou'] = [{'title': i, 'time': j} for i, j in zip(request.form.getlist('cou-title'), request.form.getlist('cou-time'))]
        if 'ass-title' in data:
            msg['ass'] = [{'title': i, 'descr': j, 'time': k} for i,j,k in zip(request.form.getlist('ass-title'), request.form.getlist('ass-descr'), request.form.getlist('ass-time'))]

        cv = TEXTEMPLATE.render(msg = msg, portrait = 'img/' + filename)
        writeTex(cv, OUT_DIR)
        return redirect("/")


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
