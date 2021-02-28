from app import app
from subprocess import Popen

import os

def allowed_file(filename):
    """ Make sure uploaded files have the correct extension """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def writeTex(rendered_tex, out_dir):
    """ Render .tex and compile with latexmk """
    cur_dir = os.getcwd()
    os.chdir(out_dir)
    with open('cv.tex', 'w') as outfile:
        outfile.write(rendered_tex)
    p = Popen(['latexmk', '-pdf', '-recorder', 'cv.tex'])
    p.communicate()
    q = Popen(['latexmk', '-c', 'cv.tex'])
    q.communicate()
    os.chdir(cur_dir)


def servePdf(pdf_path):
    """ Send file to user """


def deleteGenFiles(tex):
    """ Delete generated files """
    if (tex != 'default'):
        os.remove(app.config["IMAGE_UPLOADS"] + tex) # Uploaded image
    os.remove(app.config["OUT_DIR"] + 'cv.tex') # Rendered TEX
    os.remove(app.config["OUT_DIR"] + 'cv.pdf') # Rendered PDF
