import subprocess, imp


def download_dependences():
    module_name = 'flask'

    try:
        imp.find_module(module_name)
        print('Module \'{}\' found'.format(module_name))
    except ImportError:
        print("Error: Can\'t find module \'{}\'!".format(module_name))
        response = input('Will you install it now? (y/n)')
        if response == 'y':
            subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
        else:
            exit(1)


def initialize_env():
    import os
    if not os.path.isdir('media'):
        os.mkdir('media')
        print('Directory "media" created')


def run_application():
    from web_app import application
    application.app.run()


if __name__ == "__main__":
    download_dependences()
    initialize_env()
    run_application()
