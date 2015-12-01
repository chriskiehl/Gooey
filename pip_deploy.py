import subprocess

subprocess.call('python setup.py sdist')
subprocess.call('python setup.py sdist bdist_wheel upload')
