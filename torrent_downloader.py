# https://pypi.org/project/pythorrent/
import subprocess
def download (srcway, src):
    srcway=srcway.replace('\\', '/')
    src=src.replace('\\', '/')
    launcher=str("python -m pythorrent --file "+src)+str(" --path "+srcway+" --log=info")
    subprocess.Popen(launcher)