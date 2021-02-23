#!/usr/bin/env python3

from flask import Flask, flash, jsonify, redirect, render_template, request, session, g, Markup, url_for
from flaskext.mysql import MySQL
from flask_session import Session
import jinja2
import os
import sys
import tempfile
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from subprocess import Popen
import shutil

# Configure application
app = Flask(__name__, template_folder="../www/templates/")

# Added to work in local environment [CHANGE]
app.config["SECRET_KEY"] = "helpfulhat@4dollarCREAM"
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# For File uploads
UPLOAD_FOLDER = '../www/tex/img/'
ALLOWED_EXTENSIONS = {'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#set up mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aA868097'
app.config['MYSQL_DB'] = 'cv'


mysql = MySQL()
mysql.init_app(app)


#@app.teardown_appcontext
#def closeConnection(exception):
#    """ In order to close the DB connection """
#    if mysql is not None:
#        mysql.close()


def queryDB(query, args=(), one=False):
    """ Make queries to the DB within the app_context()
    https://flask.palletsprojects.com/en/1.1.x/appcontext/
    https://sentry.io/answers/working-outside-of-application-context/ """
    cur = mysql.get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def updateDB(update, args=()):
    """ insert, update or delete DB entries """
    cur = mysql.get_db().cursor()
    cur.execute(update, args)
    mysql.get_db().commit()


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = tempfile.mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ref: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
#DATABASE = 'db/cv.db'


# Define filter for jinja2
import re

LATEX_SUBS = (
    (re.compile(r"\\"), r"\\textbackslash"),
    (re.compile(r"([{}_#%&$])"), r"\\\1"),
    (re.compile(r"~"), r"\~{}"),
    (re.compile(r"\^"), r"\^{}"),
    (re.compile(r'"'), r"''"),
    (re.compile(r"\.\.\.+"), r"\\ldots"),
)

def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

# Set jinja2 environment in latex syntax so that it doesn't conflict with .tex
path = os.path.join(os.path.dirname(__file__),'./tex')
templateLoader = jinja2.FileSystemLoader(searchpath=path)
latex_jinja_env = jinja2.Environment(
    block_start_string = '((*',
    block_end_string = '*))',
    variable_start_string = '(((',
    variable_end_string = ')))',
    comment_start_string = '((=',
    comment_end_string = '=))',
    loader = templateLoader,
    autoescape = True
)

latex_jinja_env.filters['escape_tex'] = escape_tex
texTemplate = latex_jinja_env.get_template('template.tex')

def writeTex(rendered_tex, out_pdf_path):
#    tmp_dir = url_for('static', filename = 'tex/')
#    tmp_dir = 'appDock/www/tex/'
    tmp_dir = tempfile.mkdtemp()
    in_tmp_path = os.path.join(tmp_dir, 'rendered.tex')
    with open(in_tmp_path, 'w') as outfile:
        outfile.write(rendered_tex)
    p = Popen(['pdflatex', in_tmp_path, '-job-name', 'out', '-output-directory', tmp_dir])
    out_tmp_path = os.path.join(tmp_dir, 'out.pdf')
    print(out_tmp_path, file=sys.stderr)
    print(out_tmp_path, file=sys.stdout)
    print(out_pdf_path, file=sys.stderr)
    print(out_pdf_path, file=sys.stdout)
    p.communicate()
    shutil.copy(out_tmp_path, out_pdf_path)
    shutil.rmtree(tmp_dir)


@app.route("/")
def index():
    """ Open index page and show current assignments """
    with app.app_context():
        return render_template("index.html")

@app.route("/addtocv", methods=["POST"])
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
        portraitFilePath = ''
        if 'file' in request.files:
            file = request.files['img']
            if file.filename == '':
                flash('Ingen fil vald')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                portraitFilePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(portraitFilePath)
        if 'presentation' in data:
            msg['presentation'] = data['presentation']
        if 'edu-title' in data:
            msg['edu'] =  [{'title': i, 'time': j} for i, j in zip(request.form.getlist('edu-title'), request.form.getlist('edu-time'))]
        if 'emp-title' in data:
            msg['employment'] = [{'title': i, 'time': j} for i, j in zip(request.form.getlist('emp-title'), request.form.getlist('emp-time'))]
        if 'cou-title' in data:
            msg['courses'] = [{'title': i, 'time': j} for i, j in zip(request.form.getlist('cou-title'), request.form.getlist('cou-time'))]
        if 'ass-title' in data:
            msg['assignments'] = [{'title': i, 'descr': j, 'time': k} for i,j,k in zip(request.form.getlist('ass-title'), request.form.getlist('ass-descr'), request.form.getlist('ass-time'))]
        

#        updateDB("""INSERT INTO 
#                (name,
#                description,
#                startdate,
#                finishdate,
#                status,
#                notes,
#                client_id,
#                company_id,
#                consultant_id)
#                VALUES (?,?,?,?,?,?,?,?,?)""",
#                [
#                    name,
#                    description,
#                    start,
#                    finish,
#                    status,
#                    note,
#                    clientID,
#                    companyID,
#                    consultantID])
#        message = Markup("Uppdraget / projektet <b>%s</b> tillagd"
#                % (name))
#        flash(message, "alert-success")
        tmp_dir = 'appDock/www/tex/img/'
#        tmp_dir = url_for('static', filename = '/templates/tex/img/')
        staticImg =  [os.path.join(tmp_dir, 'banner.png'),  \
                os.path.join(tmp_dir, 'logo.png')]
        cv = texTemplate.render(msg = msg, portrait = portraitFilePath, staticImg = staticImg)
#        print(cv, file=sys.stderr)
#        print(cv, file=sys.stdout)
        writeTex(cv, os.path.join('appDock/www/pdf/', 'rendered.pdf'))
        return redirect("/")


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)

