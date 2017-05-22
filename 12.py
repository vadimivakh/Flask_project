import shelve



with shelve.open('shelve_lib') as db:

    # for i in db.items():
    #     print(i)

    for tag in db.keys():
        print(tag,':')
        for value in db.values():
            for every in value[::2]:
                print(every['filename_origin'])
        print('\n')