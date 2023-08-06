import argparse
import sys
from .download_embed import download_embeddable_package, extract_package_to_dist
import pathlib
from .copy_site_packages import copy_site_packages, copy_files
from .compile_build import compile_scripts
import os

def main_cli():
    is_64bit = sys.maxsize > 2**32
    bit = 64
    if not is_64bit:
        bit = 32
    major_version, minor_version, micro_version = sys.version_info[:3]

    parser = argparse.ArgumentParser(prog="emfreeze", description="Emfreeze freezes a python virtual environment together with the python embeddable package, to make it easy to embed it into other software without creating executables.")
    parser.add_argument("-d", "--dist-path", help="Set the path of the final build", metavar="PATH", action="store", type=pathlib.Path, default="dist/build-python-{0}.{1}.{2}-{3}bit".format(major_version, minor_version, micro_version, bit))
    parser.add_argument("--embeddable-package", help="Path of a compatible python embeddable package zip file, if emfreeze should not download it", metavar="PATH", action="store", type=pathlib.Path, required=False, default=None)
    parser.add_argument("-c", "--compile", help="Compile your toplevel scripts", action="store_true")
    parser.add_argument("--post-build-script", help="Path of a executable script (e.g. Batch-Script) which executes inside your newly build package.", required=False, default=None, metavar="PATH", action="store", type=pathlib.Path, dest="build_script")

    args = parser.parse_args()
    print(args)

    if not os.path.isfile("pyvenv.cfg") or not os.path.isdir("Lib"):
        print("Not a valid venv, execute this command only inside a venv directory")
        print(os.path.isfile("pyvenv.cfg"))
        print(os.path.isdir("Lib"))
        exit()
    if args.embeddable_package == None:
        print("Download embeddable package for version {0}.{1}.{2}-{3}bit".format(major_version, minor_version, micro_version, bit))
        filename = download_embeddable_package(major_version, minor_version, micro_version, bit)
    else:
        filename = args.embeddable_package
    print("Extract package")
    extract_package_to_dist(args.dist_path, filename)
    print("Copy site-packages and scripts")
    copy_site_packages(args.dist_path)
    copy_files(args.dist_path)
    if args.compile:
        compile_scripts(args.dist_path)
    if args.build_script != None:
        print("Execute build script")
        abs_build_script = os.path.abspath(args.build_script)
        os.chdir(args.dist_path)
        os.system(abs_build_script)