from app import app
from flask import render_template, request, redirect, flash, url_for


@app.route("/")
def index():
    """ Open index page and show current assignments """
    with app.app_context():
        return render_template("public/index.html")


@app.template_filter("escape_tex")


@app.route("/createpdf", methods=["GET", "POST"])
def createpdf():
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
        return redirect("public/index.html")

