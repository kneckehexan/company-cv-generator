from app import app
#from subprocess import Popen
from distutils.dir_util import copy_tree
from uuid import uuid4
from flask import send_from_directory, abort, safe_join, send_file
import os, tempfile, shutil, sys, re, subprocess

def allowed_file(filename):
    """ Make sure uploaded files have the correct extension """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def writeTex(rendered_tex, out_dir, img):
    """ Render .tex and compile with latexmk """
    with tempfile.TemporaryDirectory() as td:
        # Copy tex template files and folders to tempdir.
        copy_tree('app/app/templates/tex', td)
        shutil.copy(os.path.join(app.config['IMAGE_UPLOADS'], img), td + '/img/' + img)
        # Create random UUID4 for tex and pdf files to use.
        rndID = str(uuid4())
        # Path to the to-be-created pdf
        tmp_out = os.path.join(td, rndID + '.pdf')
        # Filename of the to-be-rendered tex-file.
        tmp_in = rndID + '.tex'
        # Get current working dir path.
        cur_dir = os.getcwd()
        # Change working dir to the temporary one.
        os.chdir(td)
        # Render the tex-file.
        with open(tmp_in, 'w') as f:
            f.writelines(rendered_tex)
        # Run commands to render PDF.
        subprocess.check_call('pdflatex -interaction=nonstopmode ' + tmp_in, shell=True)
#        p1 = Popen('latex ' + tmp_in, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#        p2 = Popen('dvips ' + rndID + '.dvi', shell=True, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#        p3 = Popen('ps2pdf ' + rndID + '.ps', shell=True, stdin=p2.stdout)
#        p3.wait()
        #subprocess.check_call('latex ' + tmp_in, shell=True)
        #subprocess.check_call('dvips ' + rndID + '.dvi', shell=True)
        #subprocess.check_call('ps2pdf ' + rndID + '.ps', shell=True)
        os.listdir()
        # Change back to original working directory.
        os.chdir(cur_dir)
        # Copy newly created PDF to out-put folder.
        shutil.copy2(tmp_out, out_dir)
        # Return the filename and the tmp dir should be destroyed
        return rndID


def deleteGenFiles(tex):
    """ Delete generated files NOT IMPLEMENTED """
    if (tex != 'default'):
        os.remove(app.config["IMAGE_UPLOADS"] + tex) # Uploaded image
    os.remove(app.config["OUT_DIR"] + 'cv.tex') # Rendered TEX
    os.remove(app.config["OUT_DIR"] + 'cv.pdf') # Rendered PDF
