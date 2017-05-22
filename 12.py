import shelve



with shelve.open('shelve_lib') as db:

    # for i in db.items():
    #     print(i)

    for tag in db.keys():
        print(tag,':')
        for value in db[tag][::2]:
            print(value['filename_origin'])
        #     for every in value:
        #         print(every['filename_origin'])
        # print('\n')