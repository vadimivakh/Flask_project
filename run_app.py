import subprocess, imp

#TODO:
#1)download all python packages
#2)Create empty storage if it need it
#3)Create database file to track changes

def download_dependences():

    module = 'requests'
    try:
        imp.find_module(module)
        print('Module \'{}\' found'.format(module))
    except ImportError:
        print("Error: Can\'t find module \'{}\'!".format(module))
        response = input('Will you install it now? (y/n)')
        if response == 'y':
            subprocess.run['pip', 'install', 'requests']
        else:
            exit(1)

    module = 'flask'
    try:
        imp.find_module(module)
        print('Module \'{}\' found'.format(module))
    except ImportError:
        print("Error: Can\'t find module \'{}\'!".format(module))
        response = input('Will you install it now? (y/n)')
        if response == 'y':
            subprocess.run['pip', 'install', 'flask']
        else:
            exit(1)

def initialize_env():
    # create directory, where we will save storage
    # create db file->shelve lib
    import os
    if not os.path.isdir('media'):
        os.mkdir('media')
        print('Directory "media" created')
        file = open('e:\\Python projects\\flask_project_1\\json_repository-master\\media\\shelve_lib.dat', 'w')
        print('File "shelve_lib.dat" created')
    else:
        print('Directory "media" already exists')

def run_application():
    from web_app import application
    application.app.run()

if __name__ == "__main__":
    download_dependences()
    initialize_env()
    run_application()
