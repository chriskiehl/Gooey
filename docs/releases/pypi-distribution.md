# Testing PyPi distribution before upload

The 1.0.4 release was botched when uploading to PyPi as it pulled in the 1.0.3 artifacts sitting in my dev directory.  This meant that the 1.0.4 version was now clobbered on PyPi and could no longer be used. More care is needed when deploying. 


### How to test locally before uploading

1\. build the wheel

```
python pip_build_wheel.py
``` 

this will output the wheel to the `dist/` directory. 

2/. Copy the file location. 

Copy the absolute path to the .gz output file. It will look something like this:  

```
dist/Gooey-1.0.4.tar.gz
```

3\. In a different virtual environment, install the local wheel 

```
cd ~/projects/GooeyExamples
virtualenv venv 
source ./venv/Scripts/activate
pip install /path/to/local/dist/Gooey-1.0.4.tar.gz
``` 

If everything installs OK, you're good to upload.

```
python pip_deploy.py
```

 