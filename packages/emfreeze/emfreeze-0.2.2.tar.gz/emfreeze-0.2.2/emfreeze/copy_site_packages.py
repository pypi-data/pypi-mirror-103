import shutil
import glob
from distutils.dir_util import copy_tree

def copy_files(destination):
    # for file in glob.glob("*.py"):
    #     print("Copy file:", file)
    #     shutil.copy(file, destination)
    for path in glob.glob("./*"):
        if path not in ['.\\dist', '.\\Include', '.\\Lib', '.\\pyvenv.cfg', '.\\Scripts']:
            print("Copy:", path)
            try:
                shutil.copy(path, destination)
            except:
                copy_tree(path, str(destination) + path[1:])

def copy_site_packages(destination):
    print("Copy content of site-packages")
    copy_tree("Lib/site-packages", str(destination))