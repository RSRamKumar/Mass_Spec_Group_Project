import os
import base64
import shutil

import sys
import pandas as pd
from flask import session
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template


sys.path.append('../spectra_package')
from startup import DATA_DIR
from ms_file_parsing import MSFileParser
from db_searcher import DbSearcher
from protein_query import ProteinSearcher
import shutil
from pathlib import Path


UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')

ALLOWED_EXTENSIONS = {"mzXML", "mzML", "fasta"}

app = Flask(__name__)
app.secret_key = 'someSecretKey'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 4 * 2048 * 2048


@app.route("/")
def home():
    context = {
        'title': "Home"
    }
    if 'file_type' in session:
        if session['file_type'] == 'mzxml':
            if Path(session['file_path']).is_file():
                parsing_instance = MSFileParser(ms_file_input=session['file_path'])
                output = parsing_instance.parser()
                context['output'] = output
                #print(output)
        elif session['file_type'] == 'mzml':
            if Path(session['mzml_path']).is_file() and Path(session['fasta_path']).is_file():

                db_instance = DbSearcher(mzml_file=session['mzml_path'], fasta_file=session['fasta_path'])
                vals = db_instance.db_searcher()
                context['vals'] = vals
            flash('Check if all files are uploaded.')
    return render_template('template.html', **context)





@app.route("/upload")
def upload():
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if request.form["submit"] == 'Upload':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No file selected')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template('template.html', success_msg="File uploaded successfully")
        elif request.form["submit"] == 'Clear Contents':
            # else:
            for root, dirs, files in os.walk(UPLOAD_FOLDER):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            return render_template('upload.html', success_msg="Uploaded files successfully removed.")
        return redirect(url_for('home'))

@app.route("/proteins" , methods=['GET', 'POST'])
def Protein_matches():

    contexts = {
        'title': "Home"
    }
    if Path(session['mzml_path']).is_file() and Path(session['fasta_path']).is_file():
        db_instance = DbSearcher(mzml_file=session['mzml_path'], fasta_file=session['fasta_path'])
        vals = db_instance.db_searcher()
        protein_instance = ProteinSearcher(peptide_list=vals)
        pro = protein_instance.download_protein_info()
        for d_ in pro.values():
            for item in d_:
                new1 = []
                c= item['protein']
                a = item["peptide"]
                b = item["location"]
                new1.append([a,b,c])
                new = pd.DataFrame(new1)
                new.columns = ["Peptide", "Location", "Protein"]

                contexts["new"] = new

        return render_template('template.html', **contexts)

@app.route('/Session', methods=['POST'])
def Session():
    # Putting the files in sessions
    if request.form['file_type'] == 'mzxml':
        for File in os.listdir(UPLOAD_FOLDER):
            if File.endswith(".mzXML"):
                session['file_type'] = 'mzxml'
                session['file_path'] = UPLOAD_FOLDER + "/" + File
                print(session['file_path'])
                flash('File(s) imported successfully.')
                return redirect(url_for('home'))
    elif request.form['file_type'] == 'fasta':
        for File1 in os.listdir(UPLOAD_FOLDER):
            if File1.endswith(".fasta"):
                session['file_type'] = 'fasta'
                session['fasta_path'] = UPLOAD_FOLDER + '/' + File1
                print(session['fasta_path'])
                flash('Fasta File imported successfully.')
                return redirect(url_for('home'))
    else:
        for File2 in os.listdir(UPLOAD_FOLDER):
            if File2.endswith(".mzML"):
                flash('mzML imported successfully.')
                session['file_type'] = 'mzml'
                session['mzml_path'] = UPLOAD_FOLDER + '/' + File2
                return redirect(url_for('home'))




    flash('Please Import Files.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
