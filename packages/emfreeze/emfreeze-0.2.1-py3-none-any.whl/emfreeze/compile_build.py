import compileall

def compile_scripts(path):
    compileall.compile_dir(path, legacy=True, maxlevels=0)