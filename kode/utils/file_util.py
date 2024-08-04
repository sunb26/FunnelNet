def rename_duplicates(files, sep):
    newlist = []
    for i, v in enumerate(files):
        totalcount = files.count(v)
        count = files[:i].count(v)
        newlist.append(v + sep + str(count + 1) if totalcount > 1 else v)
    return newlist
