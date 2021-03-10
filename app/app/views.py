from app import app
from flask import render_template, request, redirect, flash, url_for, Markup, g, send_from_directory, abort, Response
from app.helpers import allowed_file, writeTex, deleteImgUpload, deletePdf
from werkzeug.utils import secure_filename
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from operator import itemgetter

import os, re, jinja2, sys


# Set jinja2 environment in latex syntax so that it doesn't conflict with .tex
PATH = os.path.join(os.path.dirname(__file__),'./templates/tex')
TEMPLATELOADER = jinja2.FileSystemLoader(searchpath=PATH)
LATEX_JINJA_ENV = jinja2.Environment(
    block_start_string = '((*',
    block_end_string = '*))',
    variable_start_string = '(((',
    variable_end_string = ')))',
    comment_start_string = '((=',
    comment_end_string = '=))',
    loader = TEMPLATELOADER,
    autoescape = False
)


@app.route("/")
def index():
    """ Open index page and show current assignments """
    with app.app_context():
        return render_template("public/index.html")


LATEX_SUBS = (
    (re.compile(r"\\"), r"\\textbackslash"),
    (re.compile(r"([{}_#%&$])"), r"\\\1"),
    (re.compile(r"~"), r"\~{}"),
    (re.compile(r"\^"), r"\^{}"),
    (re.compile(r'"'), r"''"),
    (re.compile(r"\.\.\.+"), r"\\ldots"),
)


def escape_tex(value):
    """ Make sure tex syntax is escaped """
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval


LATEX_JINJA_ENV.filters['escape_tex'] = escape_tex
TEXTEMPLATE = LATEX_JINJA_ENV.get_template('template.tex')


@app.route("/createpdf", methods=["POST"])
def createpdf():
    """ Add assignment to DB """
    with app.app_context():
        # Get form data
        if request.form:
            data = request.form
        else:
            return 'no form'
        msg = {}
        msg['name'] = data['name']
        msg['role'] = data['role']
        msg['unit'] = data['unit']
        msg['unitdetail'] = data['unitdetail']
        msg['phone'] = data['phone']
        msg['email'] = data['email']
        msg['employmentdate'] = data['employmentdate']
        filename = 'default.png'
        if 'img' in request.files:
            file = request.files['img']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename).replace("_","")
                portraitFilePath = os.path.join(app.config['IMAGE_UPLOADS'], filename)
                file.save(portraitFilePath)
            else:
                flash('Ingen bildfil vald, använder "default"')
        else:
            flash('Ingen bildfil vald, använder "default"')
        if 'presentation' in data:
            msg['presentation'] = data['presentation']
        if 'edu-title' in data:
            msg['edu'] =  [{'title': i, 'time': j} for i, j in zip(request.form.getlist('edu-title'), request.form.getlist('edu-time'))]
            msg['edu'].sort(key = itemgetter('title'))
            msg['edu'].sort(key = itemgetter('time'), reverse=True)
        if 'emp-title' in data:
            msg['emp'] = [{'title': i, 'time': j} for i, j in zip(request.form.getlist('emp-title'), request.form.getlist('emp-time'))]
            msg['emp'].sort(key = itemgetter('title'))
            msg['emp'].sort(key = itemgetter('time'), reverse=True)
        if 'cou-title' in data:
            msg['cou'] = [{'title': i, 'time': j} for i, j in zip(request.form.getlist('cou-title'), request.form.getlist('cou-time'))]
            msg['cou'].sort(key = itemgetter('title'))
            msg['cou'].sort(key = itemgetter('time'), reverse=True)
        if 'ass-title' in data:
            msg['ass'] = [{'title': i, 'company': j, 'role': k, 'descr': l, 'time': m} for i,j,k,l,m in zip(request.form.getlist('ass-title'), request.form.getlist('ass-company'), request.form.getlist('ass-role'), request.form.getlist('ass-descr'), request.form.getlist('ass-time'))]
            msg['ass'].sort(key = itemgetter('title'))
            msg['ass'].sort(key = itemgetter('time'), reverse=True)

        cv = TEXTEMPLATE.render(msg = msg, portrait = 'img/' + filename)
        pdf = writeTex(cv, app.config["OUT_DIR"], filename)
        deleteImgUpload(filename)
        return redirect("/getpdf/" + pdf)


@app.route("/getpdf/<pdfname>")
def getpdf(pdfname):
    filename = f'{pdfname}.pdf'
    with open(os.path.join(app.config['OUT_DIR'], filename), 'rb') as f:
        data = f.readlines()
    os.remove(os.path.join(app.config['OUT_DIR'], filename))
    return Response(data, headers={
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename=%s;' %filename
        })
#    flash('PDF skapad och hämtad.')
#    filepath = os.path.join(app.instance_path, filename)
#    return r
#    return send_from_directory(app.config['OUT_DIR'], filename=filename, as_attachment=True)


@app.after_request
def after_request(response):
    """ Ensure responses aren't cached """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
