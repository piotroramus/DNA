import subprocess
import os.path

script = "alignment.sh"

if os.path.exists(script):
    subprocess.call("./"+script, shell=True)
else:
    print "Cannot find", script