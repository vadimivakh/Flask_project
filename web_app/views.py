from flask import Flask, request, render_template, redirect, flash, send_from_directory, make_response
# from werkzeug.exceptions import notfound
import os
import shelve
from web_app.utils import unigue_filename
from unidecode import unidecode

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'])
DBname = 'shelve_lib'
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.path.dirname(__file__), os.path.pardir, 'media')


def get_project_info():
    greeting_text = 'Hi, User! It\'s simple json repository based on Flask. Enjoy it'
    return render_template("index.html", text_block=greeting_text)


def get_storage_stat():
    with shelve.open(DBname) as database:
        for key, value in dict(database).items():
            if not len(value):
                database.pop(key)
        return render_template('stat_form.html', posts=database)


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
    return render_template('files_by_tag.html', filetag=tag, database=result)


def update_file(tag, filename):
    if request.method == 'GET':
        flag = False
        with shelve.open(DBname) as database:
            if not tag in database:
                return 'no tag "{}" in database'.format(tag)
            else:
                for file_name in database[tag]:
                    if file_name['filename_origin'] == filename:
                        filename_saved_db = file_name['filename_saved']
                        flag = True
                        break
        if flag:
            return render_template('update.html', tag=tag, filename=filename, filename_saved=filename_saved_db,
                                   old_tag=tag)
        return "no file with tag {} in database".format(tag)

    elif request.method == 'POST':
        count = 0
        old_tag = request.form['old_tag']
        filename = request.form['filename']
        filetag = request.form['filetag']
        filename_saved = request.form['filename_saved']
        update_data = [{'filename_origin': filename, 'filename_saved': filename_saved}]

        with shelve.open(DBname) as database:
            if filetag in database:
                database[filetag] += update_data
            else:
                database[filetag] = update_data

        with shelve.open('shelve_lib') as database:
            for note in database[old_tag]:
                if note['filename_origin'] == filename:
                    break
                else:
                    count += 1
            database[old_tag] = database[old_tag][:count:] + database[old_tag][count + 1::]
        return redirect('/storage/stat/')


def uploaded_file(tag, filename):
    with shelve.open(DBname) as database:
        if tag in database:
            for every_tag in database.values():
                for every_dict in every_tag:
                    if every_dict['filename_origin'] == filename:
                        filename = every_dict['filename_saved']
                        break

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True,
                               attachment_filename=unidecode(filename))
    return response
