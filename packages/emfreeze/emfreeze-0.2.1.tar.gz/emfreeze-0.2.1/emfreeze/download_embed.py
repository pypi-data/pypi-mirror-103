import os
from zipfile import ZipFile
import shutil
import urllib.request as urllib


def download_embeddable_package(major_version, minor_version, micro_version, bit):
    filename = "python-{0}.{1}.{2}-embed-amd{3}.zip".format(major_version, minor_version, micro_version, bit)
    url = "https://www.python.org/ftp/python/{0}.{1}.{2}/{3}".format(major_version, minor_version, micro_version, filename)
    urllib.urlretrieve(url, filename)
    return filename

def extract_package_to_dist(path, filename):
    try:
        os.mkdir("dist")
    except FileExistsError:
        pass
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    with ZipFile(filename, "r") as zipObj:
        zipObj.extractall(path=path)
    os.remove(filename)