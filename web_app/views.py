from flask import Flask, request, render_template, redirect, flash, send_from_directory
import os
import shelve


app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])


def get_project_info():

    response_text = 'Hi, User! It\'s simple json repository based on Flask. Enjoy it'
    return render_template("index.html", text_block=response_text)


def get_storage_stat():

    with shelve.open('shelve_lib') as db:
        return render_template('stat_form.html', posts=db)


def download_file():

    if request.method == 'GET':
        return render_template('file_form.html')

    elif request.method == 'POST':
        if request.form['filetag'] == " ":
            flash('Empty tag')
            return redirect('/storage/files/')

        file = request.files['file_input']
        filename_origin = file.filename

        if file and (filename_origin.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
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
            flash('File "{}" with tag "{}" succesfully saved in database'
                    .format(filename_origin, request.form['filetag']))

        return redirect('/storage/files/')


def upload_files(tag):

    result = []
    if request.method == 'GET':
        with shelve.open('shelve_lib') as database:
            if tag in database:
                    result += database[tag][::2]
    return render_template('files_by_tag.html', filetag=tag, info=result)


def update_file(tag, filename):

    if request.method == 'GET':
        return render_template('update.html', tag=tag, filename=filename)

    elif request.method == 'POST':
        pass


def uploaded_file(filename):

    if request.method == 'GET':
        return send_from_directory('/media', filename)
