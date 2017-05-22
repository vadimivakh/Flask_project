from flask import Flask, request, render_template, redirect, flash
import os, shelve
from web_app import utils

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])

def get_project_info():

    response_text =  'Hi, User! It\'s simple json repository based on Flask. Enjoy it'
    return render_template("index.html", text_block = response_text)


def get_storage_stat():
    # по `GET` запросу должен вернуть список всех имен файлов и их тегов
    with shelve.open('shelve_lib') as db:
        return render_template('stat_form.html', posts = db)


def download_file():
    if request.method == 'GET':
        return render_template('file_form.html')

    elif request.method == 'POST':
        if request.form['filetag'] == " ":
            flash('Empty tag')
            return redirect('/storage/files/')

        file = request.files['file_input']
        filename_origin = file.filename

        if file and filename_origin.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
            filename_saved = utils.unigue_filename(filename_origin)
            update_data = [{'filename_origin': file.filename}, {'filename_saved': filename_saved}]

            with shelve.open('shelve_lib') as db:
                if request.form['filetag'] in db:
                    db[request.form['filetag']] += update_data
                elif not request.form['filetag'] in db:
                    db[request.form['filetag']] = update_data

            file.filename = filename_saved
            filepath = os.path.join('media', file.filename)
            file.save(filepath)
            flash('File "{}" with tag "{}" succesfully saved in database'.format(filename_origin, request.form['filetag']))

        return redirect('/storage/files/')


def upload_files(tag):
# по `GET` запросу возвращает список файлов, у которых tag=tag
    result = []
    if request.method == 'GET':
        with shelve.open('shelve_lib') as db:
            if tag in db:
                    result += db[tag][::2]
    return render_template('files_by_tag.html', filetag = tag, info = result)


# @app.route('/storage/files/<tag>/', methods = ['PUT'])
def update_file(tag):
    # по `GET` запросу должен вернуть предзаполненную форму с тэгом и именем файла,
    # по `PUT` или `PATCH` запросу данные из формы должны записаться на диск и в базу
    return render_template('update.html')