import shelve, random, string


def unigue_filename(filename):

    filename_without_ext = filename.split('.')[0]
    extention = filename.split('.')[-1]

    return filename_without_ext+'_'+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))+'.'+extention