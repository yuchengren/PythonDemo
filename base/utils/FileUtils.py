import os


def deleteFile(file):
    if not os.path.exists(file):
        return
    if os.path.isfile(file):
        os.remove(file)
        return
    else:
        files = os.listdir(file)
        for i in files:
            deleteFile(os.path.join(file, i))
        if len(os.listdir(file)) == 0:
            os.removedirs(file)
