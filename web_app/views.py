from flask import Flask, request, render_template, redirect, flash, send_from_directory, make_response
import os
import shelve
from web_app.utils import unigue_filename

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])
DBname = 'shelve_lib'
UPLOAD_FOLDER = 'E:\\Python projects\\FLASK_repository_project\\media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_project_info():
    greeting_text = 'Hi, User! It\'s simple json repository based on Flask. Enjoy it'
    return render_template("index.html", text_block=greeting_text)


def get_storage_stat():
    with shelve.open(DBname) as db:
        return render_template('stat_form.html', posts=db)


def download_file():
    if request.method == 'GET':
        return render_template('file_form.html')

    elif request.method == 'POST':
        filetag = request.form['filetag']
        if filetag == " ":
            flash('Empty tag')
            return redirect('/storage/files/')

        file = request.files['file_input']
        filename_origin = file.filename

        if file and (filename_origin.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
            filename_saved = unigue_filename(filename_origin)
            update_data = [{'filename_origin': file.filename, 'filename_saved': filename_saved}]
            with shelve.open(DBname) as db:
                if filetag in db:
                    db[filetag] += update_data
                elif not filetag in db:
                    db[filetag] = update_data
            file.filename = filename_saved
            filepath = os.path.join('media', file.filename)
            file.save(filepath)
            flash('File "{}" with tag "{}" succesfully saved in database'
                  .format(filename_origin, request.form['filetag']))

        return redirect('/storage/files/')


def upload_files(tag):
    result = []
    if request.method == 'GET':
        with shelve.open(DBname) as database:
            if tag in database:
                result += database[tag]
    return render_template('files_by_tag.html', filetag=tag, info=result)


def update_file(tag, filename):
    pass
    # if request.method == 'GET':
    #     return render_template('update.html', tag=tag, filename=filename)
    #
    # elif request.method == 'POST':
    #     pass


def uploaded_file(tag, filename):

    with shelve.open(DBname) as database:
        if tag in database:
            for every_tag in database.values():
                for every_dict in every_tag:
                    if every_dict['filename_origin'] == filename:
                        filename = every_dict['filename_saved']
                        print(filename)
                        break

    response = make_response(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    response.headers['Content-Disposition'] = "attachment; filename=%s" % filename

    return response
