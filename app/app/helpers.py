from app import app
#from subprocess import Popen
import subprocess
from distutils.dir_util import copy_tree

import os, tempfile, shutil, sys

def allowed_file(filename):
    """ Make sure uploaded files have the correct extension """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def writeTex(rendered_tex, out_dir, img):
    """ Render .tex and compile with latexmk """
    with tempfile.TemporaryDirectory() as td:
        print(os.listdir(td), file=sys.stderr)
        print(os.listdir(td), file=sys.stdout)
        copy_tree('app/app/templates/tex', td)
        print(os.listdir(td), file=sys.stderr)
        print(os.listdir(td), file=sys.stdout)
        shutil.copy(app.config['IMAGE_UPLOADS'] + '/' + img, td + '/img/' + img)
        tmp_out = os.path.join(td, 'cv.pdf')
        print(os.listdir(td), file=sys.stderr)
        print(os.listdir(td), file=sys.stdout)
        tmp_in = os.path.join(td, 'cv.tex')
        with open(tmp_in, 'w') as f:
            f.writelines(rendered_tex)
        print(os.listdir(td), file=sys.stderr)
        print(os.listdir(td), file=sys.stdout)
        print(os.listdir(td+'/img'), file=sys.stderr)
        print(os.listdir(td+'/img'), file=sys.stdout)
        subprocess.call('latexmk -pdf -recorder ' + tmp_in)
#        subprocess.run(['latexmk', '-pdf', '-recorder', tmp_in])
#        p1.communicate()
        shutil.copy2(tmp_out, out_dir)


def servePdf(pdf_path):
    """ Send file to user """


def deleteGenFiles(tex):
    """ Delete generated files """
    if (tex != 'default'):
        os.remove(app.config["IMAGE_UPLOADS"] + tex) # Uploaded image
    os.remove(app.config["OUT_DIR"] + 'cv.tex') # Rendered TEX
    os.remove(app.config["OUT_DIR"] + 'cv.pdf') # Rendered PDF
