import os, sys
import shutil
from zipfile import ZipFile

TARGET_DIR = 'extracted'

def unzip (path, total_count):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_name = os.path.join(root, file)
            if (not file_name.endswith('.zip')):
                total_count += 1
            else:
                currentdir = file_name[:-4]
                if not os.path.exists(currentdir):
                    os.makedirs(currentdir)
                with ZipFile(file_name) as zipObj:
                    zipObj.extractall(currentdir)
                os.remove(file_name)
                total_count = unzip(currentdir, total_count)
    return total_count


if sys.argv[1:]:
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    for file in sys.argv[1:]:
        if (not file.endswith('.zip')):
            print('Not a zip file, skipping: '+ file)
        else:
            shutil.copy2(os.path.join(os.getcwd(), file), os.getcwd() + "/" +TARGET_DIR)

    total_count = unzip ('./'+ TARGET_DIR, 0)
    print(total_count)
else:
    print('pass filenames as commandline args')