import subprocess

subprocess.call('python setup.py sdist')
subprocess.call('python setup.py bdist_wheel --universal')
subprocess.call('twine upload dist/*')
